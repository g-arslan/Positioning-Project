# Generated by Django 2.1.5 on 2019-02-11 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('get_data_form', '0006_auto_20190204_1238'),
    ]

    operations = [
        migrations.RenameField(
            model_name='result',
            old_name='result_file',
            new_name='result_sol',
        ),
        migrations.AddField(
            model_name='result',
            name='stats_rtk',
            field=models.FileField(default=0, upload_to=''),
            preserve_default=False,
        ),
    ]