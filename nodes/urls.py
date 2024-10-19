from django.urls import path
from . import views

urlpatterns = [
    path("nodes/", views.render_node, {"node_path": ""}, name="render_root_node"),
    path("nodes/<path:node_path>/", views.render_node, name="render_node"),
]
