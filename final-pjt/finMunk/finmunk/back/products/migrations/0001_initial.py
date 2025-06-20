# Generated by Django 4.2.21 on 2025-05-21 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DepositProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=50)),
                ('product_name', models.CharField(max_length=100)),
                ('join_way', models.TextField()),
                ('maturity_type', models.TextField(blank=True, null=True)),
                ('join_deny', models.CharField(max_length=10)),
                ('max_limit', models.CharField(blank=True, max_length=50, null=True)),
                ('save_term', models.CharField(max_length=10)),
                ('interest_rate', models.FloatField()),
                ('interest_rate2', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_type', models.CharField(max_length=10)),
                ('product_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MetalPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metal_type', models.CharField(choices=[('gold', 'Gold'), ('silver', 'Silver')], max_length=10)),
                ('date', models.DateField()),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SavingProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=50)),
                ('product_name', models.CharField(max_length=100)),
                ('join_way', models.TextField()),
                ('maturity_type', models.TextField(blank=True, null=True)),
                ('join_deny', models.CharField(max_length=10)),
                ('max_limit', models.CharField(blank=True, max_length=50, null=True)),
                ('save_term', models.CharField(max_length=10)),
                ('interest_rate', models.FloatField()),
                ('interest_rate2', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
