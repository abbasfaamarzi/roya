from django.template.loader import render_to_string
from ..data import STORIES
from ..services.image_pool import random_image_urls
from .base import roya_html


def render():
    images = random_image_urls(len(STORIES))
    items = []
    for index, story in enumerate(STORIES):
        items.append({
            **story,
            "image": images[index] if index < len(images) else "",
            "avatar_html": roya_html("avatar", initials=story["initials"], alt=story["username"], size="large"),
        })
    return render_to_string("instagram_app/components/stories.html", {"stories": items})
