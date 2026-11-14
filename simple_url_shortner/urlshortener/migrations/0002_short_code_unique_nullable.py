from django.db import migrations, models


def empty_codes_to_null(apps, schema_editor):
    Url = apps.get_model("urlshortener", "Url")
    Url.objects.using(schema_editor.connection.alias).filter(short_code="").update(
        short_code=None
    )


def null_codes_to_empty(apps, schema_editor):
    Url = apps.get_model("urlshortener", "Url")
    Url.objects.using(schema_editor.connection.alias).filter(short_code__isnull=True).update(
        short_code=""
    )


class Migration(migrations.Migration):
    dependencies = [
        ("urlshortener", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="url",
            name="short_code",
            field=models.CharField(
                blank=True,
                db_index=True,
                max_length=20,
                null=True,
            ),
        ),
        migrations.RunPython(empty_codes_to_null, null_codes_to_empty),
        migrations.AlterField(
            model_name="url",
            name="short_code",
            field=models.CharField(
                blank=True,
                max_length=20,
                null=True,
                unique=True,
            ),
        ),
    ]
