from django.contrib import admin
from .models import FitnessClass, Booking

@admin.register(FitnessClass)
class FitnessClassAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'date_time', 'instructor', 'available_slots')
    search_fields = ('class_name', 'instructor')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_email', 'fitness_class')
    search_fields = ('client_name', 'client_email')
    list_filter = ('fitness_class',)
