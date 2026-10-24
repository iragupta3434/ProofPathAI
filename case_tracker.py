
import json
from pathlib import Path
from datetime import datetime, timezone

CASE_FILE = Path("cases.json")


def load_cases():
    if not CASE_FILE.exists():
        return {}

    try:
        return json.loads(
            CASE_FILE.read_text(encoding="utf-8")
        )
    except json.JSONDecodeError:
        raise ValueError(
            "cases.json is invalid. Please check the file."
        )


def save_case(
    case_id,
    issue,
    evidence,
    missing_information,
    status="evidence_review",
):
    cases = load_cases()

    cases[case_id] = {
        "case_id": case_id,
        "issue": issue,
        "available_evidence": evidence,
        "missing_information": missing_information,
        "status": status,
        "next_action": None,
        "updated_at": datetime.now(
            timezone.utc
        ).isoformat(),
    }

    CASE_FILE.write_text(
        json.dumps(cases, indent=2),
        encoding="utf-8",
    )

    return cases[case_id]


def get_case(case_id):
    return load_cases().get(case_id)


def update_case_status(
    case_id,
    new_status,
    next_action=None,
):
    cases = load_cases()

    if case_id not in cases:
        print(f"Case {case_id} not found.")
        return None

    cases[case_id]["status"] = new_status
    cases[case_id]["next_action"] = next_action
    cases[case_id]["updated_at"] = datetime.now(
        timezone.utc
    ).isoformat()

    CASE_FILE.write_text(
        json.dumps(cases, indent=2),
        encoding="utf-8",
    )

    return cases[case_id]


if __name__ == "__main__":
    case = save_case(
        case_id="PP-001",
        issue="damaged_delivery",
        evidence=[
            "invoice",
            "delivery_photo",
            "seller_messages",
        ],
        missing_information=[
            "delivery_date",
            "refund_policy",
        ],
    )

    print("Case saved successfully:")
    print(json.dumps(case, indent=2))

    print("\nRetrieved case:")
    print(json.dumps(get_case("PP-001"), indent=2))

    updated = update_case_status(
        case_id="PP-001",
        new_status="awaiting_user_information",
        next_action=(
            "Ask user for delivery date "
            "and refund policy"
        ),
    )

    print("\nUpdated case:")
    print(json.dumps(updated, indent=2))
