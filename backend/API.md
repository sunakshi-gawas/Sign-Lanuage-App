# Backend API Documentation

Complete reference for all backend API endpoints, request/response formats, and usage examples.

## 📋 Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Server health check |
| GET | `/sign_gifs/{sign_name}` | Get sign animation GIF |
| POST | `/api/translate` | Translate text to signs |
| GET | `/docs` | Interactive API documentation (Swagger UI) |
| GET | `/redoc` | Alternative API documentation (ReDoc) |

## 🔌 Detailed Endpoint Reference

### 1. Health Check

**Endpoint:** `GET /api/health`

**Description:** Returns current server status, version, and timestamp for monitoring.

**Request:**
```bash
curl http://localhost:8000/api/health
```

**Response (200 OK):**
```json
{
  "status": "ok",
  "version": "1.0.0",
  "timestamp": "2025-12-15T10:30:45.123456Z"
}
```

**Use Cases:**
- Server uptime monitoring
- Load balancer health checks
- Connection verification before API calls

---

### 2. Get Sign GIF

**Endpoint:** `GET /sign_gifs/{sign_name}`

**Description:** Retrieves animated GIF for a specific sign to display in UI.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `sign_name` | string | Yes | Name of sign (e.g., "HELLO", "THANK") |

**Supported Signs:**
- BEST
- DISLIKE
- HELLO
- NO
- OK
- PEACE
- ROCK
- SORRY
- THANK
- YES
- YOU

**Request:**
```bash
curl http://localhost:8000/sign_gifs/HELLO \
  --output hello.gif

# Or with specific sign
curl http://localhost:8000/sign_gifs/THANK \
  --output thank.gif
```

**Response (200 OK):**
- **Content-Type:** `image/gif`
- **Body:** Binary GIF data

**Error Responses:**

```json
// 404 Not Found
{
  "detail": "Sign not found: INVALID"
}

// 500 Internal Server Error
{
  "detail": "Error loading GIF file"
}
```

**Example Python:**
```python
import requests

response = requests.get('http://localhost:8000/sign_gifs/HELLO')
if response.status_code == 200:
    with open('hello.gif', 'wb') as f:
        f.write(response.content)
```

**Example JavaScript/TypeScript:**
```typescript
const response = await fetch('http://localhost:8000/sign_gifs/HELLO');
const blob = await response.blob();
const url = URL.createObjectURL(blob);
const img = document.querySelector('img');
img.src = url;
```

---

### 3. Translate Text to Sign

**Endpoint:** `POST /api/translate`

**Description:** Converts text input to sign language sequence using ML model.

**Request Body:**

```json
{
  "text": "hello world",
  "language": "en"
}
```

**Parameters:**

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `text` | string | Yes | - | Text to translate (max 200 chars) |
| `language` | string | No | "en" | Language code (currently "en" only) |

**Request Examples:**

**Basic Request (curl):**
```bash
curl -X POST http://localhost:8000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "hello", "language": "en"}'
```

**With Options (curl):**
```bash
curl -X POST http://localhost:8000/api/translate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "thank you very much",
    "language": "en"
  }'
```

**Python Example:**
```python
import requests

payload = {
    "text": "hello world",
    "language": "en"
}

response = requests.post(
    'http://localhost:8000/api/translate',
    json=payload
)

if response.status_code == 200:
    result = response.json()
    print(f"Original: {result['original_text']}")
    print(f"Signs: {result['signs']}")
    print(f"Confidence: {result['confidence']}")
else:
    print(f"Error: {response.status_code}")
```

**JavaScript/TypeScript Example:**
```typescript
const payload = {
  text: "hello world",
  language: "en"
};

const response = await fetch('http://localhost:8000/api/translate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(payload)
});

const result = await response.json();
console.log('Detected signs:', result.signs);
console.log('Confidence:', result.confidence);
```

**Response (200 OK):**
```json
{
  "original_text": "hello world",
  "signs": [
    "HELLO",
    "DISLIKE"
  ],
  "confidence": 0.92,
  "timestamp": "2025-12-15T10:32:15.456789Z",
  "processing_time_ms": 245
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| `original_text` | string | Input text as received |
| `signs` | array | List of recognized signs |
| `confidence` | float | Confidence score (0.0-1.0) |
| `timestamp` | string | ISO 8601 timestamp |
| `processing_time_ms` | integer | Time to process request |

**Error Responses:**

```json
// 400 Bad Request - Invalid input
{
  "detail": [
    {
      "loc": ["body", "text"],
      "msg": "String should have at most 200 characters",
      "type": "string_too_long"
    }
  ]
}

// 422 Unprocessable Entity
{
  "detail": "ML Server not responding"
}

// 500 Internal Server Error
{
  "detail": "Error during translation"
}
```

**Common Error Scenarios:**

| Status | Error | Cause | Solution |
|--------|-------|-------|----------|
| 400 | Bad Request | Invalid JSON format | Check request body syntax |
| 400 | String too long | Text exceeds 200 chars | Reduce text length |
| 422 | ML Server not responding | Backend can't reach ML server | Start ML server (port 8001) |
| 500 | Internal Server Error | Unexpected error | Check server logs |

---

## 📊 Data Models (Pydantic)

### TranslateRequest

Request model for text translation:

```python
from pydantic import BaseModel, Field

class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=200)
    language: str = Field(default="en")
```

### TranslateResponse

Response model for translation:

```python
from datetime import datetime
from typing import List
from pydantic import BaseModel

class TranslateResponse(BaseModel):
    original_text: str
    signs: List[str]
    confidence: float
    timestamp: datetime
    processing_time_ms: int
```

### HealthResponse

Response model for health check:

```python
from datetime import datetime
from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime
```

---

## 🔐 Authentication & Security

Currently, the API is open. For production:

### Enable API Key Authentication

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    return api_key

@app.post("/api/translate")
async def translate(
    request: TranslateRequest,
    api_key: str = Depends(verify_api_key)
):
    # Your implementation
    pass
```

### Request Example with API Key

```bash
curl -X POST http://localhost:8000/api/translate \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-key" \
  -d '{"text": "hello"}'
```

---

## 🔄 Rate Limiting

### Add Rate Limiting (Future)

```bash
pip install slowapi
```

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/translate")
@limiter.limit("100/minute")
async def translate(request: TranslateRequest):
    pass
```

---

## 📈 Performance Considerations

### Caching Translations

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_signs_for_text(text: str):
    # Cached results
    pass
```

### Request Timeouts

```python
import asyncio
from fastapi import BackgroundTasks

@app.post("/api/translate")
async def translate(request: TranslateRequest, background_tasks: BackgroundTasks):
    try:
        result = await asyncio.wait_for(
            classify_signs(request.text),
            timeout=5.0  # 5 second timeout
        )
    except asyncio.TimeoutError:
        return {"error": "Request timed out"}
```

---

## 🧪 Testing Endpoints

### Automated Testing Script

```bash
#!/bin/bash
# test_api.sh

BASE_URL="http://localhost:8000"

echo "Testing Health Check..."
curl $BASE_URL/api/health

echo -e "\n\nTesting Translation..."
curl -X POST $BASE_URL/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "hello world", "language": "en"}'

echo -e "\n\nTesting Sign GIF..."
curl $BASE_URL/sign_gifs/HELLO -o test.gif
echo "GIF saved to test.gif"
```

Make executable and run:
```bash
chmod +x test_api.sh
./test_api.sh
```

---

## 🌍 CORS Configuration

The backend is configured for CORS to support mobile app requests:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://10.0.2.2:8000",  # Android emulator
        "http://localhost:8081"   # Flutter web
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📋 API Versioning

For future versions, use versioning:

```python
from fastapi import APIRouter

v1_router = APIRouter(prefix="/api/v1")
v2_router = APIRouter(prefix="/api/v2")

@v1_router.post("/translate")
async def translate_v1(request: TranslateRequest):
    pass

@v2_router.post("/translate")
async def translate_v2(request: TranslateRequest):
    # Enhanced implementation
    pass

app.include_router(v1_router)
app.include_router(v2_router)
```

---

## 🎯 Integration Examples

### Mobile App (Flutter)

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<List<String>> translateText(String text) async {
  final response = await http.post(
    Uri.parse('http://10.0.2.2:8000/api/translate'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({'text': text, 'language': 'en'}),
  );

  if (response.statusCode == 200) {
    final data = jsonDecode(response.body);
    return List<String>.from(data['signs']);
  }
  throw Exception('Failed to translate');
}
```

### Web Frontend (React)

```typescript
async function translateText(text: string): Promise<string[]> {
  const response = await fetch('http://localhost:8000/api/translate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, language: 'en' })
  });

  if (!response.ok) throw new Error('Translation failed');
  const data = await response.json();
  return data.signs;
}
```

---

## 📞 Support & Troubleshooting

### Check API Health
```bash
curl http://localhost:8000/api/health -v
```

### View Live Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Check Server Logs
```bash
tail -f /tmp/backend.log
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Connection refused | Ensure backend is running on port 8000 |
| CORS error | Check CORS origins in app/main.py |
| ML Server error | Ensure ML server is running on port 8001 |
| Model not found | Verify sign_model.h5 exists in app/services/ |

---

**Last Updated**: December 15, 2025  
**API Version**: 1.0.0
