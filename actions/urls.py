"""URL routes for Roya action dispatch."""
from django.urls import path
from .views import dispatch_action

urlpatterns = [
    path("", dispatch_action, name="roya-action-dispatch"),
]
