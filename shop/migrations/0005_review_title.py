# Generated by Django 5.1.2 on 2024-12-01 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_alter_review_unique_together_alter_review_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='title',
            field=models.CharField(default='No Way', max_length=200),
        ),
    ]