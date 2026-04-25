from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_chequecaseid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chequecaseid',
            name='status',
            field=models.CharField(
                choices=[
                    ('PENDING', 'PENDING'),
                    ('CLEARED', 'CLEARED'),
                    ('BOUNCED', 'BOUNCED'),
                ],
                default='PENDING',
                max_length=50,
            ),
        ),
    ]
