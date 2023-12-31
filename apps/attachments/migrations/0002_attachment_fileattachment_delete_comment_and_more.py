# Generated by Django 4.2.6 on 2023-11-17 11:34

import apps.attachments.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("contenttypes", "0002_remove_content_type_name"),
        ("attachments", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Attachment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("object_id", models.PositiveIntegerField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="FileAttachment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "title",
                    models.CharField(
                        blank=True,
                        help_text="Provide a title for the file. If you leave it blank, we will use the filename",
                        max_length=200,
                        null=True,
                        verbose_name="title",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="Provide a description of the file", null=True, verbose_name="description"
                    ),
                ),
                (
                    "file",
                    models.FileField(upload_to=apps.attachments.models.user_folder_item_path, verbose_name="file"),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("REQ", "Requirement"),
                            ("QUOT", "Quotation"),
                            ("JOB", "Job"),
                            ("INV", "Invoice"),
                            ("OTH", "Other"),
                        ],
                        default="OTH",
                        max_length=4,
                        verbose_name="type",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="files",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="owner",
                    ),
                ),
                (
                    "submitted_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="files_uploaded",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="submitted by",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.DeleteModel(
            name="Comment",
        ),
        migrations.AddField(
            model_name="attachment",
            name="attachment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="attachments.fileattachment", verbose_name="attachment"
            ),
        ),
        migrations.AddField(
            model_name="attachment",
            name="content_type",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="contenttypes.contenttype"),
        ),
    ]
