#!/usr/bin/env python3
"""
Basic usage example for J.E.F.F Voice Assistant
Demonstrates how to integrate J.E.F.F into your own application
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src import VoiceAssistant
from src.utils import load_config, setup_logging


def main():
    """Basic usage example."""

    # Setup logging
    setup_logging(level='INFO')

    # Load configuration
    config = load_config('../config/config.yaml')

    # Create assistant instance
    assistant = VoiceAssistant(config)

    print("Starting J.E.F.F Voice Assistant...")
    print("This is a basic usage example.")
    print("=" * 60)

    # Run the assistant
    assistant.run()


if __name__ == "__main__":
    main()
