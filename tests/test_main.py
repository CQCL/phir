"""Tests for phir.main module."""

from phir.main import hello_world


def test_hello_world():
    """Test the hello_world function."""
    assert hello_world() == "Hello, World!"
