# Changelog

## 0.2.0 — Roya incremental upgrade

- Preserved the `roya` import package, Django app identity, `{% load roya %}` and `{% roya_component %}` template API, existing component names, and the existing component/module layout.
- Added `DatePicker` and `TimePicker` form components with native browser inputs and Python/JavaScript change events.
- Added `BottomSheet` feedback component with dismissible modal presentation.
- Added fixed-row-height `VirtualList` with windowed DOM rendering for large collections of string items.
- Added component templates, styles, exports, registry registration, and runtime mounting for the new components.
- Made runtime component mounting idempotent to prevent duplicate listeners when `Roya.mount()` is called more than once.

This is an incremental alpha release. Run the full test suite against the target Django version and verify browser behavior in the consuming application before production use.
