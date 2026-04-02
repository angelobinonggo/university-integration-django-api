# University Integration Platform

> **Laboratory Activity — IT322 Integrative Programming**  
> Django REST Framework · Hub-and-Spoke Architecture

---

## Overview

A mini University Integration System that demonstrates how multiple independent subsystems communicate through a **central Integration Hub** using REST APIs.

### Architecture: Hub-and-Spoke

```
               ┌──────────────────┐
               │  Integration Hub │   ← Central router & aggregator
               └────────┬─────────┘
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
   ┌────────────┐ ┌──────────┐ ┌───────────┐
   │ Student App│ │Library   │ │ Payment   │
   │  (spoke)   │ │App(spoke)│ │ App(spoke)│
   └────────────┘ └──────────┘ └───────────┘
```

---

## Integration Patterns Applied

| Pattern | Where Used |
|---|---|
| **Request-Response** | Hub queries each spoke via internal ORM calls |
| **Message Routing** | Hub routes each request to the correct spoke |
| **Data Transformation** | Hub aggregates + normalizes spoke responses into a unified payload |
| **Aggregator** | `/api/hub/all-summaries/` combines data for all students |

---

## Project Structure

```
university-integration-django-api/
├── university_integration/      # Django project (settings, urls)
├── student_app/                 # Spoke 1 — Student profiles
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── management/commands/seed_data.py
├── library_app/                 # Spoke 2 — Library fines
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── admin.py
│   └── urls.py
├── payment_app/                 # Spoke 3 — Tuition payments
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── admin.py
│   └── urls.py
└── integration_hub/             # Central Hub — routes & aggregates
    ├── views.py
    └── urls.py
```

---

## Setup & Run

```bash
# 1. Install dependencies
pip install django djangorestframework

# 2. Run migrations
python manage.py makemigrations student_app library_app payment_app
python manage.py migrate

# 3. Seed sample data
python manage.py seed_data

# 4. Start the server
python manage.py runserver
```

---

## API Endpoints

### Spoke — Student App
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/students/` | List all students |
| POST | `/api/students/` | Create a student |
| GET | `/api/students/{id}/` | Get student by DB id |
| PUT/PATCH | `/api/students/{id}/` | Update student |
| DELETE | `/api/students/{id}/` | Delete student |
| GET | `/api/students/by_student_id/?student_id=S001` | Lookup by student_id |

### Spoke — Library App
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/library/` | List all records |
| POST | `/api/library/` | Create a record |
| GET | `/api/library/{id}/` | Get record |
| GET | `/api/library/by_student_id/?student_id=S001` | Lookup by student_id |

### Spoke — Payment App
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/payments/` | List all payments |
| POST | `/api/payments/` | Record a payment |
| GET | `/api/payments/{id}/` | Get payment |
| GET | `/api/payments/by_student_id/?student_id=S001` | List by student_id |

### Hub — Integration Hub
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/hub/health/` | System health — all spoke status |
| GET | `/api/hub/student-summary/?student_id=S001` | Unified student report |
| GET | `/api/hub/all-summaries/` | All student summaries (Aggregator) |

---

## Sample Hub Response

```json
GET /api/hub/student-summary/?student_id=S001

{
  "integration_pattern": "Hub-and-Spoke | Request-Response | Data Transformation",
  "hub": "University Integration Platform",
  "student_profile": {
    "student_id": "S001",
    "name": "Juan dela Cruz",
    "course": "BS Information Technology",
    "year_level": 3,
    "is_enrolled": true
  },
  "library_standing": {
    "has_fines": false,
    "amount_due": "0.00",
    "library_status": "CLEAR"
  },
  "payment_summary": {
    "total_paid": 15500.0,
    "payment_count": 2,
    "payments": [...]
  },
  "clearance_status": {
    "cleared": true,
    "status": "CLEARED",
    "issues": []
  }
}
```

---

## Sample Data

Run `python manage.py seed_data` to load:

| Student ID | Name | Library | Payments |
|---|---|---|---|
| S001 | Juan dela Cruz | CLEAR | ₱15,500 paid |
| S002 | Maria Santos | HOLD (₱150 fine) | ₱15,000 paid |
| S003 | Pedro Reyes | CLEAR | ₱10,000 pending |
| S004 | Ana Garcia | No record | No payment |

---

*IT322 — Integrative Programming | Lab Activity Module 1*
