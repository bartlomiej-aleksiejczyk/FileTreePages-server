from django.urls import path
from . import views

# TODO: Add handling for absolute links.
urlpatterns = [
    path("nodes/", views.render_node, {"node_path": ""}, name="render_root_node"),
    path(
        "nodes/<path:node_path>/",
        views.render_node_with_query_handling,
        name="render_node",
    ),
]
