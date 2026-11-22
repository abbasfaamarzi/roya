# Upgrading Roya 0.1.0 → 0.2.0

## Compatibility

This release keeps the package name `roya`, the `RoyaConfig` app config, all pre-existing Python component imports, the `{% load roya %}` template library, and the `{% roya_component "..." %}` tag. Existing CSS class prefixes and the current visual design are retained; new styles are additive.

## New components

```python
from roya.components.forms import DatePicker, TimePicker
from roya.components.feedback import BottomSheet
from roya.components.layout import VirtualList

birth_date = DatePicker(label="Date", field_name="date", value="2026-11-22")
meeting_time = TimePicker(label="Time", field_name="time", value="09:30")
sheet = BottomSheet(title="Details", open=True)
large_list = VirtualList(items=[f"Row {i}" for i in range(10_000)], item_height=44)
```

Template examples:

```django
{% load roya %}
{% roya_component "date_picker" label="Date" field_name="date" %}
{% roya_component "time_picker" label="Time" field_name="time" %}
{% roya_component "bottom_sheet" title="More details" open=True %}
{% roya_component "virtual_list" items=my_string_items item_height=44 %}
```

`VirtualList` currently supports a list of strings and fixed row heights. Variable-height rows, rich per-row templates, and server-side pagination are not part of this release.

## Static files

Continue loading `roya/css/roya.css` and `roya/js/roya.js` as before. If static assets are cached by your deployment, clear/rebuild the staticfiles output.
