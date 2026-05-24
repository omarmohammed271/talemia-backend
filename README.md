# Starrise III — Django REST API

Django API serving all 6 BD dashboards from the gold Postgres schema.

## Project Structure

```
starrise_api/
├── .env
├── requirements.txt
├── manage.py
├── starrise_api/
│   ├── settings.py
│   └── urls.py
└── dashboards/
    ├── db.py          ← raw psycopg2 connection
    ├── queries.py     ← one SQL query per dashboard
    ├── views.py       ← APIView per dashboard
    └── urls.py        ← route definitions
```

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Make sure the pipeline has run first
cd ../starrise_pipeline
python run_pipeline.py

# 3. Run the API server
cd ../starrise_api
python manage.py runserver
```

## Endpoints

| Method | URL | Dashboard |
|--------|-----|-----------|
| GET | `/api/dashboard/1/` | BD Executive |
| GET | `/api/dashboard/2/` | Financials |
| GET | `/api/dashboard/3/` | Business Line |
| GET | `/api/dashboard/4/` | Account Manager |
| GET | `/api/dashboard/5/` | Commercial |
| GET | `/api/dashboard/6/` | All Opportunities |
| GET | `/api/dashboard/6/<id>/` | Single Opportunity |

## Filters (Dashboard 6 only)

```
GET /api/dashboard/6/?status=won
GET /api/dashboard/6/?business_line=Human Capital
GET /api/dashboard/6/?bd_owner=Afnan
GET /api/dashboard/6/?status=in_progress&bd_owner=Amal
```

## Example Response — Dashboard 1

```json
{
  "total_opportunities": 61,
  "in_progress": 46,
  "won_count": 10,
  "lost_count": 5,
  "won_value_sar": 2321152003.0,
  "win_rate_pct": 66.7,
  "stages": [
    {"stage": "Opportunity Development", "count": 22},
    {"stage": "Proposal Development",    "count": 8}
  ],
  "win_loss_ratio": [
    {"status": "won",  "count": 10, "pct": 66.7},
    {"status": "lost", "count": 5,  "pct": 33.3}
  ]
}
```
