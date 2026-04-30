# Migration: Add sequence_order and stop_type to RouteStations

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0001_initial'),
    ]

    operations = [
        # Add stop_type field
        migrations.AddField(
            model_name='routestations',
            name='stop_type',
            field=models.CharField(
                choices=[('INTERMEDIATE', 'Intermediate'), ('FINAL', 'Final')],
                default='INTERMEDIATE',
                help_text='INTERMEDIATE = part-load drop point; FINAL = terminal destination',
                max_length=20,
            ),
        ),
        # Add sequence_order field
        migrations.AddField(
            model_name='routestations',
            name='sequence_order',
            field=models.PositiveIntegerField(
                default=1,
                help_text='Order of this stop along the route (1-based)',
            ),
        ),
        # Update Meta ordering
        migrations.AlterModelOptions(
            name='routestations',
            options={'db_table': 'route_stations', 'ordering': ['sequence_order']},
        ),
    ]
