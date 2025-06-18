"""
Setup script for Email Box Analyzer

Configuration for packaging and distribution of the application.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_path = Path(__file__).parent / "README.md"
long_description = ""
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    with open(requirements_path, "r", encoding="utf-8") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="email-box-analyzer",
    version="1.0.0",
    author="Email Analyzer Team",
    author_email="contact@emailanalyzer.com",
    description="A comprehensive email analysis tool with visualizations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/emailanalyzer/email-box-analyzer",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Communications :: Email",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications :: Qt",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-qt>=4.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=1.0.0",
            "isort>=5.0.0",
            "pre-commit>=3.0.0",
        ],
        "build": [
            "pyinstaller>=5.0.0",
            "setuptools>=65.0.0",
            "wheel>=0.37.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "email-analyzer=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.yaml", "*.yml", "*.txt", "*.md"],
    },
    keywords="email analysis visualization imap smtp gmail outlook",
    project_urls={
        "Bug Reports": "https://github.com/emailanalyzer/email-box-analyzer/issues",
        "Source": "https://github.com/emailanalyzer/email-box-analyzer",
        "Documentation": "https://emailanalyzer.readthedocs.io/",
    },
) 