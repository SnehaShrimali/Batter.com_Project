"""
Forms for Barter.com Real Estate Marketplace
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Property, Inquiry, Appointment
import os


class PropertyForm(forms.ModelForm):
    """Form for creating and editing property listings"""

    class Meta:
        model = Property
        fields = ['title', 'description', 'property_type', 'status', 'price', 'area',
                  'bedrooms', 'bathrooms', 'address', 'city', 'state', 'zip_code', 'main_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Property Title'}),
            'property_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'area': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Area in sq ft'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Property Description'}),
            'main_image': forms.FileInput(attrs={'class': 'form-control'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Bedrooms'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Bathrooms'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zip Code'}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise forms.ValidationError('Price must be greater than zero')
        return price

    def clean_main_image(self):
        image = self.cleaned_data.get('main_image')
        if image:
            # Validate file size (5MB max)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Image file size must be under 5MB')
            # Validate file extension
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            ext = os.path.splitext(image.name)[1].lower()
            if ext not in allowed_extensions:
                raise forms.ValidationError('Only JPG, PNG, and GIF files are allowed')
        return image


class InquiryForm(forms.ModelForm):
    """Form for submitting property inquiries"""

    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone Number'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your Message'}),
        }


class AppointmentForm(forms.ModelForm):
    """Form for booking property viewing appointments"""

    class Meta:
        model = Appointment
        fields = ['appointment_date', 'payment_method', 'notes']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional Notes (Optional)'}),
        }

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data.get('appointment_date')
        if appointment_date:
            from django.utils import timezone
            if appointment_date < timezone.now():
                raise forms.ValidationError('Appointment date must be in the future')
        return appointment_date


class UserRegisterForm(UserCreationForm):
    """Form for user registration"""

    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help text from password fields
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        # Add Bootstrap classes
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})


class LoginForm(forms.Form):
    """Form for user login"""

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
