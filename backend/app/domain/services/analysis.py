from collections import Counter

from app.schemas.assessment import AssessmentSection, AssessmentSectionItem, AutomationOpportunity


def _count_manual_items(*sections: AssessmentSection) -> int:
    return sum(1 for section in sections for item in section.items if item.current_state == "manual")


def _list_bottlenecks(section: AssessmentSection) -> list[str]:
    return [item.name for item in section.items if item.pain_level >= 4]


def generate_executive_summary(
    input_section: AssessmentSection,
    logic_section: AssessmentSection,
    automation_section: AssessmentSection,
    output_section: AssessmentSection,
) -> str:
    manual_count = _count_manual_items(input_section, logic_section, automation_section, output_section)
    logic_bottlenecks = _list_bottlenecks(logic_section)
    output_bottlenecks = _list_bottlenecks(output_section)
    risks = Counter(item.risk_level for section in [input_section, logic_section, automation_section, output_section] for item in section.items)

    lines = [
        f"This assessment documents {manual_count} workflow steps that still depend on manual effort.",
        f"The logic layer shows the highest concentration of friction in {len(logic_bottlenecks)} step(s).",
        f"Output quality or delivery issues appear in {len(output_bottlenecks)} step(s).",
        f"Risk distribution is low={risks.get('low', 0)}, medium={risks.get('medium', 0)}, high={risks.get('high', 0)}.",
    ]
    if automation_section.tools:
        lines.append(f"Existing tooling already includes {', '.join(automation_section.tools[:4])}.")
    if input_section.dependencies:
        lines.append(f"Key upstream dependencies include {', '.join(input_section.dependencies[:4])}.")
    return " ".join(lines)


def _build_opportunity(item: AssessmentSectionItem, stage: str, recommendation: str, impact: str) -> AutomationOpportunity:
    return AutomationOpportunity(
        workflow_stage=stage,
        step_name=item.name,
        opportunity=recommendation,
        expected_impact=impact,
        confidence="medium" if item.risk_level == "high" else "high",
    )


def generate_automation_opportunities(
    input_section: AssessmentSection,
    logic_section: AssessmentSection,
    automation_section: AssessmentSection,
    output_section: AssessmentSection,
) -> list[AutomationOpportunity]:
    opportunities: list[AutomationOpportunity] = []

    for item in input_section.items:
        if item.current_state == "manual":
            opportunities.append(
                _build_opportunity(
                    item,
                    "Input",
                    "Capture this intake step with validated digital forms and ingestion rules.",
                    "Reduces rekeying and improves completeness at the point of entry.",
                )
            )

    for item in logic_section.items:
        if item.pain_level >= 4 or item.current_state == "manual":
            opportunities.append(
                _build_opportunity(
                    item,
                    "Logic",
                    "Convert decision rules into a workflow engine or policy automation service.",
                    "Improves consistency and shortens turnaround for rule-heavy reviews.",
                )
            )

    for item in automation_section.items:
        if "integration" in item.notes.lower() or item.current_state == "manual":
            opportunities.append(
                _build_opportunity(
                    item,
                    "Automation",
                    "Add API-based integrations and event triggers between systems.",
                    "Eliminates swivel-chair work and improves auditability across systems.",
                )
            )

    for item in output_section.items:
        if item.pain_level >= 3:
            opportunities.append(
                _build_opportunity(
                    item,
                    "Output",
                    "Standardize reporting templates and schedule delivery through automated jobs.",
                    "Improves timeliness, presentation quality, and downstream stakeholder visibility.",
                )
            )

    return opportunities[:10]
