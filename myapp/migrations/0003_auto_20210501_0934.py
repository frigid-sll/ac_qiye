# Generated by Django 3.2 on 2021-05-01 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_content_seq'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=50, verbose_name='客户姓名'),
        ),
        migrations.AlterField(
            model_name='health',
            name='name',
            field=models.CharField(max_length=50, verbose_name='健康师姓名'),
        ),
    ]