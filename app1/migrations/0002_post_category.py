# Generated by Django 3.0.3 on 2020-05-06 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('travel blogs', 'Travel Blogs'), ('movie blogs', 'Movie Blogs'), ('food blogs', 'Food Blogs'), ('other', 'Other')], default='other', max_length=30),
        ),
    ]
