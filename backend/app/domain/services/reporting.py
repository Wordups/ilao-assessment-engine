from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.schemas.assessment import AssessmentRead


def _section_rows(items: list[dict]) -> list[list[str]]:
    rows = [["Workflow Step", "State", "Pain", "Risk", "Notes"]]
    for item in items:
        rows.append(
            [
                item["name"],
                item["current_state"],
                str(item["pain_level"]),
                item["risk_level"],
                item["notes"],
            ]
        )
    return rows


def _scorecard(assessment: AssessmentRead) -> list[list[str]]:
    all_items = [
        *assessment.input_section.items,
        *assessment.logic_section.items,
        *assessment.automation_section.items,
        *assessment.output_section.items,
    ]
    manual_steps = sum(1 for item in all_items if item.current_state == "manual")
    high_risk_steps = sum(1 for item in all_items if item.risk_level == "high")
    average_pain = round(sum(item.pain_level for item in all_items) / max(len(all_items), 1), 1)
    return [
        ["Manual Steps", str(manual_steps)],
        ["High Risk Steps", str(high_risk_steps)],
        ["Average Pain", str(average_pain)],
        ["Opportunities", str(len(assessment.automation_opportunities))],
    ]


def _build_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="ExecutiveTitle",
            parent=styles["Title"],
            fontSize=24,
            leading=28,
            textColor=colors.HexColor("#0f172a"),
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ExecutiveSubhead",
            parent=styles["Heading2"],
            fontSize=12,
            leading=14,
            textColor=colors.HexColor("#0f766e"),
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="ExecutiveBody",
            parent=styles["BodyText"],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#334155"),
        )
    )
    return styles


def _header(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(colors.HexColor("#0f766e"))
    canvas.rect(0, doc.pagesize[1] - 52, doc.pagesize[0], 52, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 15)
    canvas.drawString(36, doc.pagesize[1] - 32, "ILAO Assessment Engine")
    canvas.setFont("Helvetica", 9)
    canvas.drawRightString(doc.pagesize[0] - 36, doc.pagesize[1] - 30, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf_report(assessment: AssessmentRead) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=72, bottomMargin=36)
    styles = _build_styles()
    scorecard = Table(_scorecard(assessment), colWidths=[2.2 * inch, 1.2 * inch], hAlign="LEFT")
    scorecard.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#ecfeff")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#164e63")),
                ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#99f6e4")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#ccfbf1")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story = [
        Paragraph(assessment.title, styles["ExecutiveTitle"]),
        Paragraph(f"{assessment.organization_name} | {assessment.sector} | {assessment.status.replace('_', ' ').title()}", styles["ExecutiveSubhead"]),
        Spacer(1, 12),
        scorecard,
        Spacer(1, 12),
        Paragraph("Executive Summary", styles["Heading2"]),
        Paragraph(assessment.executive_summary, styles["ExecutiveBody"]),
        Spacer(1, 12),
        Paragraph("Recommended Automation Opportunities", styles["Heading2"]),
    ]

    for index, opportunity in enumerate(assessment.automation_opportunities, start=1):
        story.append(
            Paragraph(
                f"<b>{index}. {opportunity.workflow_stage} - {opportunity.step_name}</b><br/>"
                f"{opportunity.opportunity}<br/><font color='#475569'>{opportunity.expected_impact}</font>",
                styles["ExecutiveBody"],
            )
        )
        story.append(Spacer(1, 6))

    for section_title, section in [
        ("Input", assessment.input_section),
        ("Logic", assessment.logic_section),
        ("Automation", assessment.automation_section),
        ("Output", assessment.output_section),
    ]:
        story.append(Spacer(1, 12))
        story.append(Paragraph(section_title, styles["Heading2"]))
        story.append(Paragraph(section.description or "No narrative provided for this workflow stage.", styles["ExecutiveBody"]))
        story.append(Spacer(1, 6))
        data = _section_rows([item.model_dump() for item in section.items]) if section.items else [["Workflow Step", "State", "Pain", "Risk", "Notes"], ["No steps documented", "-", "-", "-", "-"]]
        table = Table(data, repeatRows=1, colWidths=[120, 65, 40, 45, 230])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f766e")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#94a3b8")),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.HexColor("#f8fafc")]),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("LEADING", (0, 0), (-1, -1), 10),
                ]
            )
        )
        story.append(table)

    doc.build(story, onFirstPage=_header, onLaterPages=_header)
    return buffer.getvalue()
