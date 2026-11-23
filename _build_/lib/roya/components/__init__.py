"""Roya component library."""


def register_all(registry=None):
    from roya.core.registry import registry as default_registry
    from .actions import Button, FAB, IconButton
    from .content import Card, Divider, Icon, Image, Label
    from .data_display import Avatar, Chip, ListComponent
    from .feedback import Badge, BottomSheet, Dialog, Progress, Snackbar, Tooltip
    from .forms import Checkbox, DatePicker, RadioGroup, Select, Slider, Switch, TextField, TimePicker
    from .layout import (
        AnchorContainer, BoxLayout, FloatContainer, GridContainer,
        RelativeContainer, ScrollContainer, StackContainer, VirtualList,
    )
    from .navigation import AppBar, NavigationBar, NavigationDrawer, NavigationRail, Tabs

    reg = registry or default_registry
    for cls in (
        Button, FAB, IconButton,
        Label, Icon, Card, Divider, Image,
        Avatar, Chip, ListComponent,
        Dialog, Snackbar, Progress, Tooltip, Badge, BottomSheet,
        TextField, Checkbox, Switch, Slider, Select, RadioGroup, DatePicker, TimePicker,
        BoxLayout, GridContainer, StackContainer, AnchorContainer,
        RelativeContainer, FloatContainer, ScrollContainer, VirtualList,
        AppBar, Tabs, NavigationDrawer, NavigationRail, NavigationBar,
    ):
        reg.register(cls)
    return reg


__all__ = ["register_all"]