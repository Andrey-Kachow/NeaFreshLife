# Generated by Django 2.1.1 on 2018-11-20 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calc', '0003_auto_20181120_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='latest_inputs',
            name='calories',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='latest_inputs',
            name='weight',
            field=models.FloatField(null=True),
        ),
    ]
