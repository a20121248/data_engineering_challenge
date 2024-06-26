# Generated by Django 3.2.25 on 2024-04-17 00:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_department'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('hire_datetime', models.DateTimeField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.department')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.job')),
            ],
        ),
    ]
