"""
URL configuration for eonje_manna_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from core.views.event_time_select import EventDateSelectionView,EventDateSelectionDetailView,EventDateSelectionAvailableUsersCountView, EventDateSelectionDetailView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from core.views.event import EventDetailView, EventListView, MyEventListView
from core.views.login import LoginView

from core.views.group import MeetingGroupListView, MeetingGroupDetailView, GroupMemberListView
from core.views.profile import MemberListView

from core.views.membership import MembershipDetailView
from core.views.signup import SignupView
from core.views.meeting_group import (
    group_list,
    group_detail,
    group_create,
    group_delete,
    group_edit,
)
from core.views.event_location_selection import EventLocationSelectionView
from core.views.marker import MarkerSaveView, MarkerListView
from core.views.vote import VoteListView

schema_view = get_schema_view(
    openapi.Info(
        title="Your Server Name or Swagger Docs name",
        default_version="Your API version(Custom)",
        description="Your Swagger Docs descriptions",
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(name="test", email="test@test.com"),
        # license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=([permissions.AllowAny]),
)

urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("admin/", admin.site.urls),
    path("login/", LoginView.as_view()),
    path("signup/", SignupView.as_view()),

    path("api/markers/save", MarkerSaveView.as_view(), name="marker-save"),
    path("api/markers/<event_id>", MarkerListView.as_view(), name="marker-list"),

    path("profile/", MemberListView.as_view()),
    path("events/", MyEventListView.as_view()),

    path("groups/", MeetingGroupListView.as_view()),
    path('event-date-selections/', EventDateSelectionView.as_view()),
    path('event-date-selections/<int:pk>', EventDateSelectionDetailView.as_view()),
    # path('event-date-selections/all', EventDateSelectionAllView.as_view()),
    # path('event-date-selections/result', EventDateSelectionResultView.as_view()),

    path('event-date-selections/detail', EventDateSelectionDetailView.as_view()),
    path('event-date-selections/AvailableUsersCount', EventDateSelectionAvailableUsersCountView.as_view()),
    path("groups/<int:pk>", MeetingGroupDetailView.as_view()),

    path("groups/<int:pk>/membership/", MembershipDetailView.as_view()),
    path("groups/<int:group_id>/members", GroupMemberListView.as_view()),
    path("groups/<int:group_id>/events", EventListView.as_view()),
    path("groups/<int:group_id>/events/<int:pk>", EventDetailView.as_view()),
    path(
        "api/events/<int:event_id>/votes/",
        VoteListView.as_view(),
        name="event-vote-list",
    ),

]

