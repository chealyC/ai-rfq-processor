from database import save_rfq, get_rfqs
from pdf_reader import extract_text_from_pdf
from ocr_reader import extract_text_from_image, extract_text_from_scanned_pdf
from ai_processor import process_rfq

while True:
    print("\n===== RFQ PROCESSOR =====")
    print("1. Process new RFQ")
    print("2. View saved RFQs")
    print("3. Exit")

    choice = input("\nChoose an option: ")

    if choice == '1':
        filename = input("Enter RFQ filename: ")

        try:

            if filename.lower().endswith(".pdf"):

                rfq_text = extract_text_from_pdf(filename)

                # If PDF contains no selectable text,
                # try OCR instead.
                if not rfq_text.strip():
                    print("No text found. Running OCR...")
                    rfq_text = extract_text_from_scanned_pdf(filename)

            elif filename.lower().endswith((".png", ".jpg", ".jpeg")):

                print("Running OCR...")
                rfq_text = extract_text_from_image(filename)

            else:

                print("Unsupported file type.")

            rfq = process_rfq(rfq_text)

            save_rfq(rfq)

            print("\nRFQ ANALYSIS")
            print("-" * 30)

            print(f"Company: {rfq['company']}")
            print(f"Product: {rfq['product']}")
            print(f"Quantity: {rfq['quantity']}")
            print(f"Delivery date: {rfq['delivery_date']}")
            print(f"Delivery location: {rfq['delivery_location']}")

            print("\nRequirements:")

            for requirement in rfq["requirements"]:
                print(f"- {requirement}")

        except FileNotFoundError:
            print("Error: File not found.")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    elif choice == "2":
        rfqs = get_rfqs()

        print("\nSaved RFQs:")

        for i, rfq in enumerate(rfqs, start=1):
            print(f"{i}. {rfq['company']}")

        choice = int(input("Enter RFQ number: "))

        rfq = rfqs[choice - 1]

        print("\nRFQ DETAILS")
        print("-" * 30)

        print(f"Company: {rfq['company']}")
        print(f"Product: {rfq['product']}")
        print(f"Quantity: {rfq['quantity']}")
        print(f"Delivery date: {rfq['delivery_date']}")
        print(f"Delivery location: {rfq['delivery_location']}")

        print("\nRequirements:")

        requirements = rfq["requirements"].split(", ")

        for requirement in requirements:
            print(f"- {requirement}")

        print("-" * 30)
            
    elif choice == '3':
        print("Goodbye!")
        break

