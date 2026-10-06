# AI RFQ Processor

A web application that uses AI to process Requests for Quotation (RFQs).

It extracts information from RFQ documents, saves it to a database, and lets users manage RFQs from a dashboard.

## Features

* Upload PDFs and images
* Extract text using PDF tools and OCR
* Use AI to extract RFQ details
* Store data in SQLite
* Search and filter RFQs
* Update RFQ status

## Built With

* Python
* FastAPI
* SQLite
* HTML/CSS
* Groq API
* Tesseract OCR

## How It Works

```text
RFQ
 ↓
Extract text
 ↓
AI processes it
 ↓
Save to SQLite
 ↓
View on dashboard
```

## Run Locally

Clone the repository:

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

If PowerShell gives an execution policy error:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate again:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required packages:

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

Open:

```text
http://127.0.0.1:8000
```

## Why I Made It

I built this project to learn more about Python, APIs, databases, OCR and AI while exploring how automation could make repetitive business processes faster and more efficient.
