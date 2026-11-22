"""Smoke tests for the Roya library."""
import pytest



def test_registry_populated():
    from roya.core.registry import registry
    assert registry.count() > 0
    for name in ("button", "textfield", "dialog", "card", "tabs"):
        assert registry.has(name), f"missing component: {name}"


def test_button_lifecycle_and_render():
    from roya.components.actions import Button
    btn = Button(label="Hello", variant="filled")
    btn.mount()
    html = btn.render()
    assert "Hello" in html
    assert "roya-button" in html
    assert "data-roya-component=\"button\"" in html
    assert btn.lifecycle.state.value in ("ready", "rendered", "mounted")


def test_invalid_variant_rejected():
    from roya.components.actions import Button
    with pytest.raises(Exception):
        Button(variant="does-not-exist")


def test_event_dispatch():
    from roya.components.actions import Button
    btn = Button(label="Click")
    captured = []
    btn.on_click.subscribe(lambda p: captured.append(p))
    btn.click()
    assert len(captured) == 1
    assert captured[0].type == "button:click"
    assert captured[0].component_id == btn.id


def test_theme_manager_tokens():
    from roya.theme.manager import theme_manager
    color = theme_manager.resolve_color("primary")
    assert color
    spacing = theme_manager.resolve_spacing("md")
    assert spacing


def test_lifecycle_state_machine_guard():
    from roya.components.actions import Button
    from roya.core.exceptions import LifecycleError
    from roya.core.lifecycle import LifecycleState
    btn = Button(label="x")
    with pytest.raises(LifecycleError):
        btn.lifecycle.transition(LifecycleState.DESTROYED)

def test_new_components_registered():
    from roya.core.registry import registry
    for name in ("date_picker", "time_picker", "bottom_sheet", "virtual_list"):
        assert registry.has(name)


def test_date_and_time_picker_events():
    from roya.components.forms import DatePicker, TimePicker
    date = DatePicker(value="2026-11-22")
    time = TimePicker(value="09:30")
    captured = []
    date.on_change.subscribe(lambda payload: captured.append(payload.detail["value"]))
    time.on_change.subscribe(lambda payload: captured.append(payload.detail["value"]))
    date.set_value("2026-11-23")
    time.set_value("10:15")
    assert captured == ["2026-11-23", "10:15"]


def test_bottom_sheet_open_close():
    from roya.components.feedback import BottomSheet
    sheet = BottomSheet()
    events = []
    sheet.on_open.subscribe(lambda payload: events.append("open"))
    sheet.on_close.subscribe(lambda payload: events.append("close"))
    sheet.show()
    sheet.close()
    assert events == ["open", "close"]


def test_virtual_list_fixed_height_validation():
    from roya.components.layout import VirtualList
    from roya.core.exceptions import ValidationError
    assert VirtualList(items=["a", "b"], item_height=40).get_context()["total_height"] == 80
    with pytest.raises(ValidationError):
        VirtualList(items=["a"], item_height=0)
    with pytest.raises(ValidationError):
        VirtualList(items=[{"label": "not a string"}])
