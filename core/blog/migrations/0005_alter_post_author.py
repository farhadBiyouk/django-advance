# Generated by Django 4.1.2 on 2022-10-26 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0005_user_groups_user_user_permissions"),
        ("blog", "0004_alter_post_author"),
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
