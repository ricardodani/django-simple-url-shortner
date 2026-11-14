from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("urlshortener", "0002_short_code_unique_nullable"),
    ]

    operations = [
        migrations.AlterField(
            model_name="url",
            name="short_code",
            field=models.CharField(
                blank=True,
                max_length=22,
                null=True,
                unique=True,
            ),
        ),
    ]
