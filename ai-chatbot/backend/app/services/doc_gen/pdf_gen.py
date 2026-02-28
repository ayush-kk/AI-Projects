import logging
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from app.config import settings

logger = logging.getLogger(__name__)


def generate_pdf(data: dict, user_id: int) -> str:
    output_dir = Path(settings.generated_dir) / str(user_id)
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"document_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = str(output_dir / filename)

    doc = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=24,
        textColor=colors.HexColor("#4F46E5"),
        spaceAfter=20,
    )
    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading1"],
        fontSize=16,
        textColor=colors.HexColor("#1F2937"),
        spaceAfter=12,
        spaceBefore=16,
    )
    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["Normal"],
        fontSize=11,
        textColor=colors.HexColor("#374151"),
        spaceAfter=8,
        leading=16,
    )

    story = []

    title = data.get("title", "Document")
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 12))

    sections = data.get("sections", [])
    for section in sections:
        heading = section.get("heading", "")
        if heading:
            story.append(Paragraph(heading, heading_style))

        content = section.get("content", "")
        if content:
            story.append(Paragraph(content, body_style))

        bullets = section.get("bullets", [])
        for bullet in bullets:
            bullet_text = f"&bull; {bullet}"
            story.append(Paragraph(bullet_text, body_style))

        table_data = section.get("table")
        if table_data:
            headers = table_data.get("headers", [])
            rows = table_data.get("rows", [])
            if headers:
                all_rows = [headers] + rows
                t = Table(all_rows)
                t.setStyle(
                    TableStyle(
                        [
                            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F46E5")),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                            ("FONTSIZE", (0, 0), (-1, 0), 11),
                            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
                            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F9FAFB")),
                            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                            ("FONTSIZE", (0, 1), (-1, -1), 10),
                            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
                            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F3F4F6")]),
                            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                            ("TOPPADDING", (0, 0), (-1, -1), 6),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                        ]
                    )
                )
                story.append(Spacer(1, 8))
                story.append(t)
                story.append(Spacer(1, 8))

    doc.build(story)
    return filepath
