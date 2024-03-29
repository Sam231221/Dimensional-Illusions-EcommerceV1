# Generated by Django 4.0.3 on 2022-03-20 23:08

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountCoupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discountcode', models.CharField(help_text='For example:- sam3432', max_length=100, null=True)),
                ('discount', models.PositiveIntegerField(help_text='You can set discount from 1 to 90 %. Set the disount wisely.Note,DI do not accept decimal value.', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(90)], verbose_name='Discount in %')),
                ('made_on', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=13)),
                ('email', models.EmailField(max_length=100)),
                ('title', models.TextField(null=True)),
                ('content', models.TextField(null=True)),
                ('timeStamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.SlugField(max_length=10, null=True)),
                ('second_name', models.CharField(max_length=10, null=True)),
                ('email', models.EmailField(blank=True, max_length=140, null=True)),
                ('image', models.ImageField(blank=True, help_text='This will be uploaded as your profile picture. Only .png and .jpg are accepted', null=True, upload_to='thumbnails/profile/%y', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg'])])),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=50, null=True)),
                ('esewa_id', models.PositiveIntegerField(blank=True, help_text='This information will be used only for payment purpose.', null=True, validators=[django.core.validators.MinValueValidator(9000000000), django.core.validators.MaxValueValidator(9999999999)])),
                ('date_joined', models.DateTimeField(auto_now_add=True, null=True)),
                ('auth_token', models.CharField(max_length=100, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('username', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SetDiscount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('discount', models.PositiveIntegerField(help_text='You can set discount from 1 to 90 %. Set the disount wisely.Note,DI do not accept decimal value.', null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(90)], verbose_name='Discount in %')),
            ],
        ),
        migrations.CreateModel(
            name='PurchasedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_purchased', models.DateTimeField(auto_now_add=True, null=True)),
                ('complete', models.BooleanField(default=False, null=True)),
                ('transaction_id', models.CharField(max_length=200, null=True)),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Ehub.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ordered', models.DateTimeField(auto_now_add=True, null=True)),
                ('complete', models.BooleanField(default=False, null=True)),
                ('transaction_id', models.CharField(max_length=200, null=True)),
                ('discountcoupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Ehub.discountcoupon')),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Ehub.profile')),
            ],
        ),
    ]
