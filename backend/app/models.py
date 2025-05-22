from django.db import models
from django.contrib.auth.models import User  #imports django's built-in user model

#Ride Request model(Stores information about each ride request made in app)
class RideRequest(models.Model):
    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ride_requests') #defines field named rider in model 
    pickup_location = models.CharField(max_length=255) 
    dropoff_location = models.CharField(max_length=255)
    ride_time = models.DateTimeField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Ride from{self.pickup_location} to {self.dropoff_location}"
    
#Drive Profile Model
class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vehicle_type = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username}\n{self.vehicle_type}"
    
#Vehicle Model 
class Vehicle(models.Model):
    driver= models.OneToOneField(User, on_delete= models.CASCADE)
    vehicle_type= models.CharField(max_length=100)
    license_plate= models.CharField(max_length=20)

    def __str__(self):
        return f"{self.driver.username} - {self.vehicle_type}"
    

#Location Model
class Location(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name='locations')
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places= 6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.latitude}, {self.longitude})"
    
#User Profile model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True, blank =True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank= True)
    bio = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}\n{self.phone_number or 'No phone number'} "
    
#Ride Model(Information about ride taken by user)
class Ride(models.Model):
    ride_request=  models.OneToOneField(RideRequest, on_delete= models.CASCADE)
    driver = models.ForeignKey(DriverProfile, on_delete=models.CASCADE)
    rider = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_time = models.DateTimeField()
    dropoff_time = models.DateTimeField()
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    ride_time = models.DateTimeField()
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    fare = models.DecimalField(max_digits=10, decimal_places = 2, null = True, blank= True)
    
    #Rating choices (1 to 5)
    Rating_choices = [(i, str(i)) for i in range(1, 6)]
    rating = models.IntegerField(choices = Rating_choices, null= True, blank =True)

    feedback = models.TextField(null = True, blank = True)
    payment_method = models.CharField(max_length = 50, choices = [('cash', 'cash'),('credit_card','credit_card')])
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length = 20,
        choices=[
            ('pending', 'Pending'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('canceled', 'Canceled'),
            ('no_show', 'No Show'),
            ('driver_arrived', 'Driver Arrived'),
            ('on_trip', 'On Trip'),
            ('payment_pending', 'Payment Pending'),
            ('payment_completed', 'Payment Completed'),
            ('refunded', 'Refunded'),
            ('disputed', 'Disputed')
        ],
        default = 'pending'
    )


    def __str__(self):
        return f"Ride #{self.id} - {self.ride_request.rider.username} from {self.pickup_location} to {self.dropoff_location} - {self.status}"
    

#Send in-app notifications to users or dirvers
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE) #connects the notification to specific user 
    message = models.TextField() #stores notification message 
    created_at = models.DateTimeField(auto_now_add=True) #when notifictaion was created
    read = models.BooleanField(default=False)# Boolean tracks if notification was read or not

    def __str__(self):
        status = "Read" if self.read else "Unread"
        return f"Notification for {self.user.username} - {self.message} - {self.created_at} - {status}"


#Handle user complaint and support issues
class SupportTicket(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE) #connects ticket to user who submitted complaint
    subject= models.CharField(max_length = 100) #subject of ticket
    message = models.TextField() #message of ticket
    status = models.CharField(  # tracks ticket status 
        max_length = 50,
        choices = [
            ('open', 'Open'), 
            ('in_progress', 'In Progress'), 
            ('resolved', 'Resolved')
            ], 
            default = 'open'
    )
    created_at = models.DateTimeField(auto_now_add=True) # timesatmp when ticket was created 
    updated_at = models.DateTimeField(auto_now=True) #when ticket was last updated
    response = models.TextField(null=True, blank=True) #Response from support team
    response_at = models.DateTimeField(null=True, blank=True) #When response was provided

    #Readable summarising the ticket
    def __str__(self):
        return f"Ticket #{self.id} - {self.subject} - {self.status}"
    
#Allows users see frequent destinations
class SavedLocation(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE) #connects saved loctaion to specific user
    label = models.CharField(max_length=100) #sshort label for location
    address = models. CharField(max_length=255) # full address of saved location
    latitude = models.DecimalField(max_digits=9, decimal_places=6) #latitude coordinate
    longitude = models.DecimalField(max_digits=9, decimal_places=6) #longitude coordinate

    #Readable message with label and address
    def __str__(self):
        return f"{self.label}: {self.address}"

#Manage when drivers are online or offline
class DriverAvailability(models.Model):
    driver = models.OneToOneField(DriverProfile, on_delete = models.CASCADE) #connects availability status to specific driver
    is_available = models.BooleanField(default=True)  #Boolean value to chech driver is online or not 
    last_updated= models.DateTimeField(auto_now=True) #Auto updates with surrent time stamps when driver changes

    #string showing driver name and availability status
    def __str__(self):
        return f"{self.driver.user.username} - {'Available' if self.is_available else 'Unavailable'}"