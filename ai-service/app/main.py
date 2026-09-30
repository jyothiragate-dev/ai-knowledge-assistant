from pathlib import Path
import shutil

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.generation.rag_service import generate_answer
from app.ingestion.ingestion_service import (
    DOCUMENTS_DIRECTORY,
    ingest_pdf,
)
from app.schemas.query import QueryRequest, QueryResponse


app = FastAPI(
    title="AI Knowledge Assistant",
    version="1.0.0"
)


# Allow Angular frontend to communicate directly with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ai-service"
    }


@app.post("/query", response_model=QueryResponse)
def query_knowledge_base(request: QueryRequest):
    try:
        result = generate_answer(request.query)
        return result

    except Exception as error:
        print(f"Error while processing query: {error}")

        raise HTTPException(
            status_code=500,
            detail="Unable to process the query at this time."
        )


@app.post("/documents/upload")
def upload_document(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    try:
        DOCUMENTS_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True
        )

        safe_filename = Path(
            file.filename or "document.pdf"
        ).name

        file_path = (
            DOCUMENTS_DIRECTORY /
            safe_filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        result = ingest_pdf(
            str(file_path)
        )

        return {
            "message":
                "Document uploaded and indexed successfully.",
            "filename": safe_filename,
            "pages": result["pages"],
            "chunks": result["chunks"]
        }

    except HTTPException:
        raise

    except Exception as error:
        print(
            f"Error while uploading document: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=
                "Unable to upload and index the document."
        )

    finally:
        file.file.close()