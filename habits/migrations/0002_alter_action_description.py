# Generated by Django 4.2 on 2024-03-16 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("habits", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="action",
            name="description",
            field=models.TextField(
                blank=True, null=True, verbose_name="Описание привычки"
            ),
        ),
    ]