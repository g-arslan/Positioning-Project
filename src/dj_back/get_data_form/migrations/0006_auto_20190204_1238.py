# Generated by Django 2.1.5 on 2019-02-04 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_data_form', '0005_auto_20190204_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='result_file',
            field=models.FileField(upload_to=''),
        ),
    ]
