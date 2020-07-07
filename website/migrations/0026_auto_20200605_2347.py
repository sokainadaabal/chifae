# Generated by Django 2.2.12 on 2020-06-05 23:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0025_medicament_nom_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_order', models.DateTimeField(auto_now_add=True)),
                ('complete', models.BooleanField(blank=True, default=False, null=True)),
                ('transaction_id', models.CharField(max_length=255, null=True)),
                ('pharmacien', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='medicament',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='img'),
        ),
        migrations.CreateModel(
            name='Vente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qte_vendre', models.IntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('medicament', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.Medicament')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.Order')),
            ],
        ),
    ]
