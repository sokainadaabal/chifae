# Generated by Django 2.2.12 on 2020-05-30 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0019_auto_20200530_0717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
