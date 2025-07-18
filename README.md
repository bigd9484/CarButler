# 🚗 CarButler

> Your intelligent car maintenance assistant that keeps your vehicle running smoothly!

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/yourusername/carbutler/pulls)

## ✨ Features

- 📊 **Mileage & Battery Tracking** - Track your car's mileage and battery health through manual input or simulated OBD2 data
- 🔧 **Smart Maintenance Scheduling** - Get timely reminders for oil changes, tire rotations, and other maintenance tasks
- 📅 **Google Calendar Integration** - Automatically schedule service appointments in your calendar
- 📧 **Service Provider Communication** - Email local mechanics directly from the app
- 🚙 **Multi-Vehicle Support** - Manage maintenance for multiple vehicles
- 📱 **User-Friendly Interface** - Simple command-line interface with intuitive menus

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Calendar API credentials (optional)
- SMTP email configuration (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/carbutler.git
   cd carbutler
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure settings** (optional)
   ```bash
   cp config.example.json config.json
   # Edit config.json with your API credentials
   ```

## 📖 Usage

### Basic Usage

Run CarButler from the command line:

```bash
python main.py
```

### Available Commands

1. **Add Vehicle** 🚗
   - Register a new vehicle with make, model, year, and current mileage

2. **Update Mileage** 📏
   - Manually update your vehicle's current mileage
   - Option to use simulated OBD2 data

3. **Check Maintenance** 🔍
   - View upcoming maintenance tasks based on your vehicle's mileage
   - Get recommendations for oil changes, tire rotations, etc.

4. **Schedule Service** 📅
   - Create calendar events for maintenance appointments
   - Send emails to preferred service providers

5. **View History** 📊
   - Track maintenance history and costs
   - Export reports for record-keeping

### Example Workflow

```bash
# Start the application
$ python main.py

# Select "Add Vehicle"
> Enter make: Toyota
> Enter model: Camry
> Enter year: 2020
> Enter current mileage: 25000

# Update mileage
> Select vehicle: Toyota Camry 2020
> Enter new mileage: 26500

# Check maintenance
> Oil change recommended at 27500 miles (1000 miles remaining)
> Tire rotation due now

# Schedule service
> Select service: Tire Rotation
> Available dates: [Shows calendar availability]
> Email sent to Joe's Auto Shop!
```

## 🔧 Configuration

### Google Calendar Setup

1. Enable the Google Calendar API in your Google Cloud Console
2. Download credentials.json
3. Place it in the project root directory
4. Run the app - it will authenticate on first use

### Email Configuration

Add your SMTP settings to `config.json`:

```json
{
  "smtp": {
    "server": "smtp.gmail.com",
    "port": 587,
    "email": "your-email@gmail.com",
    "password": "your-app-password"
  }
}
```

## 🏗️ Project Structure

```
carbutler/
├── main.py              # Main application entry point
├── requirements.txt     # Python dependencies
├── config.json         # Configuration file (create from example)
├── config.example.json # Example configuration
├── data/
│   └── vehicles.json   # Vehicle data storage
├── modules/
│   ├── vehicle.py      # Vehicle class and management
│   ├── maintenance.py  # Maintenance scheduling logic
│   ├── calendar_api.py # Google Calendar integration
│   └── email_service.py # Email functionality
└── tests/
    └── test_*.py       # Unit tests
```

## 🤝 Contributing

We love contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Maintenance Schedules

CarButler uses industry-standard maintenance intervals:

| Service | Interval |
|---------|----------|
| Oil Change | Every 5,000-7,500 miles |
| Tire Rotation | Every 5,000-8,000 miles |
| Air Filter | Every 15,000-30,000 miles |
| Brake Inspection | Every 20,000 miles |
| Coolant Flush | Every 30,000 miles |
| Transmission Service | Every 30,000-60,000 miles |

## 🐛 Troubleshooting

### Common Issues

**Google Calendar not connecting:**
- Ensure credentials.json is in the root directory
- Check that Calendar API is enabled in Google Cloud Console
- Delete token.json and re-authenticate

**Email not sending:**
- Verify SMTP settings in config.json
- For Gmail, use an app-specific password
- Check firewall settings for SMTP port

**OBD2 simulation not working:**
- This is currently a mock implementation
- Real OBD2 support planned for future release

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- 🎉 Thanks to all contributors!
- 📚 Inspired by the need for better vehicle maintenance tracking
- 🔧 Maintenance schedules based on manufacturer recommendations

## 📮 Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/carbutler/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/carbutler/discussions)
- **Email**: carbutler@example.com

---

Made with ❤️ by the CarButler Team
