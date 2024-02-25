# Generated by Django 5.0.2 on 2024-02-24 22:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_posts_post_liked'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='post_liked',
            field=models.ManyToManyField(blank=True, default=0, related_name='post_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]