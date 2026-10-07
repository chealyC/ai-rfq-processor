from fastapi import FastAPI, Request, UploadFile, File, Form
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from quote_pdf import generate_quote_pdf

from database import (
    get_rfqs,
    get_rfq_stats,
    save_rfq,
    update_rfq_status,
    create_quote,
    search_rfqs,
    delete_rfq
)
from pdf_reader import extract_text_from_pdf
from ocr_reader import extract_text_from_image, extract_text_from_scanned_pdf
from ai_processor import process_rfq

import os
import uuid
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SECRET_KEY")
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def home(
    request: Request,
    search: str = "",
    status: str = ""
):

    if not request.session.get("logged_in"):
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    rfqs = search_rfqs(search, status)
    stats = get_rfq_stats()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "stats": stats,
            "rfqs": rfqs,
            "search": search,
            "status": status
        }
    )


@app.post("/upload")
async def upload_rfq(
    request: Request,
    file: UploadFile = File(...)
):

    if not request.session.get("logged_in"):
        return RedirectResponse(
            url="/login",
            status_code=303
        )
    MAX_FILE_SIZE = 10 * 1024 * 1024

    file_content = await file.read()

    if len(file_content) > MAX_FILE_SIZE:
        return {"error": "File is too large. Maximum size is 10 MB."}

    original_filename = file.filename

    extension = os.path.splitext(original_filename)[1]

    filename = f"{uuid.uuid4()}{extension}"

    os.makedirs("uploads", exist_ok=True)

    filepath = os.path.join("uploads", filename)

    with open(filepath, "wb") as f:
        f.write(file_content)

    try:

        extension = extension.lower()

        if extension == ".pdf":

            rfq_text = extract_text_from_pdf(filepath)

            if not rfq_text.strip():
                rfq_text = extract_text_from_scanned_pdf(filepath)

        elif extension in (".png", ".jpg", ".jpeg"):

            rfq_text = extract_text_from_image(filepath)

        else:

            return {"error": "Unsupported file type."}

        rfq = process_rfq(rfq_text)

        save_rfq(rfq)

        return RedirectResponse(
            url="/",
            status_code=303
        )

    except Exception as e:

        return {
            "error": str(e)
        }

    finally:

        if os.path.exists(filepath):
            os.remove(filepath)

@app.get("/rfq/{rfq_id}")
async def rfq_details(request: Request, rfq_id: int):

    if not request.session.get("logged_in"):
        return RedirectResponse(
            url="/login",
            status_code=303
        )
    
    rfqs = get_rfqs()

    rfq = None

    for item in rfqs:
        if item["id"] == rfq_id:
            rfq = item
            break

    if rfq is None:
        return {"error": "RFQ not found"}

    return templates.TemplateResponse(
        request=request,
        name="rfq.html",
        context={
            "rfq": rfq
        }
    )

@app.post("/rfq/{rfq_id}/status")
async def change_status(
    request: Request,
    rfq_id: int,
    status: str = Form(...)
):

    if not request.session.get("logged_in"):
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    update_rfq_status(rfq_id, status)

    return RedirectResponse(
        url=f"/rfq/{rfq_id}",
        status_code=303
    )

@app.post("/rfq/{rfq_id}/quote")
async def create_rfq_quote(
    request: Request,
    rfq_id: int,
    unit_price: float = Form(...)
):

    if not request.session.get("logged_in"):
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    rfqs = get_rfqs()

    rfq = None

    for item in rfqs:
        if item["id"] == rfq_id:
            rfq = item
            break

    if rfq is None:
        return {"error": "RFQ not found"}

    total_price = rfq["quantity"] * unit_price

    create_quote(
        rfq_id,
        unit_price,
        total_price
    )

    return RedirectResponse(
        url=f"/rfq/{rfq_id}",
        status_code=303
    )

@app.get("/rfq/{rfq_id}/quote/pdf")
async def download_quote_pdf(
    request: Request,
    rfq_id: int
):

    if not request.session.get("logged_in"):
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    rfqs = get_rfqs()

    rfq = None

    for item in rfqs:
        if item["id"] == rfq_id:
            rfq = item
            break

    if rfq is None:
        return {"error": "RFQ not found"}

    if rfq["unit_price"] is None:
        return {"error": "No quote has been created yet"}

    filename = generate_quote_pdf(rfq)

    return FileResponse(
        path=filename,
        filename=filename,
        media_type="application/pdf"
    )

@app.post("/rfq/{rfq_id}/delete")
async def delete_rfq_route(
    request: Request,
    rfq_id: int
):

    if not request.session.get("logged_in"):
        return RedirectResponse(
            url="/login",
            status_code=303
        )

    delete_rfq(rfq_id)

    return RedirectResponse(
        url="/",
        status_code=303
    )

@app.get("/login")
async def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "error": None
        }
    )


@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):

    if (
    username == os.getenv("APP_USERNAME")
    and password == os.getenv("APP_PASSWORD")
):

        request.session["logged_in"] = True

        return RedirectResponse(
            url="/",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "error": "Invalid username or password."
        }
    )

@app.get("/logout")
async def logout(request: Request):

    request.session.clear()

    return RedirectResponse(
        url="/login",
        status_code=303
    )