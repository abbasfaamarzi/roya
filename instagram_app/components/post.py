from django.template.loader import render_to_string
from .base import roya_html


def render(post, index):
    return render_to_string("instagram_app/components/post.html", {
        "post": post,
        "index": index,
        "avatar_html": roya_html("avatar", initials=post["username"][:1].upper(), alt=post["username"], size="medium"),
        "image_html": roya_html("image", src=post.get("image", ""), alt=post["caption"]) if post.get("image") else "",
        "like_button_html": roya_html("icon_button", icon="favorite", aria_label="پسندیدن"),
    })
