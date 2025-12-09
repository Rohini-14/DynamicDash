# file: report_utils.py
import os
import tempfile
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import plotly.io as pio

def export_dashboard_to_pdf(path, title, figs, kpis=None):
    """
    Save KPIs + charts into a clean A4 PDF (one chart per page if needed).
    path: output PDF file path
    title: PDF title
    figs: list of plotly figures
    kpis: dictionary of key-value metrics (optional)
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    # 🔹 Title Page
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width/2, height-100, title)

    # 🔹 KPIs (on first page under title)
    y = height - 150
    if kpis:
        c.setFont("Helvetica", 12)
        for k, v in kpis.items():
            c.drawString(80, y, f"{k}: {v}")
            y -= 20

    # Go to next page for charts
    c.showPage()

    # 🔹 Charts → 1 per page, full width
    for i, fig in enumerate(figs, start=1):
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            img_path = tmp.name
        pio.write_image(fig, img_path, format="png", width=1200, height=800)

        chart = ImageReader(img_path)

        # Fit image inside A4 with margins
        margin = 50
        img_width = width - 2*margin
        img_height = height - 2*margin

        c.drawImage(chart, margin, margin, img_width, img_height, preserveAspectRatio=True, mask='auto')
        c.showPage()

        # Cleanup temp file
        os.remove(img_path)

    # Save final PDF
    c.save()
