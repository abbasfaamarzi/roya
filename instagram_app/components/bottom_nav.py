from django.template.loader import render_to_string
from .base import roya_html


def render():
    return render_to_string("instagram_app/components/bottom_nav.html", {
        "navigation_html": roya_html("navigation_bar", items=[
            {"label": "خانه", "icon": "home"},
            {"label": "جست‌وجو", "icon": "search"},
            {"label": "ایجاد", "icon": "add"},
            {"label": "فعالیت", "icon": "favorite"},
            {"label": "نمایه", "icon": "person"},
        ], active_item=0),
    })
