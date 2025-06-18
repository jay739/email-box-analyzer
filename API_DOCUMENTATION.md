# Email Box Analyzer API Documentation

## Overview

The Email Box Analyzer API is a RESTful service built with FastAPI that provides comprehensive email analysis capabilities. The API supports multiple email providers, real-time analysis, and interactive visualizations.

## Base URL

- **Development**: `http://localhost:8000`
- **Production**: `https://api.emailanalyzer.com`

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Most endpoints require authentication except for registration and login.

### Getting Started

1. **Register a new user**:
   ```bash
   POST /api/auth/register
   ```

2. **Login to get access token**:
   ```bash
   POST /api/auth/login
   ```

3. **Include token in requests**:
   ```bash
   Authorization: Bearer <your_access_token>
   ```

## API Endpoints

### Authentication

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "name": "John Doe"
}
```

**Response**:
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": "user_123",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response**:
```json
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

#### Refresh Token
```http
POST /api/auth/refresh
Authorization: Bearer <refresh_token>
```

#### Logout
```http
POST /api/auth/logout
Authorization: Bearer <access_token>
```

### Email Providers

#### Get All Providers
```http
GET /api/providers
Authorization: Bearer <access_token>
```

**Response**:
```json
[
  {
    "id": "gmail",
    "name": "Gmail",
    "imap_host": "imap.gmail.com",
    "imap_port": 993,
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "use_ssl": true,
    "use_tls": true,
    "oauth2_supported": true
  },
  {
    "id": "outlook",
    "name": "Outlook/Hotmail",
    "imap_host": "outlook.office365.com",
    "imap_port": 993,
    "smtp_host": "smtp-mail.outlook.com",
    "smtp_port": 587,
    "use_ssl": true,
    "use_tls": true,
    "oauth2_supported": true
  }
]
```

#### Get Specific Provider
```http
GET /api/providers/{provider_id}
Authorization: Bearer <access_token>
```

### Email Connection

#### Connect to Email Account
```http
POST /api/email/connect
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "provider_id": "gmail",
  "email": "user@gmail.com",
  "password": "app_password"
}
```

**Response**:
```json
{
  "connected": true,
  "message": "Successfully connected to email account",
  "folders": [
    {
      "name": "INBOX",
      "path": "INBOX",
      "message_count": 1250,
      "unread_count": 45,
      "flags": ["\\Seen", "\\Answered"]
    }
  ],
  "stats": {
    "total_emails": 1250,
    "unread_emails": 45,
    "total_size_mb": 125.5,
    "oldest_email": "2023-01-01T00:00:00Z",
    "newest_email": "2024-01-01T00:00:00Z"
  }
}
```

#### Get Email Folders
```http
GET /api/email/folders
Authorization: Bearer <access_token>
```

#### Get Email Statistics
```http
GET /api/email/stats?folder=INBOX
Authorization: Bearer <access_token>
```

#### Get Emails
```http
GET /api/email/emails?folder=INBOX&limit=50&offset=0
Authorization: Bearer <access_token>
```

**Response**:
```json
[
  {
    "id": "email_123",
    "subject": "Meeting Tomorrow",
    "sender": "colleague@company.com",
    "recipients": ["user@gmail.com"],
    "cc": [],
    "bcc": [],
    "date": "2024-01-01T10:00:00Z",
    "body": "Hi, let's meet tomorrow at 2 PM...",
    "html_body": "<p>Hi, let's meet tomorrow at 2 PM...</p>",
    "attachments": [],
    "flags": ["\\Seen"],
    "size": 1024,
    "thread_id": "thread_456",
    "message_id": "<message@company.com>"
  }
]
```

#### Get Specific Email
```http
GET /api/email/emails/{email_id}?folder=INBOX
Authorization: Bearer <access_token>
```

#### Get Connection Status
```http
GET /api/email/status
Authorization: Bearer <access_token>
```

#### Disconnect from Email
```http
POST /api/email/disconnect
Authorization: Bearer <access_token>
```

### Analysis

#### Start Analysis
```http
POST /api/analysis/start
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "folder": "INBOX",
  "limit": 1000,
  "include_attachments": true,
  "include_sentiment": true
}
```

**Response**:
```json
{
  "analysis_id": "analysis_789"
}
```

#### Get Analysis Status
```http
GET /api/analysis/{analysis_id}/status
Authorization: Bearer <access_token>
```

**Response**:
```json
{
  "analysis_id": "analysis_789",
  "status": "running",
  "progress": 45,
  "current_step": "Analyzing emails...",
  "error": null,
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:05:00Z"
}
```

#### Get Analysis Results
```http
GET /api/analysis/{analysis_id}/results
Authorization: Bearer <access_token>
```

**Response**:
```json
{
  "success": true,
  "analysis": {
    "analysis_id": "analysis_789",
    "total_emails": 1000,
    "date_range": {
      "start": "2023-01-01T00:00:00Z",
      "end": "2024-01-01T00:00:00Z"
    },
    "total_size_mb": 125.5,
    "top_senders": [
      {
        "email": "colleague@company.com",
        "name": "John Colleague",
        "count": 150,
        "percentage": 15.0
      }
    ],
    "activity_by_time": {
      "hourly": {
        "0": 25,
        "1": 15,
        "2": 10
      },
      "daily": {
        "Monday": 200,
        "Tuesday": 180,
        "Wednesday": 220
      },
      "monthly": {
        "January": 2500,
        "February": 2300
      }
    },
    "attachment_stats": {
      "total_attachments": 150,
      "attachment_types": {
        "pdf": 50,
        "docx": 30,
        "jpg": 25
      },
      "total_attachment_size_mb": 25.5
    },
    "sentiment_analysis": {
      "positive": 600,
      "negative": 200,
      "neutral": 200,
      "sentiment_distribution": {
        "very_positive": 100,
        "positive": 500,
        "neutral": 200,
        "negative": 150,
        "very_negative": 50
      }
    },
    "thread_analysis": {
      "total_threads": 50,
      "average_thread_length": 20,
      "longest_thread": 150,
      "thread_topics": [
        {
          "topic": "Project Discussion",
          "count": 15,
          "emails": 300
        }
      ]
    },
    "domain_analysis": {
      "top_domains": [
        {
          "domain": "company.com",
          "count": 500,
          "percentage": 50.0
        }
      ],
      "domain_categories": {
        "work": 600,
        "personal": 300,
        "newsletter": 100
      }
    },
    "keyword_analysis": {
      "most_common_words": [
        {
          "word": "meeting",
          "count": 150,
          "frequency": 0.15
        }
      ],
      "keyword_trends": {
        "meeting": [10, 15, 20, 25],
        "project": [5, 8, 12, 15]
      }
    },
    "response_time_analysis": {
      "average_response_time_hours": 4.5,
      "response_time_distribution": {
        "immediate": 100,
        "within_1_hour": 200,
        "within_24_hours": 400,
        "within_week": 200,
        "no_response": 100
      }
    },
    "email_size_distribution": {
      "small": 600,
      "medium": 300,
      "large": 100
    },
    "language_analysis": {
      "primary_language": "en",
      "language_distribution": {
        "en": 900,
        "es": 50,
        "fr": 30,
        "de": 20
      }
    },
    "created_at": "2024-01-01T10:00:00Z",
    "processing_time_seconds": 45.5
  },
  "error": null
}
```

#### Get Last Analysis
```http
GET /api/analysis/last
Authorization: Bearer <access_token>
```

#### List All Analyses
```http
GET /api/analysis?limit=10&offset=0
Authorization: Bearer <access_token>
```

#### Delete Analysis
```http
DELETE /api/analysis/{analysis_id}
Authorization: Bearer <access_token>
```

### Charts and Visualizations

#### Generate Charts
```http
POST /api/charts/{analysis_id}/generate
Authorization: Bearer <access_token>
```

**Response**:
```json
{
  "charts": {
    "activity_timeline": {
      "type": "line",
      "title": "Email Activity Timeline",
      "data": [
        {
          "date": "2024-01-01",
          "count": 25
        }
      ],
      "options": {
        "xAxis": {
          "type": "time"
        },
        "yAxis": {
          "title": "Email Count"
        }
      }
    },
    "sender_distribution": {
      "type": "pie",
      "title": "Top Senders",
      "data": [
        {
          "name": "John Colleague",
          "value": 150
        }
      ],
      "options": {
        "legend": {
          "position": "right"
        }
      }
    }
  },
  "chart_urls": {
    "activity_timeline": "/api/charts/analysis_789/activity_timeline/image",
    "sender_distribution": "/api/charts/analysis_789/sender_distribution/image"
  }
}
```

#### Get Chart Image
```http
GET /api/charts/{analysis_id}/{chart_name}/image
Authorization: Bearer <access_token>
```

#### Get Analysis Charts
```http
GET /api/charts/{analysis_id}/charts
Authorization: Bearer <access_token>
```

#### Delete Analysis Charts
```http
DELETE /api/charts/{analysis_id}/charts
Authorization: Bearer <access_token>
```

### Export

#### Export Analysis Results
```http
POST /api/analysis/{analysis_id}/export
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "format": "json",
  "include_charts": true,
  "include_raw_data": false
}
```

**Response**:
```json
{
  "success": true,
  "file_name": "email_analysis_analysis_789_20241201_120000.json",
  "file_size": 1024,
  "file_url": "/api/export/analysis_789/download/json"
}
```

#### Download Export
```http
GET /api/analysis/{analysis_id}/download/{format}
Authorization: Bearer <access_token>
```

#### List Exports
```http
GET /api/analysis/{analysis_id}/exports
Authorization: Bearer <access_token>
```

## Error Responses

### Standard Error Format
```json
{
  "detail": "Error message description",
  "error_code": "ERROR_CODE",
  "timestamp": "2024-01-01T10:00:00Z"
}
```

### Common Error Codes

- `AUTHENTICATION_FAILED`: Invalid credentials
- `TOKEN_EXPIRED`: Access token has expired
- `INSUFFICIENT_PERMISSIONS`: User lacks required permissions
- `EMAIL_CONNECTION_FAILED`: Failed to connect to email server
- `ANALYSIS_NOT_FOUND`: Analysis with specified ID not found
- `ANALYSIS_IN_PROGRESS`: Analysis is still running
- `INVALID_PROVIDER`: Unsupported email provider
- `RATE_LIMIT_EXCEEDED`: Too many requests

### HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Service temporarily unavailable

## Rate Limiting

The API implements rate limiting to ensure fair usage:

- **Authentication endpoints**: 10 requests per minute
- **Email operations**: 100 requests per hour
- **Analysis operations**: 10 requests per hour
- **Chart generation**: 50 requests per hour
- **Export operations**: 20 requests per hour

## Pagination

List endpoints support pagination using `limit` and `offset` parameters:

```http
GET /api/analysis?limit=20&offset=40
```

**Response**:
```json
{
  "data": [...],
  "pagination": {
    "total": 100,
    "limit": 20,
    "offset": 40,
    "has_next": true,
    "has_prev": true
  }
}
```

## WebSocket Support

For real-time updates during analysis, the API supports WebSocket connections:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/analysis/{analysis_id}');

ws.onmessage = function(event) {
  const data = JSON.parse(event.data);
  console.log('Analysis progress:', data.progress);
};
```

## SDKs and Libraries

### Python
```python
from email_analyzer_api import EmailAnalyzerAPI

api = EmailAnalyzerAPI(base_url="http://localhost:8000")
api.login("user@example.com", "password")
analysis = api.start_analysis(folder="INBOX", limit=1000)
```

### JavaScript/TypeScript
```typescript
import { EmailAnalyzerAPI } from '@email-analyzer/api-client';

const api = new EmailAnalyzerAPI({ baseURL: 'http://localhost:8000' });
await api.login('user@example.com', 'password');
const analysis = await api.startAnalysis({ folder: 'INBOX', limit: 1000 });
```

## Examples

### Complete Analysis Workflow

```python
import requests

# 1. Login
response = requests.post('http://localhost:8000/api/auth/login', json={
    'email': 'user@example.com',
    'password': 'password'
})
token = response.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

# 2. Connect to email
response = requests.post('http://localhost:8000/api/email/connect', 
    headers=headers, json={
        'provider_id': 'gmail',
        'email': 'user@gmail.com',
        'password': 'app_password'
    })

# 3. Start analysis
response = requests.post('http://localhost:8000/api/analysis/start',
    headers=headers, json={
        'folder': 'INBOX',
        'limit': 1000,
        'include_sentiment': True
    })
analysis_id = response.json()['analysis_id']

# 4. Monitor progress
while True:
    response = requests.get(f'http://localhost:8000/api/analysis/{analysis_id}/status',
        headers=headers)
    status = response.json()
    
    if status['status'] == 'completed':
        break
    elif status['status'] == 'failed':
        raise Exception(f"Analysis failed: {status['error']}")
    
    time.sleep(5)

# 5. Get results
response = requests.get(f'http://localhost:8000/api/analysis/{analysis_id}/results',
    headers=headers)
results = response.json()['analysis']

# 6. Generate charts
response = requests.post(f'http://localhost:8000/api/charts/{analysis_id}/generate',
    headers=headers)
charts = response.json()

# 7. Export results
response = requests.post(f'http://localhost:8000/api/analysis/{analysis_id}/export',
    headers=headers, json={'format': 'json'})
export_info = response.json()
```

## Support

For API support and questions:

- **Documentation**: https://docs.emailanalyzer.com
- **API Status**: https://status.emailanalyzer.com
- **Support Email**: api-support@emailanalyzer.com
- **GitHub Issues**: https://github.com/emailanalyzer/email-box-analyzer/issues 