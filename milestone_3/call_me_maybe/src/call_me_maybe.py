from llm_sdk import Small_LLM_Model
from .encoder import Encoder
from .state import State
from .models import FunctionDef
from typing import Any, Callable
import re

Judge = Callable[[str, str], State]
Done = Callable[[str], bool]

NUM = re.compile(r"^-?\d*\.?\d*$")
INT = re.compile(r"^-?\d*$")


def build_prompt(functions: list[FunctionDef], user_prompt: str) -> str:
    """Builds initial context; ends where 'name' starts."""
    lines = ["Available functions:"]
    for f in functions:
        params = ", ".join(f"{k}: {v.type}" for k, v in f.parameters.items())
        lines.append(f"- {f.name}({params}): {f.description}")
    lines.append("")
    lines.append('Example: {"name": "fn_example", "parameters": {"x": 1.0}}')
    lines.append(f"Request: {user_prompt}")
    lines.append('Answer: {"name": "')
    return "\n".join(lines)


def closed_set_judge(options: list[str]) -> Judge:
    """Accepts tokens that keep the text as a prefix in any option."""

    def judge(cur: str, tok: str) -> State:
        if any(o.startswith(cur + tok) for o in options):
            return State.OK
        return State.INVALID

    return judge


def number_judge(integer: bool) -> Judge:
    """Accepts tokens that keep a valid number; returns a STOP at a closing."""
    pattern = INT if integer else NUM

    def judge(cur: str, tok: str) -> State:
        if pattern.match(cur + tok):
            return State.OK
        complete = cur not in ("", "-") and not cur.endswith(".")
        if complete and tok[0] in ",} \n":
            return State.STOP
        return State.INVALID

    return judge


def string_judge(cur: str, tok: str) -> State:
    """Checks if text doesn break JSON; returns STOP when
    encounters closing inverted commas."""
    if tok.startswith('"'):
        return State.STOP
    if any(c in tok for c in '"\\\n\r'):
        return State.INVALID
    return State.OK


def generate(
    model: Small_LLM_Model,
    ids: list[int],
    id_to_text: dict[int, str],
    judge: Judge,
    done: Done | None = None,
    max_steps: int = 200,
) -> str:
    """Generates the text choosing allowed tokens only."""
    ids = list(ids)
    cur = ""
    for _ in range(max_steps):
        if done is not None and done(cur):
            break

        logits = model.get_logits_from_input_ids(ids)
        ok: list[int] = []
        stop: list[int] = []
        for tid, txt in id_to_text.items():
            if not txt or tid >= len(logits):
                continue
            state = judge(cur, txt)
            if state is State.OK:
                ok.append(tid)
            elif state is State.STOP:
                stop.append(tid)

        candidates = ok + stop
        if not candidates:
            raise RuntimeError(f"No valid tokens after {cur!r}")

        best = max(candidates, key=lambda t: logits[t])
        if best in stop:
            break
        ids.append(best)
        cur += id_to_text[best]
    return cur


def process_prompt(
    model: Small_LLM_Model,
    encoder: Encoder,
    id_to_text: dict[int, str],
    funcs: list[FunctionDef],
    prompt: str,
) -> dict[str, Any]:
    """Returns {"prompt", "name", "parameters"} for a prompt."""
    by_name = {f.name: f for f in funcs}
    names = list(by_name)
    ids = encoder.encode(build_prompt(funcs, prompt))

    def name_done(cur: str) -> bool:
        return cur in names and sum(n.startswith(cur) for n in names) == 1

    name = generate(model, ids, id_to_text, closed_set_judge(names), name_done)
    func = by_name[name]
    ids += encoder.encode(name + '", "parameters": {')

    params: dict[str, Any] = {}
    for i, (pname, spec) in enumerate(func.parameters.items()):
        ids += encoder.encode(("" if i == 0 else ", ") + f'"{pname}": ')
        kind = spec.type

        if kind in ("number", "integer"):
            text = generate(
                model,
                ids,
                id_to_text,
                number_judge(kind == "integer")
            )
            params[pname] = int(text) if kind == "integer" else float(text)
            ids += encoder.encode(text)
        elif kind == "boolean":
            opts = ["true", "false"]
            text = generate(
                model, ids, id_to_text, closed_set_judge(opts),
                lambda c: c in opts,
            )
            params[pname] = text == "true"
            ids += encoder.encode(text)
        else:  # string
            ids += encoder.encode('"')
            text = generate(model, ids, id_to_text, string_judge)
            params[pname] = text
            ids += encoder.encode(text + '"')

    return {"prompt": prompt, "name": name, "parameters": params}
