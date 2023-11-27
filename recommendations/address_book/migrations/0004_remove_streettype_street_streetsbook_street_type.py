# Generated by Django 4.2.6 on 2023-11-26 15:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('address_book', '0003_remove_administrativedistrict_district_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='streettype',
            name='street',
        ),
        migrations.AddField(
            model_name='streetsbook',
            name='street_type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='address_book.streettype'),
        ),
    ]
