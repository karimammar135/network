# Generated by Django 4.1.3 on 2023-07-25 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_remove_post_likes_like'),
    ]

    operations = [
        migrations.RenameField(
            model_name='following',
            old_name='user',
            new_name='following',
        ),
    ]
