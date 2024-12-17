
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
