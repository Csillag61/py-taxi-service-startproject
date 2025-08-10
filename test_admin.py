"""
Admin Test Script for Taxi Service
This script tests the admin functionality for all models
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taxi_service.settings')
django.setup()

from django.contrib.admin.sites import site
from taxi.models import Driver, Manufacturer, Car
from taxi.admin import DriverAdmin, ManufacturerAdmin, CarAdmin

def test_admin_registration():
    """Test that all models are registered in admin"""
    print("=== Testing Admin Registration ===")
    
    # Check if models are registered
    registered_models = site._registry
    
    assert Driver in registered_models, "Driver model not registered in admin"
    assert Manufacturer in registered_models, "Manufacturer model not registered in admin"  
    assert Car in registered_models, "Car model not registered in admin"
    
    print("✅ All models are registered in admin")
    
    # Check admin classes
    assert isinstance(registered_models[Driver], DriverAdmin), "Driver admin class incorrect"
    assert isinstance(registered_models[Manufacturer], ManufacturerAdmin), "Manufacturer admin class incorrect"
    assert isinstance(registered_models[Car], CarAdmin), "Car admin class incorrect"
    
    print("✅ All admin classes are correctly configured")

def test_driver_admin_config():
    """Test Driver admin configuration"""
    print("\n=== Testing Driver Admin Configuration ===")
    
    admin_class = site._registry[Driver]
    
    # Test list_display includes license_number
    list_display = list(admin_class.list_display)
    assert "license_number" in list_display, "license_number not in list_display"
    print("✅ license_number is displayed in Driver list view")
    
    # Test fieldsets includes license_number
    fieldsets = admin_class.fieldsets
    found_license_in_fieldsets = False
    for name, options in fieldsets:
        if name == "Additional info" and "license_number" in options.get("fields", []):
            found_license_in_fieldsets = True
            break
    assert found_license_in_fieldsets, "license_number not found in fieldsets"
    print("✅ license_number is in fieldsets under 'Additional info'")
    
    # Test add_fieldsets includes license_number (only for UserAdmin)
    add_fieldsets = getattr(admin_class, 'add_fieldsets', None)
    if add_fieldsets is not None:
        found_license_in_add_fieldsets = False
        for name, options in add_fieldsets:
            if name == "Additional info" and "license_number" in options.get("fields", []):
                found_license_in_add_fieldsets = True
                break
        assert found_license_in_add_fieldsets, "license_number not found in add_fieldsets"
        print("✅ license_number is in add_fieldsets under 'Additional info'")

def test_car_admin_config():
    """Test Car admin configuration"""
    print("\n=== Testing Car Admin Configuration ===")
    
    admin_class = site._registry[Car]
    
    # Test search by model
    search_fields = admin_class.search_fields
    assert "model" in search_fields, "model not in search_fields"
    print("✅ Car admin allows search by model")
    
    # Test filter by manufacturer
    list_filter = admin_class.list_filter
    assert "manufacturer" in list_filter, "manufacturer not in list_filter"
    print("✅ Car admin allows filter by manufacturer")
    
    # Test filter_horizontal for drivers
    filter_horizontal = admin_class.filter_horizontal
    assert "drivers" in filter_horizontal, "drivers not in filter_horizontal"
    print("✅ Car admin has horizontal filter for drivers")

def test_manufacturer_admin_config():
    """Test Manufacturer admin configuration"""
    print("\n=== Testing Manufacturer Admin Configuration ===")
    
    admin_class = site._registry[Manufacturer]
    
    # Test list_display
    list_display = admin_class.list_display
    assert "name" in list_display, "name not in list_display"
    assert "country" in list_display, "country not in list_display"
    print("✅ Manufacturer admin displays name and country")
    
    # Test search functionality
    search_fields = admin_class.search_fields
    assert "name" in search_fields, "name not in search_fields"
    print("✅ Manufacturer admin allows search by name")

def create_test_data():
    """Create some test data to verify admin functionality"""
    print("\n=== Creating Test Data ===")
    
    # Create manufacturer
    manufacturer, created = Manufacturer.objects.get_or_create(
        name="Toyota",
        defaults={"country": "Japan"}
    )
    if created:
        print("✅ Created test manufacturer: Toyota")
    else:
        print("✅ Test manufacturer already exists: Toyota")
    
    # Create driver
    driver, created = Driver.objects.get_or_create(
        username="test_driver",
        defaults={
            "first_name": "John",
            "last_name": "Doe", 
            "email": "john@example.com",
            "license_number": "ABC123"
        }
    )
    if created:
        print("✅ Created test driver: test_driver")
    else:
        print("✅ Test driver already exists: test_driver")
    
    # Create car
    car, created = Car.objects.get_or_create(
        model="Camry",
        manufacturer=manufacturer,
    )
    if created:
        car.drivers.add(driver)
        print("✅ Created test car: Toyota Camry")
    else:
        print("✅ Test car already exists: Toyota Camry")

def main():
    """Run all admin tests"""
    print("🚗 TAXI SERVICE ADMIN TESTING 🚗\n")
    
    try:
        test_admin_registration()
        test_driver_admin_config()
        test_car_admin_config()
        test_manufacturer_admin_config()
        create_test_data()
        
        print("\n🎉 ALL ADMIN TESTS PASSED! 🎉")
        print("\nYou can now:")
        print("1. Visit http://127.0.0.1:8000/admin/")
        print("2. Log in with your superuser credentials")
        print("3. Test all the admin features:")
        print("   - Create/edit Drivers with license numbers")
        print("   - Create/edit Manufacturers")
        print("   - Create/edit Cars with search and filter functionality")
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n💥 ERROR: {e}")

if __name__ == "__main__":
    main()
