from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.FileField(upload_to='patient_profile/', null=True, blank=True)
    phone_number = models.CharField(max_length=250)
    age = models.IntegerField(null=True, blank=True)
    dob = models.CharField(max_length=250, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    # is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}'

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.FileField(upload_to='doctor_profile/', null=True, blank=True)
    phone_number = models.CharField(max_length=250)
    address = models.TextField(blank=True, null=True)
    specialization = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.user.username}'    

# Appointment Model
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    problems_facing = models.TextField(blank=True, null=True)
    appointment_date = models.DateTimeField()
    is_approved = models.BooleanField(default=False)
    status = models.CharField(max_length=30, choices=(('Cancelled', 'Cancelled'), ('Pending', 'Pending'), ('Rescheduled', 'Rescheduled'), ('Confirmed', 'Confirmed'), ('Completed', 'Completed')))
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=500)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f'Appointment of {self.patient.user.username} with {self.doctor.user.username} on {self.appointment_date}'

class Prescription(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    medications = models.TextField(blank=True, null=True)
    prescribed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f'Prescription for {self.patient.user.username} by {self.doctor.user.username} on {self.prescribed_at}'


# Billing Model
class Billing(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Billing for {self.patient.user.username}'

