from django.template.loader import render_to_string
from ..data import POSTS
from ..services.image_pool import random_image_urls
from .post import render as render_post


def render():
    image_urls = random_image_urls(len(POSTS))
    cards = []
    for index, post in enumerate(POSTS):
        item = dict(post)
        item["image"] = image_urls[index] if index < len(image_urls) else ""
        cards.append(render_post(item, index))
    return render_to_string("instagram_app/components/feed.html", {"posts_html": cards})
