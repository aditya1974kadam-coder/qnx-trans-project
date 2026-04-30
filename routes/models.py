from django.db import models
from django.contrib.auth import get_user_model
from branches.models import BranchMaster

User = get_user_model()

# RouteStations model
class RouteStations(models.Model):
    STOP_TYPE_INTERMEDIATE = 'INTERMEDIATE'
    STOP_TYPE_FINAL = 'FINAL'
    STOP_TYPE_CHOICES = [
        (STOP_TYPE_INTERMEDIATE, 'Intermediate'),
        (STOP_TYPE_FINAL, 'Final'),
    ]

    id = models.AutoField(primary_key=True)    
    route_station = models.ForeignKey(
        BranchMaster, related_name='route_stations_branch', on_delete=models.SET_NULL, null=True)
    km = models.FloatField(null=True, blank=True)
    # Sequence order of this stop within the route (1 = first intermediate stop, 2 = second, etc.)
    sequence_order = models.PositiveIntegerField(default=1, help_text="Order of this stop along the route (1-based)")
    # Whether this is an intermediate unloading point or the final destination
    stop_type = models.CharField(
        max_length=20, choices=STOP_TYPE_CHOICES, default=STOP_TYPE_INTERMEDIATE,
        help_text="INTERMEDIATE = part-load drop point; FINAL = terminal destination"
    )
    created_by = models.ForeignKey(
        User, on_delete=models.SET_DEFAULT, related_name='route_stations_created_by', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='route_stations_updated_by')
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    flag = models.BooleanField(default=True)

    class Meta:
        db_table = 'route_stations'
        ordering = ['sequence_order']

    def __str__(self):
        return f"{self.route_station} (seq={self.sequence_order}, {self.stop_type})"

# RouteMaster model
class RouteMaster(models.Model):
    id = models.AutoField(primary_key=True)
    route_name = models.CharField(max_length=255,unique=True)
    from_branch = models.ForeignKey(
        BranchMaster, related_name='route_stations_from_branch', on_delete=models.SET_NULL, null=True)
    to_branch = models.ForeignKey(
        BranchMaster, related_name='route_stations_to_branch', on_delete=models.SET_NULL, null=True)
    route_stations = models.ManyToManyField(
        'RouteStations', related_name='route_master_stations', blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_DEFAULT, related_name='route_master_created_by', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='route_master_updated_by')
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    flag = models.BooleanField(default=True)

    class Meta:
        db_table = 'route_master'

    def __str__(self):
        return f"{self.route_name}"


# SlapMaster model
class SlapMaster(models.Model):
    id = models.AutoField(primary_key=True)
    up_km = models.IntegerField(default=0)
    to_km = models.IntegerField(default=0)
    no_day = models.IntegerField(default=0)
    time = models.IntegerField(default=0)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_DEFAULT, related_name='slap_master_created_by', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='slap_master_updated_by')
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    flag = models.BooleanField(default=True)

    class Meta:
        db_table = 'slap_master'

    def __str__(self):
        return f"{self.id}"