# Generated by Django 5.0.2 on 2024-03-16 13:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0002_extra_booking_mealreservation'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='BreakdownChart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('base_meal_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_extras_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BreakdownChartExtra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('breakdown_chart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extras', to='students.breakdownchart')),
                ('extra_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='students.extraitem')),
            ],
        ),
    ]