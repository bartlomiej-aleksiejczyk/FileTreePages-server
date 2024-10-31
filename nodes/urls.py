from django.urls import path
from .views.general_views import render_node_with_query_handling

# TODO: Add handling for absolute links.
urlpatterns = [
    path(
        "nodes/",
        render_node_with_query_handling,
        {"node_path": ""},
        name="render_root_node",
    ),
    path(
        "nodes/<path:node_path>/",
        render_node_with_query_handling,
        name="render_node",
    ),
]
