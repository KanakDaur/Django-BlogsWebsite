# Generated by Django 3.0.3 on 2020-05-30 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0020_auto_20200530_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.FileField(default='media/def.jpeg', upload_to='images/'),
        ),
    ]