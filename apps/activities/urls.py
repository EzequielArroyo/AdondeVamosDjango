from django.urls import path

from .views import ActivityCreateView, ActivityDeleteView, ActivityListView, ActivityDetailView, ActivityJoinView, ActivityLeaveView, ActivityUpdateView, MyActivitiesView, MyJoinedActivitiesView

app_name = "activities"
urlpatterns = [
    path("", ActivityListView.as_view(), name="list"),
    path("create/", ActivityCreateView.as_view(), name="create"),
    path("<int:pk>/", ActivityDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", ActivityUpdateView.as_view(), name="edit"),
    path("<int:pk>/join/", ActivityJoinView.as_view(), name="join"),
    path("<int:pk>/leave/", ActivityLeaveView.as_view(), name="leave"),
    path("my/", MyActivitiesView.as_view(), name="my_activities"),
    path("joined/", MyJoinedActivitiesView.as_view(), name="my_joined_activities"),
    path("<int:pk>/delete/", ActivityDeleteView.as_view(), name="delete"),
]