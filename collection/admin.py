from django.contrib import admin
from .models import VehicleParkDispatch
# ---------------------------------------------------------------------------
# Area 8 — Admin Registration
# ---------------------------------------------------------------------------
# Register your models here.
@admin.register(VehicleParkDispatch)
class VehicleParkDispatchAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'booking_memo', 'vehicle_no', 'driver_name',
        'current_stop', 'next_stop', 'stop_sequence', 'status',
        'parked_at', 'unloading_completed_at', 'dispatched_at',
        'created_at',
    )
    list_filter = ('status', 'current_stop', 'vehicle_no')
    search_fields = ('booking_memo__memo_no', 'vehicle_no__vehical_number')
    ordering = ('booking_memo', 'stop_sequence')
    readonly_fields = ('created_at', 'updated_at')

