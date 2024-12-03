from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Patient, Appointment, Billing, Prescription, Doctor

class AppointmentBookingForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'problems_facing', 'appointment_date']
        
    appointment_date = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'datetime-local'}))

class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['amount']

class MedicalHistoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['medical_history']

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medications', 'notes']

    medications = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

class RescheduleAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date']

    appointment_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={
        'type': 'datetime-local',  # For browsers that support datetime-local input
    }))

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'

class DoctorForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, label="Username")
    first_name = forms.CharField(max_length=150, required=True, label="First Name")
    last_name = forms.CharField(max_length=150, required=True, label="Last Name")
    email = forms.EmailField(required=True, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")

    class Meta:
        model = Doctor
        exclude = ['user']

class DoctorEditForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=False, label="Username")
    first_name = forms.CharField(max_length=150, required=False, label="First Name")
    last_name = forms.CharField(max_length=150, required=False, label="Last Name")
    email = forms.EmailField(required=False, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, required=False, label="Password")

    class Meta:
        model = Doctor
        exclude = ['user']

class PatientForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, label="Username")
    first_name = forms.CharField(max_length=150, required=True, label="First Name")
    last_name = forms.CharField(max_length=150, required=True, label="Last Name")
    email = forms.EmailField(required=True, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Password")

    class Meta:
        model = Patient
        exclude = ['user']

class PatientEditForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=False, label="Username")
    first_name = forms.CharField(max_length=150, required=False, label="First Name")
    last_name = forms.CharField(max_length=150, required=False, label="Last Name")
    email = forms.EmailField(required=False, label="Email")
    password = forms.CharField(widget=forms.PasswordInput, required=False, label="Password")

    class Meta:
        model = Patient
        exclude = ['user']
