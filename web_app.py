from ocr_reader import extract_text_from_image
from pdf_reader import extract_text_from_pdf
from ai_processor import process_rfq
from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from database import get_rfqs, save_rfq, update_rfq_status, get_rfq_stats, create_quote
from fastapi.staticfiles import StaticFiles
from quote_pdf import generate_quote_pdf

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home(request: Request, status: str = "", search: str = ""):

    rfqs = get_rfqs()
    stats = get_rfq_stats()

    if status:
        rfqs = [
            rfq for rfq in rfqs
            if rfq["status"] == status
        ]

    if search:
        search = search.lower()

        rfqs = [
            rfq for rfq in rfqs
            if search in rfq["company"].lower()
            or search in rfq["product"].lower()
        ]

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "rfqs": rfqs,
            "status": status,
            "search": search,
            "stats": stats
        }
    )

@app.post("/upload")
async def upload_rfq(file: UploadFile = File(...)):

    contents = await file.read()

    filepath = f"uploads/{file.filename}"

    with open(filepath, "wb") as f:
        f.write(contents)

    if file.filename.lower().endswith(".pdf"):

        rfq_text = extract_text_from_pdf(filepath)

    elif file.filename.lower().endswith((".png", ".jpg", ".jpeg")):

        rfq_text = extract_text_from_image(filepath)

    else:

        return {"error": "Unsupported file type"}

    rfq = process_rfq(rfq_text)

    save_rfq(rfq)

    return RedirectResponse("/", status_code=303)

@app.get("/rfq/{rfq_id}")
def view_rfq(request: Request, rfq_id: int):

    rfqs = get_rfqs()

    for rfq in rfqs:

        if rfq["id"] == rfq_id:

            return templates.TemplateResponse(
                request=request,
                name="rfq.html",
                context={
                    "rfq": rfq
                }
            )

    return {"error": "RFQ not found"}

@app.post("/rfq/{rfq_id}/status")
async def change_rfq_status(rfq_id: int, status: str = Form(...)):

    update_rfq_status(rfq_id, status)

    return RedirectResponse(
        f"/rfq/{rfq_id}",
        status_code=303
    )

@app.post("/rfq/{rfq_id}/quote")
async def make_quote(
    rfq_id: int,
    unit_price: float = Form(...)
):

    rfqs = get_rfqs()

    for rfq in rfqs:

        if rfq["id"] == rfq_id:

            total_price = unit_price * rfq["quantity"]

            create_quote(
                rfq_id,
                unit_price,
                total_price
            )

            return RedirectResponse(
                f"/rfq/{rfq_id}",
                status_code=303
            )

    return {"error": "RFQ not found"}

@app.get("/rfq/{rfq_id}/quote/pdf")
def download_quote_pdf(rfq_id: int):

    rfqs = get_rfqs()

    for rfq in rfqs:

        if rfq["id"] == rfq_id:

            if rfq["total_price"] is None:
                return {"error": "Quote has not been created"}

            filename = generate_quote_pdf(rfq)

            return FileResponse(
                filename,
                media_type="application/pdf",
                filename=filename
            )

    return {"error": "RFQ not found"}