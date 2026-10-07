# AI RFQ Processor

An AI-powered web application for processing Requests for Quotation (RFQs).

The application extracts structured information from RFQ documents, stores the data in a database, and provides a dashboard for reviewing RFQs, creating quotations, and generating customer email responses.

## Features

- Upload PDF and image-based RFQs
- Extract text from PDFs
- OCR for scanned documents and images
- AI-powered RFQ information extraction
- SQLite database storage
- RFQ search and filtering
- RFQ status management
- Automatic quotation calculations
- PDF quotation generation
- AI-generated customer email drafts
- Editable and persistent email drafts
- Session-based authentication
- File upload size limits and temporary file cleanup

## Tech Stack

- Python
- FastAPI
- SQLite
- Jinja2
- HTML / CSS
- Groq API
- OpenAI-compatible API
- Tesseract OCR
- PyPDF
- ReportLab
- Git / GitHub

## How It Works

```text
RFQ Document
     ↓
PDF / Image Text Extraction
     ↓
AI Information Extraction
     ↓
Structured RFQ Data
     ↓
SQLite Database
     ↓
RFQ Dashboard
     ↓
Create Quote
     ↓
Generate Customer Email
