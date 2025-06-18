#!/usr/bin/env python3
"""
Build script for Windows executable distribution.

This script creates a standalone executable for the Email Box Analyzer API server.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    """Build the Windows executable."""
    print("Building Email Box Analyzer for Windows...")
    
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
        "--distpath=dist/windows",
        "--workpath=build/windows",
        "--specpath=build/windows",
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
        "--add-data=src;src",
        "--icon=resources/icon.ico" if os.path.exists("resources/icon.ico") else "",
        str(src_dir / "main.py")
    ]
    
    # Remove empty icon argument if no icon exists
    cmd = [arg for arg in cmd if arg]
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build completed successfully!")
        print(f"Executable created at: {project_root}/dist/windows/email-analyzer-api.exe")
        
        # Create a batch file for easy startup
        batch_content = """@echo off
echo Starting Email Box Analyzer API Server...
echo.
echo The API server will be available at: http://localhost:8000
echo API documentation: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.
email-analyzer-api.exe
pause
"""
        
        batch_file = project_root / "dist" / "windows" / "start-api-server.bat"
        with open(batch_file, "w") as f:
            f.write(batch_content)
        
        print(f"Startup script created at: {batch_file}")
        
        # Create README for Windows
        readme_content = """# Email Box Analyzer API Server - Windows

## Quick Start

1. Double-click `start-api-server.bat` to start the API server
2. Open your web browser and go to: http://localhost:8000/docs
3. Use the interactive API documentation to test the endpoints

## Manual Start

If the batch file doesn't work, you can start the server manually:

```cmd
email-analyzer-api.exe
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
- Check Windows Defender or antivirus software if the executable is blocked

## Support

For issues and questions, please check the main project documentation.
"""
        
        readme_file = project_root / "dist" / "windows" / "README.txt"
        with open(readme_file, "w") as f:
            f.write(readme_content)
        
        print(f"Documentation created at: {readme_file}")
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 