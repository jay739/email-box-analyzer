#!/usr/bin/env python3
"""
Build script for Linux executable distribution.

This script creates a standalone executable and package for the Email Box Analyzer API server.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    """Build the Linux executable and package."""
    print("Building Email Box Analyzer for Linux...")
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    src_dir = project_root / "src"
    
    # Ensure we're in the right directory
    os.chdir(project_root)
    
    # Clean previous builds
    print("Cleaning previous builds...")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # PyInstaller command for FastAPI server
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name=email-analyzer-api",
        "--distpath=dist/linux",
        "--workpath=build/linux",
        "--specpath=build/linux",
        "--hidden-import=fastapi",
        "--hidden-import=uvicorn",
        "--hidden-import=pydantic",
        "--hidden-import=email",
        "--hidden-import=imaplib",
        "--hidden-import=smtplib",
        "--hidden-import=ssl",
        "--hidden-import=json",
        "--hidden-import=datetime",
        "--hidden-import=typing",
        "--hidden-import=asyncio",
        "--hidden-import=logging",
        "--hidden-import=pathlib",
        "--hidden-import=sqlite3",
        "--hidden-import=hashlib",
        "--hidden-import=secrets",
        "--hidden-import=bcrypt",
        "--hidden-import=jwt",
        "--add-data=src:src",
        str(src_dir / "main.py")
    ]
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build completed successfully!")
        print(f"Executable created at: {project_root}/dist/linux/email-analyzer-api")
        
        # Create a shell script for easy startup
        script_content = """#!/bin/bash
echo "Starting Email Box Analyzer API Server..."
echo ""
echo "The API server will be available at: http://localhost:8000"
echo "API documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
./email-analyzer-api
"""
        
        script_file = project_root / "dist" / "linux" / "start-api-server.sh"
        with open(script_file, "w") as f:
            f.write(script_content)
        
        # Make the script executable
        os.chmod(script_file, 0o755)
        
        print(f"Startup script created at: {script_file}")
        
        # Create README for Linux
        readme_content = """# Email Box Analyzer API Server - Linux

## Quick Start

1. Open Terminal
2. Navigate to this directory: `cd /path/to/email-analyzer-api`
3. Run the startup script: `./start-api-server.sh`
4. Open your web browser and go to: http://localhost:8000/docs

## Manual Start

If the script doesn't work, you can start the server manually:

```bash
./email-analyzer-api
```

## API Endpoints

- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/health

## Configuration

The server uses default settings. To customize:

1. Create a `.env` file in the same directory
2. Add your configuration variables
3. Restart the server

## Troubleshooting

- If the server won't start, check if port 8000 is already in use
- Make sure you have the necessary permissions to run executables
- Check if all required libraries are installed
- You may need to install additional dependencies: `sudo apt-get install libssl-dev`

## Support

For issues and questions, please check the main project documentation.
"""
        
        readme_file = project_root / "dist" / "linux" / "README.txt"
        with open(readme_file, "w") as f:
            f.write(readme_content)
        
        print(f"Documentation created at: {readme_file}")
        
        # Create systemd service file
        service_content = """[Unit]
Description=Email Box Analyzer API Server
After=network.target

[Service]
Type=simple
User=email-analyzer
WorkingDirectory=/opt/email-analyzer-api
ExecStart=/opt/email-analyzer-api/email-analyzer-api
Restart=always
RestartSec=10
Environment=PORT=8000

[Install]
WantedBy=multi-user.target
"""
        
        service_file = project_root / "dist" / "linux" / "email-analyzer-api.service"
        with open(service_file, "w") as f:
            f.write(service_content)
        
        print(f"Systemd service file created at: {service_file}")
        
        # Create installation script
        install_script_content = """#!/bin/bash
# Email Box Analyzer API Server Installation Script

set -e

echo "Installing Email Box Analyzer API Server..."

# Create user if it doesn't exist
if ! id "email-analyzer" &>/dev/null; then
    echo "Creating email-analyzer user..."
    sudo useradd -r -s /bin/false email-analyzer
fi

# Create installation directory
sudo mkdir -p /opt/email-analyzer-api

# Copy files
sudo cp email-analyzer-api /opt/email-analyzer-api/
sudo cp start-api-server.sh /opt/email-analyzer-api/
sudo cp README.txt /opt/email-analyzer-api/

# Set permissions
sudo chown -R email-analyzer:email-analyzer /opt/email-analyzer-api
sudo chmod +x /opt/email-analyzer-api/email-analyzer-api
sudo chmod +x /opt/email-analyzer-api/start-api-server.sh

# Install systemd service
sudo cp email-analyzer-api.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable email-analyzer-api

echo "Installation completed!"
echo ""
echo "To start the service:"
echo "  sudo systemctl start email-analyzer-api"
echo ""
echo "To check status:"
echo "  sudo systemctl status email-analyzer-api"
echo ""
echo "To view logs:"
echo "  sudo journalctl -u email-analyzer-api -f"
echo ""
echo "The API will be available at: http://localhost:8000"
"""
        
        install_script_file = project_root / "dist" / "linux" / "install.sh"
        with open(install_script_file, "w") as f:
            f.write(install_script_content)
        
        # Make installation script executable
        os.chmod(install_script_file, 0o755)
        
        print(f"Installation script created at: {install_script_file}")
        
        # Create DEB package if dpkg-deb is available
        try:
            subprocess.run(["dpkg-deb", "--version"], check=True, capture_output=True)
            create_deb_package(project_root)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("dpkg-deb not available, skipping DEB package creation")
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def create_deb_package(project_root):
    """Create a DEB package for the application."""
    print("Creating DEB package...")
    
    # Create package structure
    package_name = "email-analyzer-api"
    package_version = "1.0.0"
    package_dir = project_root / "dist" / "linux" / f"{package_name}-{package_version}"
    debian_dir = package_dir / "DEBIAN"
    opt_dir = package_dir / "opt" / package_name
    etc_dir = package_dir / "etc" / "systemd" / "system"
    
    # Create directories
    os.makedirs(debian_dir, exist_ok=True)
    os.makedirs(opt_dir, exist_ok=True)
    os.makedirs(etc_dir, exist_ok=True)
    
    # Copy files
    shutil.copy2(
        project_root / "dist" / "linux" / "email-analyzer-api",
        opt_dir / "email-analyzer-api"
    )
    shutil.copy2(
        project_root / "dist" / "linux" / "start-api-server.sh",
        opt_dir / "start-api-server.sh"
    )
    shutil.copy2(
        project_root / "dist" / "linux" / "README.txt",
        opt_dir / "README.txt"
    )
    shutil.copy2(
        project_root / "dist" / "linux" / "email-analyzer-api.service",
        etc_dir / "email-analyzer-api.service"
    )
    
    # Create control file
    control_content = f"""Package: {package_name}
Version: {package_version}
Section: utils
Priority: optional
Architecture: amd64
Depends: libc6
Maintainer: Email Analyzer Team <support@emailanalyzer.com>
Description: Email Box Analyzer API Server
 A comprehensive email analysis platform with a modern web interface
 and powerful backend API for analyzing email data from various providers.
 .
 Features:
  - Multi-provider email support (Gmail, Outlook, Yahoo, etc.)
  - Comprehensive email analysis and statistics
  - Interactive visualizations and charts
  - RESTful API with automatic documentation
  - Background job processing
  - Export capabilities (JSON, CSV, Excel, PDF)
Homepage: https://github.com/emailanalyzer/email-box-analyzer
"""
    
    control_file = debian_dir / "control"
    with open(control_file, "w") as f:
        f.write(control_content)
    
    # Create postinst script
    postinst_content = """#!/bin/bash
# Post-installation script for Email Box Analyzer API Server

# Create user if it doesn't exist
if ! id "email-analyzer" &>/dev/null; then
    useradd -r -s /bin/false email-analyzer
fi

# Set permissions
chown -R email-analyzer:email-analyzer /opt/email-analyzer-api
chmod +x /opt/email-analyzer-api/email-analyzer-api
chmod +x /opt/email-analyzer-api/start-api-server.sh

# Reload systemd and enable service
systemctl daemon-reload
systemctl enable email-analyzer-api

echo "Email Box Analyzer API Server installed successfully!"
echo "To start the service: sudo systemctl start email-analyzer-api"
echo "The API will be available at: http://localhost:8000"
"""
    
    postinst_file = debian_dir / "postinst"
    with open(postinst_file, "w") as f:
        f.write(postinst_content)
    
    os.chmod(postinst_file, 0o755)
    
    # Create prerm script
    prerm_content = """#!/bin/bash
# Pre-removal script for Email Box Analyzer API Server

# Stop and disable service
systemctl stop email-analyzer-api || true
systemctl disable email-analyzer-api || true
systemctl daemon-reload
"""
    
    prerm_file = debian_dir / "prerm"
    with open(prerm_file, "w") as f:
        f.write(prerm_content)
    
    os.chmod(prerm_file, 0o755)
    
    # Build DEB package
    deb_file = project_root / "dist" / "linux" / f"{package_name}_{package_version}_amd64.deb"
    
    try:
        subprocess.run([
            "dpkg-deb", "--build", str(package_dir), str(deb_file)
        ], check=True)
        print(f"DEB package created at: {deb_file}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create DEB package: {e}")

if __name__ == "__main__":
    main() 