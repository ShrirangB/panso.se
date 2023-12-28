# Create your tests here.
from __future__ import annotations

from typing import TYPE_CHECKING

from django.test import TestCase

from data_converters import (
    bandwidth_to_bandwidth,
    bit_to_bit,
    bool_to_bool,
    bytes_to_bytes,
    dollar_to_cents,
    float_to_float,
    hertz_an_hertz,
    temp_to_temp,
    watt_to_watt,
)

if TYPE_CHECKING:
    from django.http import HttpResponse


class IntelTests(TestCase):
    """Tests things for the Intel app."""

    # TODO: Test that we get the correct data from the API.
    def test_get_filter_data(self: IntelTests) -> None:
        """Test that the filter data is available."""
        response: HttpResponse = self.client.get("/api/v1/intel/filter")
        assert response.status_code == 200
        assert response["Content-Type"] == "application/json"
        assert response.json() == []

    def test_get_processor_ids(self: IntelTests) -> None:
        """Test that the processor ids are available."""
        response: HttpResponse = self.client.get("/api/v1/intel/processors")
        assert response.status_code == 200
        assert response["Content-Type"] == "application/json"
        assert response.json() == []


class HertzConversionTest(TestCase):
    """Tests the hertz_an_hertz function."""

    def test_conversion_gigahertz(self: HertzConversionTest) -> None:
        result: int | None = hertz_an_hertz("2.8 GHz")
        assert result == 2800000000

    def test_conversion_megahertz(self: HertzConversionTest) -> None:
        result: int | None = hertz_an_hertz("2.8 MHz")
        assert result == 2800000

    def test_conversion_kilohertz(self: HertzConversionTest) -> None:
        result: int | None = hertz_an_hertz("2.8 KHz")
        assert result == 2800

    def test_conversion_hertz(self: HertzConversionTest) -> None:
        result: int | None = hertz_an_hertz("2.8 Hz")
        assert result == 2

    def test_conversion_empty_string(self: HertzConversionTest) -> None:
        result: int | None = hertz_an_hertz("")
        assert result is None

    def test_conversion_digit_string(self: HertzConversionTest) -> None:
        result: int | None = hertz_an_hertz("12345")
        assert result == 12345

    def test_conversion_terahertz(self: HertzConversionTest) -> None:
        result: int | None = hertz_an_hertz("2.8 THz")
        assert result == 2800000000000

    def test_conversion_invalid_input(self: HertzConversionTest) -> None:
        result: int | None = hertz_an_hertz("invalid input")
        assert not result


class BytesConversionTest(TestCase):
    """Tests the bytes_to_bytes function."""

    def test_conversion_gigabytes(self: BytesConversionTest) -> None:
        result: int | None = bytes_to_bytes("2.8 GB")
        assert result == 2800000000

    def test_conversion_megabytes(self: BytesConversionTest) -> None:
        result: int | None = bytes_to_bytes("2.8 MB")
        assert result == 2800000

    def test_conversion_kilobytes(self: BytesConversionTest) -> None:
        result: int | None = bytes_to_bytes("2.8 KB")
        assert result == 2800

    def test_conversion_bytes(self: BytesConversionTest) -> None:
        result: int | None = bytes_to_bytes("2.8 B")
        assert result == 2

    def test_conversion_empty_string(self: BytesConversionTest) -> None:
        result: int | None = bytes_to_bytes("")
        assert result is None

    def test_conversion_digit_string(self: BytesConversionTest) -> None:
        result: int | None = bytes_to_bytes("12345")
        assert result == 12345

    def test_conversion_terabytes(self: BytesConversionTest) -> None:
        result: int | None = bytes_to_bytes("2.8 TB")
        assert result == 2800000000000

    def test_conversion_invalid_input(self: BytesConversionTest) -> None:
        result: int | None = bytes_to_bytes("invalid input")
        assert not result


class WattConversionTest(TestCase):
    """Tests the watt_to_watt function."""

    def test_conversion_kilowatts(self: WattConversionTest) -> None:
        result: int | None = watt_to_watt("2.8 kW")
        assert result == 2800

    def test_conversion_watts(self: WattConversionTest) -> None:
        result: int | None = watt_to_watt("2.8 W")
        assert result == 2

    def test_conversion_empty_string(self: WattConversionTest) -> None:
        result: int | None = watt_to_watt("")
        assert result is None

    def test_conversion_digit_string(self: WattConversionTest) -> None:
        result: int | None = watt_to_watt("12345")
        assert result == 12345

    def test_conversion_invalid_input(self: WattConversionTest) -> None:
        result: int | None = watt_to_watt("invalid input")
        assert not result


class BooleanConversionTest(TestCase):
    """Tests the bool_to_bool function."""

    def test_conversion_true(self: BooleanConversionTest) -> None:
        result: bool | None = bool_to_bool("Yes")
        assert result is True

    def test_conversion_false(self: BooleanConversionTest) -> None:
        result: bool | None = bool_to_bool("No")
        assert result is False

    def test_conversion_empty_string(self: BooleanConversionTest) -> None:
        result: bool | None = bool_to_bool("")
        assert result is None

    def test_conversion_invalid_input(self: BooleanConversionTest) -> None:
        result: bool | None = bool_to_bool("invalid input")
        assert not result


class BandwidthConversionTest(TestCase):
    """Tests the bandwidth_to_bandwidth function."""

    def test_conversion_gigabytes(self: BandwidthConversionTest) -> None:
        result: int | None = bandwidth_to_bandwidth("2.8 GB/s")
        assert result == 2800000000

    def test_conversion_megabytes(self: BandwidthConversionTest) -> None:
        result: int | None = bandwidth_to_bandwidth("2.8 MB/s")
        assert result == 2800000

    def test_conversion_kilobytes(self: BandwidthConversionTest) -> None:
        result: int | None = bandwidth_to_bandwidth("2.8 KB/s")
        assert result == 2800

    def test_conversion_bytes(self: BandwidthConversionTest) -> None:
        result: int | None = bandwidth_to_bandwidth("2.8 B/s")
        assert result == 2

    def test_conversion_empty_string(self: BandwidthConversionTest) -> None:
        result: int | None = bandwidth_to_bandwidth("")
        assert result is None

    def test_conversion_digit_string(self: BandwidthConversionTest) -> None:
        result: int | None = bandwidth_to_bandwidth("12345")
        assert result == 12345

    def test_conversion_terabytes(self: BandwidthConversionTest) -> None:
        result: int | None = bandwidth_to_bandwidth("2.8 TB/s")
        assert result == 2800000000000

    def test_conversion_invalid_input(self: BandwidthConversionTest) -> None:
        result: int | None = bandwidth_to_bandwidth("invalid input")
        assert not result


class FloatConversionTest(TestCase):
    """Tests the float_to_float function."""

    def test_conversion_float(self: FloatConversionTest) -> None:
        result: float | None = float_to_float("2.8")
        assert result == 2.8

    def test_conversion_empty_string(self: FloatConversionTest) -> None:
        result: float | None = float_to_float("")
        assert result is None

    def test_conversion_invalid_input(self: FloatConversionTest) -> None:
        result: float | None = float_to_float("invalid input")
        assert not result


class BitConversionTest(TestCase):
    """Tests the bit_to_bit function."""

    def test_conversion_positive_bit(self: BitConversionTest) -> None:
        result: int | None = bit_to_bit("64-bit")
        assert result == 64

    def test_conversion_negative_bit(self: BitConversionTest) -> None:
        result: int | None = bit_to_bit("-32-bit")
        assert result == -32

    def test_conversion_invalid_input(self: BitConversionTest) -> None:
        result: int | None = bit_to_bit("invalid input")
        assert result is None

    def test_conversion_empty_string(self: BitConversionTest) -> None:
        result: int | None = bit_to_bit("")
        assert result is None

    def test_conversion_digit_string(self: BitConversionTest) -> None:
        result: int | None = bit_to_bit("128")
        assert result == 128

    def test_conversion_zero_bit(self: BitConversionTest) -> None:
        result: int | None = bit_to_bit("0-bit")
        assert result == 0

    def test_conversion_large_bit(self: BitConversionTest) -> None:
        result: int | None = bit_to_bit("1024-bit")
        assert result == 1024

    def test_conversion_float_bit(self: BitConversionTest) -> None:
        result: int | None = bit_to_bit("64.5-bit")
        assert result is None

    def test_conversion_non_digit_bit(self: BitConversionTest) -> None:
        result: int | None = bit_to_bit("some-bit")
        assert result is None

    def test_conversion_non_digit_bit_2(self: BitConversionTest) -> None:
        result: int | None = bit_to_bit("some-bit-bit")
        assert result is None


class TemperatureConversionTest(TestCase):
    """Tests the temp_to_temp function."""

    def test_conversion_celsius(self: TemperatureConversionTest) -> None:
        result: float | None = temp_to_temp("2.8 °C")
        assert result == 2.8

    def test_conversion_fahrenheit(self: TemperatureConversionTest) -> None:
        result: float | None = temp_to_temp("2.8 °F")
        assert result == -16.22222222222222

    def test_conversion_kelvin(self: TemperatureConversionTest) -> None:
        result: float | None = temp_to_temp("2.8 K")
        assert result == -270.34999999999997

    def test_conversion_empty_string(self: TemperatureConversionTest) -> None:
        result: float | None = temp_to_temp("")
        assert result is None

    def test_conversion_digit_string(self: TemperatureConversionTest) -> None:
        result: float | None = temp_to_temp("12345")
        assert result == 12345

    def test_conversion_invalid_input(self: TemperatureConversionTest) -> None:
        result: float | None = temp_to_temp("invalid input")
        assert not result


class DollarConversionTest(TestCase):
    """Tests the dollar_to_cents function."""

    def test_conversion_dollar(self: DollarConversionTest) -> None:
        result: int | None = dollar_to_cents("$2.8")
        assert result == 280

    def test_conversion_empty_string(self: DollarConversionTest) -> None:
        result: int | None = dollar_to_cents("")
        assert result is None

    def test_conversion_invalid_input(self: DollarConversionTest) -> None:
        result: int | None = dollar_to_cents("invalid input")
        assert not result
