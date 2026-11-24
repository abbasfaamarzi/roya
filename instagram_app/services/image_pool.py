"""Random image discovery from the project's root images/ directory."""
from pathlib import Path
from random import sample

PROJECT_ROOT = Path(__file__).resolve().parents[2]
IMAGE_DIR = PROJECT_ROOT / "images"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"}


def image_files():
    if not IMAGE_DIR.is_dir():
        return []
    return sorted(
        path for path in IMAGE_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def image_count():
    return len(image_files())


def random_image_urls(count):
    candidates = image_files()
    if not candidates or count <= 0:
        return []
    selected = sample(candidates, min(count, len(candidates)))
    return [f"/demo-images/{path.name}" for path in selected]
