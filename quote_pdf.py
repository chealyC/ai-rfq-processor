from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors
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

    # Customer email
    if rfq["email"]:
        y -= 18

        pdf.setFont("Helvetica", 10)
        pdf.drawString(50, y, rfq["email"])

    # RFQ details
    y -= 35

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "RFQ Details")

    y -= 25

    pdf.setFont("Helvetica", 11)

    # Product
    pdf.drawString(50, y, "Product:")

    product_style = ParagraphStyle(
        "Product",
        fontName="Helvetica",
        fontSize=11,
        leading=14,
        textColor=colors.black,
        alignment=TA_LEFT
    )

    product_paragraph = Paragraph(
        rfq["product"],
        product_style
    )

    product_paragraph.wrapOn(
        pdf,
        500,
        100
    )

    product_paragraph.drawOn(
        pdf,
        110,
        y - product_paragraph.height + 4
    )

    y -= max(25, product_paragraph.height + 8)

    # Quantity
    pdf.drawString(
        50,
        y,
        f"Quantity: {rfq['quantity']:,}"
    )

    y -= 20

    # Delivery date
    pdf.drawString(
        50,
        y,
        f"Delivery Date: {rfq['delivery_date']}"
    )

    y -= 20

    # Delivery location
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

    description_left = table_left + 10
    description_width = 260

    quantity_x = 350
    unit_price_x = 450
    total_x = table_right - 10

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

    pdf.drawString(
        description_left,
        y + 3,
        "DESCRIPTION"
    )

    pdf.drawRightString(
        quantity_x,
        y + 3,
        "QUANTITY"
    )

    pdf.drawRightString(
        unit_price_x,
        y + 3,
        "UNIT PRICE"
    )

    pdf.drawRightString(
        total_x,
        y + 3,
        "TOTAL"
    )

    # Product row
    y -= 38

    product_style = ParagraphStyle(
        "TableProduct",
        fontName="Helvetica",
        fontSize=9,
        leading=11,
        textColor=colors.black,
        alignment=TA_LEFT
    )

    product_paragraph = Paragraph(
        rfq["product"],
        product_style
    )

    product_paragraph.wrapOn(
        pdf,
        description_width,
        60
    )

    product_paragraph.drawOn(
        pdf,
        description_left,
        y - product_paragraph.height + 3
    )

    # Quantity
    pdf.drawRightString(
        quantity_x,
        y,
        f"{rfq['quantity']:,}"
    )

    # Unit price
    pdf.drawRightString(
        unit_price_x,
        y,
        f"£{rfq['unit_price']:,.2f}"
    )

    # Total price
    pdf.drawRightString(
        total_x,
        y,
        f"£{rfq['total_price']:,.2f}"
    )

    # Move below the product description
    y -= max(25, product_paragraph.height + 12)

    # Bottom table line
    pdf.setStrokeColorRGB(0.85, 0.85, 0.85)

    pdf.line(
        50,
        y,
        width - 50,
        y
    )

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
    pdf.drawString(
        50,
        y,
        "Additional Information"
    )

    y -= 25

    # Delivery
    pdf.setFont("Helvetica-Bold", 10)
    pdf.drawString(
        50,
        y,
        "Delivery"
    )

    pdf.setFont("Helvetica", 10)

    pdf.drawString(
        50,
        y - 18,
        rfq["delivery_location"]
    )

    # Payment
    pdf.setFont("Helvetica-Bold", 10)

    pdf.drawString(
        250,
        y,
        "Payment Terms"
    )

    pdf.setFont("Helvetica", 10)

    pdf.drawString(
        250,
        y - 18,
        "To be agreed"
    )

    # Validity
    pdf.setFont("Helvetica-Bold", 10)

    pdf.drawString(
        450,
        y,
        "Quote Validity"
    )

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