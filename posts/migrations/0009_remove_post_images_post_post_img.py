# Generated by Django 5.0.7 on 2024-07-20 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_image_post_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='images',
        ),
        migrations.AddField(
            model_name='post',
            name='post_img',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
