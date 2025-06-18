#!/usr/bin/env python3
"""
Build script for macOS application distribution.

This script creates a standalone application bundle for the Email Box Analyzer API server.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    """Build the macOS application."""
    print("Building Email Box Analyzer for macOS...")
    
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
        "--name=EmailAnalyzerAPI",
        "--distpath=dist/macos",
        "--workpath=build/macos",
        "--specpath=build/macos",
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
        "--icon=resources/icon.icns" if os.path.exists("resources/icon.icns") else "",
        str(src_dir / "main.py")
    ]
    
    # Remove empty icon argument if no icon exists
    cmd = [arg for arg in cmd if arg]
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build completed successfully!")
        print(f"Executable created at: {project_root}/dist/macos/EmailAnalyzerAPI")
        
        # Create a shell script for easy startup
        script_content = """#!/bin/bash
echo "Starting Email Box Analyzer API Server..."
echo ""
echo "The API server will be available at: http://localhost:8000"
echo "API documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
./EmailAnalyzerAPI
"""
        
        script_file = project_root / "dist" / "macos" / "start-api-server.sh"
        with open(script_file, "w") as f:
            f.write(script_content)
        
        # Make the script executable
        os.chmod(script_file, 0o755)
        
        print(f"Startup script created at: {script_file}")
        
        # Create README for macOS
        readme_content = """# Email Box Analyzer API Server - macOS

## Quick Start

1. Open Terminal
2. Navigate to this directory: `cd /path/to/EmailAnalyzerAPI`
3. Run the startup script: `./start-api-server.sh`
4. Open your web browser and go to: http://localhost:8000/docs

## Manual Start

If the script doesn't work, you can start the server manually:

```bash
./EmailAnalyzerAPI
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
- Check macOS Security settings if the executable is blocked
- You may need to allow the application in System Preferences > Security & Privacy

## Support

For issues and questions, please check the main project documentation.
"""
        
        readme_file = project_root / "dist" / "macos" / "README.txt"
        with open(readme_file, "w") as f:
            f.write(readme_content)
        
        print(f"Documentation created at: {readme_file}")
        
        # Create a simple app bundle structure
        app_bundle_dir = project_root / "dist" / "macos" / "EmailAnalyzerAPI.app"
        contents_dir = app_bundle_dir / "Contents"
        macos_dir = contents_dir / "MacOS"
        resources_dir = contents_dir / "Resources"
        
        # Create directory structure
        os.makedirs(macos_dir, exist_ok=True)
        os.makedirs(resources_dir, exist_ok=True)
        
        # Copy executable to app bundle
        shutil.copy2(
            project_root / "dist" / "macos" / "EmailAnalyzerAPI",
            macos_dir / "EmailAnalyzerAPI"
        )
        
        # Create Info.plist
        info_plist_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>EmailAnalyzerAPI</string>
    <key>CFBundleIdentifier</key>
    <string>com.emailanalyzer.api</string>
    <key>CFBundleName</key>
    <string>Email Analyzer API</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>"""
        
        info_plist_file = contents_dir / "Info.plist"
        with open(info_plist_file, "w") as f:
            f.write(info_plist_content)
        
        print(f"App bundle created at: {app_bundle_dir}")
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 