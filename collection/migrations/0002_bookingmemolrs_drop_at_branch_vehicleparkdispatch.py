# Migration: Add drop_at_branch to BookingMemoLRs + create VehicleParkDispatch

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('branches', '0001_initial'),
        ('collection', '0001_initial'),
        ('lr_booking', '0001_initial'),
        ('vehicals', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Area 5 — Add drop_at_branch to BookingMemoLRs
        migrations.AddField(
            model_name='bookingmemolrs',
            name='drop_at_branch',
            field=models.ForeignKey(
                blank=True,
                help_text='Branch/stop where this LR cargo should be unloaded (leave blank for final destination)',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='booking_memo_lr_drop_branch',
                to='branches.branchmaster',
            ),
        ),

        # Area 2 — Create VehicleParkDispatch model
        migrations.CreateModel(
            name='VehicleParkDispatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stop_sequence', models.PositiveIntegerField(
                    default=1,
                    help_text='1-based sequence number of this stop within the route',
                )),
                ('status', models.CharField(
                    choices=[
                        ('IN_TRANSIT', 'In Transit'),
                        ('PARKED', 'Parked'),
                        ('UNLOADING', 'Unloading'),
                        ('DISPATCHED', 'Dispatched'),
                        ('COMPLETED', 'Completed'),
                    ],
                    default='IN_TRANSIT',
                    help_text='Current status of the vehicle at this stop',
                    max_length=20,
                )),
                ('parked_at', models.DateTimeField(
                    blank=True,
                    help_text='Timestamp when vehicle was marked as PARKED (arrived at this stop)',
                    null=True,
                )),
                ('unloading_completed_at', models.DateTimeField(
                    blank=True,
                    help_text='Timestamp when cargo unloading was marked complete at this stop',
                    null=True,
                )),
                ('dispatched_at', models.DateTimeField(
                    blank=True,
                    help_text='Timestamp when vehicle was re-dispatched towards the next stop',
                    null=True,
                )),
                ('remark', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('flag', models.BooleanField(default=True)),
                ('booking_memo', models.ForeignKey(
                    help_text='The booking memo / trip this stop log belongs to',
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='park_dispatch_logs',
                    to='collection.bookingmemo',
                )),
                ('created_by', models.ForeignKey(
                    default=1,
                    on_delete=django.db.models.deletion.SET_DEFAULT,
                    related_name='vpd_created_by',
                    to=settings.AUTH_USER_MODEL,
                )),
                ('current_stop', models.ForeignKey(
                    help_text='The branch/stop where the vehicle currently is (or is heading to)',
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='park_dispatch_current_stop',
                    to='branches.branchmaster',
                )),
                ('driver_name', models.ForeignKey(
                    help_text='Driver on this trip',
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='park_dispatch_driver',
                    to='vehicals.drivermaster',
                )),
                ('lr_bookings_at_stop', models.ManyToManyField(
                    blank=True,
                    help_text='LR bookings to be unloaded at this stop',
                    related_name='park_dispatch_lr_stops',
                    to='lr_booking.lr_bokking',
                )),
                ('next_stop', models.ForeignKey(
                    blank=True,
                    help_text='The next planned stop after current_stop (null when this is the final stop)',
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='park_dispatch_next_stop',
                    to='branches.branchmaster',
                )),
                ('updated_by', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='vpd_updated_by',
                    to=settings.AUTH_USER_MODEL,
                )),
                ('vehicle_no', models.ForeignKey(
                    help_text='Vehicle on this trip',
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='park_dispatch_vehicle',
                    to='vehicals.vehicalmaster',
                )),
            ],
            options={
                'db_table': 'vehicle_park_dispatch',
                'ordering': ['booking_memo', 'stop_sequence'],
            },
        ),
    ]
