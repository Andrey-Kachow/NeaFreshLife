# Generated by Django 2.1.1 on 2019-01-23 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0010_auto_20181125_1848'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/food'),
        ),
    ]
