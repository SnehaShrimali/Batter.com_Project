from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import timezone
from .forms import UserRegisterForm, PropertyForm, AppointmentForm
from .models import Property, Inquiry, Appointment, ApprovalRequest


def home(request):
    """Home page - public landing page"""
    properties = Property.objects.filter(status='available')[:6]
    return render(request, 'home.html', {'properties': properties})


def property_search(request):
    """Browse all available properties with search & filter"""
    properties = Property.objects.filter(status='available')
    property_types = Property.PROPERTY_TYPES

    search_query = request.GET.get('q', '')
    property_type = request.GET.get('type', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    city = request.GET.get('city', '')

    if search_query:
        properties = properties.filter(title__icontains=search_query) | \
                     properties.filter(description__icontains=search_query) | \
                     properties.filter(city__icontains=search_query)
    if property_type:
        properties = properties.filter(property_type=property_type)
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)
    if city:
        properties = properties.filter(city__icontains=city)

    cities = Property.objects.values_list('city', flat=True).distinct().order_by('city')

    return render(request, 'property_search.html', {
        'properties': properties,
        'property_types': property_types,
        'cities': cities,
        'search_query': search_query,
        'selected_type': property_type,
        'min_price': min_price,
        'max_price': max_price,
        'selected_city': city,
    })


@ensure_csrf_cookie
def login_view(request):
    """Login page"""
    if request.user.is_authenticated:
        return redirect('properties:dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('properties:dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


@ensure_csrf_cookie
def register_view(request):
    """Register page"""
    if request.user.is_authenticated:
        return redirect('properties:dashboard')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('properties:dashboard')
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})


@login_required
def dashboard(request):
    """Dashboard page - requires login"""
    user_properties = Property.objects.filter(owner=request.user)
    available_count = user_properties.filter(status='available').count()
    pending_count = user_properties.filter(status='pending').count()
    pending_approval_count = ApprovalRequest.objects.filter(user=request.user, status='pending').count()
    return render(request, 'dashboard.html', {
        'properties': user_properties,
        'property_count': user_properties.count(),
        'properties_available': available_count,
        'properties_pending': pending_count,
        'pending_approval_count': pending_approval_count,
    })


@login_required
def property_list(request):
    """List all properties for the current user"""
    properties = Property.objects.filter(owner=request.user)
    return render(request, 'property_list.html', {'properties': properties})


@login_required
def property_create(request):
    """Create a new property listing"""
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.save()
            messages.success(request, 'Property listed successfully!')
            return redirect('properties:property_detail', slug=property.slug)
    else:
        form = PropertyForm()

    return render(request, 'property_form.html', {'form': form, 'title': 'Add New Property'})


def property_detail(request, slug):
    """View individual property details"""
    property = get_object_or_404(Property, slug=slug)
    return render(request, 'property_detail.html', {'property': property})


@login_required
def property_update(request, slug):
    """Edit an existing property"""
    property = get_object_or_404(Property, slug=slug, owner=request.user)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated successfully!')
            return redirect('properties:property_detail', slug=property.slug)
    else:
        form = PropertyForm(instance=property)

    return render(request, 'property_form.html', {'form': form, 'title': 'Edit Property'})


@login_required
def property_delete(request, slug):
    """Delete a property"""
    property = get_object_or_404(Property, slug=slug, owner=request.user)
    if request.method == 'POST':
        property.delete()
        messages.success(request, 'Property deleted successfully!')
        return redirect('properties:property_list')
    return render(request, 'property_confirm_delete.html', {'property': property})


def custom_logout(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('properties:home')


@login_required
def book_appointment(request, slug):
    """Book a viewing appointment for a property"""
    property = get_object_or_404(Property, slug=slug)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.property = property
            appointment.user = request.user
            appointment.save()
            messages.success(request, f'Appointment booked for {property.title}!')
            return redirect('properties:my_appointments')
    else:
        form = AppointmentForm()
    return render(request, 'book_appointment.html', {'form': form, 'property': property})


@login_required
def my_appointments(request):
    """View user's booked appointments"""
    appointments = Appointment.objects.filter(user=request.user).order_by('appointment_date')
    return render(request, 'my_appointments.html', {'appointments': appointments})


# ====== ADMIN / MEDIATOR VIEWS ======

@staff_member_required
def admin_dashboard(request):
    """Admin/Mediator dashboard"""
    total_properties = Property.objects.count()
    pending_properties = Property.objects.filter(status='pending').count()
    available_properties = Property.objects.filter(status='available').count()
    total_users = User.objects.count()
    total_inquiries = Inquiry.objects.count()
    total_appointments = Appointment.objects.count()
    pending_approvals = ApprovalRequest.objects.filter(status='pending').count()
    recent_properties = Property.objects.order_by('-created_at')[:5]
    recent_inquiries = Inquiry.objects.order_by('-created_at')[:5]

    return render(request, 'admin_dashboard.html', {
        'total_properties': total_properties,
        'pending_properties': pending_properties,
        'available_properties': available_properties,
        'total_users': total_users,
        'total_inquiries': total_inquiries,
        'total_appointments': total_appointments,
        'pending_approvals': pending_approvals,
        'recent_properties': recent_properties,
        'recent_inquiries': recent_inquiries,
    })


@staff_member_required
def admin_property_list(request):
    """Admin: View all properties with CRUD"""
    status_filter = request.GET.get('status', '')
    properties = Property.objects.all().order_by('-created_at')
    if status_filter:
        properties = properties.filter(status=status_filter)
    return render(request, 'admin_property_list.html', {
        'properties': properties,
        'status_filter': status_filter,
    })


@staff_member_required
def admin_property_detail(request, pk):
    """Admin: View & manage single property"""
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Property.STATUS_CHOICES):
            property.status = new_status
            property.save()
            messages.success(request, f'Property status updated to {property.get_status_display()}')
        return redirect('properties:admin_property_detail', pk=property.pk)
    return render(request, 'admin_property_detail.html', {'property': property})


@staff_member_required
def admin_property_delete(request, pk):
    """Admin: Delete any property"""
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        property.delete()
        messages.success(request, 'Property deleted successfully!')
        return redirect('properties:admin_property_list')
    return render(request, 'admin_confirm_delete.html', {'obj': property, 'type': 'property'})


@staff_member_required
def admin_user_list(request):
    """Admin: View all users (sellers/buyers)"""
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_user_list.html', {'users': users})


@staff_member_required
def admin_user_delete(request, pk):
    """Admin: Delete a user"""
    user = get_object_or_404(User, pk=pk)
    if user == request.user:
        messages.error(request, 'You cannot delete yourself!')
        return redirect('properties:admin_user_list')
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User "{username}" deleted successfully!')
        return redirect('properties:admin_user_list')
    return render(request, 'admin_confirm_delete.html', {'obj': user, 'type': 'user'})


@staff_member_required
def admin_inquiry_list(request):
    """Admin: View all inquiries"""
    inquiries = Inquiry.objects.all().order_by('-created_at')
    return render(request, 'admin_inquiry_list.html', {'inquiries': inquiries})


@staff_member_required
def admin_inquiry_delete(request, pk):
    """Admin: Delete an inquiry"""
    inquiry = get_object_or_404(Inquiry, pk=pk)
    if request.method == 'POST':
        inquiry.delete()
        messages.success(request, 'Inquiry deleted successfully!')
        return redirect('properties:admin_inquiry_list')
    return render(request, 'admin_confirm_delete.html', {'obj': inquiry, 'type': 'inquiry'})


@staff_member_required
def admin_appointment_list(request):
    """Admin: View all appointments"""
    appointments = Appointment.objects.all().order_by('-appointment_date')
    return render(request, 'admin_appointment_list.html', {'appointments': appointments})


@staff_member_required
def admin_appointment_delete(request, pk):
    """Admin: Delete an appointment"""
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment deleted successfully!')
        return redirect('properties:admin_appointment_list')
    return render(request, 'admin_confirm_delete.html', {'obj': appointment, 'type': 'appointment'})


# ====== APPROVAL REQUEST VIEWS (USER SIDE) ======

@login_required
def approval_request_create(request):
    """User: Create a new approval request"""
    if request.method == 'POST':
        request_type = request.POST.get('request_type')
        subject = request.POST.get('subject')
        description = request.POST.get('description')

        if request_type and subject and description:
            ApprovalRequest.objects.create(
                user=request.user,
                request_type=request_type,
                subject=subject,
                description=description,
            )
            messages.success(request, 'Approval request submitted successfully!')
            return redirect('properties:my_approval_requests')
        else:
            messages.error(request, 'Please fill in all required fields.')

    return render(request, 'approval_request_form.html', {
        'request_types': ApprovalRequest.REQUEST_TYPES,
    })


@login_required
def my_approval_requests(request):
    """User: View my approval requests"""
    approval_requests = ApprovalRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_approval_requests.html', {'approval_requests': approval_requests})


# ====== APPROVAL REQUEST VIEWS (ADMIN SIDE) ======

@staff_member_required
def admin_approval_list(request):
    """Admin: View all approval requests"""
    status_filter = request.GET.get('status', '')
    approval_requests = ApprovalRequest.objects.all().order_by('-created_at')
    if status_filter:
        approval_requests = approval_requests.filter(status=status_filter)
    return render(request, 'admin_approval_list.html', {
        'approval_requests': approval_requests,
        'status_filter': status_filter,
    })


@staff_member_required
def admin_approval_action(request, pk):
    """Admin: Approve or reject an approval request"""
    approval_req = get_object_or_404(ApprovalRequest, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        admin_notes = request.POST.get('admin_notes', '')

        if action in ['approved', 'rejected']:
            approval_req.status = action
            approval_req.admin_notes = admin_notes
            approval_req.reviewed_by = request.user
            approval_req.reviewed_at = timezone.now()
            approval_req.save()
            status_display = 'approved' if action == 'approved' else 'rejected'
            messages.success(request, f'Approval request has been {status_display}!')
        return redirect('properties:admin_approval_list')
    return redirect('properties:admin_approval_list')
