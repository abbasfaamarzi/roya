# Roya Language 1.0

Roya Language is a KV-inspired declarative UI format for the existing Roya component registry. It does not replace Python components, Django templates or CSS. It provides a compact page tree, reusable style rules, context expressions and named Python action bindings.

## Render a page from Django

```python
from django.http import HttpResponse
from roya.lang import render_roya
from instagram_app.logic import build_context

def home(request):
    return HttpResponse(render_roya(
        request,
        "instagram_app/pages/home.roya",
        build_context(),
    ))
```

The .roya file must be discoverable by Django's template loader. The renderer returns a safe HTML fragment and includes the small browser action runtime plus a CSRF token for the action endpoint.

## Basic syntax

```kv
#:roya 1.0
#:logic shop.actions

box_layout:
    direction: "column"
    gap: "md"

    for product in products key product.id:
        card:
            label:
                text: product.name
            button:
                label: "Add to cart"
                on_press:
                    action: shop.add_to_cart
                    args:
                        product_id: product.id
```

## Reusable rules and CSS

```kv
<ProductCard@box_layout>:
    direction: "column"
    class_name: "product-card"
    style:
        border-radius: "16px"
        padding: "12px"
```

A rule aliases a registered Roya component and supplies default component properties. `style` creates inline CSS declarations on that component's root element. Keep complex responsive states and pseudo-selectors in normal CSS files.

## Python actions

```python
from roya.actions import action

@action("shop.add_to_cart")
def add_to_cart(request, product_id):
    # Validate permissions and ownership, then update the database.
    return {"added": True, "product_id": product_id}
```

Add `path("roya/actions/", include("roya.actions.urls"))` to the project's URL configuration. The Falcon update adds this route to the repository's `royaproject/urls.py` sample project.

Only explicitly registered actions can be called. The browser sends POST JSON with same-origin credentials and the Django CSRF header. Action functions must still enforce their own authentication, authorization, input validation and business rules.

## First-release limits

- `for`, `if`, component nesting, properties, style rules, `#:include`, `#:logic`, and named event bindings are supported.
- Expressions support constants, context names, safe attribute/key access, basic arithmetic/comparisons, boolean operations, and `str`, `int`, `float`, `len`, `bool`.
- Expressions are evaluated during server rendering; this first release is not a client-side reactive state engine.
- `on_press`, `on_release`, `on_click`, `on_change`, `on_submit`, `on_focus`, and `on_blur` are supported when the registered component declares that event.
- CSS remains available for responsive media queries, pseudo-classes, animations and complex selectors.
- Action results may include `updates: {"#selector": "new text"}` to update text content in the page. Use this only with selectors and text derived from trusted application logic.
