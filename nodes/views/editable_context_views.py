import os
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .view_file_handlers import load_json_or_404, save_json


def get_nested(data, path):
    keys = path.split(".")
    for key in keys:
        data = data.get(key)
        if data is None:
            return None
    return data


def set_nested(data, path, value):
    keys = path.split(".")
    for key in keys[:-1]:
        data = data.setdefault(key, {})
    data[keys[-1]] = value


def remove_nested(data, path):
    keys = path.split(".")
    for key in keys[:-1]:
        data = data.get(key, {})
    data.pop(keys[-1], None)


# JSON Action Handlers
def handle_get_action(json_data, element_path):
    print(type(json_data))
    result = get_nested(json_data["editableContext"], element_path)
    if result is not None:
        return JsonResponse({"value": result})
    return HttpResponseBadRequest("Path not found.")


def handle_remove_action(json_data, json_path, element_path):
    remove_nested(json_data["editableContext"], element_path)
    save_json(json_data, json_path)
    return JsonResponse({"status": "removed", "path": element_path})


def handle_set_all_action(json_data, json_path, element_value):
    json_data["editableContext"] = (
        element_value  # expecting `element_value` to be a dict
    )
    save_json(json_data, json_path)
    return JsonResponse({"status": "set_all", "data": json_data["editableContext"]})


def handle_append_action(json_data, json_path, element_path, element_value):
    nested_data = get_nested(json_data["editableContext"], element_path)
    if isinstance(nested_data, list):
        nested_data.append(element_value)
    elif isinstance(nested_data, dict) and isinstance(element_value, dict):
        nested_data.update(element_value)
    else:
        return HttpResponseBadRequest(
            "Append action requires either a list or dictionary target."
        )
    save_json(json_data, json_path)
    return JsonResponse({"status": "appended", "data": json_data["editableContext"]})


def handle_remove_from_list_action(json_data, json_path, element_path, element_value):
    nested_data = get_nested(json_data["editableContext"], element_path)
    if isinstance(nested_data, list):
        try:
            if isinstance(element_value, int):
                nested_data.pop(element_value)
            else:
                nested_data.remove(element_value)
        except (IndexError, ValueError):
            return HttpResponseBadRequest("Index out of range or value not found.")
        save_json(json_data, json_path)
        return JsonResponse(
            {"status": "removed_from_list", "data": json_data["editableContext"]}
        )
    return HttpResponseBadRequest("Target for remove_from_list is not a list.")


def handle_change_action(json_data, json_path, element_path, element_value):
    set_nested(json_data["editableContext"], element_path, element_value)
    save_json(json_data, json_path)
    return JsonResponse(
        {"status": "changed", "path": element_path, "value": element_value}
    )


@csrf_exempt
def editable_context_view(request, node_path=""):
    # Determine if the request is JSON or form data
    if request.content_type == "application/json":
        data = json.loads(request.body)
    else:
        data = request.POST.dict()

    action = data.get("action")
    element_path = data.get("path")
    element_value = data.get("value")
    node_dir = os.path.join(settings.PAGES_BASE_DIR, node_path)
    json_path = os.path.join(settings.PAGES_BASE_DIR, node_path, "metadata.json")

    # Load the JSON data
    json_data = load_json_or_404(
        node_dir, "metadata.json", "Unable to load node metadata"
    )

    # Action handling
    if action == "get":
        return handle_get_action(json_data, element_path)
    elif action == "remove":
        return handle_remove_action(json_data, json_path, element_path)
    elif action == "set_all":
        return handle_set_all_action(json_data, json_path, element_value)
    elif action == "append":
        return handle_append_action(json_data, json_path, element_path, element_value)
    elif action == "remove_from_list":
        return handle_remove_from_list_action(
            json_data, json_path, element_path, element_value
        )
    elif action == "change":
        return handle_change_action(json_data, json_path, element_path, element_value)
    else:
        return HttpResponseBadRequest("Invalid action specified.")
