# Generated by Django 2.2.12 on 2020-06-02 09:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0023_auto_20200601_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='fournisseur',
            name='nom_pharmacie',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='website.Pharmcie'),
        ),
    ]
