import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barter_project.settings')
django.setup()

from django.contrib.auth.models import User
from properties.models import Property

# Get or create a test user
user = User.objects.filter(username='admin').first()
if not user:
    user = User.objects.create_superuser('admin', 'admin@barter.com', 'admin123')

# Sample properties data
properties_data = [
    {
        'title': 'Luxury Villa with Pool',
        'description': 'Beautiful luxury villa with swimming pool, garden, and modern amenities. Perfect for families.',
        'property_type': 'house',
        'status': 'available',
        'price': 750000,
        'area': 3500,
        'bedrooms': 4,
        'bathrooms': 3,
        'address': '123 Main Street',
        'city': 'New York',
        'state': 'NY',
        'zip_code': '10001',
    },
    {
        'title': 'Modern Downtown Apartment',
        'description': 'Stylish apartment in the heart of downtown. Close to restaurants, shops, and transit.',
        'property_type': 'apartment',
        'status': 'available',
        'price': 450000,
        'area': 1200,
        'bedrooms': 2,
        'bathrooms': 2,
        'address': '456 Center Ave',
        'city': 'New York',
        'state': 'NY',
        'zip_code': '10002',
    },
    {
        'title': 'Cozy Suburban Townhouse',
        'description': 'Perfect starter home in a quiet neighborhood. Recently renovated with new appliances.',
        'property_type': 'townhouse',
        'status': 'pending',
        'price': 350000,
        'area': 1800,
        'bedrooms': 3,
        'bathrooms': 2,
        'address': '789 Oak Lane',
        'city': 'Albany',
        'state': 'NY',
        'zip_code': '12201',
    },
]

# Create properties
for prop_data in properties_data:
    prop = Property.objects.create(owner=user, **prop_data)
    print(f"Created: {prop.title}")

print("Sample data added successfully!")