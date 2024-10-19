import uuid
from django.db import models


class Node(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):
    node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="tags")
    tag_name = models.CharField(max_length=255)
    intensity = models.IntegerField()

    def __str__(self):
        return f"{self.tag_name} ({self.intensity})"


class Link(models.Model):
    source_node = models.ForeignKey(
        Node, on_delete=models.CASCADE, related_name="outgoing_links"
    )
    target_node = models.ForeignKey(
        Node, on_delete=models.CASCADE, related_name="incoming_links"
    )
    weight = models.IntegerField()

    def __str__(self):
        return f"{self.source_node} -> {self.target_node} (Weight: {self.weight})"
