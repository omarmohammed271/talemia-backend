"""
Dashboard API Views
Response format for dashboards 1-5:
  {
    "cards":  { ... },
    "charts": { ... }
  }

Dashboard 6:
  {
    "count":   N,
    "results": [ {...}, ... ]
  }
"""

import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .db import execute_query
from . import queries


class DashboardView(APIView):
    """Base class — runs one query, parses nested JSON, returns cards + charts."""

    query = None

    def get(self, request):
        try:
            rows = execute_query(self.query)
            if not rows:
                return Response(
                    {"error": "No data. Run the pipeline first."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            row = rows[0]

            # Parse JSON strings → Python dicts/lists
            parsed = {}
            for key, val in row.items():
                if isinstance(val, str):
                    try:
                        parsed[key] = json.loads(val)
                    except Exception:
                        parsed[key] = val
                else:
                    parsed[key] = val

            return Response(parsed)

        except Exception as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class Dashboard1View(DashboardView):
    """BD Executive Dashboard"""
    query = queries.DASHBOARD_1


class Dashboard2View(DashboardView):
    """Financials Focused Dashboard"""
    query = queries.DASHBOARD_2


class Dashboard3View(DashboardView):
    """Business Line Focused Dashboard"""
    query = queries.DASHBOARD_3


class Dashboard4View(DashboardView):
    """Account Manager Dashboard"""
    query = queries.DASHBOARD_4


class Dashboard5View(DashboardView):
    """Commercial Dashboard"""
    query = queries.DASHBOARD_5


class Dashboard6ListView(APIView):
    """
    All Opportunities — with optional filters.

    Query params:
        ?status=won|lost|in_progress
        ?business_line=<partial name>
        ?bd_owner=<partial name>
        ?stage=<partial name>
    """

    def get(self, request):
        params  = {}
        filters = []

        filter_map = {
            "status":        ("status = %(status)s",                   "status"),
            "business_line": ("business_line_en ILIKE %(business_line)s", "business_line"),
            "bd_owner":      ("bd_owner_en ILIKE %(bd_owner)s",           "bd_owner"),
            "stage":         ("stage ILIKE %(stage)s",                    "stage"),
        }

        for qp, (clause, key) in filter_map.items():
            val = request.query_params.get(qp)
            if val:
                filters.append(clause)
                params[key] = f"%{val}%" if "ILIKE" in clause else val

        where = "WHERE " + " AND ".join(filters) if filters else ""
        sql   = queries.DASHBOARD_6_ALL.format(where_clause=where)

        try:
            rows = execute_query(sql, params)
            return Response({"count": len(rows), "results": rows})
        except Exception as exc:
            return Response({"error": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Dashboard6DetailView(APIView):
    """Single opportunity by ID."""

    def get(self, request, opportunity_id: int):
        try:
            rows = execute_query(
                queries.DASHBOARD_6_SINGLE,
                {"opportunity_id": opportunity_id},
            )
            if not rows:
                return Response(
                    {"error": f"Opportunity {opportunity_id} not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            return Response(rows[0])
        except Exception as exc:
            return Response({"error": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)