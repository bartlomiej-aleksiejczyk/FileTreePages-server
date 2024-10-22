from django import template

register = template.Library()


@register.inclusion_tag("partials/breadcrumbs.html")
def build_breadcrumbs(node_path):
    path_parts = [part for part in node_path.split("/") if part]
    breadcrumbs = [
        {"name": part, "path": "/".join(path_parts[: i + 1])}
        for i, part in enumerate(path_parts)
    ]
    return {"breadcrumbs": breadcrumbs}
