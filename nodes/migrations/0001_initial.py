# Generated by Django 5.0.6 on 2024-10-19 09:13

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('file_path', models.CharField(max_length=1024)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.IntegerField()),
                ('source_node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_links', to='nodes.node')),
                ('target_node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incoming_links', to='nodes.node')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=255)),
                ('intensity', models.IntegerField()),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='nodes.node')),
            ],
        ),
    ]
