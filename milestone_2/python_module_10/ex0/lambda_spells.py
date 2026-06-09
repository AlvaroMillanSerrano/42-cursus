from typing import Any


def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    try:
        return sorted(artifacts, key=lambda art: art['power'], reverse=True)
    except Exception as e:
        print(e)
        return artifacts


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    try:
        return list(filter(lambda mage: mage["power"] >= min_power, mages))
    except Exception as e:
        print(e)
        return mages


def spell_transformer(spells: list[str]) -> list[str]:
    try:
        return list(map(lambda spell: f"*{spell}*", spells))
    except Exception as e:
        print(e)
        return spells


def mage_stats(mages: list[dict]) -> dict:
    if not mages:
        return {'max_power': 0, 'min_power': 0, 'avg_power': 0.0}
    try:
        max_mage = max(mages, key=lambda m: m['power'])
        min_mage = min(mages, key=lambda m: m['power'])
        total_power = sum(map(lambda m: m['power'], mages))
        avg_power = round(total_power / len(mages), 2)
        return {
            'max_power': int(max_mage['power']),
            'min_power': int(min_mage['power']),
            'avg_power': float(avg_power)
        }
    except Exception as e:
        print(f"Error: {e}")
        return mages


if __name__ == "__main__":
    print("Testing artifact sorter...")
    artifacts: list[dict[str, Any]] = [
        {'name': 'Crystal Orb', 'power': 85, 'type': 'focus'},
        {'name': 'Zenith', 'power': 300, 'type': 'relic'},
        {'name': 'Fire Staff', 'power': 92, 'type': 'focus'},
        {'name': 'Terraprisma', 'power': 295, 'type': 'relic'}
    ]
    sorted_arts = artifact_sorter(artifacts)
    if not sorted_arts:
        print("Error: artifacts list is empty..")
    else:
        res = ""
        for art in sorted_arts:
            res += f"{art['name']} ({art['power']} power)"
            if sorted_arts.index(art) < len(sorted_arts) - 1:
                res += " comes before "
        print(res)
    print("\nTesting power filter...")
    mages: list[dict[str, Any]] = [
        {'name': 'Rasmodius', 'power': 80, 'element': 'valley'},
        {'name': 'Cornyx', 'power': 84, 'element': 'fire'},
        {'name': 'Zullie', 'power': 68, 'element': 'crystal'},
        {'name': 'Gandalf', 'power': 85, 'element': 'energy'},
        {'name': 'Saruman', 'power': 74, 'element': 'energy'}
    ]
    power = 80
    filt_mages = power_filter(mages, power)
    print(f"Mages with min power {power}:")
    for mage in filt_mages:
        print(f"-{mage['name']}({mage['power']}), element: {mage['element']}")
    print("\nTesting spell transformer...")
    spells: list[str] = [
        'Chaos Bed Vestiges',
        'PK Thunder',
        'Magic Missile',
        'Ignite'
    ]
    print(*spell_transformer(spells))
    print("\nTesting mage stats...")
    m_stats = mage_stats(mages)
    print(
        f"-Max power: {m_stats['max_power']}",
        f"-Min power: {m_stats['min_power']}",
        f"-Average power: {m_stats['avg_power']}",
        sep="\n"
    )
