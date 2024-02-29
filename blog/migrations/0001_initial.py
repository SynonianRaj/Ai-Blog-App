# Generated by Django 5.0.2 on 2024-02-29 19:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('post_id', models.AutoField(primary_key=True, serialize=False)),
                ('post_title', models.CharField(max_length=100)),
                ('post_content', models.TextField()),
                ('post_keywords', models.CharField(max_length=255)),
                ('post_meta_tag', models.CharField(max_length=255)),
                ('img_src', models.URLField(blank=True, null=True)),
                ('img_alt', models.CharField(blank=True, max_length=255, null=True)),
                ('pub_date', models.DateTimeField()),
                ('author', models.CharField(max_length=100)),
                ('post_liked', models.ManyToManyField(blank=True, default=[0], related_name='post_likes', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
