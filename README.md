# AI RFQ Processor

A small web application for processing Requests for Quotation (RFQs).

The idea is to take an RFQ document, extract the important information, and store it in a database so it can be searched and managed from a dashboard. 

## Features

* Upload RFQ PDFs and images
* Extract text from PDFs
* OCR for scanned documents and images
* Use an LLM to extract RFQ information
* Store RFQs in SQLite
* View individual RFQs
* Update RFQ status
* Search by company or product
* Filter RFQs by status

## Tech Stack

* Python
* FastAPI
* SQLite
* Jinja2
* HTML/CSS
* Groq API
* Tesseract OCR
* pypdf

## How it works

```text
RFQ file
   ↓
PDF / OCR text extraction
   ↓
AI processing
   ↓
Structured RFQ data
   ↓
SQLite database
   ↓
Web dashboard
```

## Running locally

Clone the repository and enter the project directory:

```bash
git clone https://github.com/chealyC/ai-rfq-processor.git
cd ai-rfq-processor
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks the script with an execution policy error, run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate the environment again:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add your Groq API key:

```env
GROQ_API_KEY=your_api_key_here
```

Start the application:

```bash
uvicorn web_app:app --reload
```

Then open:

```text
http://127.0.0.1:8000
```

## Project Structure

```text
ai-rfq-processor/
├── ai_processor.py
├── database.py
├── main.py
├── ocr_reader.py
├── pdf_reader.py
├── web_app.py
├── requirements.txt
├── static/
│   └── style.css
├── templates/
│   ├── index.html
│   └── rfq.html
└── uploads/
```

## Why I made it

This project was built as a practical project to learn more about APIs, databases, OCR, AI integration and web development with Python.

I'm also interested in how smaller businesses could use simple software to automate repetitive administrative work.
