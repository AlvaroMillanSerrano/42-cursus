import argparse
import json
import os
import sys
from typing import Any
from .encoder import Encoder
from .models import FunctionDef
from .vocab import load_id_to_text
from .call_me_maybe import process_prompt
from llm_sdk import Small_LLM_Model


def parse_arguments() -> Any:
    parser = argparse.ArgumentParser(
        description="Call Me Maybe - Function Calling CLI"
    )
    parser.add_argument(
        "--functions_definition",
        default="data/input/functions_definition.json",
        help="Path to the functions definition JSON file"
    )
    parser.add_argument(
        "--input",
        default="data/input/function_calling_tests.json",
        help="Path to the input prompts JSON file"
    )
    parser.add_argument(
        "--output",
        default="data/output/function_calls.json",
        help="Path to the output JSON file"
    )
    return parser.parse_args()


def load_json_file(file_path: str) -> Any:
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' doesn't exist.")
        sys.exit(1)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(
            f"Error: File '{file_path}' doesn't contain a valid JSON: {e}",
        )
        sys.exit(1)


def main() -> None:
    args = parse_arguments()
    functions = load_json_file(args.functions_definition)
    prompts = load_json_file(args.input)
    print("File loaded successfully.")
    print(f"Avaiable functions: {len(functions)}")
    print(f"Prompts to process: {len(prompts)}")
    model = Small_LLM_Model()
    encoder = Encoder(model)
    results: list[dict[str, Any]] = []
    funcs = [FunctionDef(**f) for f in functions]
    id_to_text = load_id_to_text(model.get_path_to_vocab_file())
    for item in prompts:
        try:
            results.append(
                process_prompt(
                    model,
                    encoder,
                    id_to_text,
                    funcs,
                    item["prompt"]
                )
            )
        except (RuntimeError, ValueError, KeyError) as e:
            print(f"Error processing {item!r}: {e}", file=sys.stderr)

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
