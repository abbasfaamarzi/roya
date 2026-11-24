"""Python actions and demo data for the Roya Instagram-style application.

This is an in-memory demonstration. Replace these stores with Django models,
permissions and transactions before using it as a multi-user production app.
"""
from uuid import uuid4

from roya.actions import action
from .data import POSTS, STORIES, SUGGESTIONS
from .services.image_pool import random_image_urls

_LIKED_POST_IDS = set()
_SAVED_POST_IDS = set()
_FOLLOWING_USERNAMES = set()
_POST_LIKES = {}
_USER_POSTS = []
_POST_CACHE = {}
_IMAGE_CACHE = {}


def _image_for(key, fallback=""):
    return _IMAGE_CACHE.get(str(key), fallback)


def build_context():
    """Build all view data while preserving demo interaction state."""
    source_posts = list(_USER_POSTS) + [dict(item) for item in POSTS]
    image_candidates = random_image_urls(len(source_posts) + len(STORIES) + len(SUGGESTIONS) + 1)
    image_index = 0

    def image_for_key(key):
        nonlocal image_index
        key = str(key)
        if key not in _IMAGE_CACHE:
            candidate = image_candidates[image_index] if image_index < len(image_candidates) else ""
            _IMAGE_CACHE[key] = candidate
            image_index += 1
        return _IMAGE_CACHE[key]

    posts = []
    _POST_CACHE.clear()
    for index, raw_post in enumerate(source_posts):
        item = dict(raw_post)
        post_id = str(item.get("id") or f"post-{index + 1}")
        username = str(item.get("username") or "roya.user")
        initial_likes = max(int(item.get("likes", 0) or 0), 0)
        item["id"] = post_id
        item["username"] = username
        item["initials"] = str(item.get("initials") or username[:1].upper())
        item["likes"] = _POST_LIKES.setdefault(post_id, initial_likes)
        item["liked"] = post_id in _LIKED_POST_IDS
        item["saved"] = post_id in _SAVED_POST_IDS
        item["comments_count"] = int(item.get("comments_count", 12 + (index % 7)))
        if item.get("image"):
            item["image"] = str(item["image"])
        elif post_id.startswith("user-"):
            item["image"] = ""
        else:
            item["image"] = image_for_key(f"post:{post_id}")
        posts.append(item)
        _POST_CACHE[post_id] = {
            "id": post_id,
            "username": username,
            "location": str(item.get("location", "")),
            "caption": str(item.get("caption", "")),
            "image": item["image"],
            "likes": item["likes"],
            "comments_count": item["comments_count"],
            "liked": item["liked"],
            "saved": item["saved"],
        }

    stories = []
    for story in STORIES:
        item = dict(story)
        username = str(item.get("username", ""))
        item["image"] = item.get("image") or image_for_key(f"story:{username}")
        stories.append(item)

    suggestions = []
    for user in SUGGESTIONS:
        item = dict(user)
        username = str(item.get("username", ""))
        item["image"] = item.get("image") or image_for_key(f"suggestion:{username}")
        item["following"] = username in _FOLLOWING_USERNAMES
        item["reason"] = item.get("reason") or "پیشنهاد برای شما"
        suggestions.append(item)

    profile = {
        "username": "roya.you",
        "full_name": "حساب نمایشی رویا",
        "initials": "R",
        "image": image_for_key("profile:roya.you"),
    }
    return {"posts": posts, "stories": stories, "suggestions": suggestions, "profile": profile}


@action("instagram.open_story")
def open_story(request, username, image=""):
    return {"modal": "story", "username": str(username), "image": str(image)}


@action("instagram.open_post")
def open_post(request, post_id):
    post = _POST_CACHE.get(str(post_id))
    if not post:
        return {"notice": "این پست دیگر در دسترس نیست.", "notice_type": "error"}
    return {"modal": "post", "post": dict(post)}


@action("instagram.toggle_like")
def toggle_like(request, post_id, likes=0):
    post_id = str(post_id)
    try:
        initial_likes = max(int(likes), 0)
    except (TypeError, ValueError):
        initial_likes = 0
    _POST_LIKES.setdefault(post_id, initial_likes)
    if post_id in _LIKED_POST_IDS:
        _LIKED_POST_IDS.remove(post_id)
        _POST_LIKES[post_id] = max(_POST_LIKES[post_id] - 1, 0)
        liked = False
    else:
        _LIKED_POST_IDS.add(post_id)
        _POST_LIKES[post_id] += 1
        liked = True
    if post_id in _POST_CACHE:
        _POST_CACHE[post_id]["likes"] = _POST_LIKES[post_id]
        _POST_CACHE[post_id]["liked"] = liked
    return {"liked": liked, "likes": _POST_LIKES[post_id], "post_id": post_id}


@action("instagram.toggle_save")
def toggle_save(request, post_id):
    post_id = str(post_id)
    if post_id in _SAVED_POST_IDS:
        _SAVED_POST_IDS.remove(post_id)
        saved = False
    else:
        _SAVED_POST_IDS.add(post_id)
        saved = True
    if post_id in _POST_CACHE:
        _POST_CACHE[post_id]["saved"] = saved
    return {"saved": saved, "post_id": post_id}


@action("instagram.toggle_follow")
def toggle_follow(request, username):
    username = str(username)
    if username in _FOLLOWING_USERNAMES:
        _FOLLOWING_USERNAMES.remove(username)
        following = False
    else:
        _FOLLOWING_USERNAMES.add(username)
        following = True
    return {"following": following, "username": username}


@action("instagram.search_posts")
def search_posts(request, event):
    return {"filter_text": str(event.get("value", "")).strip()}


@action("instagram.navigate")
def navigate(request, target):
    return {"navigate_to": str(target)}


@action("instagram.open_create")
def open_create(request):
    return {"open_create": True}


@action("instagram.close_create")
def close_create(request):
    return {"close_create": True}


@action("instagram.publish_post")
def publish_post(request, event):
    caption = str(event.get("value", "")).strip()
    if not caption:
        return {"notice": "ابتدا متن پست را بنویسید.", "notice_type": "error"}
    if len(caption) > 500:
        return {"notice": "متن پست نباید بیشتر از ۵۰۰ نویسه باشد.", "notice_type": "error"}

    post_id = f"user-{uuid4().hex[:12]}"
    post = {
        "id": post_id,
        "username": "roya.you",
        "location": "",
        "caption": caption,
        "likes": 0,
        "comments_count": 0,
        "image": "",
        "initials": "R",
    }
    _USER_POSTS.insert(0, post)
    return {"published": True, "reload": True, "notice": "پست شما اضافه شد."}


@action("instagram.share_post")
def share_post(request, post_id):
    post = _POST_CACHE.get(str(post_id), {})
    return {
        "share_text": f"{post.get('username', '')}: {post.get('caption', '')}",
    }