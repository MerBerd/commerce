# Generated by Django 3.2.7 on 2022-01-02 08:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Listings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(max_length=64)),
                ('Description', models.CharField(max_length=400)),
                ('StartPrice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('PostedTime', models.DateTimeField(auto_now_add=True)),
                ('Photo', models.URLField(blank=True, max_length=1000, null=True)),
                ('Active', models.BooleanField(default=True)),
                ('Author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to=settings.AUTH_USER_MODEL)),
                ('Category', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='auctions.category')),
                ('WatchedBy', models.ManyToManyField(blank=True, related_name='Watchlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Listings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Bids', to='auctions.listings')),
            ],
        ),
    ]
