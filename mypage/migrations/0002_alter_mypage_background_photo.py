<<<<<<< HEAD
# Generated by Django 5.0.3 on 2024-11-22 12:40
=======
# Generated by Django 5.1.3 on 2024-11-22 12:29
>>>>>>> b6694999069083bced671a9e349698850c828de8

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mypage',
            name='background_photo',
            field=models.ImageField(upload_to='images/'),
        ),
    ]