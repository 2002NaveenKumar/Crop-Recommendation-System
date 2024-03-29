# Generated by Django 3.2.19 on 2023-06-11 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_delete_customuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nitrogen', models.CharField(max_length=255)),
                ('phosphorus', models.CharField(max_length=255)),
                ('potassium', models.CharField(max_length=255)),
                ('temperature', models.CharField(max_length=255)),
                ('humidity', models.CharField(max_length=255)),
                ('ph', models.CharField(max_length=255)),
                ('rainfall', models.CharField(max_length=255)),
                ('result', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
        ),
    ]
