import os
from django import template

register = template.Library()


def contains_main_file(directory_path):
    """Check if the directory contains a main.* file, and handle PermissionError."""
    try:
        for file in os.listdir(directory_path):
            if file.startswith("main.") and os.path.isfile(
                os.path.join(directory_path, file)
            ):
                return True
    except PermissionError:
        # Skip directories we don't have permission to access
        return False
    return False


def traverse_directory(current_path, base_path):
    """Recursively build a nested dictionary representing the directory structure with links, handling PermissionError."""
    tree = {}
    try:
        with os.scandir(current_path) as it:
            for entry in it:
                if not entry.is_dir():
                    continue
                    # Check if the directory contains a main.* file
                if not contains_main_file(entry.path):
                    continue
                relative_path = os.path.relpath(entry.path, base_path)
                subdir_tree = traverse_directory(entry.path, base_path)
                tree[entry.name] = {
                    "type": "directory",
                    "path": relative_path,
                    "children": subdir_tree,
                }
    except PermissionError:
        # Skip directories we don't have permission to access
        return tree  # Return an empty tree for directories we can't access
    return tree


@register.inclusion_tag("partials/sidebar_navbar.html")
def build_sidebar_navbar(base_dir):
    """Build the sidebar tree structure starting from the provided base directory."""
    directory_tree = traverse_directory(base_dir, base_dir)

    return {
        "tree": {
            "Home": {
                "type": "root",
                "path": "",
                "children": directory_tree,
            }
        }
    }
