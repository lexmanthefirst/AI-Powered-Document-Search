# RAG Chatbot API

AI-powered document search and RAG (Retrieval Augmented Generation) query service built with FastAPI, PostgreSQL, ChromaDB, and OpenRouter.

## Features

- **Document Ingestion**: Upload and process PDF, DOCX, and TXT files
- **Vector Search**: Semantic search using ChromaDB for efficient retrieval
- **RAG Query**: Answer questions using retrieved context with OpenRouter LLMs
- **ACID Compliant**: PostgreSQL with proper transaction management
- **Correlation ID Tracking**: Request tracing for debugging and monitoring
- **Async Everything**: Built with async/await for high performance

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with asyncpg
- **Vector Store**: ChromaDB
- **LLM Provider**: OpenRouter
- **ORM**: SQLAlchemy 2.0 (async)
- **Migrations**: Alembic

## Prerequisites

- Python 3.11+
- PostgreSQL 14+
- OpenRouter API Key

## Installation

1. **Clone and navigate to the project**
```bash
cd RAG-chatbot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
Edit `.env` file:
```env
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/rag_chatbot
OPENROUTER_API_KEY=your_key_here
DB_ECHO=False
LOG_LEVEL=INFO
```

4. **Setup PostgreSQL database**
```bash
createdb rag_chatbot
```

5. **Run Alembic migrations**
```bash
alembic upgrade head
```

## Running the Application

### Development
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

API will be available at `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

## API Endpoints

### Upload Document
```bash
POST /documents/upload
Content-Type: multipart/form-data

curl -X POST "http://localhost:8000/documents/upload" \
  -H "X-Correlation-ID: unique-id-123" \
  -F "file=@document.pdf"
```

### Query RAG
```bash
POST /query/
Content-Type: application/json

{
  "question": "What is the main topic of the document?"
}
```

Response:
```json
{
  "answer": "The main topic is...",
  "retrieved_chunks": [
    {
      "text": "Relevant chunk content...",
      "similarity_score": 0.0,
      "source": "document.pdf"
    }
  ]
}
```

### List Documents
```bash
GET /documents/
```

### Get Document Details
```bash
GET /documents/{document_id}
```

## Project Structure

```
RAG-chatbot/
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── documents.py      # Document management endpoints
│   │       └── query.py          # RAG query endpoint
│   ├── core/
│   │   ├── config.py             # Application settings
│   │   ├── database.py           # Database configuration
│   │   └── logging.py            # Structured logging
│   ├── middleware/
│   │   └── correlation_id.py    # Correlation ID middleware
│   ├── models/
│   │   ├── base.py               # Base models with CRUD
│   │   └── document.py           # Document model
│   ├── schemas/
│   │   ├── document.py           # Document schemas
│   │   └── query.py              # Query schemas
│   ├── services/
│   │   ├── ingestion.py          # Document ingestion logic
│   │   ├── llm_service.py        # OpenRouter integration
│   │   └── vector_store.py       # ChromaDB integration
│   ├── utils/
│   │   └── response.py           # Standard API responses
│   └── main.py                   # Application entry point
├── alembic/                      # Database migrations
├── tests/                        # Test suite
├── .env                          # Environment variables
└── requirements.txt              # Python dependencies
```

## Database Schema

### Documents Table
```sql
- id: VARCHAR (UUID, Primary Key)
- filename: VARCHAR
- content_type: VARCHAR
- file_size: INTEGER
- chunk_count: INTEGER
- created_at: TIMESTAMP WITH TIMEZONE
- updated_at: TIMESTAMP WITH TIMEZONE
```

## Vector Store

ChromaDB stores document chunks with:
- **Embeddings**: Generated via OpenRouter
- **Metadata**: `document_id`, `chunk_index`, `source`
- **Documents**: Text chunks (300-1000 characters)

## Configuration

### Database Settings
- Connection pooling configured for ACID compliance
- Read Committed isolation level
- Automatic rollback on errors

### Logging
- JSON-formatted structured logs
- Correlation ID tracking across requests
- Configurable log levels

## Development

### Running Tests
```bash
pytest tests/ -v
```

### Code Style
Follow PEP 8 guidelines.

## License

MIT
