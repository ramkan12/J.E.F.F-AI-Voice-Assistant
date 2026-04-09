"""
Setup script for J.E.F.F Voice Assistant
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="jeff-voice-assistant",
    version="2.0.0",
    author="Riham Khan",
    author_email="ramkan12@users.noreply.github.com",
    description="A Python-based voice assistant with natural language processing capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ramkan12/J.E.F.F-Voice-Assistant",
    project_urls={
        "Bug Tracker": "https://github.com/ramkan12/J.E.F.F-Voice-Assistant/issues",
        "Documentation": "https://github.com/ramkan12/J.E.F.F-Voice-Assistant/blob/main/docs/",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "gTTS>=2.3.0",
        "SpeechRecognition>=3.10.0",
        "requests>=2.31.0",
        "PyYAML>=6.0",
        "PyAudio>=0.2.13",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "jeff=main:main",
            "jeff-cli=jeff_cli:main",
        ],
    },
    include_package_data=True,
    keywords="voice assistant, speech recognition, text-to-speech, AI assistant",
)
