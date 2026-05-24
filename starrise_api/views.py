from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from .db import execute_query
from . import queries


class DashboardMixin:
    """Shared error handling for all dashboard views."""

    def fetch(self, sql: str, params: dict = None) -> Response:
        try:
            rows = execute_query(sql, params)
            if not rows:
                return Response(
                    {"error": "No data found. Run the pipeline first."},
                    status=status.HTTP_404_NOT_FOUND,
                )
            return Response(rows[0] if len(rows) == 1 else rows)
        except Exception as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class Dashboard1View(DashboardMixin, APIView):
    @extend_schema(
        summary="BD Executive Dashboard",
        description="Returns KPIs, pipeline stage distribution, and win/loss chart data for the BD executive view.",
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT, 500: OpenApiTypes.OBJECT},
        tags=["Dashboards"],
    )
    def get(self, request):
        return self.fetch(queries.DASHBOARD_1)


class Dashboard2View(DashboardMixin, APIView):
    @extend_schema(
        summary="Financials Dashboard",
        description="Returns revenue metrics, conversion funnel, and top opportunity data for the financials view.",
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT, 500: OpenApiTypes.OBJECT},
        tags=["Dashboards"],
    )
    def get(self, request):
        return self.fetch(queries.DASHBOARD_2)


class Dashboard3View(DashboardMixin, APIView):
    @extend_schema(
        summary="Business Line Dashboard",
        description="Returns win/loss breakdown by business line and overall status distribution.",
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT, 500: OpenApiTypes.OBJECT},
        tags=["Dashboards"],
    )
    def get(self, request):
        return self.fetch(queries.DASHBOARD_3)


class Dashboard4View(DashboardMixin, APIView):
    @extend_schema(
        summary="Account Manager Dashboard",
        description="Returns BD owner performance metrics, client rankings, and win-likelihood data.",
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT, 500: OpenApiTypes.OBJECT},
        tags=["Dashboards"],
    )
    def get(self, request):
        return self.fetch(queries.DASHBOARD_4)


class Dashboard5View(DashboardMixin, APIView):
    @extend_schema(
        summary="Commercial Dashboard",
        description="Returns pipeline stage breakdown, business line pipeline values, and top client data.",
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT, 500: OpenApiTypes.OBJECT},
        tags=["Dashboards"],
    )
    def get(self, request):
        return self.fetch(queries.DASHBOARD_5)


class Dashboard6ListView(DashboardMixin, APIView):
    @extend_schema(
        summary="Opportunities List",
        description="Returns all opportunities with optional filters.",
        parameters=[
            OpenApiParameter("status", OpenApiTypes.STR, OpenApiParameter.QUERY,
                             description="Filter by status: won, lost, or in_progress", required=False,
                             enum=["won", "lost", "in_progress"]),
            OpenApiParameter("business_line", OpenApiTypes.STR, OpenApiParameter.QUERY,
                             description="Filter by business line name (case-insensitive partial match)", required=False),
            OpenApiParameter("bd_owner", OpenApiTypes.STR, OpenApiParameter.QUERY,
                             description="Filter by BD owner name (case-insensitive partial match)", required=False),
        ],
        responses={200: OpenApiTypes.OBJECT, 500: OpenApiTypes.OBJECT},
        tags=["Opportunities"],
    )
    def get(self, request):
        sql    = queries.DASHBOARD_6_ALL
        params = {}

        filters = []
        if s := request.query_params.get("status"):
            filters.append("status = %(status)s")
            params["status"] = s
        if bl := request.query_params.get("business_line"):
            filters.append("business_line_en ILIKE %(business_line)s")
            params["business_line"] = f"%{bl}%"
        if bd := request.query_params.get("bd_owner"):
            filters.append("bd_owner_en ILIKE %(bd_owner)s")
            params["bd_owner"] = f"%{bd}%"

        if filters:
            sql = queries.DASHBOARD_6_ALL.replace(
                "ORDER BY",
                "WHERE " + " AND ".join(filters) + "\nORDER BY",
            )

        try:
            rows = execute_query(sql, params)
            return Response({
                "count":   len(rows),
                "results": rows,
            })
        except Exception as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class Dashboard6DetailView(DashboardMixin, APIView):
    @extend_schema(
        summary="Opportunity Detail",
        description="Returns full details for a single opportunity identified by its numeric ID.",
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT, 500: OpenApiTypes.OBJECT},
        tags=["Opportunities"],
    )
    def get(self, request, opportunity_id: int):
        return self.fetch(
            queries.DASHBOARD_6_SINGLE,
            params={"opportunity_id": opportunity_id},
        )
