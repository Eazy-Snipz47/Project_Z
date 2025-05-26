from django.contrib import admin
from .models import(
    RideRequest, 
    DriverProfile, 
    Vehicle, 
    Location, 
    UserProfile,
    Ride,
    Notification,
    SupportTicket,
    SavedLocation,
    DriverAvailability
)

admin.site.register(RideRequest)
admin.site.register(DriverProfile)
admin.site.register(Vehicle)
admin.site.register(Location)
admin.site.register(UserProfile)
admin.site.register(Ride)
admin.site.register(Notification)
admin.site.register(SupportTicket)
admin.site.register(SavedLocation)
admin.site.register(DriverAvailability)

# Register your models here.
