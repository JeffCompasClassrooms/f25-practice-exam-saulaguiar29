import pytest
from battery import Battery
from unittest.mock import Mock

@pytest.fixture
def charged_battery():
    """Battery at full capacity (100/100)"""
    return Battery(100)

@pytest.fixture
def partially_charged_battery():
    """Battery partially charged (70/100)"""
    b = Battery(100)
    b.mCharge = 70
    return b

def describe_battery():

    # BASIC STATE TESTS
    def it_initializes_correctly():
        battery = Battery(100)
        assert battery.getCapacity() == 100
        assert battery.getCharge() == 100

    def it_returns_current_charge(partially_charged_battery):
        assert partially_charged_battery.getCharge() == 70

    # NEW TEST — Ensure state does not change with invalid recharge
    def it_does_not_change_charge_on_invalid_recharge(partially_charged_battery):
        partially_charged_battery.recharge(-5)
        assert partially_charged_battery.getCharge() == 70

    # RECHARGE TESTS
    def it_recharges_successfully(partially_charged_battery):
        result = partially_charged_battery.recharge(20)
        assert result is True
        assert partially_charged_battery.getCharge() == 90

    def it_caps_recharge_at_capacity(partially_charged_battery):
        result = partially_charged_battery.recharge(50)
        assert result is True
        assert partially_charged_battery.getCharge() == 100

    def it_fails_recharge_with_zero(partially_charged_battery):
        result = partially_charged_battery.recharge(0)
        assert result is False
        assert partially_charged_battery.getCharge() == 70

    def it_fails_recharge_when_full(charged_battery):
        result = charged_battery.recharge(10)
        assert result is False

    # NEW TEST — Recharge returns False if amount is negative
    def it_fails_recharge_with_negative_value(partially_charged_battery):
        result = partially_charged_battery.recharge(-10)
        assert result is False

    # DRAIN TESTS
    def it_drains_successfully(partially_charged_battery):
        result = partially_charged_battery.drain(20)
        assert result is True
        assert partially_charged_battery.getCharge() == 50

    def it_caps_drain_at_zero(partially_charged_battery):
        result = partially_charged_battery.drain(100)
        assert result is True
        assert partially_charged_battery.getCharge() == 0

    def it_fails_drain_with_zero(partially_charged_battery):
        result = partially_charged_battery.drain(0)
        assert result is False
        assert partially_charged_battery.getCharge() == 70

    # NEW TEST — Drain fails on negative amount
    def it_fails_drain_with_negative_value(partially_charged_battery):
        result = partially_charged_battery.drain(-10)
        assert result is False

    # MOCK TESTS FOR EXTERNAL MONITOR
    def it_notifies_monitor_on_recharge(partially_charged_battery):
        mock_monitor = Mock()
        partially_charged_battery.external_monitor = mock_monitor

        partially_charged_battery.recharge(20)

        mock_monitor.notify_recharge.assert_called_once_with(90)

    def it_notifies_monitor_on_drain(partially_charged_battery):
        mock_monitor = Mock()
        partially_charged_battery.external_monitor = mock_monitor

        partially_charged_battery.drain(20)

        mock_monitor.notify_drain.assert_called_once_with(50)

    def it_does_not_notify_on_failed_recharge(charged_battery):
        mock_monitor = Mock()
        charged_battery.external_monitor = mock_monitor

        charged_battery.recharge(10)

        mock_monitor.notify_recharge.assert_not_called()

    # NEW TEST — Monitor isn’t called on failed drain
    def it_does_not_notify_on_failed_drain(partially_charged_battery):
        mock_monitor = Mock()
        partially_charged_battery.external_monitor = mock_monitor

        partially_charged_battery.drain(0)

        mock_monitor.notify_drain.assert_not_called()

    def it_works_without_monitor(partially_charged_battery):
        partially_charged_battery.external_monitor = None

        result = partially_charged_battery.recharge(10)
        assert result is True
        assert partially_charged_battery.getCharge() == 80
