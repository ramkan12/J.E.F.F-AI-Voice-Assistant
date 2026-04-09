"""
Unit tests for command handlers
"""

import pytest
from jeff.commands import CommandHandler


class TestCommandHandler:
    """Test suite for CommandHandler class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.handler = CommandHandler()

    def test_get_greeting(self):
        """Test that greeting is returned."""
        greeting = self.handler.get_greeting()
        assert isinstance(greeting, str)
        assert len(greeting) > 0

    def test_get_time(self):
        """Test time retrieval."""
        time_str = self.handler.get_time()
        assert "time" in time_str.lower()
        assert isinstance(time_str, str)

    def test_get_date(self):
        """Test date retrieval."""
        date_str = self.handler.get_date()
        assert "today" in date_str.lower()
        assert isinstance(date_str, str)

    def test_tell_joke(self):
        """Test joke telling."""
        joke = self.handler.tell_joke()
        assert isinstance(joke, str)
        assert len(joke) > 0

    def test_calculate_simple_addition(self):
        """Test simple addition calculation."""
        result = self.handler.calculate("calculate 5 plus 3")
        assert "8" in result or "answer" in result.lower()

    def test_calculate_multiplication(self):
        """Test multiplication calculation."""
        result = self.handler.calculate("25 * 4")
        assert "100" in result

    def test_calculate_invalid_expression(self):
        """Test calculation with invalid characters."""
        result = self.handler.calculate("calculate rm -rf /")
        assert "sorry" in result.lower() or "can only do" in result.lower()

    def test_get_name_info(self):
        """Test name information retrieval."""
        name_info = self.handler.get_name_info()
        assert "J.E.F.F" in name_info
        assert isinstance(name_info, str)

    def test_get_help(self):
        """Test help text retrieval."""
        help_text = self.handler.get_help()
        assert "help" in help_text.lower() or "can" in help_text.lower()
        assert isinstance(help_text, str)

    def test_weather_without_api_key(self):
        """Test weather request without API key."""
        result = self.handler.get_weather()
        # Should return error message about missing API key
        assert "api key" in result.lower() or "sorry" in result.lower()


# Example of how to run:
# pytest tests/test_commands.py -v
