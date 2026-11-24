from django.template.loader import render_to_string
from .base import roya_html


def render():
    return render_to_string("instagram_app/components/create_post.html", {
        "close_button_html": roya_html("icon_button", icon="close", aria_label="بستن"),
        "submit_button_html": roya_html("button", label="انتشار", variant="filled"),
    })
