#!/usr/bin/env python3
"""
J.E.F.F Voice Assistant
Main entry point for the application.
"""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from jeff import VoiceAssistant
from jeff.utils import load_config, setup_logging


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="J.E.F.F - Just an Extremely Friendly Fella Voice Assistant"
    )
    parser.add_argument(
        '--config',
        type=str,
        default='config/config.yaml',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--log-level',
        type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set logging level'
    )
    parser.add_argument(
        '--log-file',
        type=str,
        help='Path to log file (optional)'
    )

    return parser.parse_args()


def main():
    """Main application entry point."""
    args = parse_arguments()

    # Setup logging
    setup_logging(level=args.log_level, log_file=args.log_file)

    # Load configuration
    config = load_config(args.config)

    # Create and run assistant
    assistant = VoiceAssistant(config)

    try:
        assistant.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
