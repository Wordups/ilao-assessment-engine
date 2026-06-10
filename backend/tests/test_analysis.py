from app.domain.services.analysis import generate_automation_opportunities, generate_executive_summary
from app.schemas.assessment import AssessmentSection, AssessmentSectionItem


def _section(name: str) -> AssessmentSection:
    return AssessmentSection(
        description=f"{name} description",
        dependencies=["Email"],
        tools=["Sheets"],
        items=[
            AssessmentSectionItem(
                name=f"{name} task",
                current_state="manual",
                pain_level=4,
                risk_level="medium",
                notes="Needs integration",
            )
        ],
    )


def test_generate_summary_and_opportunities() -> None:
    input_section = _section("Input")
    logic_section = _section("Logic")
    automation_section = _section("Automation")
    output_section = _section("Output")

    summary = generate_executive_summary(input_section, logic_section, automation_section, output_section)
    opportunities = generate_automation_opportunities(input_section, logic_section, automation_section, output_section)

    assert "manual effort" in summary
    assert len(opportunities) >= 4
