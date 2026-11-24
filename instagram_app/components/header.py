from django.template.loader import render_to_string
from .base import roya_html


def render():
    return render_to_string("instagram_app/components/header.html", {
        "appbar_html": roya_html("appbar", title="Roya Social", subtitle=""),
        "search_html": roya_html("textfield", placeholder="جست‌وجو", field_name="search"),
        "create_button_html": roya_html("button", label="ایجاد پست", variant="filled"),
        "avatar_html": roya_html("avatar", initials="RY", alt="نمایه شما", size="medium"),
    })
