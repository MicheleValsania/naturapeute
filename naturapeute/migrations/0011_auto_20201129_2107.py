# Generated by Django 3.1.2 on 2020-11-29 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('naturapeute', '0010_auto_20201129_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='therapist',
            name='slug',
            field=models.SlugField(max_length=100, null=True, unique=True),
        ),
    ]