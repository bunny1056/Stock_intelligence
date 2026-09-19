import os
from pathlib import Path

from dotenv import load_dotenv
from pypdf import PdfReader

from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

REPORT_DIR = Path("data/reports")
VECTORSTORE_DIR = "vectorstore"

COMPANIES = [
    "RELIANCE",
    "TCS",
    "INFY",
    "HDFCBANK",
    "ICICIBANK",
    "ITC",
    "HINDUNILVR",
    "MARUTI",
    "SUNPHARMA",
    "BHARTIARTL"
]


def load_pdf(pdf_path, company):
    documents = []

    reader = PdfReader(str(pdf_path))

    for page_number, page in enumerate(reader.pages):
        text = page.extract_text()

        if not text:
            continue

        documents.append(
            Document(
                page_content=text,
                metadata={
                    "company": company,
                    "source": pdf_path.name,
                    "page": page_number + 1
                }
            )
        )

    return documents


def load_all_reports():
    documents = []

    for company in COMPANIES:
        company_dir = REPORT_DIR / company

        if not company_dir.exists():
            continue

        for pdf_file in company_dir.glob("*.pdf"):
            print(f"Processing {company}: {pdf_file.name}")
            documents.extend(load_pdf(pdf_file, company))

    return documents


def build_vectorstore():
    documents = load_all_reports()

    print(f"\nLoaded {len(documents)} pages")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    vectorstore.save_local(VECTORSTORE_DIR)

    print("FAISS vector database created successfully.")


if __name__ == "__main__":
    build_vectorstore()
