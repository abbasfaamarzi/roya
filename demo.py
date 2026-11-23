"""Roya component showcase — renders every registered component with sample props."""
from __future__ import annotations

import html
import re
import traceback
from pathlib import Path

import django
from django.apps import apps
from django.conf import settings
from django.utils.safestring import mark_safe


# Keep the demo runnable as a standalone script while respecting an existing
# Django project configuration when this module is imported elsewhere.
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="roya-demo",
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
            "roya",
        ],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [],
                "APP_DIRS": True,
                "OPTIONS": {},
            }
        ],
        USE_TZ=True,
        DEFAULT_AUTO_FIELD="django.db.models.AutoField",
    )

if not apps.ready:
    django.setup()

from roya.core.component import Component
from roya.core.properties import Property
from roya.core.registry import registry


SAMPLE_PROPS = {
    "appbar": {"title": "برنامه من", "subtitle": "نمایش نمونه"},
    "avatar": {"initials": "AF", "alt": "تصویر کاربر", "size": "large"},
    "badge": {"value": "3", "color": "error", "size": "medium"},
    "bottom_sheet": {"title": "تنظیمات", "open": False},
    "box_layout": {"direction": "column", "gap": "md"},
    "button": {"label": "دکمه نمونه"},
    "card": {"variant": "elevated", "clickable": True},
    "checkbox": {"label": "پذیرفتن شرایط", "checked": True, "field_name": "terms"},
    "chip": {"label": "برچسب"},
    "date_picker": {
        "field_name": "birthday",
        "value": "1990-01-01",
        "label": "تاریخ تولد",
    },
    "dialog": {"title": "تأیید عملیات", "message": "آیا مطمئن هستید؟", "open": False},
    "fab": {"icon": "add", "label": "ایجاد", "extended": True, "fixed": False},
    "icon": {"icon": "star"},
    "icon_button": {"icon": "settings", "aria_label": "تنظیمات", "selected": True},
    "image": {"src": "https://picsum.photos/240", "alt": "تصویر نمونه"},
    "label": {"text": "متن نمونه"},
    "list": {
        "items": [
            {"label": "داشبورد", "description": "نمای کلی"},
            {"label": "پروفایل", "description": "اطلاعات کاربری"},
            {"label": "تنظیمات", "description": "مدیریت برنامه"},
        ],
        "selectable": True,
        "selected_items": ["داشبورد"],
        "divider": True,
    },
    "navigation_bar": {
        "items": [
            {"label": "خانه", "icon": "home"},
            {"label": "جستجو", "icon": "search"},
            {"label": "پروفایل", "icon": "person"},
        ],
        "active_item": 0,
    },
    "navigation_drawer": {
        "items": [
            {"label": "خانه", "icon": "home"},
            {"label": "پیام‌ها", "icon": "mail"},
            {"label": "تنظیمات", "icon": "settings"},
        ],
        "selected_item": "خانه",
        "open": False,
    },
    "navigation_rail": {
        "items": [
            {"label": "خانه", "icon": "home"},
            {"label": "جستجو", "icon": "search"},
            {"label": "تنظیمات", "icon": "settings"},
        ],
        "selected_item": "خانه",
        "label_mode": "all",
    },
    "progress": {"value": 68, "buffer": 82, "thickness": "6px"},
    "radio_group": {
        "options": ["روزانه", "هفتگی", "ماهانه"],
        "value": "هفتگی",
        "field_name": "period",
        "direction": "column",
    },
    "select": {
        "items": ["تهران", "اصفهان", "شیراز"],
        "value": "تهران",
        "label": "شهر",
        "field_name": "city",
    },
    "slider": {"value": 40, "min": 0, "max": 100, "step": 5, "show_value": True},
    "snackbar": {"message": "پیام نمونه برای کاربر"},
    "switch": {"label": "فعال‌سازی اعلان‌ها", "checked": True, "field_name": "notifications"},
    "tabs": {
        "items": [
            {"label": "مشخصات"},
            {"label": "فعالیت‌ها"},
            {"label": "تنظیمات"},
        ],
        "active_tab": 0,
    },
    "textfield": {
        "label": "نام",
        "placeholder": "نام خود را وارد کنید",
        "field_name": "name",
    },
    "time_picker": {"field_name": "time", "value": "12:30", "label": "زمان"},
    "tooltip": {"text": "برای ادامه کلیک کنید", "title": "راهنما", "trigger": "hover"},
    "virtual_list": {
        "items": [f"آیتم شماره {i}" for i in range(1, 9)],
        "item_height": 48,
        "overscan": 3,
        "aria_label": "فهرست نمونه",
    },
}

SAMPLE_CHILDREN = {
    "adaptive_container": ["<div>محتوای واکنش‌گرا</div>", "<div>محتوای دوم</div>"],
    "anchor_container": ["<div>محتوای متصل به لنگر</div>"],
    "box_layout": ["<div>فرزند اول</div>", "<div>فرزند دوم</div>"],
    "bottom_sheet": ["<p>این یک پنل نمونه با محتوای آزمایشی است.</p>"],
    "card": ["<p>محتوای داخل کارت</p>"],
    "dialog": ["<p>آیا از انجام این عملیات مطمئن هستید؟</p>"],
    "float_container": ["<div>محتوای شناور</div>"],
    "grid_container": ["<div>سلول ۱</div>", "<div>سلول ۲</div>", "<div>سلول ۳</div>"],
    "relative_container": ["<div>محتوای موقعیت‌دهی‌شده</div>"],
    "scroll_container": [
        "<div>ردیف اسکرول ۱</div>",
        "<div>ردیف اسکرول ۲</div>",
        "<div>ردیف اسکرول ۳</div>",
        "<div>ردیف اسکرول ۴</div>",
    ],
    "stack_container": ["<div>لایه ۱</div>", "<div>لایه ۲</div>", "<div>لایه ۳</div>"],
}
class HTMLFragment(Component):
    """Trusted static HTML fragment used only by the local component demo."""

    name = "demo_html_fragment"
    template_name = None

    def __init__(self, html: str):
        super().__init__()
        self.html = html

    def render(self) -> str:
        return mark_safe(self.html)


def _names():
    """Return registered component names using Roya's public registry API."""
    return registry.list()


def _declared_properties(cls):
    """Collect Property descriptors declared by a component and its bases."""
    properties = {}
    for base in cls.__mro__:
        for name, descriptor in vars(base).items():
            if isinstance(descriptor, Property):
                properties.setdefault(name, descriptor)
    return properties


def _filter_accepted(cls, props):
    """Pass only actual Property names; never infer aliases or trust **kwargs."""
    accepted = _declared_properties(cls)
    return {key: value for key, value in props.items() if key in accepted}


def _instantiate(cls, name):
    """Create a component with supported sample properties and real children."""
    props = dict(SAMPLE_PROPS.get(name, {}))
    filtered = _filter_accepted(cls, props)
    inst = cls(**filtered) if filtered else cls()

    for html in SAMPLE_CHILDREN.get(name, []):
        inst.add_child(HTMLFragment(html))

    return inst


def _run_hooks(inst):
    """Mount a component after its initial render, without calling hooks twice."""
    mount = getattr(inst, "mount", None)
    if callable(mount):
        mount()


def _get_html(inst):
    render = getattr(inst, "render", None)
    if callable(render):
        return str(render())
    return f"<pre>{type(inst).__name__}: no render method</pre>"


def _make_visible(html, name):
    # Overlays remain closed until the user activates their demo trigger.
    return html


def _item_label(item):
    if isinstance(item, dict):
        return str(item.get("label") or item.get("title") or item.get("text") or "")
    return str(item)


def _sample_preview(name, inst):
    """Return an explicitly demo-only visual when a component has no template."""
    p = lambda key, default="": html.escape(str(getattr(inst, key, default)))
    items = getattr(inst, "items", []) or []
    children = "".join(str(child.render()) for child in getattr(inst, "children", []))
    labels = [_item_label(item) for item in items]
    safe_labels = [html.escape(label) for label in labels]

    if name == "badge":
        return f'<span class="demo-badge">{p("value", "3")}</span>'
    if name == "checkbox":
        checked = " checked" if getattr(inst, "checked", False) else ""
        return f'<label class="demo-control"><input type="checkbox"{checked} disabled><span>{p("label")}</span></label>'
    if name == "fab":
        return f'<button class="demo-fab" type="button"><span>＋</span>{p("label", "ایجاد")}</button>'
    if name == "icon_button":
        return f'<button class="demo-icon-button" type="button" aria-label="{p("aria_label", "عملیات")}">⚙</button>'
    if name == "list":
        rows = "".join(f'<li>{label}</li>' for label in safe_labels)
        return f'<ul class="demo-list">{rows}</ul>'
    if name == "navigation_bar":
        buttons = "".join(f'<span class="demo-nav-item{" active" if i == getattr(inst, "active_item", 0) else ""}">●<small>{label}</small></span>' for i, label in enumerate(safe_labels))
        return f'<nav class="demo-nav-bar">{buttons}</nav>'
    if name == "navigation_drawer":
        rows = "".join(f'<li class="{"active" if label == getattr(inst, "selected_item", "") else ""}">◦ {label}</li>' for label in safe_labels)
        return f'<aside class="demo-drawer"><strong>منوی برنامه</strong><ul>{rows}</ul></aside>'
    if name == "navigation_rail":
        rows = "".join(f'<span class="demo-rail-item{" active" if label == getattr(inst, "selected_item", "") else ""}">◉<small>{label}</small></span>' for label in safe_labels)
        return f'<nav class="demo-rail">{rows}</nav>'
    if name == "progress":
        value = max(0, min(100, int(getattr(inst, "value", 0))))
        return f'<div class="demo-progress"><div class="demo-progress__track"><span style="width:{value}%"></span></div><small>{value}%</small></div>'
    if name == "radio_group":
        options = getattr(inst, "options", []) or []
        rows = "".join(f'<label class="demo-control"><input type="radio" disabled{" checked" if str(option) == str(getattr(inst, "value", "")) else ""}><span>{html.escape(str(option))}</span></label>' for option in options)
        return f'<div class="demo-radio">{rows}</div>'
    if name == "select":
        options = "".join(f'<option{" selected" if label == str(getattr(inst, "value", "")) else ""}>{label}</option>' for label in safe_labels)
        return f'<label class="demo-field"><span>{p("label")}</span><select disabled>{options}</select></label>'
    if name == "slider":
        value = int(getattr(inst, "value", 0))
        return f'<label class="demo-field"><span>مقدار: {value}</span><input type="range" min="{p("min", 0)}" max="{p("max", 100)}" value="{value}" disabled></label>'
    if name == "switch":
        checked = " checked" if getattr(inst, "checked", False) else ""
        return f'<label class="demo-control"><input type="checkbox" role="switch"{checked} disabled><span>{p("label")}</span></label>'
    if name == "tooltip":
        return f'<span class="demo-tooltip-target">{p("title", "راهنما")}<span class="demo-tooltip-bubble">{p("text")}</span></span>'
    if name in {"adaptive_container", "anchor_container", "float_container", "relative_container", "scroll_container", "stack_container"}:
        return f'<div class="demo-layout-preview"><small>پیش‌نمایش چیدمان</small>{children}</div>'
    return ""


def _render(name):
    try:
        cls = registry.get(name)
        inst = _instantiate(cls, name)

        html_output = _get_html(inst)
        _run_hooks(inst)
        html_output = _make_visible(html_output, name)

        # Component._fallback_render() emits this exact empty wrapper when a
        # component has no Django template. Show a clearly marked demo sample
        # instead of misreporting the empty wrapper as a rendered component.
        is_fallback = bool(re.search(
            r'<div id="[^"]+" class="roya-component" data-roya-component="[^"]+"></div>',
            html_output,
        ))
        if is_fallback:
            preview = _sample_preview(name, inst)
            if preview:
                return preview, "sample", "پیش‌نمایش نمونه؛ قالب اصلی ندارد"

        # Overlay components are opened from explicit controls in the demo.
        if name in {"dialog", "bottom_sheet", "navigation_drawer"}:
            labels = {
                "dialog": "نمایش Dialog",
                "bottom_sheet": "نمایش Bottom Sheet",
                "navigation_drawer": "نمایش منو",
            }
            html_output = (
                f'<button type="button" class="roya-demo-open" '
                f'data-roya-open="{html.escape(inst.id, quote=True)}">{labels[name]}</button>'
                + html_output
            )

        stripped = re.sub(r"<[^>]+>", "", html_output).strip()
        has_component_markup = bool(re.search(r'data-roya-component="[^"]+"', html_output))
        has_structural_content = bool(re.search(
            r"<(input|img|button|canvas|svg|textarea|select|hr|progress|meter|ul|ol|table|a|nav|section)\b",
            html_output,
        ))
        if stripped or has_structural_content or has_component_markup:
            return html_output, "ok", ""
        preview = _sample_preview(name, inst)
        if preview:
            return preview, "sample", "پیش‌نمایش نمونه"
        return html_output, "empty", "بدون محتوای قابل نمایش"
    except Exception as exc:
        return (
            f"<pre>ERROR in {name}: {type(exc).__name__}: {exc}\n\n"
            f"{traceback.format_exc()}</pre>",
            "error",
            type(exc).__name__,
        )


def main():
    DEMO_CSS = r'''
/* Material 3 demo shell */
:root { color-scheme: light; }
body {
  margin: 0; min-height: 100vh; padding: clamp(16px, 3vw, 36px);
  background: #f6f2f8; color: #1d1b20;
  font-family: "Vazirmatn", "Noto Sans Arabic", "Segoe UI", system-ui, sans-serif;
  line-height: 1.65;
}
body[data-roya-theme="dark"] { background: #141218; color: #e6e1e9; }
.demo-header {
  display:flex; align-items:center; justify-content:space-between; gap:20px;
  max-width:1440px; margin:0 auto 18px; padding:24px 28px;
  border-radius:28px; color:#fff; background:linear-gradient(120deg,#4f378b,#6750a4 58%,#8066bd);
  box-shadow:0 8px 28px rgb(44 30 70 / .18);
}
.demo-header h1 { margin:0; color:inherit; font-size:clamp(1.35rem,3vw,2rem); font-weight:750; }
.demo-header p { margin:5px 0 0; color:rgb(255 255 255 / .82); font-size:.9rem; }
.demo-header button {
  flex:0 0 auto; min-width:48px; min-height:48px; border:1px solid rgb(255 255 255 / .45);
  border-radius:50%; background:rgb(255 255 255 / .12); color:white; font-size:1.15rem; cursor:pointer;
}
.demo-toolbar {
  display:flex; align-items:center; gap:12px; max-width:1440px; margin:0 auto 16px;
}
.demo-search {
  flex:1; min-height:50px; padding:0 18px; border:1px solid #cac4d0; border-radius:16px;
  background:#fffbfe; color:#1d1b20; font:inherit; outline:none;
}
.demo-search:focus { border-color:#6750a4; box-shadow:0 0 0 3px rgb(103 80 164 / .14); }
#demo-count { color:#625e68; font-size:.82rem; white-space:nowrap; }
.summary {
  max-width:1440px; margin:0 auto 18px; color:#625e68; font-size:.86rem;
}
.grid {
  display:grid; gap:16px; max-width:1440px; margin:0 auto;
  grid-template-columns:repeat(auto-fill,minmax(min(100%,310px),1fr));
}
.card {
  min-width:0; padding:18px; border:1px solid #e5dfea; border-radius:20px;
  background:#fffbfe; box-shadow:0 1px 3px rgb(30 20 45 / .06);
  transition:box-shadow .18s ease, transform .18s ease, border-color .18s ease;
}
.card:hover { border-color:#d4c8e3; box-shadow:0 6px 20px rgb(30 20 45 / .09); transform:translateY(-1px); }
.card h2 {
  display:flex; align-items:center; flex-wrap:wrap; gap:8px; margin:0 0 16px;
  padding:0 0 12px; border-bottom:1px solid #eee8f2; color:#49454f;
  font-size:.9rem; font-weight:700;
}
.badge { border-radius:999px; padding:3px 9px; font-size:.68rem; }
.badge--ok { background:#d7f3df; color:#14532d; }
.badge--sample { background:#eaddff; color:#381e72; }
.badge--warn { background:#fff0c2; color:#694b00; }
.badge--error { background:#f9dedc; color:#8c1d18; }
.card :is(button, input, select) { font:inherit; }
.card .roya-demo-open {
  min-height:44px; padding:9px 16px; border:0; border-radius:999px;
  background:#eaddff; color:#21005d; font-weight:650; cursor:pointer;
}
.card .roya-demo-open:hover { box-shadow:0 2px 7px rgb(0 0 0 / .12); }
body[data-roya-theme="dark"] .card {
  background:#211f26; border-color:#49454f; color:#e6e1e9;
}
body[data-roya-theme="dark"] .card h2 { color:#cac4d0; border-color:#49454f; }
body[data-roya-theme="dark"] .summary, body[data-roya-theme="dark"] #demo-count { color:#cac4d0; }
body[data-roya-theme="dark"] .demo-search { background:#211f26; color:#e6e1e9; border-color:#625d69; }
@media (max-width:640px) {
  body { padding:12px; }
  .demo-header { padding:18px; border-radius:22px; }
  .demo-header p { font-size:.78rem; }
  .demo-toolbar { align-items:stretch; flex-direction:column; }
  #demo-count { text-align:start; }
  .grid { grid-template-columns:1fr; gap:12px; }
}
'''
    DEMO_JS = r'''
// Search/filter component cards and toggle the Material 3 demo theme.
(function () {
  var search = document.getElementById("demo-search");
  var count = document.getElementById("demo-count");
  var cards = Array.prototype.slice.call(document.querySelectorAll(".grid > .card"));
  var toggle = document.getElementById("demo-theme-toggle");
  function filterCards() {
    var query = (search.value || "").trim().toLocaleLowerCase();
    var visible = 0;
    cards.forEach(function (card) {
      var match = !query || card.textContent.toLocaleLowerCase().indexOf(query) !== -1;
      card.hidden = !match;
      if (match) visible += 1;
    });
    count.textContent = visible + " از " + cards.length + " کامپوننت";
  }
  search.addEventListener("input", filterCards);
  toggle.addEventListener("click", function () {
    var dark = document.body.getAttribute("data-roya-theme") !== "dark";
    if (dark) document.body.setAttribute("data-roya-theme", "dark");
    else document.body.removeAttribute("data-roya-theme");
    toggle.setAttribute("aria-pressed", dark ? "true" : "false");
  });
  filterCards();
}());
'''
    names = _names()
    cards, ok, samples, empty, failed = [], [], [], [], []

    for name in names:
        html, status, info = _render(name)
        if status == "ok":
            ok.append(name)
            badge = '<span class="badge badge--ok">OK</span>'
        elif status == "sample":
            samples.append(name)
            badge = f'<span class="badge badge--sample">نمونه نمایشی</span>'
        elif status == "empty":
            empty.append(name)
            badge = f'<span class="badge badge--warn">{info}</span>'
        else:
            failed.append(name)
            badge = '<span class="badge badge--error">ERROR</span>'

        cards.append(
            f'<section class="card"><h2>{name} {badge}</h2>{html}</section>'
        )

    total = len(names)
    project_root = Path(__file__).resolve().parent
    package_root = project_root / "roya"
    if not (package_root / "static/roya/css/roya.css").is_file():
        package_root = project_root
    css_file = package_root / "static/roya/css/roya.css"
    js_file = package_root / "static/roya/js/roya.js"
    package_css = css_file.read_text(encoding="utf-8") if css_file.is_file() else ""
    package_js = js_file.read_text(encoding="utf-8") if js_file.is_file() else ""

    page = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Roya Demo</title>
<style>
  :root {{ --p:#6750A4; --bg:#FFFBFE; --fg:#1C1B1F; }}
  body {{ font-family: Tahoma, Arial, sans-serif; background:#F5F5F5;
         color:var(--fg); margin:0; padding:24px; }}
  h1 {{ color:var(--p); margin:0 0 8px; }}
  .summary {{ margin:0 0 24px; font-size:13px; color:#555; }}
  .grid {{ display:grid; gap:16px;
          grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); }}
  .card {{ background:var(--bg); border-radius:12px; padding:16px;
          box-shadow:0 2px 8px rgba(0,0,0,.08); min-width:0; }}
  .card h2 {{ margin:0 0 12px; font-size:14px; color:var(--p);
             border-bottom:1px solid #EEE; padding-bottom:8px; }}
  pre {{ background:#F0F0F0; padding:8px; border-radius:6px;
        overflow-x:auto; font-size:12px; direction:ltr; }}
  .badge {{ font-size:11px; padding:2px 6px; border-radius:4px;
           margin-inline-start:8px; font-weight:normal; }}
  .badge--ok {{ background:#E6F4EA; color:#137333; }}
  .badge--warn {{ background:#FEF7E0; color:#B06000; }}
  .badge--sample {{ background:#E8EAF6; color:#3949AB; }}
  .badge--error {{ background:#FCE8E6; color:#C5221F; }}

  .demo-badge {{ display:inline-flex; min-width:24px; height:24px; align-items:center;
      justify-content:center; border-radius:999px; padding:0 7px; background:#B3261E;
      color:white; font-weight:bold; }}
  .demo-control {{ display:flex; align-items:center; gap:10px; padding:8px 4px; }}
  .demo-control input {{ accent-color:#6750A4; }}
  .demo-fab {{ border:0; border-radius:24px; padding:12px 18px; background:#6750A4;
      color:white; box-shadow:0 3px 8px #0002; }}
  .demo-icon-button {{ width:44px; height:44px; border:0; border-radius:50%;
      background:#EADDFF; color:#21005D; font-size:20px; }}
  .demo-list, .demo-drawer ul {{ margin:0; padding:0; list-style:none; }}
  .demo-list li, .demo-drawer li {{ padding:10px 12px; border-bottom:1px solid #eee; }}
  .demo-nav-bar, .demo-rail {{ display:flex; gap:12px; justify-content:space-around;
      padding:12px; border-radius:14px; background:#F0ECF8; }}
  .demo-nav-item, .demo-rail-item {{ display:flex; flex-direction:column; align-items:center; gap:4px; }}
  .demo-nav-item.active, .demo-rail-item.active {{ color:#6750A4; font-weight:bold; }}
  .demo-drawer {{ max-width:260px; padding:14px; border-radius:12px; background:#F7F2FA; }}
  .demo-drawer strong {{ display:block; margin-bottom:8px; }}
  .demo-progress__track {{ height:8px; background:#E7E0EC; border-radius:20px; overflow:hidden; flex:1; }}
  .demo-progress__track span {{ display:block; height:100%; background:#6750A4; border-radius:20px; }}
  .demo-progress {{ display:flex; align-items:center; gap:12px; }}
  .demo-radio {{ display:grid; gap:4px; }}
  .demo-field {{ display:grid; gap:7px; max-width:280px; }}
  .demo-field select, .demo-field input {{ width:100%; padding:9px; border:1px solid #aaa;
      border-radius:8px; background:white; box-sizing:border-box; }}
  .demo-tooltip-target {{ display:inline-block; position:relative; padding:12px 16px;
      border-radius:8px; background:#F0ECF8; }}
  .demo-tooltip-bubble {{ display:block; margin-top:8px; padding:8px 10px;
      background:#333; color:white; border-radius:6px; }}
  .demo-layout-preview {{ display:grid; gap:10px; padding:12px; min-height:55px;
      border:1px dashed #9A88C7; border-radius:10px; }}
  .demo-layout-preview > div {{ padding:10px; background:#EEE8F8; border-radius:7px; }}
  .demo-virtual-preview {{ margin-top:10px; border:1px solid #ddd; border-radius:8px; overflow:hidden; }}
  .demo-virtual-row {{ padding:9px 12px; border-bottom:1px solid #eee; }}
  .card .roya-demo-open {{ display:inline-flex; align-items:center; justify-content:center; }}
  {package_css}
  {DEMO_CSS}
</style>
</head>
<body>
<header class="demo-header">
  <div>
    <h1>Roya · کتابخانه کامپوننت‌ها ({total})</h1>
    <p>نمایش زنده اجزای رابط کاربری با زبان طراحی Material 3</p>
  </div>
  <button type="button" id="demo-theme-toggle" aria-label="تغییر حالت روشن و تاریک" title="تغییر پوسته">◐</button>
</header>
<div class="demo-toolbar">
  <input id="demo-search" class="demo-search" type="search" placeholder="جست‌وجوی کامپوننت..." aria-label="جست‌وجوی کامپوننت">
  <span id="demo-count">در حال نمایش همه کامپوننت‌ها</span>
</div>
<p class="summary">
  <strong>{len(ok)}</strong> رندر واقعی ·
  <strong>{len(samples)}</strong> پیش‌نمایش نمونه ·
  <strong>{len(empty)}</strong> خالی ·
  <strong>{len(failed)}</strong> خطا
</p>
<div class="grid">
{chr(10).join(cards)}
</div>
<script>
{package_js}
  {DEMO_JS}
</script>
</body>
</html>
"""

    output = Path(__file__).resolve().parent / "demo.html"
    output.write_text(page, encoding="utf-8")
    print(f"Wrote {output}")
    if not package_css or not package_js:
        print("WARNING: Roya static CSS/JS was not found; check package_root paths.")
    print(
        f"  {total} components: {len(ok)} rendered, {len(samples)} sample previews, "
        f"{len(empty)} empty, {len(failed)} error"
    )
    if samples:
        print(f"  sample previews: {', '.join(samples)}")
    if empty:
        print(f"  empty:  {', '.join(empty)}")
    if failed:
        print(f"  failed: {', '.join(failed)}")


if __name__ == "__main__":
    main()
