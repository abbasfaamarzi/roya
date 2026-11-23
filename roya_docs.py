"""
Roya Component Documentation
============================

KivyMD-style API reference for the Roya Material Design 3 components.
This module is intentionally **standalone**: it does not import Django,
the component classes, or the template engine. All metadata is encoded
as plain Python dictionaries, so the file is importable anywhere —
inside a Django project, in a test runner, or from a plain Python REPL.

It mirrors the way KivyMD documents each widget in its docstrings:

    * short summary
    * properties table (name, type, default, description)
    * events table (name, wire, description)
    * usage example (Python + JavaScript)
    * accessibility notes
    * implementation notes

CLI usage
---------
::

    python roya_docs.py                    # print full Markdown to stdout
    python roya_docs.py --list             # list all documented components
    python roya_docs.py bottom_sheet       # print one component
    python roya_docs.py --format=console   # plain-text console render

Programmatic usage
------------------
::

    from roya_docs import COMPONENT_DOCS, render_docs
    print(render_docs("badge"))
    for name, doc in COMPONENT_DOCS.items():
        print(name, doc["summary"])

Version
-------
0.2.2 — aligned with the 2026-11 component parity pass
(sync of BottomSheet, AppBar, Badge, AnchorContainer with the
``components.json`` reference pack).
"""

from __future__ import annotations

import argparse
import sys
from typing import Any, Dict, Iterable, List, Optional

# --- Windows console safety (UTF-8 stdout) -------------------------------
# On Windows the console defaults to a legacy code page (cp1251 on
# Russian locales, cp1256 on Persian locales, cp1252 elsewhere), which
# turns Persian titles and em-dashes into mojibake when the script
# prints Markdown to the terminal. Force the console code page to UTF-8
# (``chcp 65001``) and reconfigure Python's stdout wrapper so Unicode
# round-trips end-to-end. The try/except guards non-Windows and
# restricted environments.
try:
    import os as _os
    if sys.platform == "win32":
        _os.system("chcp 65001 >nul")
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


__version__ = "0.2.2"


# =============================================================================
# COMPONENT_DOCS — detailed entries for the v25 synchronized components
# =============================================================================

COMPONENT_DOCS: Dict[str, Dict[str, Any]] = {
    # -----------------------------------------------------------------
    # AnchorContainer
    # -----------------------------------------------------------------
    "anchor_container": {
        "category": "Layout",
        "title": "AnchorContainer",
        "class_path": "roya.components.layout.anchor.AnchorContainer",
        "template": "roya/components/layout/anchor.html",
        "css_classes": ["roya-anchor"],
        "summary": (
            "Flex container that aligns its children to a horizontal edge or "
            "center and a vertical edge or center."
        ),
        "description": (
            "AnchorContainer is the Roya equivalent of KivyMD's MDAnchorLayout. "
            "It uses CSS flexbox under the hood: ``justify-content`` is driven "
            "by ``horizontal_anchor`` and ``align-items`` by ``vertical_anchor``. "
            "Optional ``offset_x`` / ``offset_y`` are emitted as CSS ``padding``, "
            "so children are pushed away from the anchored edge by a measurable "
            "amount. RTL safe: ``left`` maps to ``flex-start`` and ``right`` to "
            "``flex-end`` following the container's writing direction."
        ),
        "properties": [
            {
                "name": "horizontal_anchor",
                "type": "str",
                "default": "'center'",
                "description": "One of ``'left'``, ``'center'``, ``'right'``.",
            },
            {
                "name": "vertical_anchor",
                "type": "str",
                "default": "'center'",
                "description": "One of ``'top'``, ``'center'``, ``'bottom'``.",
            },
            {
                "name": "offset_x",
                "type": "str",
                "default": "'0'",
                "description": "CSS padding value applied left and right.",
            },
            {
                "name": "offset_y",
                "type": "str",
                "default": "'0'",
                "description": "CSS padding value applied top and bottom.",
            },
        ],
        "events": [],
        "python_methods": [
            {
                "name": "get_context",
                "description": (
                    "Extends the base context with ``ha``, ``va``, ``ox``, "
                    "``oy`` short aliases used by the template."
                ),
            },
        ],
        "usage_python": (
            "from roya.components.layout.anchor import AnchorContainer\n"
            "\n"
            "box = AnchorContainer(\n"
            "    horizontal_anchor=\"right\",\n"
            "    vertical_anchor=\"bottom\",\n"
            "    offset_x=\"24px\",\n"
            "    offset_y=\"16px\",\n"
            ")\n"
            "box.add_child(my_widget)\n"
            "html = box.render()"
        ),
        "accessibility": [
            "No interactive focus management — the container itself is inert.",
            "Children keep their own focus and keyboard behavior.",
        ],
        "notes": [
            "Children render in document order; no automatic wrapping.",
            "Use ``offset_x``/``offset_y`` with explicit CSS units (e.g. ``24px``).",
        ],
    },

    # -----------------------------------------------------------------
    # AppBar
    # -----------------------------------------------------------------
    "appbar": {
        "category": "Navigation",
        "title": "AppBar",
        "class_path": "roya.components.navigation.appbar.AppBar",
        "template": "roya/components/navigation/appbar.html",
        "css_classes": [
            "roya-appbar",
            "roya-appbar__leading",
            "roya-appbar__title",
            "roya-appbar__actions",
        ],
        "summary": (
            "Top application bar with title, optional subtitle, a leading "
            "navigation icon and an arbitrary list of right-side action icons."
        ),
        "description": (
            "AppBar is the Roya equivalent of KivyMD's MDTopAppBar. It renders "
            "a ``<header>`` with three logical regions: a ``leading`` block "
            "(where ``left_icon`` and any children land), a flexible ``title`` "
            "block, and a right-aligned ``actions`` block populated from "
            "``right_icons``. Background and text colors can be overridden per "
            "instance through ``bg_color`` and ``text_color``; when left empty, "
            "the global CSS variables are used. ``fixed=True`` makes the bar "
            "sticky at the top of its scroll container."
        ),
        "properties": [
            {
                "name": "title",
                "type": "str",
                "default": "''",
                "description": "Main label rendered inside ``.roya-appbar__title``.",
            },
            {
                "name": "subtitle",
                "type": "str",
                "default": "''",
                "description": "Secondary label rendered below the title as ``<small>``.",
            },
            {
                "name": "position",
                "type": "str",
                "default": "'top'",
                "description": "One of ``'top'``, ``'bottom'`` (bottom bars use the same markup).",
            },
            {
                "name": "fixed",
                "type": "bool",
                "default": "True",
                "description": "Adds ``.roya-appbar--fixed`` (sticky at top).",
            },
            {
                "name": "sticky",
                "type": "bool",
                "default": "True",
                "description": "Reserved for future scroll-collapse behavior.",
            },
            {
                "name": "elevation",
                "type": "int",
                "default": "2",
                "description": "0–4, mapped to ``--roya-shadow-N`` in CSS.",
            },
            {
                "name": "scroll_behavior",
                "type": "str",
                "default": "'elevate'",
                "description": "One of ``'elevate'``, ``'collapse'``, ``'hide'``.",
            },
            {
                "name": "variant",
                "type": "str",
                "default": "'small'",
                "description": "One of ``'small'``, ``'medium'``, ``'large'``, ``'center-aligned'``.",
            },
            {
                "name": "left_icon",
                "type": "str",
                "default": "'menu'",
                "description": "Material icon name for the leading navigation button; empty string hides it.",
            },
            {
                "name": "right_icons",
                "type": "list[str]",
                "default": "[]",
                "description": "Material icon names rendered as action buttons.",
            },
            {
                "name": "bg_color",
                "type": "str",
                "default": "''",
                "description": "CSS color string; empty falls back to ``--roya-surface``.",
            },
            {
                "name": "text_color",
                "type": "str",
                "default": "''",
                "description": "CSS color string; empty falls back to ``--roya-on-surface``.",
            },
        ],
        "events": [
            {
                "name": "on_action",
                "wire": "appbar:action",
                "description": (
                    "Emitted when a right-side action icon is clicked. The "
                    "payload carries ``icon`` and ``action`` fields."
                ),
            },
            {
                "name": "on_menu_open",
                "wire": "appbar:menu-open",
                "description": "Emitted when the leading navigation icon toggles the menu open.",
            },
            {
                "name": "on_menu_close",
                "wire": "appbar:menu-close",
                "description": "Emitted when the leading navigation icon toggles the menu closed.",
            },
            {
                "name": "on_scroll",
                "wire": "appbar:scroll",
                "description": "Emitted by the JS interaction layer on scroll (reserved).",
            },
            {
                "name": "on_collapse",
                "wire": "appbar:collapse",
                "description": "Emitted when a collapse variant finishes collapsing.",
            },
        ],
        "python_methods": [],
        "usage_python": (
            "from roya.components.navigation.appbar import AppBar\n"
            "\n"
            "bar = AppBar(\n"
            "    title=\"داشبورد\",\n"
            "    subtitle=\"خلاصه\",\n"
            "    left_icon=\"arrow-back\",\n"
            "    right_icons=[\"search\", \"more_vert\"],\n"
            "    bg_color=\"#1a73e8\",\n"
            "    text_color=\"#ffffff\",\n"
            "    fixed=True,\n"
            ")\n"
            "html = bar.render()"
        ),
        "usage_js": (
            "document.querySelector('[data-roya-component=\"appbar\"]')\n"
            "  .addEventListener('appbar:action', (e) => {\n"
            "    console.log('icon clicked:', e.detail.icon);\n"
            "  });"
        ),
        "accessibility": [
            "Leading and action buttons are real ``<button>`` elements with ``aria-label``.",
            "Focus ring follows the global ``:focus-visible`` rule (3px primary tint).",
            "Icons use ``aria-hidden='true'`` so screen readers announce the label only.",
        ],
        "notes": [
            "``right_icons`` accepts any Material icon name; unknown glyphs fall back to the raw string.",
            "JS wiring for the leading icon toggles ``el.dataset.menuOpen`` and emits ``appbar:menu-open`` / ``appbar:menu-close``.",
        ],
    },

    # -----------------------------------------------------------------
    # Badge
    # -----------------------------------------------------------------
    "badge": {
        "category": "Feedback",
        "title": "Badge",
        "class_path": "roya.components.feedback.badge.Badge",
        "template": "roya/components/feedback/badge.html",
        "css_classes": [
            "roya-badge",
            "roya-badge--small",
            "roya-badge--medium",
            "roya-badge--large",
        ],
        "summary": (
            "Small counter or status dot rendered inline to show notifications, "
            "counts, or a presence indicator."
        ),
        "description": (
            "Badge is the Roya equivalent of KivyMD's MDBadge. When ``value`` "
            "is numeric and exceeds ``max_value``, it renders as ``'{max_value}+'``. "
            "When ``dot=True`` it renders as a small circular indicator with an "
            "``aria-label`` and no text. Visibility is a two-step check: the "
            "outer ``visible`` flag and the ``value or dot`` gate, so an empty "
            "``value`` combined with ``dot=False`` renders nothing."
        ),
        "properties": [
            {
                "name": "value",
                "type": "str",
                "default": "''",
                "description": "Text or number to display. Numeric values respect ``max_value``.",
            },
            {
                "name": "max_value",
                "type": "int",
                "default": "99",
                "description": "Numeric threshold above which ``'{max_value}+'`` is shown.",
            },
            {
                "name": "visible",
                "type": "bool",
                "default": "True",
                "description": "Master switch; ``False`` suppresses all markup.",
            },
            {
                "name": "color",
                "type": "str",
                "default": "'error'",
                "description": "Semantic color token (``'error'``, ``'primary'``, …) mapped to CSS.",
            },
            {
                "name": "size",
                "type": "str",
                "default": "'medium'",
                "description": "One of ``'small'``, ``'medium'``, ``'large'``.",
            },
            {
                "name": "position",
                "type": "str",
                "default": "'top-end'",
                "description": "Anchor corner when used as an overlay badge.",
            },
            {
                "name": "dot",
                "type": "bool",
                "default": "False",
                "description": "Render a dot-only indicator instead of text.",
            },
            {
                "name": "show_zero",
                "type": "bool",
                "default": "False",
                "description": "When ``True``, a literal '0' value is rendered instead of hidden.",
            },
            {
                "name": "bg_color",
                "type": "str",
                "default": "'0.9,0.2,0.2,1'",
                "description": "CSS background color. Overrides the theme's error token.",
            },
            {
                "name": "overlap",
                "type": "bool",
                "default": "True",
                "description": "Reserved for parent-positioned badges (API parity with the reference pack).",
            },
        ],
        "events": [],
        "python_methods": [],
        "usage_python": (
            "from roya.components.feedback.badge import Badge\n"
            "\n"
            "counter = Badge(value=\"12\", color=\"primary\", size=\"small\")\n"
            "html = counter.render()\n"
            "\n"
            "notification_dot = Badge(dot=True, bg_color=\"#22c55e\")"
        ),
        "accessibility": [
            "Dot mode sets ``aria-label='اعلان جدید'`` so it is not silent to screen readers.",
            "Numeric overflow still exposes the original count via the title attribute (future).",
        ],
        "notes": [
            "Sizing: small=18px, medium=22px, large=26px.",
            "``bg_color`` accepts either CSS colors (``'#f00'``) or the RGBA string format from the reference pack.",
        ],
    },

    # -----------------------------------------------------------------
    # BottomSheet
    # -----------------------------------------------------------------
    "bottom_sheet": {
        "category": "Feedback",
        "title": "BottomSheet",
        "class_path": "roya.components.feedback.bottom_sheet.BottomSheet",
        "template": "roya/components/feedback/bottom_sheet.html",
        "css_classes": [
            "roya-bottom-sheet",
            "roya-bottom-sheet__panel",
            "roya-bottom-sheet__handle",
            "roya-bottom-sheet__backdrop",
            "roya-bottom-sheet__title",
            "roya-bottom-sheet__close",
        ],
        "summary": (
            "Dismissible panel that slides up from the bottom edge. Can be "
            "modal (with backdrop) or persistent."
        ),
        "description": (
            "BottomSheet is the Roya equivalent of KivyMD's MDBottomSheet. It "
            "starts hidden (``hidden`` attribute) and slides into view when "
            "``open=True``. Three dismissal paths are wired: a handle drag "
            "downward (only when ``detachable=True``), a backdrop click "
            "(only when ``close_on_backdrop=True``), and the Escape key (only "
            "when ``close_on_escape=True``). The panel exposes three height "
            "states — collapsed, initial and expanded — and a per-instance "
            "``corner_radius`` for the top corners."
        ),
        "properties": [
            {
                "name": "open",
                "type": "bool",
                "default": "False",
                "description": "Whether the sheet is currently visible.",
            },
            {
                "name": "title",
                "type": "str",
                "default": "''",
                "description": "Optional heading rendered as ``<h2>``.",
            },
            {
                "name": "dismissible",
                "type": "bool",
                "default": "True",
                "description": "When ``False``, all close paths are ignored (programmatic ``close()`` too).",
            },
            {
                "name": "modal",
                "type": "bool",
                "default": "True",
                "description": "Adds ``role='dialog'`` and ``aria-modal`` to the panel.",
            },
            {
                "name": "max_height",
                "type": "str",
                "default": "'85vh'",
                "description": "CSS max-height for the panel.",
            },
            {
                "name": "detachable",
                "type": "bool",
                "default": "True",
                "description": "Show the drag handle and enable swipe-to-dismiss.",
            },
            {
                "name": "backdrop",
                "type": "bool",
                "default": "True",
                "description": "Render the dark backdrop behind the sheet.",
            },
            {
                "name": "close_on_backdrop",
                "type": "bool",
                "default": "True",
                "description": "Whether clicking the backdrop closes the sheet.",
            },
            {
                "name": "close_on_escape",
                "type": "bool",
                "default": "True",
                "description": "Whether the Escape key closes the sheet.",
            },
            {
                "name": "initial_height",
                "type": "str",
                "default": "'40%'",
                "description": "Height when the sheet first opens.",
            },
            {
                "name": "expanded_height",
                "type": "str",
                "default": "'90%'",
                "description": "Fully expanded height.",
            },
            {
                "name": "collapsed_height",
                "type": "str",
                "default": "'15%'",
                "description": "Minimum height reachable by dragging.",
            },
            {
                "name": "bg_color",
                "type": "str",
                "default": "''",
                "description": "Optional CSS background color; empty uses the theme surface.",
            },
            {
                "name": "corner_radius",
                "type": "str",
                "default": "'16px'",
                "description": "Top-left and top-right border radius.",
            },
        ],
        "events": [
            {
                "name": "on_open",
                "wire": "bottom-sheet:open",
                "description": "Emitted by ``show()`` after the sheet becomes visible.",
            },
            {
                "name": "on_close",
                "wire": "bottom-sheet:close",
                "description": (
                    "Emitted when the sheet is closed — by the close button, "
                    "backdrop click, Escape, or a downward drag. The ``detail.reason`` "
                    "field distinguishes ``'swipe'`` from other paths."
                ),
            },
        ],
        "python_methods": [
            {
                "name": "show",
                "description": "Open the sheet and emit ``on_open`` if it was closed.",
            },
            {
                "name": "close",
                "description": "Close the sheet and emit ``on_close`` if it was open and dismissible.",
            },
        ],
        "usage_python": (
            "from roya.components.feedback.bottom_sheet import BottomSheet\n"
            "\n"
            "sheet = BottomSheet(\n"
            "    open=True,\n"
            "    title=\"تنظیمات\",\n"
            "    detachable=True,\n"
            "    close_on_escape=True,\n"
            "    bg_color=\"#fff8f0\",\n"
            "    corner_radius=\"20px\",\n"
            ")\n"
            "sheet.add_child(HTMLFragment('<p>محتوای پنل</p>'))\n"
            "html = sheet.render()"
        ),
        "usage_js": (
            "document.querySelector('[data-roya-component=\"bottom_sheet\"]')\n"
            "  .addEventListener('bottom-sheet:close', (e) => {\n"
            "    console.log('closed, reason:', e.detail.reason);\n"
            "  });"
        ),
        "accessibility": [
            "Panel carries ``role='dialog'`` and ``aria-modal='true'`` when ``modal=True``.",
            "Escape is honored unless ``close_on_escape=False``.",
            "Backdrop click closes unless ``close_on_backdrop=False``.",
            "Close button carries an explicit ``aria-label='بستن'``.",
        ],
        "notes": [
            "``close()`` is a no-op when ``dismissible=False``.",
            "Drag-to-dismiss requires ``detachable=True`` and a downward movement of >80px.",
            "Height values accept any CSS length: ``'40%'``, ``'320px'``, ``'60vh'``.",
        ],
    },

    "button": {
        "category": "Actions",
        "title": "Button",
        "class_path": "roya.components.actions.button.Button",
        "template": "roya/components/actions/button.html",
        "css_classes": ["roya-button"],
        "summary": "Filled, elevated, outlined, text or tonal MD3 button.",
        "description": "Emits button:click. Supports loading state, icon-only mode, and full-width layout.",
        "properties": [
            {'name': 'label', 'type': 'str', 'default': '', 'description': 'Button text.'},
            {'name': 'variant', 'type': 'str', 'default': 'filled', 'description': 'filled, elevated, outlined, text, tonal.'},
            {'name': 'size', 'type': 'str', 'default': 'medium', 'description': 'small, medium, large.'},
            {'name': 'disabled', 'type': 'bool', 'default': 'False', 'description': 'Native disabled attribute.'},
            {'name': 'loading', 'type': 'bool', 'default': 'False', 'description': 'Shows a spinner.'},
            {'name': 'icon_only', 'type': 'bool', 'default': 'False', 'description': 'Circular icon-only mode.'},
            {'name': 'full_width', 'type': 'bool', 'default': 'False', 'description': 'Stretches to 100 percent width.'},
        ],
        "events": [{'name': 'on_click', 'wire': 'button:click', 'description': 'Fired on activation.'}],
        "python_methods": [],
        "usage_python": "from roya.components.actions.button import Button\n\nbtn = Button(label='ذخیره', variant='filled', size='medium')\nhtml = btn.render()",
        "usage_js": "document.addEventListener('button:click', (e) => console.log(e.detail));",
        "accessibility": [
            "Native <button> element.",
            "Focus ring inherits the global :focus-visible rule.",
        ],
        "notes": [
            "Ripple behavior auto-attached in the JS interaction layer.",
        ],
    },

    "card": {
        "category": "Content",
        "title": "Card",
        "class_path": "roya.components.content.card.Card",
        "template": "roya/components/content/card.html",
        "css_classes": ["roya-card", "roya-card--elevated", "roya-card--outlined", "roya-card--filled"],
        "summary": "Surface container grouping related content.",
        "description": "Variants elevated, outlined, filled. Clickable mode adds tabindex and card:click.",
        "properties": [
            {'name': 'variant', 'type': 'str', 'default': 'elevated', 'description': 'elevated, outlined, filled.'},
            {'name': 'clickable', 'type': 'bool', 'default': 'False', 'description': 'Adds tabindex and card:click.'},
            {'name': 'selected', 'type': 'bool', 'default': 'False', 'description': 'Highlights the card.'},
        ],
        "events": [{'name': 'on_click', 'wire': 'card:click', 'description': 'Fired when clickable and activated.'}],
        "python_methods": [],
        "usage_python": "from roya.components.content.card import Card\n\nc = Card(variant='elevated', clickable=True)\nhtml = c.render()",
        "usage_js": "",
        "accessibility": [
            "Clickable cards receive tabindex=0.",
            "Enter and Space trigger card:click.",
        ],
        "notes": [
            "Clickable variant auto-injects pointer cursor.",
        ],
    },

    "chip": {
        "category": "Data Display",
        "title": "Chip",
        "class_path": "roya.components.data_display.chip.Chip",
        "template": "roya/components/data_display/chip.html",
        "css_classes": ["roya-chip"],
        "summary": "Compact pill for filters, tags, or selections.",
        "description": "Toggles is-selected on click; emits chip:select / chip:deselect.",
        "properties": [
            {'name': 'label', 'type': 'str', 'default': '', 'description': 'Chip text.'},
            {'name': 'variant', 'type': 'str', 'default': 'assist', 'description': 'assist, filter, input, suggestion.'},
            {'name': 'clickable', 'type': 'bool', 'default': 'True', 'description': 'Enables click/Enter/Space handling.'},
            {'name': 'selected', 'type': 'bool', 'default': 'False', 'description': 'Initial selected state.'},
            {'name': 'leading_icon', 'type': 'str', 'default': '', 'description': 'Optional leading icon.'},
            {'name': 'trailing_icon', 'type': 'str', 'default': '', 'description': 'Optional trailing icon.'},
        ],
        "events": [
            {'name': 'on_click', 'wire': 'chip:click', 'description': 'Fired on click.'},
            {'name': 'on_select', 'wire': 'chip:select', 'description': 'Fired when selected toggles on.'},
            {'name': 'on_deselect', 'wire': 'chip:deselect', 'description': 'Fired when selected toggles off.'},
        ],
        "python_methods": [],
        "usage_python": "from roya.components.data_display.chip import Chip\n\nc = Chip(label='فارسی', clickable=True, selected=True)\nhtml = c.render()",
        "usage_js": "",
        "accessibility": [
            "Clickable chips carry role=button and aria-pressed.",
            "Enter and Space trigger activation.",
        ],
        "notes": [
            "Leading and trailing icons use aria-hidden=true.",
        ],
    },

    "dialog": {
        "category": "Feedback",
        "title": "Dialog",
        "class_path": "roya.components.feedback.dialog.Dialog",
        "template": "roya/components/feedback/dialog.html",
        "css_classes": ["roya-dialog", "roya-dialog__panel", "roya-dialog__backdrop", "roya-dialog__close"],
        "summary": "Modal window with backdrop, close button, and Escape support.",
        "description": "Opens via data-roya-open or R.open(id). Closes on backdrop, close button, or Escape unless suppressed.",
        "properties": [
            {'name': 'open', 'type': 'bool', 'default': 'False', 'description': 'Whether the dialog is visible.'},
            {'name': 'title', 'type': 'str', 'default': '', 'description': 'Heading text.'},
            {'name': 'message', 'type': 'str', 'default': '', 'description': 'Body message.'},
            {'name': 'modal', 'type': 'bool', 'default': 'True', 'description': 'Adds role=dialog and aria-modal.'},
            {'name': 'dismissible', 'type': 'bool', 'default': 'True', 'description': 'Whether close paths work.'},
            {'name': 'close_on_escape', 'type': 'bool', 'default': 'True', 'description': 'Escape key closes.'},
            {'name': 'close_on_outside', 'type': 'bool', 'default': 'True', 'description': 'Backdrop click closes.'},
            {'name': 'persistent', 'type': 'bool', 'default': 'False', 'description': 'Prevents all close paths.'},
            {'name': 'max_width', 'type': 'str', 'default': '560px', 'description': 'CSS max-width of the panel.'},
        ],
        "events": [{'name': 'on_close', 'wire': 'dialog:close', 'description': 'Emitted when the dialog closes.'}],
        "python_methods": [],
        "usage_python": "from roya.components.feedback.dialog import Dialog\n\nd = Dialog(open=True, title='تأیید', message='آیا مطمئنید؟')\nhtml = d.render()",
        "usage_js": "document.addEventListener('dialog:close', (e) => console.log(e.detail.id));",
        "accessibility": [
            "role=dialog and aria-modal=true when modal.",
            "Escape honored unless close_on_escape=False.",
            "Backdrop click honored unless close_on_outside=False.",
            "Close button carries an explicit aria-label.",
        ],
        "notes": [
            "persistent=True suppresses every close path (including programmatic).",
        ],
    },

    "tabs": {
        "category": "Navigation",
        "title": "Tabs",
        "class_path": "roya.components.navigation.tabs.Tabs",
        "template": "roya/components/navigation/tabs.html",
        "css_classes": ["roya-tabs", "roya-tab", "roya-tab--active"],
        "summary": "Horizontal or vertical tab strip with arrow-key navigation.",
        "description": "Uses role=tablist. Arrow keys move focus; Home and End jump to extremes.",
        "properties": [
            {'name': 'items', 'type': 'list', 'default': '[]', 'description': 'List of label dicts.'},
            {'name': 'active_tab', 'type': 'int', 'default': '0', 'description': 'Zero-based index of the active tab.'},
            {'name': 'orientation', 'type': 'str', 'default': 'horizontal', 'description': 'horizontal or vertical.'},
            {'name': 'variant', 'type': 'str', 'default': 'primary', 'description': 'primary or secondary.'},
        ],
        "events": [
            {'name': 'on_change', 'wire': 'tab:change', 'description': 'Fired when the active tab changes.'},
            {'name': 'on_select', 'wire': 'tab:select', 'description': 'Fired when a tab is selected.'},
        ],
        "python_methods": [],
        "usage_python": "from roya.components.navigation.tabs import Tabs\n\nt = Tabs(items=[{'label': 'مشخصات'}, {'label': 'فعالیت'}], active_tab=0)\nhtml = t.render()",
        "usage_js": "",
        "accessibility": [
            "role=tablist, role=tab, aria-selected maintained.",
            "Arrow keys cycle focus; Home/End jump.",
            "Roving tabindex keeps one tab reachable.",
        ],
        "notes": [
            "Vertical orientation uses flex-direction:column and border-inline-end.",
        ],
    },

    "textfield": {
        "category": "Forms",
        "title": "TextField",
        "class_path": "roya.components.forms.textfield.TextField",
        "template": "roya/components/forms/textfield.html",
        "css_classes": ["roya-textfield", "roya-textfield__input"],
        "summary": "Labeled text input with hint and focus ring.",
        "description": "Native input keeps keyboard, touch, and screen-reader behavior.",
        "properties": [
            {'name': 'label', 'type': 'str', 'default': '', 'description': 'Visible label.'},
            {'name': 'placeholder', 'type': 'str', 'default': '', 'description': 'Placeholder text.'},
            {'name': 'field_name', 'type': 'str', 'default': '', 'description': 'HTML name attribute.'},
            {'name': 'value', 'type': 'str', 'default': '', 'description': 'Initial value.'},
            {'name': 'type', 'type': 'str', 'default': 'text', 'description': 'HTML input type.'},
            {'name': 'disabled', 'type': 'bool', 'default': 'False', 'description': 'Native disabled.'},
            {'name': 'readonly', 'type': 'bool', 'default': 'False', 'description': 'Native readonly.'},
            {'name': 'required', 'type': 'bool', 'default': 'False', 'description': 'Native required.'},
        ],
        "events": [],
        "python_methods": [],
        "usage_python": "from roya.components.forms.textfield import TextField\n\ntf = TextField(label='نام', placeholder='نام خود را وارد کنید', field_name='name')\nhtml = tf.render()",
        "usage_js": "",
        "accessibility": [
            "Native input inherits label association.",
            "Focus ring via :focus-within on the wrapper.",
        ],
        "notes": [
            "type=email/tel/number passed through to HTML.",
        ],
    },
}


# =============================================================================
# OTHER_COMPONENTS — brief reference for the rest of the library
# =============================================================================

OTHER_COMPONENTS: Dict[str, str] = {
    "button": "Filled/elevated/outlined/text/tonal MD3 button. Emits ``button:click``.",
    "fab": "Floating action button; ``extended=True`` adds a text label. Emits ``fab:click``.",
    "icon_button": "Circular icon-only button; ``aria-pressed`` toggles a ``selected`` state.",
    "card": "Surface container; variants: elevated, outlined, filled, clickable, selected.",
    "chip": "Compact selectable pill; toggles ``is-selected`` on click.",
    "avatar": "Circular wrapper for initials or an image.",
    "list": "Vertical list with optional multi-select; emits ``list:item-click`` / ``list:item-select``.",
    "progress": "Linear progress bar; ``indeterminate=True`` animates a sweeping indicator.",
    "dialog": "Modal confirmation window with backdrop and Escape handling.",
    "snackbar": "Bottom inline notification strip.",
    "tooltip": "Hover/focus/click-triggered tooltip bubble.",
    "textfield": "Labeled text input with hint and focus ring.",
    "checkbox": "Native checkbox with accent-color matching the theme.",
    "switch": "Material-style toggle with RTL-aware thumb position.",
    "slider": "Range slider with optional value output.",
    "select": "Dropdown select; supports multiple selection.",
    "radio_group": "Grouped radio inputs with row/column layout.",
    "tabs": "Horizontal or vertical tab strip; arrow-key navigation built in.",
    "navigation_bar": "Bottom app-level navigation with icons and labels.",
    "navigation_drawer": "Overlay drawer with backdrop and auto-close.",
    "navigation_rail": "Vertical side navigation for larger screens.",
    "box_layout": "Flex container with row/column direction and gap.",
    "stack_container": "Stacked layout with wrap and gap.",
    "grid_container": "CSS grid container.",
    "scroll_container": "Scrollable region with smooth/overscroll options.",
    "virtual_list": "Windowed list renderer for large datasets; emits ``virtual-list:item-click``.",
    "date_picker": "Native date input.",
    "time_picker": "Native time input.",
    "adaptive_container": "Responsive container with per-breakpoint direction.",
    "float_container": "Floating (absolutely positioned) container.",
    "relative_container": "Relatively positioned container.",
}


# =============================================================================
# Helpers
# =============================================================================

def list_components() -> List[str]:
    """Return every documented component name, alphabetically sorted."""
    return sorted(set(COMPONENT_DOCS) | set(OTHER_COMPONENTS))


def get_component_doc(name: str) -> Optional[Dict[str, Any]]:
    """Return the detailed doc entry for ``name`` or ``None``."""
    if name in COMPONENT_DOCS:
        return COMPONENT_DOCS[name]
    if name in OTHER_COMPONENTS:
        return {
            "title": name,
            "summary": OTHER_COMPONENTS[name],
            "properties": [],
            "events": [],
            "python_methods": [],
            "usage_python": "",
            "usage_js": "",
            "accessibility": [],
            "notes": ["Brief entry — see ``COMPONENT_DOCS`` for the full reference."],
        }
    return None


def _render_markdown(name: str, doc: Dict[str, Any]) -> str:
    """Render one component's doc dict as Markdown."""
    parts: List[str] = []
    title = doc.get("title") or name
    category = doc.get("category") or "Component"
    parts.append(f"## {title} ({category})\n")
    parts.append(f"**Summary:** {doc.get('summary', '').strip()}\n")

    if doc.get("description"):
        parts.append(doc["description"].strip() + "\n")

    if doc.get("class_path"):
        parts.append(f"**Class:** `{doc['class_path']}`  ")
    if doc.get("template"):
        parts.append(f"**Template:** `{doc['template']}`  ")
    if doc.get("css_classes"):
        parts.append("**CSS:** " + ", ".join(f"`.{c}`" for c in doc["css_classes"]) + "  ")
    parts.append("")

    props = doc.get("properties") or []
    if props:
        parts.append("### Properties\n")
        parts.append("| Name | Type | Default | Description |")
        parts.append("|------|------|---------|-------------|")
        for p in props:
            parts.append(
                f"| `{p['name']}` | `{p['type']}` | `{p['default']}` | {p['description']} |"
            )
        parts.append("")

    events = doc.get("events") or []
    if events:
        parts.append("### Events\n")
        parts.append("| Prop | Wire | Description |")
        parts.append("|------|------|-------------|")
        for e in events:
            parts.append(
                f"| `{e['name']}` | `{e['wire']}` | {e['description']} |"
            )
        parts.append("")

    methods = doc.get("python_methods") or []
    if methods:
        parts.append("### Python Methods\n")
        for m in methods:
            parts.append(f"- `{m['name']}()` — {m['description']}")
        parts.append("")

    if doc.get("usage_python"):
        parts.append("### Usage (Python)\n")
        parts.append("```python")
        parts.append(doc["usage_python"].strip())
        parts.append("```\n")

    if doc.get("usage_js"):
        parts.append("### Usage (JavaScript)\n")
        parts.append("```javascript")
        parts.append(doc["usage_js"].strip())
        parts.append("```\n")

    a11y = doc.get("accessibility") or []
    if a11y:
        parts.append("### Accessibility\n")
        for note in a11y:
            parts.append(f"- {note}")
        parts.append("")

    notes = doc.get("notes") or []
    if notes:
        parts.append("### Notes\n")
        for note in notes:
            parts.append(f"- {note}")
        parts.append("")

    return "\n".join(parts)


def render_docs(name: Optional[str] = None, format: str = "markdown") -> str:
    """Render the docs.

    Parameters
    ----------
    name : str, optional
        When provided, render only that component. Otherwise render all.
    format : {"markdown", "console"}
        ``markdown`` produces a ready-to-paste README section.
        ``console`` produces a compact plain-text summary.
    """
    names: Iterable[str] = [name] if name else list_components()

    if format == "console":
        lines = [f"Roya Components v{__version__}", "=" * 32]
        for n in names:
            doc = get_component_doc(n)
            if not doc:
                lines.append(f"  ! unknown component: {n}")
                continue
            lines.append(f"\n* {doc.get('title', n)}")
            lines.append(f"    {doc.get('summary', '').strip()}")
            for p in doc.get("properties") or []:
                lines.append(
                    f"    - {p['name']}: {p['type']} = {p['default']}"
                )
        return "\n".join(lines)

    sections: List[str] = [
        f"# Roya Component Reference (v{__version__})",
        "",
        (
            "Auto-generated from ``roya_docs.py``. Each section follows the "
            "KivyMD documentation pattern: summary, properties, events, "
            "usage, accessibility, notes."
        ),
        "",
    ]
    for n in names:
        doc = get_component_doc(n)
        if not doc:
            sections.append(f"## {n}\n\n_(unknown component)_\n")
            continue
        sections.append(_render_markdown(n, doc))
        sections.append("---\n")
    return "\n".join(sections)


# =============================================================================
# CLI
# =============================================================================

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="roya_docs",
        description="Print the Roya component reference.",
    )
    parser.add_argument(
        "component",
        nargs="?",
        help="Show only this component (e.g. bottom_sheet).",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List every documented component and exit.",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "console"),
        default="markdown",
        help="Output format (default: markdown).",
    )
    args = parser.parse_args(argv)

    if args.list:
        for name in list_components():
            doc = get_component_doc(name) or {}
            print(f"{name:<24} {doc.get('summary', '')[:90]}")
        return 0

    print(render_docs(args.component, format=args.format))
    return 0


if __name__ == "__main__":
    sys.exit(main())

