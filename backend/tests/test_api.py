from fastapi.testclient import TestClient

from app.main import app


def sample_payload() -> dict:
    return {
        "title": "Workflow Intake Review",
        "organization_name": "Demo Org",
        "sector": "Legal Aid",
        "respondent_name": "Alex Rivera",
        "respondent_email": "alex@example.org",
        "status": "draft",
        "input_section": {
            "description": "Requests arrive by email and phone.",
            "dependencies": ["Shared inbox"],
            "tools": ["Outlook"],
            "items": [
                {
                    "name": "Capture intake notes",
                    "current_state": "manual",
                    "pain_level": 4,
                    "risk_level": "medium",
                    "notes": "Staff re-enter information into the tracker.",
                }
            ],
        },
        "logic_section": {
            "description": "Eligibility is reviewed by hand.",
            "dependencies": ["Eligibility policy"],
            "tools": ["Spreadsheet"],
            "items": [
                {
                    "name": "Check eligibility",
                    "current_state": "manual",
                    "pain_level": 5,
                    "risk_level": "high",
                    "notes": "Rules live in a spreadsheet.",
                }
            ],
        },
        "automation_section": {
            "description": "Few automated integrations exist.",
            "dependencies": ["Email templates"],
            "tools": ["Outlook"],
            "items": [
                {
                    "name": "Notify reviewers",
                    "current_state": "semi-automated",
                    "pain_level": 3,
                    "risk_level": "medium",
                    "notes": "Needs integration with the case system.",
                }
            ],
        },
        "output_section": {
            "description": "Weekly reports are prepared manually.",
            "dependencies": ["Tracker export"],
            "tools": ["Excel"],
            "items": [
                {
                    "name": "Assemble weekly report",
                    "current_state": "manual",
                    "pain_level": 4,
                    "risk_level": "medium",
                    "notes": "Formatting is repeated every week.",
                }
            ],
        },
    }


def test_create_get_and_export_assessment() -> None:
    with TestClient(app) as client:
        headers = {"X-Dev-User": "api-test-user"}

        create_response = client.post("/api/v1/assessments", json=sample_payload(), headers=headers)
        assert create_response.status_code == 201
        created = create_response.json()
        assert created["organization_name"] == "Demo Org"
        assert "manual effort" in created["executive_summary"]

        get_response = client.get(f"/api/v1/assessments/{created['id']}", headers=headers)
        assert get_response.status_code == 200
        fetched = get_response.json()
        assert fetched["id"] == created["id"]

        export_response = client.get(f"/api/v1/assessments/{created['id']}/export", headers=headers)
        assert export_response.status_code == 200
        assert export_response.headers["content-type"].startswith("application/json")
        assert "Workflow Intake Review" in export_response.text

        report_response = client.get(f"/api/v1/assessments/{created['id']}/report", headers=headers)
        assert report_response.status_code == 200
        assert report_response.headers["content-type"].startswith("application/pdf")
        assert report_response.content.startswith(b"%PDF")
