from django.template.loader import render_to_string
from ..data import SUGGESTIONS
from .base import roya_html


def render():
    suggestions = []
    for user in SUGGESTIONS:
        suggestions.append({
            **user,
            "avatar_html": roya_html("avatar", initials=user["initials"], alt=user["username"], size="small"),
        })
    return render_to_string("instagram_app/components/sidebar.html", {
        "suggestions": suggestions,
        "profile_avatar_html": roya_html("avatar", initials="RY", alt="نمایه شما", size="large"),
    })
