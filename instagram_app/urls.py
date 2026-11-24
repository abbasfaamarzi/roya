from django.urls import include, path
from . import views

app_name = "instagram_app"

urlpatterns = [
    path("roya/actions/", include("roya.actions.urls")),
    path("", views.home, name="home"),
    path("health/", views.health, name="health"),
    path("demo-images/<str:filename>", views.demo_image, name="demo_image"),
    path("static/roya/<path:asset_path>", views.roya_static_asset, name="roya_static_asset"),
    path("static/instagram/<path:asset_path>", views.static_asset, name="static_asset"),
]
