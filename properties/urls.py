from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.property_search, name='property_search'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.custom_logout, name='logout'),
    path('properties/', views.property_list, name='property_list'),
    path('properties/create/', views.property_create, name='property_create'),
    path('properties/<slug:slug>/', views.property_detail, name='property_detail'),
    path('properties/<slug:slug>/edit/', views.property_update, name='property_update'),
    path('properties/<slug:slug>/delete/', views.property_delete, name='property_delete'),
    path('appointments/', views.my_appointments, name='my_appointments'),
    path('properties/<slug:slug>/book/', views.book_appointment, name='book_appointment'),
    # Admin / Mediator URLs
    path('admin-area/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-area/properties/', views.admin_property_list, name='admin_property_list'),
    path('admin-area/properties/<int:pk>/', views.admin_property_detail, name='admin_property_detail'),
    path('admin-area/properties/<int:pk>/delete/', views.admin_property_delete, name='admin_property_delete'),
    path('admin-area/users/', views.admin_user_list, name='admin_user_list'),
    path('admin-area/users/<int:pk>/delete/', views.admin_user_delete, name='admin_user_delete'),
    path('admin-area/inquiries/', views.admin_inquiry_list, name='admin_inquiry_list'),
    path('admin-area/inquiries/<int:pk>/delete/', views.admin_inquiry_delete, name='admin_inquiry_delete'),
    path('admin-area/appointments/', views.admin_appointment_list, name='admin_appointment_list'),
    path('admin-area/appointments/<int:pk>/delete/', views.admin_appointment_delete, name='admin_appointment_delete'),
    path('approval-requests/', views.my_approval_requests, name='my_approval_requests'),
    path('approval-requests/create/', views.approval_request_create, name='approval_request_create'),
    path('admin-area/approvals/', views.admin_approval_list, name='admin_approval_list'),
    path('admin-area/approvals/<int:pk>/action/', views.admin_approval_action, name='admin_approval_action'),
]
