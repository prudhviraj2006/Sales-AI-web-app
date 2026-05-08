import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import os

def test_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate("scratch/test_report.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    
    elements = []
    elements.append(Paragraph("PDF Generation Test", styles['Title']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("This is a test of the ReportLab PDF generation.", styles['Normal']))
    
    data = [['Col 1', 'Col 2'], ['Value 1', 'Value 2']]
    t = Table(data)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.blue),
                           ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke)]))
    elements.append(t)
    
    doc.build(elements)
    print("PDF generated successfully at scratch/test_report.pdf")

if __name__ == "__main__":
    os.makedirs("scratch", exist_ok=True)
    test_pdf()
