# Generated by Django 2.2 on 2019-05-07 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20190507_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=20170404100000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
