from __future__ import annotations

from functools import lru_cache

from rich import print
from rich.console import Console

err_console = Console(stderr=True)


@lru_cache(maxsize=1024)
def hertz_an_hertz(hz: str) -> int | None:  # noqa: PLR0911
    """Convert GHz, MHz, and KHz to Hz.

    Example:
        >>> hz_to_hz("2.8 GHz")
        2800000000
        >>> hz_to_hz("2.8 MHz")
        2800000
        >>> hz_to_hz("2.8 KHz")
        2800
        >>> hz_to_hz("2.8 Hz")
        2

    Args:
        hz (str): The value to convert.

    Returns:
        int: The value in Hz.
    """
    try:
        if not hz:
            return None
        if hz.isdigit():
            return int(hz)

        if hz.startswith("Up to "):
            hz = hz.replace("Up to ", "")
            return hertz_an_hertz(hz)

        if "THz" in hz:
            return int(float(hz.replace("THz", "")) * 1_000_000_000_000)
        if "GHz" in hz:
            return int(float(hz.replace("GHz", "")) * 1_000_000_000)
        if "MHz" in hz:
            return int(float(hz.replace("MHz", "")) * 1_000_000)
        if "KHz" in hz:
            return int(float(hz.replace("KHz", "")) * 1_000)
        if "Hz" in hz:
            return int(float(hz.replace("Hz", "")))
        return int(hz)
    except ValueError:
        err_console.print(f"Could not convert '{hz}' to Hz")
        return None


@lru_cache(maxsize=1024)
def bytes_to_bytes(b: str) -> int | None:  # noqa: PLR0911
    """Convert MB, GB, and TB to bytes.

    Example:
        >>> bytes_to_bytes("2.8 GB")
        2800000000
        >>> bytes_to_bytes("2.8 MB")
        2800000
        >>> bytes_to_bytes("2.8 KB")
        2800
        >>> bytes_to_bytes("2.8 B")
        2

    Args:
        b (str): The value to convert.

    Returns:
        int: The value in bytes.
    """
    try:
        if not b:
            return None
        if b.isdigit():
            return int(b)
        if "TB" in b:
            return int(float(b.replace("TB", "")) * 1_000_000_000_000)
        if "GB" in b:
            return int(float(b.replace("GB", "")) * 1_000_000_000)
        if "MB" in b:
            return int(float(b.replace("MB", "")) * 1_000_000)
        if "KB" in b:
            return int(float(b.replace("KB", "")) * 1_000)
        if "B" in b:
            return int(float(b.replace("B", "")))
        return int(b)
    except ValueError:
        err_console.print(f"Could not convert '{b}' to bytes")
        return None


@lru_cache(maxsize=1024)
def watt_to_watt(w: str) -> int | None:
    """Convert 11 W to 11.

    Args:
        w (str): The value to convert.

    Returns:
        int: The value in W.
    """
    try:
        if not w:
            return None
        if w.isdigit():
            return int(w)
        if "kW" in w:
            return int(float(w.replace("kW", "")) * 1_000)
        if "W" in w:
            return int(float(w.replace("W", "")))
        return int(w)
    except ValueError:
        err_console.print(f"Could not convert '{w}' to W")
        return None


@lru_cache(maxsize=1024)
def bool_to_bool(b: str) -> bool | None:
    """Convert Yes to True and No to False.

    Args:
        b (str): The value to convert.

    Returns:
        bool: The value in bool.
    """
    try:
        if not b:
            return None
        if b == "Yes":
            return True
        if b == "No":
            return False
    except ValueError:
        err_console.print(f"Could not convert '{b}' to bool")
        return None


@lru_cache(maxsize=1024)
def bandwidth_to_bandwidth(b: str) -> int | None:  # noqa: PLR0911
    """Convert 76.8 GB/s to 76800000000.

    Args:
        b (str): The value to convert.

    Returns:
        int: The value in bytes.
    """
    try:
        if not b:
            return None
        if b.isdigit():
            return int(b)
        if "TB/s" in b:
            return int(float(b.replace("TB/s", "")) * 1_000_000_000_000)
        if "GB/s" in b:
            return int(float(b.replace("GB/s", "")) * 1_000_000_000)
        if "MB/s" in b:
            return int(float(b.replace("MB/s", "")) * 1_000_000)
        if "KB/s" in b:
            return int(float(b.replace("KB/s", "")) * 1_000)
        if "B/s" in b:
            return int(float(b.replace("B/s", "")))
        return int(b)
    except ValueError:
        err_console.print(f"Could not convert '{b}' to bytes")
        return None


@lru_cache(maxsize=1024)
def float_to_float(f: str) -> float | None:
    """Convert 2.8 to 2.8.

    Args:
        f (str): The value to convert.

    Returns:
        float: The value in float.
    """
    try:
        if not f:
            return None
        if f.isdigit():
            return float(f)
        return float(f)
    except ValueError:
        err_console.print(f"Could not convert '{f}' to float")
        return None


@lru_cache(maxsize=1024)
def bit_to_bit(b: str) -> int | None:
    """Convert 64-bit to 64.

    Args:
        b (str): The value to convert.

    Returns:
        int: The value in int.
    """
    try:
        if not b:
            return None
        if b.isdigit():
            return int(b)
        return int(b.replace("-bit", ""))
    except ValueError:
        err_console.print(f"Could not convert '{b}' to int (bit)")
        return None


@lru_cache(maxsize=1024)
def temp_to_temp(t: str) -> float | None:  # noqa: PLR0911
    """Convert 100 °C to 100.

    Args:
        t (str): The value to convert.

    Returns:
        float: The value in float.
    """
    try:
        if not t:
            return None
        if t.isdigit():
            return float(t)
        if "°C" in t:
            temp = float(t.replace("°C", ""))
            print(f"Temp in C: {t} -> {temp} Celsius")
            return temp
        if "°F" in t:
            temp: float = (float(t.replace("°F", "")) - 32) * 5.0 / 9.0
            print(f"Temp in F: {t} -> {temp} Celsius")
            return temp
        if "K" in t:
            temp = float(t.replace("K", "")) - 273.15
            print(f"Temp in K: {t} -> {temp} Celsius")
            return temp

        print(f"Could not convert '{t}' to float (temp)")
        return float(t)
    except ValueError:
        err_console.print(f"Could not convert '{t}' to float (temp)")
        return None


@lru_cache(maxsize=1024)
def dollar_to_cents(d: str) -> int | None:
    """Convert $100 to 10000.

    Args:
        d (str): The value to convert.

    Returns:
        int: The value in int.
    """
    try:
        if not d:
            return None
        if d.isdigit():
            return int(d)

        d = d.replace(",", "")

        if "$" in d:
            return int(float(d.replace("$", "")) * 100)
        if "USD" in d:
            return int(float(d.replace("USD", "")) * 100)
        return int(d)
    except ValueError:
        err_console.print(f"Could not convert '{d}' to int (dollar)")
        return None
