from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="cover_static",
            field=models.CharField(
                blank=True,
                default="",
                max_length=200,
                verbose_name="Image statique (chemin dans /static/)",
            ),
        ),
    ]
