# Generated by Django 2.2.12 on 2020-05-30 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_auto_20200529_2129'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicament',
            name='image',
        ),
        migrations.AddField(
            model_name='medicament',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='img', verbose_name='image'),
        ),
    ]
