# Deployment Guide

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- Git (for version control)
- Virtual environment (recommended)

## Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/typing_speed_test.git
cd typing_speed_test
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run tests:
```bash
pytest
```

6. Start the application:
```bash
python src/main.py
```

## Production Deployment

### System Requirements
- CPU: 1+ cores
- RAM: 512MB minimum
- Storage: 100MB minimum
- OS: Linux (recommended), Windows, or macOS

### Installation Steps

1. Prepare the environment:
```bash
sudo apt update  # For Ubuntu/Debian
sudo apt install python3 python3-pip python3-venv
```

2. Create application directory:
```bash
sudo mkdir /opt/typing_speed_test
sudo chown $USER:$USER /opt/typing_speed_test
```

3. Clone and setup:
```bash
git clone https://github.com/yourusername/typing_speed_test.git /opt/typing_speed_test
cd /opt/typing_speed_test
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env for production settings
```

### Running as a Service (Linux)

1. Create systemd service file:
```bash
sudo nano /etc/systemd/system/typing-speed-test.service
```

2. Add service configuration:
```ini
[Unit]
Description=Typing Speed Test Application
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/opt/typing_speed_test
Environment=PATH=/opt/typing_speed_test/venv/bin
ExecStart=/opt/typing_speed_test/venv/bin/python src/main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Enable and start service:
```bash
sudo systemctl enable typing-speed-test
sudo systemctl start typing-speed-test
```

### Monitoring

1. Check service status:
```bash
sudo systemctl status typing-speed-test
```

2. View logs:
```bash
sudo journalctl -u typing-speed-test
```

## Backup and Recovery

1. Backup data:
```bash
cp -r /opt/typing_speed_test/data /backup/typing_speed_test_$(date +%Y%m%d)
```

2. Restore from backup:
```bash
cp -r /backup/typing_speed_test_YYYYMMDD/data /opt/typing_speed_test/
```

## Troubleshooting

1. GUI Issues:
   - Ensure DISPLAY environment variable is set
   - Check Tkinter installation

2. Permission Issues:
   - Verify file ownership and permissions
   - Check log files for access errors

3. Configuration Issues:
   - Validate .env file settings
   - Check file paths in configuration
