# Generated by Django 4.1.2 on 2022-10-26 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_user_groups_user_user_permissions"),
        ("blog", "0002_alter_post_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="accounts.profile"
            ),
        ),
    ]
