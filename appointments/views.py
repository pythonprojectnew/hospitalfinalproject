from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from .models import Patient, Doctor, Appointment, Billing, Prescription
from django.contrib.auth.models import User
from .forms import (
    AppointmentBookingForm,
    AppointmentForm,
    DoctorEditForm,
    DoctorForm, 
    MedicalHistoryUpdateForm,
    PatientEditForm,
    PatientForm, 
    PrescriptionForm
)

# Patient Registration View
def register_patient(request):
    if request.method == 'POST':
        usern = request.POST['username']
        first = request.POST['firstname']
        last = request.POST['lastname']
        mail = request.POST['email']
        address = request.POST['address']
        profile_pic = request.POST.get('profile_pic')
        phone = request.POST['phone']
        med = request.POST['med']
        age = request.POST['age']  # Get age from the form
        gender = request.POST['gender'] 
        password = request.POST['password1']
        password1= request.POST['password2']
        if password == password1:
            if User.objects.filter(username=usern).exists():
                messages.error(request, "Username already taken")
                return redirect("register_patient")
            elif User.objects.filter(email=mail).exists():
                messages.error(request, "Email already registered")
                return redirect("register_patient")
            else:
                user=User.objects.create_user(username=usern, first_name=first, last_name=last, email=mail, password=password)
                user.save()
                patient = Patient(user=user, phone_number=phone, profile_pic=profile_pic, address=address, medical_history=med, age=age, gender=gender)
                patient.user=user
                patient.save()
                print("User saved")
                return redirect('login')
        else:
            messages.error(request, "Password doesn't match")
    return render(request, 'register_patient.html', {'page':'register'})

def register_doctor(request):
    if request.method == 'POST':
        usern = request.POST['username']
        first = request.POST['firstname']
        last = request.POST['lastname']
        mail = request.POST['email']
        profile_pic = request.POST.get('profile_pic')
        address = request.POST['address']
        phone = request.POST['phone']
        specialization = request.POST['specialization']
        password = request.POST['password1']
        password1= request.POST['password2']
        if password == password1:
            if User.objects.filter(username=usern).exists():
                messages.error(request, "Username already taken")
                return redirect("register_doctor")
            elif User.objects.filter(email=mail).exists():
                messages.error(request, "Email already registered")
                return redirect("register_doctor")
            else:
                user=User.objects.create_user(username=usern, first_name=first, last_name=last, email=mail, password=password, is_staff=True)
                user.save()
                doctor = Doctor(user=user, phone_number=phone, profile_pic=profile_pic, address=address, specialization=specialization)
                doctor.user=user
                doctor.save()
                print("User saved")
                return redirect('login')
        else:
            messages.error(request, "Password doesn't match")
    return render(request, 'register_doctor.html', {'page':'register'})

def patient_profile(request):
    current_user = request.user
    patient = Patient.objects.get(user=current_user)
    return render(request, 'patient_profile.html',{'patient':patient})

@login_required(login_url='login')
def edit_patient_profile(request):
    user = get_object_or_404(User, id=request.user.id)
    patient = get_object_or_404(Patient, user=user)
    if request.method == 'POST':
        form = PatientEditForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            # Update User fields if the patient is linked to a User
            if patient.user:
                user = patient.user
                user.username = form.cleaned_data.get('username', user.username)
                user.first_name = form.cleaned_data.get('first_name', user.first_name)
                user.last_name = form.cleaned_data.get('last_name', user.last_name)
                user.email = form.cleaned_data.get('email', user.email)

                # Update password if provided
                if form.cleaned_data.get('password'):
                    user.set_password(form.cleaned_data['password'])

                user.save()

            # Save the Patient model instance
            form.save(commit=False)  # Custom handling for User fields
            patient.save()

            messages.success(request, "Patient details updated successfully.")
            return redirect('patient_profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        # Prepopulate form with user-related fields
        initial_data = {
            'username': patient.user.username if patient.user else '',
            'first_name': patient.user.first_name if patient.user else '',
            'last_name': patient.user.last_name if patient.user else '',
            'email': patient.user.email if patient.user else '',
        }
        form = PatientEditForm(instance=patient, initial=initial_data)

    return render(request, 'edit_patient_profile.html', {'user': user, 'form': form})


def doctor_profile(request):
    current_user = request.user
    doctor = Doctor.objects.get(user=current_user)
    return render(request, 'doctor_profile.html',{'doctor':doctor})


def edit_doctor_profile(request):
    user = get_object_or_404(User, id=request.user.id)
    doctor = get_object_or_404(Doctor, user=user)

    if request.method == 'POST':
        form = DoctorEditForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            # Update User fields (if linked via a related model)
            if doctor.user:
                user = doctor.user
                user.username = form.cleaned_data.get('username', user.username)
                user.first_name = form.cleaned_data.get('first_name', user.first_name)
                user.last_name = form.cleaned_data.get('last_name', user.last_name)
                user.email = form.cleaned_data.get('email', user.email)
                
                if form.cleaned_data.get('password'):
                    user.set_password(form.cleaned_data['password'])

                user.save()

            # Update Doctor fields (if any additional data is being edited)
            form.save(commit=False)
            doctor.save()

            messages.success(request, "Doctor details updated successfully.")
            return redirect('doctor_profile')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        # Prepopulate form fields using the Doctor and related User model
        initial_data = {
            'username': doctor.user.username if doctor.user else '',
            'first_name': doctor.user.first_name if doctor.user else '',
            'last_name': doctor.user.last_name if doctor.user else '',
            'email': doctor.user.email if doctor.user else '',
        }
        form = DoctorEditForm(instance=doctor, initial=initial_data)

    return render(request, 'edit_doctor_profile.html', {'form': form, 'title': 'Edit Doctor'})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            if user.is_staff == True:
                if user.is_superuser == True:
                    auth.login(request, user)
                    return redirect('view_appointments')
                else:
                    auth.login(request, user)
                    return redirect('doctor_dashboard')
            else:
                auth.login(request, user)
                return redirect('patient_dashboard')
        else:
            messages.error(request, "Enter valid credentials")
            return redirect('login')
    return render(request, 'login.html', {'page':'login'})

def logout(request):
    auth.logout(request)
    return redirect('/')

def doctors_list(request):
    doctors = Doctor.objects.all()  # Fetch all registered doctors
    return render(request, 'doctors.html', {'doctors': doctors, 'page':'doctors'})

# Appointment Booking View (for Patients)
@login_required(login_url='login')
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient
            appointment.status = 'Pending'
            appointment.save()
            return redirect(f'/appointment/book/payment/{appointment.id}')
    else:
        form = AppointmentBookingForm()
    return render(request, 'book_appointment.html', {'form': form, 'page':'book'})

def appointment_payment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    if request.method == 'POST':
        appointment.payment_status = True
        appointment.save()
        return redirect('patient_dashboard')
    return render(request, 'appointment_payment.html', {'appointment':appointment})

def appointment_payment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    if request.method == 'POST':
        appointment.payment_status = True
        appointment.save()
        messages.success(request, "Payment has been completed and the appointment has been booked")
        return redirect('patient_dashboard')
    return render(request, 'appointment_payment.html', {'appointment':appointment})

def appointment_payment_cancel(request):
    messages.error(request, "Payment has been cancelled")
    return redirect('patient_dashboard')

def appointment_completed(request, appointment_id, patient_id):
    appointment = Appointment.objects.get(id=appointment_id)
    patient = Patient.objects.get(id=patient_id)
    if request.method == 'POST':
        appointment.status = 'Completed'
        appointment.save()
        Billing.objects.create(patient=patient, appointment=appointment)
        return redirect('doctor_dashboard')
    return redirect('patient_detail')

# Update Medical Record View
def update_medical_record(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    
    if request.method == 'POST':
        form = MedicalHistoryUpdateForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_detail', patient_id=patient.id)
    else:
        form = MedicalHistoryUpdateForm(instance=patient)
    
    return render(request, 'update_medical_record.html', {'form': form, 'patient': patient})

# Prescription (for Doctors)
def prescribe_medication(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.doctor = appointment.doctor
            prescription.patient = appointment.patient
            prescription.appointment = appointment
            prescription.save()
            return redirect('doctor_dashboard')
    else:
        form = PrescriptionForm()
    return render(request, 'prescribe_medication.html', {'form': form, 'appointment': appointment})

def doctor_dashboard(request):
    doctor = request.user.doctor
    pending_appointments = Appointment.objects.filter(
        doctor=doctor
    ).exclude(status__in=['Completed', 'Cancelled']).order_by('appointment_date')
    
    completed_appointments = Appointment.objects.filter(
        doctor=doctor, status='Completed'
    ).order_by('-appointment_date')

    return render(request, 'doctor_dashboard.html', {
        'pending_appointments': pending_appointments,
        'completed_appointments': completed_appointments,
        'page':'dashboard',
    })


# Patient Detail View (for Doctors)
def patient_detail(request, patient_id, appointment_id):
    # Retrieve the patient and the most recent appointment
    patient = get_object_or_404(Patient, id=patient_id)
    appointment = Appointment.objects.get(id=appointment_id)
    # prescriptions = Prescription.objects.filter(appointment=appointment)
    if appointment:
        prescriptions = Prescription.objects.filter(appointment=appointment)
    else:
        prescriptions = []
    print("Prescriptions fetched:", prescriptions)
    # Update Medical History
    if request.method == 'POST' and 'update_history' in request.POST:
        history_form = MedicalHistoryUpdateForm(request.POST, instance=patient)
        if history_form.is_valid():
            history_form.save()
            return redirect('patient_detail', patient_id=patient.id, appointment_id=appointment.id)
    else:
        history_form = MedicalHistoryUpdateForm(instance=patient)

    # Prescribe Medication
    if request.method == 'POST' and 'prescribe_medication' in request.POST:
        prescription_form = PrescriptionForm(request.POST)
        if prescription_form.is_valid():
            try:
                # Save the prescription
                prescription = prescription_form.save(commit=False)
                prescription.doctor = appointment.doctor
                prescription.patient = appointment.patient
                prescription.appointment = appointment
                prescription.save()
                return redirect('patient_detail', patient_id=patient.id, appointment_id=appointment.id)
            except Exception as e:
                # Print the exception in the console for debugging
                print("Error saving prescription:", str(e))
        else:
            print("Prescription form is not valid:", prescription_form.errors)
    else:
        prescription_form = PrescriptionForm()

    context = {
        'patient': patient,
        'prescriptions': prescriptions,
        'appointment': appointment,
        'history_form': history_form,
        'prescription_form': prescription_form,
    }
    return render(request, 'patient_detail.html', context)

def index(request):
    return render(request, 'index.html', {'page':'index'})

def patient_dashboard(request):
    patient = request.user.patient  # Assuming the logged-in user is a patient

    # Get patient's appointments and medical history
    appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')
    prescriptions = Prescription.objects.filter(patient=patient).order_by('-prescribed_at')

    return render(request, 'patient_dashboard.html', {
        'patient': patient,
        'appointments': appointments,
        'prescriptions': prescriptions,
    })

def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user.patient)
    
    # Only allow cancellation of pending appointments
    if appointment.status == 'Pending' or appointment.status == 'Rescheduled':
        appointment.status = 'Cancelled'
        appointment.save()
        messages.success(request, "Appointment canceled successfully.")
    else:
        messages.error(request, "You cannot cancel completed appointments.")

    return redirect('patient_dashboard')

# Reschedule Appointment View
def reschedule_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user.patient)

    if request.method == 'POST':
        # form = RescheduleAppointmentForm(request.POST, instance=appointment)
        date = request.POST['datetime']
        appointment.appointment_date = date
        appointment.status = 'Rescheduled'
        appointment.save()
        # if form.is_valid():
        #     form.save()
        return redirect('patient_dashboard')
    # else:
    #     form = RescheduleAppointmentForm(instance=appointment)

    return render(request, 'reschedule_appointment.html', {'appointment': appointment})

def view_details(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    prescription = Prescription.objects.filter(appointment=appointment).first()
    billing = Billing.objects.get(appointment=appointment)
    return render(request, 'view_detials.html', {'appointment':appointment, 'prescription':prescription, 'billing':billing})

def prescription_payment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    prescription = Prescription.objects.filter(appointment=appointment).first()
    if request.method == 'POST':
        prescription.total_cost=500
        prescription.payment_status=True
        prescription.save()
        total = int(prescription.appointment.consultation_fee) + int(prescription.total_cost)
        billing = Billing.objects.get(appointment=appointment)
        billing.amount = total
        billing.is_paid = True
        billing.save()
        return redirect('patient_dashboard')
    return render(request, 'prescription_payment.html', {'appointment':appointment})

# ---- Appointment Views ----

def view_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, 'admin_appointments.html', {'appointments': appointments})

def add_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_appointments')
    else:
        form = AppointmentForm()
    return render(request, 'form_template.html', {'form': form, 'title': 'Add Appointment'})

def edit_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('view_appointments')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'form_template.html', {'form': form, 'title': 'Edit Appointment'})

def delete_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    appointment.delete()
    return redirect('view_appointments')


# ---- Doctor Views ----

def view_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'admin_doctor.html', {'doctors': doctors})

def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new User
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password, is_staff=True)

            # Create a Doctor and link it to the User
            doctor = form.save(commit=False)
            doctor.user = user
            doctor.save()
            return redirect('view_doctors')
    else:
        form = DoctorForm()
    return render(request, 'form_template.html', {'form': form, 'title': 'Add Doctor'})

def edit_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)

    if request.method == 'POST':
        form = DoctorEditForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            # Update User fields (if linked via a related model)
            if doctor.user:
                user = doctor.user
                user.username = form.cleaned_data.get('username', user.username)
                user.first_name = form.cleaned_data.get('first_name', user.first_name)
                user.last_name = form.cleaned_data.get('last_name', user.last_name)
                user.email = form.cleaned_data.get('email', user.email)
                
                if form.cleaned_data.get('password'):
                    user.set_password(form.cleaned_data['password'])

                user.save()

            # Update Doctor fields (if any additional data is being edited)
            form.save(commit=False)
            doctor.save()

            messages.success(request, "Doctor details updated successfully.")
            return redirect('view_doctors')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        # Prepopulate form fields using the Doctor and related User model
        initial_data = {
            'username': doctor.user.username if doctor.user else '',
            'first_name': doctor.user.first_name if doctor.user else '',
            'last_name': doctor.user.last_name if doctor.user else '',
            'email': doctor.user.email if doctor.user else '',
        }
        form = DoctorEditForm(instance=doctor, initial=initial_data)

    return render(request, 'form_template.html', {'form': form, 'title': 'Edit Doctor'})

def delete_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    doctor.delete()
    return redirect('view_doctors')

# ---- Patient Views ----

def view_patients(request):
    patients = Patient.objects.all()
    return render(request, 'admin_patient.html', {'patients': patients})

def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a new User
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)

            # Create a Patient and link it to the User
            patient = form.save(commit=False)
            patient.user = user
            patient.save()
            return redirect('view_patients')
    else:
        form = PatientForm()
    return render(request, 'form_template.html', {'form': form, 'title': 'Add Patient'})

def edit_patient(request, id):
    patient = get_object_or_404(Patient, id=id)

    if request.method == 'POST':
        form = PatientEditForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            # Update User fields if the patient is linked to a User
            if patient.user:
                user = patient.user
                user.username = form.cleaned_data.get('username', user.username)
                user.first_name = form.cleaned_data.get('first_name', user.first_name)
                user.last_name = form.cleaned_data.get('last_name', user.last_name)
                user.email = form.cleaned_data.get('email', user.email)

                # Update password if provided
                if form.cleaned_data.get('password'):
                    user.set_password(form.cleaned_data['password'])

                user.save()

            # Save the Patient model instance
            form.save(commit=False)  # Custom handling for User fields
            patient.save()

            messages.success(request, "Patient details updated successfully.")
            return redirect('view_patients')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        # Prepopulate form with user-related fields
        initial_data = {
            'username': patient.user.username if patient.user else '',
            'first_name': patient.user.first_name if patient.user else '',
            'last_name': patient.user.last_name if patient.user else '',
            'email': patient.user.email if patient.user else '',
        }
        form = PatientEditForm(instance=patient, initial=initial_data)

    return render(request, 'form_template.html', {'form': form, 'title': 'Edit Patient'})

def delete_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    patient.delete()
    return redirect('view_patients')