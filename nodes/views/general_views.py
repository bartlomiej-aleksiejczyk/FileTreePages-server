import os
import mimetypes
from django.http import (
    FileResponse,
    Http404,
    HttpResponseNotAllowed,
)
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.views.decorators.clickjacking import xframe_options_exempt
from .editable_context_views import editable_context_view
from .node_renderers import render_node

DEFAULT_RENDERING_METHOD = "txt_render"
AUTOMATIC_RENDER_LOOKUP = {
    "main.html": "html_safe_render",
    "main.md": "markdown_render",
    "main.txt": "txt_render",
    "main.enc": "encrypted_file_render",
}


# TODO: Fix path traversal vulnerability
# TODO: Separate generic download and download with MIME type detection
@xframe_options_exempt
def serve_node_file(request, node_path, file_name):
    file_path_full = os.path.join(settings.PAGES_BASE_DIR, node_path, file_name)

    if not os.path.exists(file_path_full):
        raise Http404("File not found")

    mime_type, _ = mimetypes.guess_type(file_path_full)
    mime_type = mime_type or "application/octet-stream"

    response = FileResponse(open(file_path_full, "rb"), content_type=mime_type)

    response["X-Frame-Options"] = "SAMEORIGIN"

    return response


# TODO: Fix CSRF
@csrf_exempt
def render_node_with_query_handling(request, node_path=""):
    file_name = request.GET.get("file")
    if request.method == "POST":
        return editable_context_view(request, node_path)
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET", "POST"])
    if file_name:
        return serve_node_file(request, node_path, file_name)
    return render_node(request, node_path)
