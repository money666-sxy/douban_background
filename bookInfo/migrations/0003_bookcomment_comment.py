# Generated by Django 3.0.3 on 2020-04-14 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookInfo', '0002_auto_20200414_1057'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookcomment',
            name='comment',
            field=models.TextField(null=True),
        ),
    ]