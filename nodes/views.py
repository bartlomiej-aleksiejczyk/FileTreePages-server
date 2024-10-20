import os
import json
from copy import deepcopy
from django.http import HttpResponse, Http404
from django.shortcuts import render
import markdown
import nh3
from .models import Node

BASE_DIR = "information_system/"
DEFAULT_RENDERING_METHOD = "txt_render"


def html_safe_render(node_dir, node_path, request):
    # TODO: disable classless css here if using for page archive
    main_html_file = os.path.join(node_dir, "main.html")

    if os.path.exists(main_html_file):
        with open(main_html_file, "r") as file:
            html_content = file.read()
    else:
        raise Http404("Main HTML file not found")

    safe_html_content = nh3.clean(html_content)

    context = {"content": safe_html_content, "node_path": node_path}
    return render(request, "node_templates/html_node.html", context)


def markdown_render(node_dir, node_path, request):
    main_md_file = os.path.join(node_dir, "main.md")

    if os.path.exists(main_md_file):
        with open(main_md_file, "r") as file:
            markdown_content = file.read()
    else:
        raise Http404("Main markdown file not found")

    md = markdown.Markdown(extensions=["mdx_wikilink_plus"])
    html_content = md.convert(markdown_content)

    context = {"content": html_content, "node_path": node_path}
    return render(request, "node_templates/txt_node.html", context)


def txt_render(node_dir, node_path, request):
    main_txt_file = os.path.join(node_dir, "main.txt")
    if os.path.exists(main_txt_file):
        with open(main_txt_file, "r") as file:
            markdown_content = file.read()
    else:
        raise Http404("Main txt file not found")

    context = {"content": markdown_content, "node_path": node_path}
    return render(request, "node_templates/txt_node.html", context)


RENDERING_METHODS = {
    "markdown_render": markdown_render,
    "txt_render": txt_render,
    "html_safe_render": html_safe_render,
}


def render_node(request, node_path):
    node_dir = os.path.join(BASE_DIR, node_path)
    metadata_file = os.path.join(node_dir, "metadata.json")

    if not os.path.isdir(node_dir):
        raise Http404("Node not found")

    if os.path.exists(metadata_file):
        with open(metadata_file, "r") as file:
            metadata = json.load(file)
            rendering_method_name = metadata.get(
                "rendering_method", DEFAULT_RENDERING_METHOD
            )
    else:
        rendering_method_name = DEFAULT_RENDERING_METHOD
    rendering_method = RENDERING_METHODS[rendering_method_name]

    return rendering_method(node_dir, node_path, request)
