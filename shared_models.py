
from typing import Any, Optional
from pydantic import BaseModel, Field


class EvidenceAuditRequest(BaseModel):
    case_id: str = Field(..., min_length=1)
    task: str = "evidence_audit"
    facts: dict[str, Any] = Field(default_factory=dict)


class EvidenceAuditResponse(BaseModel):
    case_id: str
    agent: str = "evidence_analyst"
    available_evidence: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)
    findings: list[str] = Field(default_factory=list)
    ready_for_policy_check: bool = False
    error: Optional[str] = None


if __name__ == "__main__":
    request = EvidenceAuditRequest(
        case_id="PP-001",
        task="evidence_audit",
        facts={
            "issue": "damaged_delivery",
            "invoice_available": True,
            "photo_available": True,
            "seller_messages_available": True,
            "delivery_date": None,
            "refund_policy_available": False,
        },
    )

    response = EvidenceAuditResponse(
        case_id=request.case_id,
        available_evidence=[
            "invoice",
            "delivery_photo",
            "seller_messages",
        ],
        missing_information=[
            "delivery_date",
            "refund_policy",
        ],
        findings=[
            "Basic evidence is available for initial review."
        ],
        ready_for_policy_check=False,
    )

    print("REQUEST:")
    print(request.model_dump_json(indent=2))

    print("\nRESPONSE:")
    print(response.model_dump_json(indent=2))
