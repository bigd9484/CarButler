#!/usr/bin/env python3
"""
CarButler - Intelligent Car Maintenance Assistant
Main application entry point with CLI interface
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import random

# Mock imports for external services (will be replaced with actual implementations)
class MockGoogleCalendar:
    """Mock Google Calendar API for demonstration"""
    def create_event(self, title: str, date: datetime, duration: int = 60) -> str:
        return f"mock_event_{random.randint(1000, 9999)}"

class MockEmailService:
    """Mock SMTP email service for demonstration"""
    def send_email(self, to: str, subject: str, body: str) -> bool:
        print(f"\n📧 [MOCK EMAIL] To: {to}")
        print(f"Subject: {subject}")
        print(f"Body: {body[:100]}...")
        return True

class MockOBD2:
    """Mock OBD2 interface for demonstration"""
    def get_mileage(self) -> int:
        return random.randint(1000, 100000)
    
    def get_battery_voltage(self) -> float:
        return round(random.uniform(11.5, 14.5), 2)


class Vehicle:
    """Represents a vehicle with its properties and maintenance history"""
    
    def __init__(self, make: str, model: str, year: int, mileage: int, vin: Optional[str] = None):
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.vin = vin or f"MOCK{random.randint(10000, 99999)}"
        self.battery_voltage = 12.6  # Default healthy battery
        self.maintenance_history: List[Dict] = []
        self.last_oil_change = mileage - random.randint(1000, 4000)
        self.last_tire_rotation = mileage - random.randint(2000, 6000)
        self.last_air_filter = mileage - random.randint(10000, 20000)
        
    def to_dict(self) -> Dict:
        """Convert vehicle to dictionary for JSON storage"""
        return {
            'make': self.make,
            'model': self.model,
            'year': self.year,
            'mileage': self.mileage,
            'vin': self.vin,
            'battery_voltage': self.battery_voltage,
            'maintenance_history': self.maintenance_history,
            'last_oil_change': self.last_oil_change,
            'last_tire_rotation': self.last_tire_rotation,
            'last_air_filter': self.last_air_filter
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Vehicle':
        """Create vehicle from dictionary"""
        vehicle = cls(data['make'], data['model'], data['year'], data['mileage'], data.get('vin'))
        vehicle.battery_voltage = data.get('battery_voltage', 12.6)
        vehicle.maintenance_history = data.get('maintenance_history', [])
        vehicle.last_oil_change = data.get('last_oil_change', vehicle.mileage - 3000)
        vehicle.last_tire_rotation = data.get('last_tire_rotation', vehicle.mileage - 4000)
        vehicle.last_air_filter = data.get('last_air_filter', vehicle.mileage - 15000)
        return vehicle
    
    def __str__(self) -> str:
        return f"{self.year} {self.make} {self.model} ({self.mileage:,} miles)"


class MaintenanceSchedule:
    """Manages maintenance schedules and recommendations"""
    
    # Standard maintenance intervals (in miles)
    INTERVALS = {
        'oil_change': (5000, 7500),
        'tire_rotation': (5000, 8000),
        'air_filter': (15000, 30000),
        'brake_inspection': (20000, 20000),
        'coolant_flush': (30000, 30000),
        'transmission_service': (30000, 60000)
    }
    
    @staticmethod
    def check_maintenance_due(vehicle: Vehicle) -> List[Tuple[str, int, str]]:
        """
        Check which maintenance items are due or upcoming
        Returns: List of (service_name, miles_until_due, status)
        """
        due_items = []
        
        # Check oil change
        oil_interval = MaintenanceSchedule.INTERVALS['oil_change'][1]
        miles_since_oil = vehicle.mileage - vehicle.last_oil_change
        miles_until_oil = oil_interval - miles_since_oil
        
        if miles_until_oil <= 0:
            due_items.append(('Oil Change', 0, 'OVERDUE'))
        elif miles_until_oil <= 500:
            due_items.append(('Oil Change', miles_until_oil, 'DUE SOON'))
        elif miles_until_oil <= 1000:
            due_items.append(('Oil Change', miles_until_oil, 'UPCOMING'))
            
        # Check tire rotation
        tire_interval = MaintenanceSchedule.INTERVALS['tire_rotation'][1]
        miles_since_tire = vehicle.mileage - vehicle.last_tire_rotation
        miles_until_tire = tire_interval - miles_since_tire
        
        if miles_until_tire <= 0:
            due_items.append(('Tire Rotation', 0, 'OVERDUE'))
        elif miles_until_tire <= 500:
            due_items.append(('Tire Rotation', miles_until_tire, 'DUE SOON'))
        elif miles_until_tire <= 1000:
            due_items.append(('Tire Rotation', miles_until_tire, 'UPCOMING'))
            
        # Check air filter
        air_interval = MaintenanceSchedule.INTERVALS['air_filter'][1]
        miles_since_air = vehicle.mileage - vehicle.last_air_filter
        miles_until_air = air_interval - miles_since_air
        
        if miles_until_air <= 0:
            due_items.append(('Air Filter', 0, 'OVERDUE'))
        elif miles_until_air <= 2000:
            due_items.append(('Air Filter', miles_until_air, 'UPCOMING'))
            
        return due_items


class CarButler:
    """Main application class for CarButler"""
    
    def __init__(self):
        self.data_dir = 'data'
        self.vehicles_file = os.path.join(self.data_dir, 'vehicles.json')
        self.config_file = 'config.json'
        self.vehicles: List[Vehicle] = []
        self.current_vehicle: Optional[Vehicle] = None
        
        # Initialize mock services
        self.calendar = MockGoogleCalendar()
        self.email = MockEmailService()
        self.obd2 = MockOBD2()
        
        # Create data directory if it doesn't exist
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        # Load vehicles
        self.load_vehicles()
        
    def load_vehicles(self):
        """Load vehicles from JSON file"""
        if os.path.exists(self.vehicles_file):
            try:
                with open(self.vehicles_file, 'r') as f:
                    data = json.load(f)
                    self.vehicles = [Vehicle.from_dict(v) for v in data]
            except Exception as e:
                print(f"⚠️  Error loading vehicles: {e}")
                self.vehicles = []
    
    def save_vehicles(self):
        """Save vehicles to JSON file"""
        try:
            with open(self.vehicles_file, 'w') as f:
                data = [v.to_dict() for v in self.vehicles]
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Error saving vehicles: {e}")
    
    def add_vehicle(self):
        """Add a new vehicle"""
        print("\n🚗 Add New Vehicle")
        print("-" * 40)
        
        make = input("Enter make (e.g., Toyota): ").strip()
        model = input("Enter model (e.g., Camry): ").strip()
        
        while True:
            try:
                year = int(input("Enter year (e.g., 2020): ").strip())
                if 1900 <= year <= datetime.now().year + 1:
                    break
                else:
                    print("Please enter a valid year.")
            except ValueError:
                print("Please enter a valid year.")
        
        while True:
            try:
                mileage = int(input("Enter current mileage: ").strip())
                if mileage >= 0:
                    break
                else:
                    print("Mileage must be positive.")
            except ValueError:
                print("Please enter a valid number.")
        
        vehicle = Vehicle(make, model, year, mileage)
        self.vehicles.append(vehicle)
        self.save_vehicles()
        
        print(f"\n✅ Successfully added {vehicle}")
        input("\nPress Enter to continue...")
    
    def select_vehicle(self) -> Optional[Vehicle]:
        """Select a vehicle from the list"""
        if not self.vehicles:
            print("\n❌ No vehicles found. Please add a vehicle first.")
            return None
            
        print("\n🚗 Select Vehicle")
        print("-" * 40)
        
        for i, vehicle in enumerate(self.vehicles, 1):
            print(f"{i}. {vehicle}")
            
        while True:
            try:
                choice = int(input("\nSelect vehicle number: ").strip())
                if 1 <= choice <= len(self.vehicles):
                    return self.vehicles[choice - 1]
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Please enter a valid number.")
    
    def update_mileage(self):
        """Update vehicle mileage"""
        vehicle = self.select_vehicle()
        if not vehicle:
            return
            
        print(f"\n📏 Update Mileage for {vehicle}")
        print("-" * 40)
        print(f"Current mileage: {vehicle.mileage:,} miles")
        
        # Offer OBD2 option
        use_obd2 = input("\nUse OBD2 reader? (y/n) [n]: ").strip().lower() == 'y'
        
        if use_obd2:
            print("\n🔌 Reading from OBD2 (simulated)...")
            new_mileage = self.obd2.get_mileage()
            battery = self.obd2.get_battery_voltage()
            print(f"📊 OBD2 Data:")
            print(f"   Mileage: {new_mileage:,} miles")
            print(f"   Battery: {battery}V")
            
            confirm = input("\nAccept these readings? (y/n): ").strip().lower()
            if confirm == 'y':
                vehicle.mileage = new_mileage
                vehicle.battery_voltage = battery
            else:
                return
        else:
            while True:
                try:
                    new_mileage = int(input("Enter new mileage: ").strip())
                    if new_mileage >= vehicle.mileage:
                        vehicle.mileage = new_mileage
                        break
                    else:
                        print("New mileage must be greater than current mileage.")
                except ValueError:
                    print("Please enter a valid number.")
        
        self.save_vehicles()
        print(f"\n✅ Mileage updated to {vehicle.mileage:,} miles")
        
        # Check battery health
        if vehicle.battery_voltage < 12.0:
            print(f"\n⚠️  Warning: Battery voltage low ({vehicle.battery_voltage}V)")
        
        input("\nPress Enter to continue...")
    
    def check_maintenance(self):
        """Check maintenance schedule"""
        vehicle = self.select_vehicle()
        if not vehicle:
            return
            
        print(f"\n🔧 Maintenance Status for {vehicle}")
        print("-" * 40)
        
        due_items = MaintenanceSchedule.check_maintenance_due(vehicle)
        
        if not due_items:
            print("✅ All maintenance up to date!")
        else:
            for service, miles, status in due_items:
                if status == 'OVERDUE':
                    print(f"🔴 {service}: OVERDUE")
                elif status == 'DUE SOON':
                    print(f"🟡 {service}: Due in {miles:,} miles")
                else:
                    print(f"🟢 {service}: Due in {miles:,} miles")
        
        # Battery status
        print(f"\n🔋 Battery Status: {vehicle.battery_voltage}V ", end="")
        if vehicle.battery_voltage >= 12.4:
            print("(Good)")
        elif vehicle.battery_voltage >= 12.0:
            print("(Fair)")
        else:
            print("(Poor - Consider replacement)")
            
        input("\nPress Enter to continue...")
    
    def schedule_service(self):
        """Schedule a service appointment"""
        vehicle = self.select_vehicle()
        if not vehicle:
            return
            
        due_items = MaintenanceSchedule.check_maintenance_due(vehicle)
        if not due_items:
            print("\n✅ No maintenance currently due!")
            input("\nPress Enter to continue...")
            return
            
        print(f"\n📅 Schedule Service for {vehicle}")
        print("-" * 40)
        
        # Show due items
        print("Services due:")
        for i, (service, miles, status) in enumerate(due_items, 1):
            status_icon = "🔴" if status == "OVERDUE" else "🟡"
            print(f"{i}. {status_icon} {service}")
            
        # Select service
        while True:
            try:
                choice = int(input("\nSelect service to schedule: ").strip())
                if 1 <= choice <= len(due_items):
                    selected_service = due_items[choice - 1][0]
                    break
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Select date
        print(f"\n📅 Available dates for {selected_service}:")
        dates = []
        for i in range(1, 8):
            date = datetime.now() + timedelta(days=i)
            if date.weekday() < 5:  # Weekdays only
                dates.append(date)
                print(f"{len(dates)}. {date.strftime('%A, %B %d, %Y')}")
        
        while True:
            try:
                choice = int(input("\nSelect date: ").strip())
                if 1 <= choice <= len(dates):
                    selected_date = dates[choice - 1]
                    break
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Please enter a valid number.")
        
        # Create calendar event
        event_id = self.calendar.create_event(
            f"{selected_service} - {vehicle}",
            selected_date,
            duration=60
        )
        
        print(f"\n✅ Calendar event created! (ID: {event_id})")
        
        # Send email
        send_email = input("\nSend email to service provider? (y/n): ").strip().lower()
        if send_email == 'y':
            provider_email = input("Enter service provider email: ").strip()
            
            subject = f"Service Request: {selected_service} for {vehicle}"
            body = f"""
Dear Service Provider,

I would like to schedule a {selected_service} for my {vehicle}.

Preferred Date: {selected_date.strftime('%A, %B %d, %Y')}
Current Mileage: {vehicle.mileage:,} miles

Please confirm availability.

Thank you,
CarButler User
            """
            
            if self.email.send_email(provider_email, subject, body):
                print("\n✅ Email sent successfully!")
            else:
                print("\n❌ Failed to send email.")
                
        # Update maintenance record
        vehicle.maintenance_history.append({
            'service': selected_service,
            'scheduled_date': selected_date.isoformat(),
            'mileage': vehicle.mileage,
            'status': 'scheduled'
        })
        self.save_vehicles()
        
        input("\nPress Enter to continue...")
    
    def view_history(self):
        """View maintenance history"""
        vehicle = self.select_vehicle()
        if not vehicle:
            return
            
        print(f"\n📊 Maintenance History for {vehicle}")
        print("-" * 40)
        
        if not vehicle.maintenance_history:
            print("No maintenance history recorded.")
        else:
            for record in vehicle.maintenance_history:
                date = datetime.fromisoformat(record['scheduled_date']).strftime('%B %d, %Y')
                print(f"\n• {record['service']}")
                print(f"  Date: {date}")
                print(f"  Mileage: {record['mileage']:,}")
                print(f"  Status: {record['status'].upper()}")
                
        input("\nPress Enter to continue...")
    
    def main_menu(self):
        """Display main menu and handle user input"""
        while True:
            print("\n" + "="*50)
            print("🚗 CarButler - Your Car Maintenance Assistant")
            print("="*50)
            
            if self.vehicles:
                print(f"\nActive Vehicles: {len(self.vehicles)}")
                if len(self.vehicles) == 1:
                    print(f"Current: {self.vehicles[0]}")
            
            print("\n📋 Main Menu:")
            print("1. Add Vehicle")
            print("2. Update Mileage")
            print("3. Check Maintenance")
            print("4. Schedule Service")
            print("5. View History")
            print("6. Exit")
            
            choice = input("\nSelect option (1-6): ").strip()
            
            if choice == '1':
                self.add_vehicle()
            elif choice == '2':
                self.update_mileage()
            elif choice == '3':
                self.check_maintenance()
            elif choice == '4':
                self.schedule_service()
            elif choice == '5':
                self.view_history()
            elif choice == '6':
                print("\n👋 Thank you for using CarButler!")
                sys.exit(0)
            else:
                print("\n❌ Invalid option. Please try again.")
                input("\nPress Enter to continue...")


def main():
    """Main entry point"""
    print("\n🚗 Welcome to CarButler!")
    print("Initializing...")
    
    try:
        app = CarButler()
        app.main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
