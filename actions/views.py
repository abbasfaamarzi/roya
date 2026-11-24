"""HTTP dispatcher for registered Roya Python actions."""
import inspect
import json
import logging

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .registry import action_registry

logger = logging.getLogger("roya.actions")
_MAX_BODY_BYTES = 65536
_RESERVED_ARGUMENTS = {"request", "event", "component_id"}


@require_POST
def dispatch_action(request):
    if len(request.body) > _MAX_BODY_BYTES:
        return JsonResponse({"ok": False, "error": "Request body is too large."}, status=413)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return JsonResponse({"ok": False, "error": "Invalid JSON request."}, status=400)

    if not isinstance(payload, dict):
        return JsonResponse({"ok": False, "error": "The request must be a JSON object."}, status=400)

    name = payload.get("action")
    args = payload.get("args", {})
    event = payload.get("event", {})
    component_id = payload.get("component_id", "")
    if not isinstance(name, str) or not name or not isinstance(args, dict):
        return JsonResponse({"ok": False, "error": "Action name and args are required."}, status=400)
    if not isinstance(event, dict) or not isinstance(component_id, str):
        return JsonResponse({"ok": False, "error": "Invalid event payload."}, status=400)
    if _RESERVED_ARGUMENTS.intersection(args):
        return JsonResponse({"ok": False, "error": "Reserved action arguments cannot be overridden."}, status=400)

    function = action_registry.get(name)
    if function is None:
        return JsonResponse({"ok": False, "error": "Unknown action."}, status=404)

    try:
        signature = inspect.signature(function)
        parameters = signature.parameters
        kwargs = dict(args)
        if "request" in parameters:
            kwargs["request"] = request
        if "event" in parameters:
            kwargs["event"] = event
        if "component_id" in parameters:
            kwargs["component_id"] = component_id
        signature.bind(**kwargs)
    except (TypeError, ValueError):
        logger.info("Invalid arguments for Roya action %s", name, exc_info=True)
        return JsonResponse({"ok": False, "error": "Invalid action arguments."}, status=400)

    try:
        result = function(**kwargs)
        return JsonResponse({"ok": True, "result": result}, json_dumps_params={"default": str})
    except Exception:
        logger.exception("Roya action failed: %s", name)
        return JsonResponse({"ok": False, "error": "Action execution failed."}, status=500)