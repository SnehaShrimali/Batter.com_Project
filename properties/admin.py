from django.contrib import admin
from .models import Property, Inquiry, Appointment, ApprovalRequest

class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'property_type', 'status', 'price', 'city', 'owner', 'created_at']
    list_filter = ['status', 'property_type', 'city']
    search_fields = ['title', 'description', 'city', 'address']
    prepopulated_fields = {'slug': ['title']}
    date_hierarchy = 'created_at'

class InquiryAdmin(admin.ModelAdmin):
    list_display = ['property', 'name', 'email', 'phone', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'message']

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['property', 'user', 'appointment_date', 'payment_method', 'created_at']
    list_filter = ['payment_method', 'appointment_date']
    search_fields = ['property__title', 'user__username']
    date_hierarchy = 'appointment_date'

class ApprovalRequestAdmin(admin.ModelAdmin):
    list_display = ['subject', 'user', 'request_type', 'status', 'created_at', 'reviewed_by']
    list_filter = ['status', 'request_type', 'created_at']
    search_fields = ['subject', 'description', 'user__username']
    date_hierarchy = 'created_at'

admin.site.register(Property, PropertyAdmin)
admin.site.register(Inquiry, InquiryAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(ApprovalRequest, ApprovalRequestAdmin)
