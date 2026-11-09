import argparse
from collections import defaultdict
import json
from pathlib import Path
import sys


def string_list(value, label):
    if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value):
        raise ValueError(f"{label} must be a list of nonempty identifiers")
    if len(value) != len(set(value)):
        raise ValueError(f"{label} contains duplicate identifiers")
    return value


def wave_number(value, key):
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{key}.wave must be a positive integer")
    return value


def validate(plan):
    if not isinstance(plan, dict):
        raise ValueError("plan must be an object")
    baseline = plan.get("baseline")
    if not isinstance(baseline, dict) or any(
        not isinstance(k, str) or not k.strip() or not isinstance(v, str) or not v.strip()
        for k, v in baseline.items()
    ):
        raise ValueError("baseline must map capability identifiers to nonempty evidence")
    requirements = string_list(plan.get("requirements"), "requirements")
    if not isinstance(plan.get("issues"), list):
        raise ValueError("issues must be a list")

    issues = {}
    errors = []
    for row in plan["issues"]:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"].strip():
            raise ValueError("each issue needs a nonempty id")
        key = row["id"]
        if "blocked_by" in row:
            raise ValueError(f"{key}.blocked_by is replaced by wave: put each prerequisite in an earlier wave")
        if key in issues:
            errors.append(f"duplicate issue {key}")
        issues[key] = {
            "wave": wave_number(row.get("wave"), key),
            **{
                field: string_list(row.get(field, []), f"{key}.{field}")
                for field in ("owns", "provides", "requires", "protects")
            },
        }
    for key, row in issues.items():
        for protected in row["protects"]:
            if protected not in issues:
                errors.append(f"{key}: unknown protected issue {protected}")
    if errors:
        return errors

    providers = {capability: None for capability in baseline}
    owners = defaultdict(list)
    for key, row in issues.items():
        for capability in row["provides"]:
            if capability in providers:
                errors.append(f"{capability}: multiple providers (baseline or issues)")
            else:
                providers[capability] = key
        for requirement in row["owns"]:
            if requirement not in requirements:
                errors.append(f"{key}: unknown requirement {requirement}")
            owners[requirement].append(key)
    for requirement in requirements:
        if not owners[requirement]:
            errors.append(f"{requirement}: no owner")
        elif len(owners[requirement]) > 1:
            errors.append(f"{requirement}: multiple owners {', '.join(owners[requirement])}")

    for key, row in issues.items():
        for capability in row["requires"]:
            if capability not in providers:
                errors.append(f"{key}: no provider for {capability}")
            else:
                producer = providers[capability]
                if producer is not None and producer != key and issues[producer]["wave"] >= row["wave"]:
                    errors.append(
                        f"{key} (wave {row['wave']}): requires {capability} from {producer} "
                        f"(wave {issues[producer]['wave']}); merge the issues or move {key} to a later wave"
                    )
        for protected in row["protects"]:
            if issues[protected]["wave"] <= row["wave"]:
                errors.append(f"{key}: gate must be in an earlier wave than {protected}")
    return errors


def main():
    parser = argparse.ArgumentParser(description="Check declared plan ownership, wave-ordered capabilities and gates.")
    parser.add_argument("plan", type=Path)
    args = parser.parse_args()
    try:
        errors = validate(json.loads(args.plan.read_text()))
    except (OSError, ValueError) as exc:
        print(f"Invalid plan: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Declared graph checks passed. Semantic readiness review is still required.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
