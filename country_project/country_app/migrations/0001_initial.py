# Generated by Django 5.0 on 2023-12-29 03:56

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='customuser_groups', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='customuser_user_permissions', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('country_code', models.CharField(max_length=255, unique=True)),
                ('curr_symbol', models.CharField(max_length=255, unique=True)),
                ('phone_code', models.CharField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('my_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Country_CustomUser', to='country_app.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('state_code', models.CharField(max_length=255)),
                ('gst_code', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='country_app.country')),
            ],
            options={
                'unique_together': {('name', 'country')},
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('city_code', models.CharField(max_length=255)),
                ('phone_code', models.CharField(max_length=255)),
                ('population', models.IntegerField(default=0)),
                ('avg_age', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('num_of_adult_males', models.IntegerField(default=0)),
                ('num_of_adult_females', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='country_app.state')),
            ],
            options={
                'unique_together': {('name', 'city_code', 'state')},
            },
        ),
    ]