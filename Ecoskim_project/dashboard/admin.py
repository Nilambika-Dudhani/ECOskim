from django.contrib import admin
from .models import WasteDetection


@admin.register(WasteDetection)
class WasteDetectionAdmin(admin.ModelAdmin):

    list_display = (
        'waste_name',
        'waste_type',
        'confidence',
        'classification',
        'detected_at',
    )

    list_filter = (
        'waste_type',
        'classification',
    )

    search_fields = (
        'waste_name',
        'waste_type',
        'classification',
    )

    ordering = (
        '-detected_at',
    )