# Roya — Material Design 3 Components for Django

Object-oriented, fully-logged, standards-compliant component library for Django,
inspired by KivyMD 2.0's architecture and rebuilt for the web.

## Structure

- `roya.core` — Component base, Property descriptors, Event bus, Lifecycle, State, Validation, Registry
- `roya.foundation` — Color, Typography, Spacing, Elevation, Shape, Motion, Breakpoints tokens
- `roya.theme` — ThemeManager, DesignTokens, dynamic palettes
- `roya.components` — Layout, Actions, Content, Forms, Feedback, Navigation, Data Display
- `roya.behaviors` — Hover, Focus, Ripple, Motion, Elevation, Touch, StateLayer
- `roya.controllers` — Viewport, Responsive, Theme, Navigation, Focus
- `roya.effects` — StiffScrollEffect, SmoothScroll, SnapScroll, Transition
- `roya.templatetags` — `{% roya_component "button" label="Save" %}`

## Install

```python
# settings.py
INSTALLED_APPS = [
    "roya",
    # ...
]
```

## Usage

```django
{% load roya %}
{% roya_component "button" label="Submit" variant="filled" %}
```

Or in Python:

```python
from roya.components.actions import Button
btn = Button(label="Submit", variant="filled")
btn.on_click.subscribe(lambda payload: print("clicked", payload.to_dict()))
html = btn.render()
```

## Standards

- Material Design 3 tokens and variants
- WCAG 2.2 AA accessibility targets
- RTL / LTR ready
- Declarative Django template API
- Object-oriented lifecycle (`REGISTERED → INITIALIZED → VALIDATED → RENDERED → MOUNTED → READY → UNMOUNTED → DESTROYED`)
- Centralized logging on every module (`roya.*`)

## License

MIT

## Added in 0.2.0

- `DatePicker` and `TimePicker` native date/time fields.
- `BottomSheet` dismissible panel.
- `VirtualList` fixed-height windowed list for string collections.
- Existing `roya` imports and Django template tag API remain unchanged. See `UPGRADE_0.2.0.md`.
