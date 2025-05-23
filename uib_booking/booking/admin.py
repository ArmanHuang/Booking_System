from django.contrib import admin 
from django.shortcuts import get_object_or_404
from django.utils.html import format_html
from django.conf import settings
from .models import MeetingRoom, Booking
from django.urls import reverse


admin.site.site_header = "Dashboard Admin UIB"
admin.site.site_title = "Admin UIB"
admin.site.index_title = "Selamat Datang di Admin UIB"


@admin.register(MeetingRoom)
class MeetingRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'capacity', 'is_active', 'image_preview', 'facilities')
    search_fields = ('name', 'location')  
    list_filter = ('is_active',)
    class Media:
        css = {
        'all': ('css/admin_custom.css',)
    }
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="width: 150px; height: 150px; object-fit: cover;" /></a>',
                obj.image.url,
                obj.image.url
            )
        fallback_image_url = settings.MEDIA_URL + 'default-image.jpg'
        return format_html(
            '<a href="{}" target="_blank"><img src="{}" style="width: 150px; height: 150px; object-fit: cover;" /></a>',
            fallback_image_url,
            fallback_image_url
        )
    image_preview.short_description = 'Image'


    def facilities(self, obj):
        if not obj.facilities:
            return "-"
        items = [f.strip() for f in obj.facilities.splitlines() if f.strip()]
        numbered = "<ol>" + "".join(f"<li>{item}</li>" for item in items) + "</ol>"
        return format_html(numbered)
    facilities.short_description = "Facilities"

   
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'user', 'date', 'start_time', 'end_time', 'status')
    list_filter = ('status', 'date')
    search_fields = ('room__name', 'user__username', 'purpose')
    
    class Media:
        css = {
        'all': ('css/admin_custom.css',)
    }
        
        
def change_view(self, request, object_id, form_url='', extra_context=None):
    booking = get_object_or_404(Booking, pk=object_id)
    if not extra_context:
        extra_context = {}
    extra_context['print_url'] = reverse('admin-booking-print', args=[booking.pk])
    extra_context['download_url'] = reverse('admin-booking-download', args=[booking.pk])
    return super().change_view(request, object_id, form_url, extra_context=extra_context)