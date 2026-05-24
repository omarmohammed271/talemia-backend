from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from . import views

urlpatterns = [
    path("api/schema/",          SpectacularAPIView.as_view(),                            name="schema"),
    path("api/docs/",            SpectacularSwaggerView.as_view(url_name="schema"),       name="swagger-ui"),
    path("api/redoc/",           SpectacularRedocView.as_view(url_name="schema"),         name="redoc"),

    path("api/dashboard/1/",           views.Dashboard1View.as_view(),       name="dashboard-executive"),
    path("api/dashboard/2/",           views.Dashboard2View.as_view(),       name="dashboard-financials"),
    path("api/dashboard/3/",           views.Dashboard3View.as_view(),       name="dashboard-business-line"),
    path("api/dashboard/4/",           views.Dashboard4View.as_view(),       name="dashboard-account-manager"),
    path("api/dashboard/5/",           views.Dashboard5View.as_view(),       name="dashboard-commercial"),
    path("api/dashboard/6/",           views.Dashboard6ListView.as_view(),   name="dashboard-opportunities"),
    path("api/dashboard/6/<int:opportunity_id>/", views.Dashboard6DetailView.as_view(), name="dashboard-opportunity-detail"),
]
