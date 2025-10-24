"""
Test state normalization to ensure non-binary state values are handled correctly.

This test verifies the fix for: ValueError: Invalid value for state: 93
Where protocol bytes with values like 93 (non-binary) need to be normalized to 0 or 1.
"""
import pytest
from cync_lan.devices import CyncDevice


class TestStateNormalization:
    """Test that state values are properly normalized to 0 or 1."""

    def test_state_setter_normalizes_positive_integers(self):
        """Test that positive non-zero integers are normalized to 1."""
        device = CyncDevice(cync_id=1, name="test_device")
        
        # Test various positive values
        for value in [1, 2, 50, 93, 100, 255]:
            device.state = value
            assert device.state == 1, f"State {value} should be normalized to 1"

    def test_state_setter_normalizes_zero(self):
        """Test that zero remains zero."""
        device = CyncDevice(cync_id=1, name="test_device")
        device.state = 0
        assert device.state == 0, "State 0 should remain 0"

    def test_state_setter_normalizes_boolean(self):
        """Test that boolean values are properly handled."""
        device = CyncDevice(cync_id=1, name="test_device")
        
        device.state = True
        assert device.state == 1, "State True should be normalized to 1"
        
        device.state = False
        assert device.state == 0, "State False should be normalized to 0"

    def test_state_setter_normalizes_float(self):
        """Test that float values are properly handled."""
        device = CyncDevice(cync_id=1, name="test_device")
        
        device.state = 1.5
        assert device.state == 1, "State 1.5 should be normalized to 1"
        
        device.state = 0.0
        assert device.state == 0, "State 0.0 should remain 0"

    def test_state_setter_handles_string_values(self):
        """Test that string values are properly handled."""
        device = CyncDevice(cync_id=1, name="test_device")
        
        # Test "on" strings
        for value in ["on", "ON", "On", "true", "True", "yes", "YES", "y", "Y", "t", "T"]:
            device.state = value
            assert device.state == 1, f"State '{value}' should be normalized to 1"
        
        # Test "off" strings  
        for value in ["off", "OFF", "Off", "false", "False", "no", "NO", "n", "N", "f", "F"]:
            device.state = value
            assert device.state == 0, f"State '{value}' should be normalized to 0"

    def test_state_setter_rejects_invalid_strings(self):
        """Test that invalid string values raise ValueError."""
        device = CyncDevice(cync_id=1, name="test_device")
        
        with pytest.raises(ValueError, match="Invalid value for state"):
            device.state = "invalid"

    def test_state_setter_rejects_invalid_types(self):
        """Test that invalid types raise TypeError."""
        device = CyncDevice(cync_id=1, name="test_device")
        
        with pytest.raises(TypeError, match="Invalid type for state"):
            device.state = None
        
        with pytest.raises(TypeError, match="Invalid type for state"):
            device.state = []

    def test_specific_protocol_value_93(self):
        """
        Test the specific case from the bug report.
        
        The protocol was sending state value 93, which should be normalized to 1 (on).
        """
        device = CyncDevice(cync_id=1, name="test_device")
        device.state = 93
        assert device.state == 1, "Protocol value 93 should be normalized to 1 (on)"
