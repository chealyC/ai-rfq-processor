from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import date


def generate_quote_pdf(rfq):

    filename = f"quote_{rfq['id']}.pdf"

    pdf = canvas.Canvas(filename, pagesize=A4)

    width, height = A4

    # Header
    pdf.setFont("Helvetica-Bold", 24)
    pdf.drawString(50, height - 60, "QUOTATION")

    pdf.setFont("Helvetica", 10)

    pdf.drawRightString(
        width - 50,
        height - 45,
        f"Quote #{rfq['id']:05d}"
    )

    pdf.drawRightString(
        width - 50,
        height - 60,
        f"Date: {date.today().strftime('%d %B %Y')}"
    )

    # Company information
    y = height - 120

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Customer")

    y -= 25

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, rfq["company"])

    # RFQ details
    y -= 50

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "RFQ Details")

    y -= 25

    pdf.setFont("Helvetica", 11)

    pdf.drawString(50, y, f"Product: {rfq['product']}")
    y -= 20

    pdf.drawString(50, y, f"Quantity: {rfq['quantity']}")
    y -= 20

    pdf.drawString(50, y, f"Delivery Date: {rfq['delivery_date']}")
    y -= 20

    pdf.drawString(
        50,
        y,
        f"Delivery Location: {rfq['delivery_location']}"
    )

    # Pricing

    y -= 50

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Pricing")

    y -= 25

    # Table dimensions

    table_left = 50
    table_right = width - 50
    table_width = table_right - table_left

    # Table background
    pdf.setFillColorRGB(0.95, 0.95, 0.95)
    pdf.rect(
        table_left,
        y - 14,
        table_width,
        34,
        fill=1,
        stroke=0
    )

    pdf.setFillColorRGB(0, 0, 0)

    # Table headers
    pdf.setFont("Helvetica-Bold", 9)

    pdf.drawString(table_left + 10, y + 3, "DESCRIPTION")

    pdf.drawRightString(
        350,
        y + 3,
        "QUANTITY"
    )

    pdf.drawRightString(
        450,
        y + 3,
        "UNIT PRICE"
    )

    pdf.drawRightString(
        table_right - 10,
        y + 3,
        "TOTAL"
    )

    # Product row
    y -= 38

    pdf.setFont("Helvetica", 10)

    pdf.drawString(
        60,
        y,
        rfq["product"]
    )

    pdf.drawRightString(
        350,
        y,
        f"{rfq['quantity']:,}"
    )

    pdf.drawRightString(
        450,
        y,
        f"£{rfq['unit_price']:,.2f}"
    )

    pdf.drawRightString(
        table_right - 10,
        y,
        f"£{rfq['total_price']:,.2f}"
    )

    # Bottom table line
    y -= 18

    pdf.setStrokeColorRGB(0.85, 0.85, 0.85)
    pdf.line(50, y, width - 50, y)

    # Total
    y -= 30

    pdf.setFont("Helvetica-Bold", 11)

    pdf.drawString(
        390,
        y,
        "TOTAL"
    )

    pdf.drawRightString(
        width - 50,
        y,
        f"£{rfq['total_price']:,.2f}"
    )

    # Delivery and payment

    y -= 55

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Additional Information")

    y -= 25

    pdf.setFont("Helvetica", 10)

    # Delivery
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(50, y, "Delivery")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(
        50,
        y - 18,
        rfq["delivery_location"]
    )

    # Payment
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(250, y, "Payment Terms")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(
        250,
        y - 18,
        "To be agreed"
    )

    # Validity
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(450, y, "Quote Validity")

    pdf.setFont("Helvetica", 10)
    pdf.drawString(
        450,
        y - 18,
        "30 days"
    )

    # Footer
    pdf.setFont("Helvetica", 9)

    pdf.drawString(
        50,
        40,
        "Thank you for your enquiry."
    )

    pdf.save()

    return filename