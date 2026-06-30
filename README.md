# SmileCare Dental API

An AI-powered dental clinic receptionist API built with **FastAPI** and **Mistral AI**. The service understands user messages, detects intent, extracts booking-related entities, and returns structured JSON responses grounded in SmileCare Dental clinic information.

## Features

- **Intent detection** — Classifies user messages into supported intents (greeting, service inquiry, appointment booking, clinic hours, contact info, and more).
- **Entity extraction** — Pulls structured fields such as `service`, `date`, and `time` from booking requests.
- **Clinic-grounded answers** — Responses are constrained to SmileCare Dental services, hours, and contact details defined in the system prompt.
- **Structured API output** — Every chat response returns `intent`, `entities`, and a natural-language `response`.
- **Interactive docs** — Swagger UI available at `/docs` when the server is running.

## Tech Stack


| Layer         | Technology                                                  |
| ------------- | ----------------------------------------------------------- |
| API framework | [FastAPI](https://fastapi.tiangolo.com/)                    |
| ASGI server   | [Uvicorn](https://www.uvicorn.org/)                         |
| LLM           | [Mistral AI](https://mistral.ai/) via `langchain-mistralai` |
| Validation    | [Pydantic](https://docs.pydantic.dev/)                      |
| Config        | `python-dotenv`                                             |


## Project Structure

```
SmileCare-Dental/
├── src/
│   ├── main.py              # FastAPI app entry point
│   ├── core/
│   │   └── logger.py        # Logging configuration
│   ├── routes/
│   │   └── chat_route.py    # Chat endpoint and response parsing
│   ├── schemas/
│   │   └── chatSchema.py    # Request/response models
│   └── llm/
│       ├── llm.py           # Mistral LLM client configuration
│       └── PROMPT.py        # System prompt and clinic knowledge base
├── photos/                  # API output reference screenshots
│   ├── Screenshot 2026-06-30 115010.png
│   ├── Screenshot 2026-06-30 115100.png
│   ├── Screenshot 2026-06-30 115129.png
│   ├── Screenshot 2026-06-30 120035.png
│   ├── Screenshot 2026-06-30 120047.png
│   └── Screenshot 2026-06-30 120052.png
├── .env                     # Environment variables (not committed)
└── README.md
```

## Prerequisites

- Python 3.10+
- A [Mistral AI API key](https://console.mistral.ai/)

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd SmileCare-Dental
```

### 2. Create and activate a virtual environment

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install fastapi uvicorn langchain-mistralai python-dotenv
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
LOG_LEVEL=INFO
```

## Running the Server

From the project root:

```bash
uvicorn src.main:app --reload
```

The API will be available at:

- **Base URL:** `http://127.0.0.1:8000`
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

## API Endpoints

### `GET /`

Health check for the API.

**Response**

```json
{
  "message": "Dental API is running"
}
```

### `GET /health`

Service health status.

**Response**

```json
{
  "status": "healthy"
}
```

### `POST /chat/`

Send a user message to the AI receptionist.

**Request body**

```json
{
  "messages": "Do you provide braces?"
}
```

**Response**

```json
{
  "intent": "service_inquiry",
  "entities": {
    "service": "Braces"
  },
  "response": "Yes, SmileCare Dental offers Braces treatment."
}
```

## Supported Intents

The AI receptionist is configured to handle the following intents:


| Intent                 | Description                           |
| ---------------------- | ------------------------------------- |
| `greeting`             | Hello, hi, good morning, etc.         |
| `service_inquiry`      | Questions about available treatments  |
| `book_appointment`     | Scheduling or booking a visit         |
| `clinic_hours`         | Operating hours questions             |
| `contact_info`         | Phone, email, or contact details      |
| `service_availability` | Whether a specific service is offered |
| `unsupported_service`  | Requests for services not listed      |
| `clinic_information`   | General clinic overview               |
| `goodbye`              | Thanks, bye, see you                  |


## Clinic Information (Knowledge Base)

The assistant uses the following SmileCare Dental details:

- **Hours:** Monday–Friday, 10:00 AM – 7:00 PM
- **Services:** Dental Cleaning, Root Canal, Braces, Teeth Whitening
- **Phone:** 9876543210
- **Email:** [support@smilecare.com](mailto:support@smilecare.com)

Clinic details and intent rules are defined in `src/llm/PROMPT.py` and can be updated there without changing application code.

## Example Usage

**cURL**

```bash
curl -X POST "http://127.0.0.1:8000/chat/" \
  -H "Content-Type: application/json" \
  -d "{\"messages\": \"I want to book a root canal next Tuesday at 11 AM\"}"
```

**PowerShell**

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/chat/" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"messages": "Hello"}'
```

## Output Reference

The screenshots below show real API behaviour from Swagger UI (`/docs`), server logs, and the interactive API documentation at `http://127.0.0.1:8000`.

### API Documentation (Swagger UI)

Overview of available endpoints and schemas in `/docs`.

![Swagger UI API documentation](photos/Screenshot%202026-06-30%20120052.png)

---

### Greeting

**Input:** `"Hi"`

![Greeting intent response](photos/Screenshot%202026-06-30%20115010.png)

```json
{
  "intent": "greeting",
  "entities": {},
  "response": "Hello! Welcome to SmileCare Dental. How can I assist you today?"
}
```

### Clinic Hours

**Input:** `"What are your timings?"`

![Clinic hours intent response](photos/Screenshot%202026-06-30%20115100.png)

```json
{
  "intent": "clinic_hours",
  "entities": {},
  "response": "SmileCare Dental is open Monday to Friday from 10:00 AM to 7:00 PM."
}
```

### Clinic Information

**Input:** `"What services do you provide?"`

![Clinic information intent response](photos/Screenshot%202026-06-30%20115129.png)

```json
{
  "intent": "clinic_information",
  "entities": {},
  "response": "SmileCare Dental offers the following services: Dental Cleaning, Root Canal, Braces, and Teeth Whitening. We are open Monday to Friday from 10:00 AM to 7:00 PM."
}
```

### Appointment Booking

**Input:** `"Book root canal tomorrow"`

![Appointment booking intent response](photos/Screenshot%202026-06-30%20120047.png)

```json
{
  "intent": "book_appointment",
  "entities": {
    "service": "Root Canal",
    "date": "tomorrow",
    "time": null
  },
  "response": "I'd be happy to help schedule your Root Canal appointment. What time would you prefer tomorrow? Our clinic is open from 10:00 AM to 7:00 PM."
}
```

### Server Logs

Structured logging output when handling a chat request (intent detection, entity extraction, and `200 OK` response).

![Server logs for chat request](photos/Screenshot%202026-06-30%20120035.png)

```
2026-06-30 12:00:08 | INFO     | src.main | SmileCare Dental API starting
2026-06-30 12:00:21 | INFO     | src.routes.chat_route | Chat request received: message='Book root canal tomorrow'
2026-06-30 12:00:23 | INFO     | src.routes.chat_route | Chat response: intent='book_appointment' entities={'service': 'Root Canal', 'date': 'tomorrow', 'time': None}
INFO: 127.0.0.1:54328 - "POST /chat/ HTTP/1.1" 200 OK
```

## How It Works

1. The client sends a plain-text `messages` field to `POST /chat/`.
2. The message is appended to the system prompt from `PROMPT.py`.
3. The Mistral model (`mistral-large-latest`) generates a structured JSON response.
4. The API strips optional markdown code fences and parses the JSON.
5. A typed `ChatResponse` is returned with `intent`, `entities`, and `response`.
6. Structured logs record each request, detected intent, entities, and response status.

