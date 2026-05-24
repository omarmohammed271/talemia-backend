from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/1/",           views.Dashboard1View.as_view(),       name="dashboard-executive"),
    path("dashboard/2/",           views.Dashboard2View.as_view(),       name="dashboard-financials"),
    path("dashboard/3/",           views.Dashboard3View.as_view(),       name="dashboard-business-line"),
    path("dashboard/4/",           views.Dashboard4View.as_view(),       name="dashboard-account-manager"),
    path("dashboard/5/",           views.Dashboard5View.as_view(),       name="dashboard-commercial"),
    path("dashboard/6/",           views.Dashboard6ListView.as_view(),   name="dashboard-opportunities"),
    path("dashboard/6/<int:opportunity_id>/", views.Dashboard6DetailView.as_view(), name="dashboard-opportunity-detail"),
]
