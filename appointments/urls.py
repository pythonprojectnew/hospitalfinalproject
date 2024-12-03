from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register_patient/', views.register_patient, name='register_patient'),
    path('register_doctor/', views.register_doctor, name='register_doctor'),
    
    path('patient/profile/', views.patient_profile, name='patient_profile'),
    path('patient/edit/', views.edit_patient_profile, name='edit_patient_profile'),
    path('doctor/profile/', views.doctor_profile, name='doctor_profile'),
    path('doctor/edit/', views.edit_doctor_profile, name='edit_doctor_profile'),

    path('appointment/book/', views.book_appointment, name='book_appointment'),
    path('appointment/book/payment/<int:appointment_id>', views.appointment_payment, name='appointment_payment'),
    path('appointment/book/payment/cancel/', views.appointment_payment_cancel, name='appointment_payment_cancel'),
    path('appointment/<int:appointment_id>/prescribe/', views.prescribe_medication, name='prescribe_medication'),

    path('doctors/', views.doctors_list, name='doctors_list'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/appointment_completed/<int:appointment_id>/<int:patient_id>', views.appointment_completed, name='appointment_completed'),
    path('doctor/patient/<int:patient_id>/<int:appointment_id>', views.patient_detail, name='patient_detail'),
    path('doctor/patient/<int:patient_id>/<int:appointment_id>/update-medical-record/', views.update_medical_record, name='update_medical_record'),

    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('patient/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('patient/appointment/<int:appointment_id>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    path('patient/appointment/<int:appointment_id>/view_details/', views.view_details, name='view_details'),
    path('prescription_payment/<int:appointment_id>/', views.prescription_payment, name='prescription_payment'),
    path('patient/appointment/<int:appointment_id>/reschedule/', views.reschedule_appointment, name='reschedule_appointment'),

    path('appointments/', views.view_appointments, name='view_appointments'),
    path('appointments/add/', views.add_appointment, name='add_appointment'),
    path('appointments/edit/<int:id>/', views.edit_appointment, name='edit_appointment'),
    path('appointments/delete/<int:id>/', views.delete_appointment, name='delete_appointment'),
    
    path('admin_doctors/', views.view_doctors, name='view_doctors'),
    path('doctors/add/', views.add_doctor, name='add_doctor'),
    path('doctors/edit/<int:id>/', views.edit_doctor, name='edit_doctor'),
    path('doctors/delete/<int:id>/', views.delete_doctor, name='delete_doctor'),
    
    path('patients/', views.view_patients, name='view_patients'),
    path('patients/add/', views.add_patient, name='add_patient'),
    path('patients/edit/<int:id>/', views.edit_patient, name='edit_patient'),
    path('patients/delete/<int:id>/', views.delete_patient, name='delete_patient'),
]
