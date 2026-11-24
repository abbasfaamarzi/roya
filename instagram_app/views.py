from pathlib import Path
import mimetypes

from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import render

from .components import header, stories, feed, sidebar, bottom_nav, create_post
from .services.image_pool import image_count

APP_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = APP_ROOT.parent
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}
ALLOWED_STATIC_ROOT = (APP_ROOT / "static" / "instagram").resolve()


def home(request):
    from roya.lang import render_roya
    from .logic import build_context

    roya_html = render_roya(
        request,
        "instagram_app/pages/home.roya",
        build_context(),
    )
    return render(
        request,
        "instagram_app/pages/language.html",
        {"roya_html": roya_html},
    )


def health(request):
    return JsonResponse({
        "ok": True,
        "app": "instagram_app",
        "image_count": image_count(),
        "architecture": "widget modules + independent templates/css/js",
    })


def demo_image(request, filename):
    if Path(filename).name != filename:
        raise Http404("Invalid image name")
    path = (PROJECT_ROOT / "images" / filename).resolve()
    images_root = (PROJECT_ROOT / "images").resolve()
    if path.parent != images_root or path.suffix.lower() not in ALLOWED_IMAGE_EXTENSIONS or not path.is_file():
        raise Http404("Image not found")
    content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return FileResponse(path.open("rb"), content_type=content_type)


def static_asset(request, asset_path):
    path = (ALLOWED_STATIC_ROOT / asset_path).resolve()
    if ALLOWED_STATIC_ROOT not in path.parents or not path.is_file():
        raise Http404("Asset not found")
    content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return FileResponse(path.open("rb"), content_type=content_type)


def roya_static_asset(request, asset_path):
    candidates = [
        (PROJECT_ROOT / "static" / "roya" / asset_path).resolve(),
        (PROJECT_ROOT / "roya" / "static" / "roya" / asset_path).resolve(),
    ]
    for path in candidates:
        if path.is_file() and any(
            root in path.parents for root in (
                (PROJECT_ROOT / "static" / "roya").resolve(),
                (PROJECT_ROOT / "roya" / "static" / "roya").resolve(),
            )
        ):
            content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
            return FileResponse(path.open("rb"), content_type=content_type)
    raise Http404("Roya asset not found")
