# Generated by Django 3.0.1 on 2020-01-19 04:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservas', '0004_auto_20200119_0324'),
    ]

    operations = [
        migrations.AddField(
            model_name='roombooking',
            name='booking_season',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to='reservas.BookingSeason'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='roombooking',
            name='booking_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]
