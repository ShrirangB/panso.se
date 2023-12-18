from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from itertools import batched
from typing import TYPE_CHECKING, Any

import dateparser
import hishel
from django.core.management.base import BaseCommand, CommandError
from rich import print
from rich.console import Console
from rich.progress import track
from selectolax.lexbor import LexborHTMLParser, LexborNode

from intel.management.commands._product_ids import product_ids
from intel.models import Processor

if TYPE_CHECKING:
    from collections.abc import Generator
    from datetime import datetime

    from httpx import Response
from django.db import transaction

storage = hishel.FileStorage(ttl=60 * 60 * 24 * 7)  # 1 week
err_console = Console(stderr=True)


@dataclass(frozen=True)
class ProcessorData:
    """Data about a processor."""

    html: str
    ids: str


def get_html() -> Generator[ProcessorData, Any, None]:
    """Get the HTML from Intel ARK so we can parse it."""
    for batch in list(batched(product_ids, 100)):
        ids: str = ",".join(batch)
        url: str = f"https://www.intel.com/content/www/us/en/products/compare.html?productIds={ids}"
        print(f"Visiting {url}")
        with hishel.CacheClient(storage=storage) as client:
            response: Response = client.get(url=url, timeout=60)
            processor_data: ProcessorData = ProcessorData(html=response.text, ids=ids)
            yield processor_data


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
    if not hz:
        return None
    if hz.isdigit():
        return int(hz)
    if "THz" in hz:
        return int(float(hz.replace("THz", "")) * 1_000_000_000_000)
    if "GHz" in hz:
        return int(float(hz.replace("GHz", "")) * 1_000_000_000)
    if "MHz" in hz:
        return int(float(hz.replace("MHz", "")) * 1_000_000)
    if "KHz" in hz:
        return int(float(hz.replace("KHz", "")) * 1_000)
    return int(hz)


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
    return int(b)


@lru_cache(maxsize=1024)
def watt_to_watt(w: str) -> int | None:
    """Convert 11 W to 11.

    Args:
        w (str): The value to convert.

    Returns:
        int: The value in W.
    """
    if not w:
        return None
    if w.isdigit():
        return int(w)

    return int(float(w.replace("W", "")))


@lru_cache(maxsize=1024)
def bool_to_bool(b: str) -> bool | None:
    """Convert Yes to True and No to False.

    Args:
        b (str): The value to convert.

    Returns:
        bool: The value in bool.
    """
    if not b:
        return None

    if b == "Yes":
        return True
    if b == "No":
        return False
    return None


@lru_cache(maxsize=1024)
def bandwidth_to_bandwidth(b: str) -> int | None:
    """Convert 76.8 GB/s to 76800000000.

    Args:
        b (str): The value to convert.

    Returns:
        int: The value in bytes.
    """
    if not b:
        return None
    if b.isdigit():
        return int(b)
    if "GB/s" in b:
        return int(float(b.replace("GB/s", "")) * 1_000_000_000)
    if "MB/s" in b:
        return int(float(b.replace("MB/s", "")) * 1_000_000)
    if "KB/s" in b:
        return int(float(b.replace("KB/s", "")) * 1_000)
    return int(b)


@lru_cache(maxsize=1024)
def float_to_float(f: str) -> float | None:
    """Convert 2.8 to 2.8.

    Args:
        f (str): The value to convert.

    Returns:
        float: The value in float.
    """
    if not f:
        return None
    if f.isdigit():
        return float(f)
    return float(f)


@lru_cache(maxsize=1024)
def bit_to_bit(b: str) -> int | None:
    """Convert 64-bit to 64.

    Args:
        b (str): The value to convert.

    Returns:
        int: The value in int.
    """
    if not b:
        return None
    if b.isdigit():
        return int(b)
    return int(b.replace("-bit", ""))


@lru_cache(maxsize=1024)
def temp_to_temp(t: str) -> float | None:
    """Convert 100 °C to 100.

    Args:
        t (str): The value to convert.

    Returns:
        float: The value in float.
    """
    if not t:
        return None
    if t.isdigit():
        return float(t)
    return float(t.replace("°C", ""))


@lru_cache(maxsize=1024)
def dollar_to_cents(d: str) -> int | None:
    """Convert $100 to 10000.

    Args:
        d (str): The value to convert.

    Returns:
        int: The value in int.
    """
    if not d:
        return None
    if d.isdigit():
        return int(d)
    return int(float(d.replace("$", "")) * 100)


def create_defaults(data: list[LexborNode], _id: str) -> dict | None:  # noqa: PLR0912, C901, PLR0915
    """Create the defaults for the processor.

    Args:
        data (list[LexborNode]): The data to parse.
        _id (str): The ID of the processor.

    Returns:
        dict: The defaults for the processor that we can use to create the processor object.
    """
    node: LexborNode
    defaults: dict | None = {}
    for node in data:
        node_attributes: dict[str, str | None] = node.attributes
        if not node_attributes:
            err_console.print(f"Could not find attributes for {_id}")
            return None

        if "class" in node_attributes:
            class_value: str | None = node_attributes["class"]
            price_regex = r"\$\d+.\d+"
            if class_value and class_value.startswith("$") and re.match(pattern=price_regex, string=class_value):
                price: int | None = dollar_to_cents(d=class_value)
                defaults["recommended_customer_price"] = price

        if "data-key" in node_attributes:
            # TODO: Add OnDemandAvailableUpgrade
            # TODO: We should check if we are missing any fields.

            data_key: str | None = node_attributes["data-key"]
            if not data_key:
                err_console.print(f"Could not find data-key for {_id}")
                return None

            # Product Collection - Intel® Xeon® D Processor
            if data_key == "ProductGroup":
                defaults["product_collection"] = node.text(strip=True) or None

            # Vertical Segment - Server
            if data_key == "MarketSegment":
                defaults["vertical_segment"] = node.text(strip=True) or None

            # Processor Number - D-2738
            if data_key == "ProcessorNumber":
                defaults["processor_number"] = node.text(strip=True) or None

            # Lithography - 14 nm
            if data_key == "Lithography":
                defaults["lithography"] = node.text(strip=True) or None

            # Use Conditions - Automotive, Base Transceiver Station
            if data_key == "CertifiedUseConditions":
                defaults["use_conditions"] = node.text(strip=True) or None

            # Total Cores - 8
            if data_key == "CoreCount":
                defaults["total_cores"] = int(node.text(strip=True)) or None

            # # of Performance-cores - 8
            if data_key == "PerfCoreCount":
                defaults["performance_cores"] = int(node.text(strip=True)) or None

            # Total Threads - 16
            if data_key == "ThreadCount":
                defaults["total_threads"] = int(node.text(strip=True)) or None

            # of Efficient-cores - 8
            if data_key == "EffCoreCount":
                defaults["efficiency_cores"] = int(node.text(strip=True)) or None

            # Max Turbo Frequency - 2.8 GHz (Converts to 2800000000)
            if data_key == "ClockSpeedMax":
                defaults["max_turbo_frequency"] = hertz_an_hertz(node.text(strip=True))

            # Processor Base Frequency - 2.2 GHz (Converts to 2200000000)
            if data_key == "ClockSpeed":
                defaults["base_frequency"] = hertz_an_hertz(node.text(strip=True))

            # Cache - 16.5 MB
            if data_key == "Cache":
                defaults["cache"] = node.text(strip=True) or None

            if data_key == "UltraPathInterconnectLinks":  # 0
                defaults["upi_links"] = int(node.text(strip=True)) or None

            # TDP - 65 W (Converts to 65)
            if data_key == "MaxTDP":
                defaults["tdp"] = watt_to_watt(node.text(strip=True))

            if data_key == "Bus":
                defaults["bus_speed"] = node.text(strip=True) or None

            if data_key == "TurboBoostMaxTechMaxFreq":  # 4.8 GHz -> 4800000000
                defaults["turbo_boost_max_technology_3_0_frequency"] = hertz_an_hertz(node.text(strip=True))

            if data_key == "PCoreTurboFreq":  # 4.8 GHz -> 4800000000
                defaults["single_performance_core_turbo_frequency"] = hertz_an_hertz(node.text(strip=True))

            if data_key == "ECoreTurboFreq":  # 4.5 GHz -> 4500000000
                defaults["single_efficiency_core_turbo_frequency"] = hertz_an_hertz(node.text(strip=True))

            if data_key == "ProcessorBasePower":  # 15 W -> 15
                defaults["processor_base_power"] = watt_to_watt(node.text(strip=True))

            if data_key == "MaxTurboPower":  # 64 W -> 64
                defaults["max_turbo_frequency"] = watt_to_watt(node.text(strip=True))

            if data_key == "AssuredPowerMin":  # 15 W -> 15
                defaults["min_assured_power"] = watt_to_watt(node.text(strip=True))

            if data_key == "AssuredPowerMax":  # 64 W -> 64
                defaults["max_assured_power"] = watt_to_watt(node.text(strip=True))

            if data_key == "BusNumPorts":  # 0
                defaults["number_of_qpi_links"] = int(node.text(strip=True)) or None

            if data_key == "PCoreBaseFreq":  # 2.8 GHz -> 2800000000
                defaults["p_core_base_frequency"] = hertz_an_hertz(node.text(strip=True))

            if data_key == "ECoreBaseFreq":  # 2.2 GHz -> 2200000000
                defaults["e_core_base_frequency"] = hertz_an_hertz(node.text(strip=True))

            if data_key == "TotalL2Cache":  # 24 MB
                defaults["l2_cache"] = node.text(strip=True) or None

            if data_key == "ThermalVelocityBoostFreq":  # 4.4 GHz -> 4400000000
                defaults["thermal_velocity_boost_frequency"] = hertz_an_hertz(node.text(strip=True))

            if data_key == "TurboBoostTech2MaxFreq":  # 4.8 GHz -> 4800000000
                defaults["turbo_boost_2_0_frequency"] = hertz_an_hertz(node.text(strip=True))

            if data_key == "StatusCodeText":  # Launched
                defaults["marketing_status"] = node.text(strip=True) or None

            if data_key == "BornOnDate":  # Q4'20
                defaults["launch_date"] = node.text(strip=True) or None

            if data_key == "Embedded":  # Yes -> True
                defaults["embedded_options_available"] = bool_to_bool(node.text(strip=True))

            # https://www.intel.com/content/www/us/en/products/docs/processors/xeon-d/network-segments-product-brief.html
            if data_key == "ProductBriefUrl":
                defaults["product_brief_url"] = node.text(strip=True) or None

            # https://www.intel.com/content/www/us/en/products/docs/processors/core/core-technical-resources.html
            if data_key == "DatasheetUrl":
                defaults["datasheet"] = node.text(strip=True) or None

            if data_key == "ServicingStatus":  # End of Servicing Lifetime
                defaults["servicing_status"] = node.text(strip=True) or None

            if data_key == "ESUDate":  # 6/30/2022 12:00:00 AM -> 2022-06-30
                date_string: str | None = node.text(strip=True) or None
                if date_string:
                    parsed_date: datetime | None = dateparser.parse(
                        date_string=date_string,
                        languages=["en"],
                        settings={"PREFER_DAY_OF_MONTH": "first"},
                    )
                    if parsed_date:
                        defaults["end_of_servicing_updates_date"] = parsed_date
                    else:
                        defaults["end_of_servicing_updates_date"] = None
                else:
                    defaults["end_of_servicing_updates_date"] = None

            if data_key == "MaxMem":  # 1 TB -> 1000000000000
                defaults["max_memory_size"] = bytes_to_bytes(node.text(strip=True))

            if data_key == "MemoryTypes":  # DDR4
                # TODO: Don't remove newlines
                defaults["memory_types"] = node.text(strip=True) or None

            if data_key == "MemoryMaxSpeedMhz":  # 2933 MHz -> 2933000000
                defaults["max_memory_speed"] = hertz_an_hertz(node.text(strip=True))

            if data_key == "NumMemoryChannels":  # 4
                defaults["max_number_of_memory_channels"] = int(node.text(strip=True)) or None

            if data_key == "OptaneDCPersistentMemoryVersion":  # No -> False
                defaults["optane_supported"] = bool_to_bool(node.text(strip=True))

            if data_key == "ECCMemory":  # Yes -> True
                defaults["ecc_memory_supported"] = bool_to_bool(node.text(strip=True))

            if data_key == "MaxMemoryBandwidth":  # 41.6 GB/s -> 41600000000
                defaults["max_memory_bandwidth"] = bandwidth_to_bandwidth(node.text(strip=True))

            if data_key == "PhysicalAddressExtension":  # 46-bit
                # TODO: Should we convert this to an int?
                defaults["physical_address_extensions"] = bit_to_bit(node.text(strip=True))

            if data_key == "ScalableSockets":  # 1S
                defaults["scalability"] = node.text(strip=True) or None

            if data_key == "PCIExpressRevision":  # 4.0
                defaults["pci_express_revision"] = node.text(strip=True) or None

            if data_key == "MicroprocessorPCIeRevision":
                defaults["microprocessor_pcie_revision"] = node.text(strip=True) or None

            if data_key == "ChipsetPCHPCIeRevision":
                defaults["chipset_pch_pcie_revision"] = node.text(strip=True) or None

            if data_key == "NumPCIExpressPorts":
                defaults["max_amount_of_pci_express_lanes"] = int(node.text(strip=True)) or None

            if data_key == "IntelThunderbolt4":
                defaults["thunderbolt_4_support"] = bool_to_bool(node.text(strip=True))

            if data_key == "DMIRevision":
                defaults["direct_media_interface_revision"] = node.text(strip=True) or None

            if data_key == "MaxDMILanesCount":
                defaults["max_amount_of_direct_media_interface_lanes"] = int(node.text(strip=True)) or None

            if data_key == "NumUSBPorts":
                defaults["number_of_usb_ports"] = int(node.text(strip=True)) or None

            if data_key == "USBRevision":
                defaults["usb_revision"] = node.text(strip=True) or None

            if data_key == "IntegratedLAN":
                defaults["integrated_lan"] = bool_to_bool(node.text(strip=True))

            if data_key == "SATA6PortCount":
                defaults["number_of_sata_6_0_ports"] = int(node.text(strip=True)) or None

            if data_key == "USBConfigurationDescription":
                defaults["usb_configuration"] = node.text(strip=True) or None

            if data_key == "NumSATAPorts":
                defaults["number_of_sata_ports"] = int(node.text(strip=True)) or None

            if data_key == "IntegratedIDE":
                defaults["integrated_ide"] = bool_to_bool(node.text(strip=True))

            if data_key == "GeneralPurposeIO":
                defaults["general_purpose_io"] = bool_to_bool(node.text(strip=True))

            if data_key == "UART":
                defaults["uart"] = node.text(strip=True) or None

            if data_key == "SocketsSupported":
                defaults["sockets_supported"] = node.text(strip=True) or None

            if data_key == "PackageCarrier":
                defaults["package_carrier"] = node.text(strip=True) or None

            if data_key == "DigitalThermalSensorTemperatureMax":
                defaults["digital_thermal_sensor_temperature_max"] = temp_to_temp(node.text(strip=True))

            if data_key == "PackageSize":
                defaults["package_size"] = node.text(strip=True) or None

            if data_key == "MaxCPUs":
                defaults["max_cpu_configuration"] = int(node.text(strip=True)) or None

            if data_key == "OperatingTemperature":  # -40 to 85
                defaults["operating_temperature_range"] = node.text(strip=True) or None

            if data_key == "OperatingTemperatureMax":
                defaults["operating_temperature_max"] = temp_to_temp(node.text(strip=True))

            if data_key == "OperatingTemperatureMin":
                defaults["operating_temperature_min"] = temp_to_temp(node.text(strip=True))

            if data_key == "ThermalSolutionSpecification":
                defaults["thermal_solution_specification"] = node.text(strip=True) or None

            if data_key == "TCase":
                defaults["t_case"] = temp_to_temp(node.text(strip=True))

            if data_key == "ResourceDirectorTechVersion":
                defaults["resource_director_technology"] = bool_to_bool(node.text(strip=True))

            if data_key == "OptaneMemorySupport":
                defaults["optane_supported"] = bool_to_bool(node.text(strip=True))

            if data_key == "TBTVersion":
                defaults["turbo_boost_technology"] = node.text(strip=True) or None

            if data_key == "HyperThreading":
                defaults["hyper_threading_technology"] = bool_to_bool(node.text(strip=True))

            if data_key == "EM64":
                defaults["_64_bit"] = bool_to_bool(node.text(strip=True))

            if data_key == "InstructionSet":
                defaults["instruction_set"] = node.text(strip=True) or None

            if data_key == "InstructionSetExtensions":
                defaults["instruction_set_extensions"] = node.text(strip=True) or None

            if data_key == "AVX512FusedMultiplyAddUnits":
                defaults["avx_512_fma_units"] = bool_to_bool(node.text(strip=True))

            if data_key == "SpeedstepTechnology":
                defaults["enhanced_speedstep_technology"] = bool_to_bool(node.text(strip=True))

            if data_key == "ThermalMonitoring2Indicator":
                defaults["thermal_monitoring_technologies"] = bool_to_bool(node.text(strip=True))

            if data_key == "QuickAssistTechnology":
                defaults["integrated_quick_assist_technology"] = bool_to_bool(node.text(strip=True))

            if data_key == "VolumeManagementDeviceVersion":
                defaults["volume_management_device"] = bool_to_bool(node.text(strip=True))

            if data_key == "TimeCoordinatedComputing":
                defaults["time_coordinated_computing"] = bool_to_bool(node.text(strip=True))

            if data_key == "GaussianNeuralAcceleratorVersion":
                defaults["gaussian_neural_accelerator"] = bool_to_bool(node.text(strip=True))

            if data_key == "IntelThreadDirector":
                defaults["thread_director"] = bool_to_bool(node.text(strip=True))

            if data_key == "ImageProcessingUnitVersion":
                defaults["image_processing_unit"] = bool_to_bool(node.text(strip=True))

            if data_key == "IntelSmartSoundTechnology":
                defaults["smart_sound_technology"] = bool_to_bool(node.text(strip=True))

            if data_key == "IntelWakeonVoice":
                defaults["wake_on_voice"] = bool_to_bool(node.text(strip=True))

            if data_key == "IntelHighDefinitionAudio":
                defaults["high_definition_audio"] = bool_to_bool(node.text(strip=True))

            if data_key == "MipiSoundwireVersion":
                defaults["mipi_soundwire_version"] = float_to_float(node.text(strip=True))

            # Intel® Deep Learning Boost (Intel® DL Boost) on CPU - Yes (Converts to True)
            if data_key == "DeepLearningBoostVersion":
                defaults["deep_learning_boost_version"] = node.text(strip=True) or None

            if data_key == "AdaptixTechVersion":
                defaults["adaptix_technology"] = bool_to_bool(node.text(strip=True))

            if data_key == "SpeedShiftTechVersion":
                defaults["speed_shift_technology"] = bool_to_bool(node.text(strip=True))

            if data_key == "TurboBoostMaxTechVersion":
                defaults["turbo_boost_max_technology_3_0"] = bool_to_bool(node.text(strip=True))

            if data_key == "FlexMemoryTechnology":
                defaults["flex_memory_access"] = bool_to_bool(node.text(strip=True))

            if data_key == "ThermalVelocityBoostVersion":
                defaults["thermal_velocity_boost"] = bool_to_bool(node.text(strip=True))

            if data_key == "HaltState":
                defaults["idle_states"] = bool_to_bool(node.text(strip=True))

            if data_key == "AdaptiveBoostTechVesion":
                defaults["adaptive_boost_technology"] = bool_to_bool(node.text(strip=True))

            if data_key == "TransactionalSynchronizationExtensionVersion":
                defaults["transactional_synchronization_extensions"] = bool_to_bool(node.text(strip=True))

            if data_key == "DemandBasedSwitching":
                defaults["demand_based_switching"] = bool_to_bool(node.text(strip=True))

            if data_key == "IdentityProtectionTechVersion":
                defaults["identity_protection_technology"] = bool_to_bool(node.text(strip=True))

            if data_key == "IntelQAssistSWAccel":
                defaults["quick_assist_software_acceleration"] = bool_to_bool(node.text(strip=True))

            if data_key == "IntelTotalMemoryEncryption":
                defaults["total_memory_encryption"] = bool_to_bool(node.text(strip=True))

            if data_key == "AESTech":
                defaults["aes_new_instructions"] = bool_to_bool(node.text(strip=True))

            if data_key == "SoftwareGuardExtensions":
                defaults["software_guard_extensions"] = node.text(strip=True) or None

            if data_key == "TXT":
                defaults["trusted_execution_technology"] = bool_to_bool(node.text(strip=True))

            if data_key == "ExecuteDisable":
                defaults["execute_disable_bit"] = bool_to_bool(node.text(strip=True))

            if data_key == "DeviceProtectionTechBootGuardVersion":
                defaults["boot_guard"] = bool_to_bool(node.text(strip=True))

            if data_key == "IntelPlatformFWResSupport":
                defaults["platform_firmware_resilience"] = bool_to_bool(node.text(strip=True))

            if data_key == "MaxEncSizeSupportIntelSGX":
                # TODO: For some reason this is bigger than 2^32
                # defaults["maximum_enclave_size_for_sgx"] = bytes_to_bytes(node.text(strip=True))
                pass

            if data_key == "IntelCryptoAcceleration":
                defaults["crypto_acceleration"] = bool_to_bool(node.text(strip=True))

            if data_key == "VTX":
                defaults["virtualization_technology"] = bool_to_bool(node.text(strip=True))

            if data_key == "VTD":
                defaults["virtualization_technology_for_directed_io"] = bool_to_bool(node.text(strip=True))

            if data_key == "VProTechnologyOptions":
                defaults["vpro_eligibility"] = bool_to_bool(node.text(strip=True))

            if data_key == "ThreatDetectTech":
                defaults["threat_detection_technology"] = bool_to_bool(node.text(strip=True))

            if data_key == "ActiveManagementTech":
                defaults["active_management_technology"] = bool_to_bool(node.text(strip=True))

            if data_key == "StandardManageability":
                defaults["standard_manageability"] = bool_to_bool(node.text(strip=True))

            if data_key == "RemotePlatformErase":
                defaults["remote_platform_erase"] = bool_to_bool(node.text(strip=True))

            if data_key == "OneClickRecovery":
                defaults["one_click_recovery"] = bool_to_bool(node.text(strip=True))

            if data_key == "IntelHardwareShield":
                defaults["hardware_shield"] = bool_to_bool(node.text(strip=True))

            if data_key == "IntelControlFlowEnforcementTechnology":
                defaults["control_flow_enforcement_technology"] = bool_to_bool(node.text(strip=True))

            if data_key == "IntelTotalMemoryEncryptionWithMultikey":
                defaults["total_memory_encryption_multi_key"] = bool_to_bool(node.text(strip=True))

            if data_key == "SecureKeyTechVersion":
                defaults["secure_key"] = bool_to_bool(node.text(strip=True))

            if data_key == "OSGuardTechVersion":
                defaults["os_guard"] = bool_to_bool(node.text(strip=True))

            if data_key == "ModeBasedExecutionControlVersion":
                defaults["mode_based_execute_control"] = bool_to_bool(node.text(strip=True))

            if data_key == "StableImagePlatformProgramVersion":
                defaults["stable_image_platform_program"] = bool_to_bool(node.text(strip=True))

            if data_key == "VTRP":
                defaults["virtualization_technology_with_redirect_protection"] = bool_to_bool(node.text(strip=True))

            if data_key == "ExtendedPageTables":
                defaults["virtualization_technology_with_extended_page_tables"] = bool_to_bool(node.text(strip=True))

            if data_key == "ProcessorGraphicsModelId":
                defaults["processor_graphics"] = node.text(strip=True) or None

            if data_key == "GraphicsMaxFreq":
                defaults["graphics_max_dynamic_frequency"] = hertz_an_hertz(node.text(strip=True))

            if data_key == "GraphicsOutput":
                defaults["graphics_output"] = node.text(strip=True) or None

            if data_key == "GraphicsExecutionUnits":
                defaults["execution_units"] = int(node.text(strip=True)) or None

            if data_key == "GraphicsMaxResolutionHDMI":
                defaults["max_resolution_hdmi"] = node.text(strip=True) or None

            if data_key == "GraphicsMaxResolutionDP":
                defaults["max_resolution_dp"] = node.text(strip=True) or None

            if data_key == "GraphicsMaxResolutionIFP":
                defaults["max_resolution_edp_integrated_flat_panel"] = node.text(strip=True) or None

            if data_key == "GraphicsDirectXSupport":
                defaults["directx_support"] = node.text(strip=True) or None

            if data_key == "GraphicsOpenGLSupport":
                defaults["opengl_support"] = node.text(strip=True) or None

            if data_key == "GraphicsOpenCLSupport":
                defaults["opencl_support"] = node.text(strip=True) or None

            if data_key == "MultiFormatCodecEngines":
                defaults["multi_format_codec_engines"] = node.text(strip=True) or None

            if data_key == "QuickSyncVideo":
                defaults["intel_quick_sync_video"] = bool_to_bool(node.text(strip=True))

            if data_key == "NumDisplaysSupported":
                defaults["number_of_displays_supported"] = int(node.text(strip=True)) or None

            if data_key == "GraphicsDeviceId":
                defaults["device_id"] = node.text(strip=True) or None

            if data_key == "GraphicsFreq":
                defaults["graphics_base_frequency"] = hertz_an_hertz(node.text(strip=True))

            if data_key == "Graphics4KSupportLevel":
                defaults["_4k_support"] = node.text(strip=True) or None

            if data_key == "CVTHD":
                defaults["intel_clear_video_hd_technology"] = bool_to_bool(node.text(strip=True))

            if data_key == "InTru3D":
                defaults["intel_in_tru_3d_technology"] = bool_to_bool(node.text(strip=True))

            if data_key == "ClearVideoTechnology":
                defaults["intel_clear_video_technology"] = bool_to_bool(node.text(strip=True))

            if data_key == "NetworkInterfaces":
                defaults["network_interfaces"] = node.text(strip=True) or None

            for key, value in defaults.items():
                if not value:
                    continue
                if not isinstance(value, str):
                    continue
                defaults[key] = value.replace("®", "")
                defaults[key] = value.replace("™", "")
                defaults[key] = value.replace("©", "")
    return defaults


def process_html(processor_data: ProcessorData) -> None:
    """Process the HTML from Intel ARK.

    Args:
        processor_data: The data about the processor.
    """
    html: str = processor_data.html
    ids: str = processor_data.ids
    parser: LexborHTMLParser = LexborHTMLParser(html=html)
    defaults: dict | None = None
    processors_to_update: list[Processor] = []
    for _id in track(sequence=ids.split(sep=","), description="Processing HTML..."):
        print(f"Processing {_id}")
        selector = f'[data-product-id="{_id}"]'
        data: list[LexborNode] = parser.css(selector)
        if not data:
            print(f"Could not find {_id}")
            continue

        defaults: dict | None = create_defaults(data=data, _id=_id)
        if not defaults:
            print(f"Could not create defaults for {_id}")
            continue

        # Get the names of the processors
        for child in data:
            arkproductlink: LexborNode | None = child.css_first('[data-component="arkproductlink"]')
            if not arkproductlink:
                continue
            name: str = arkproductlink.text(strip=True)
            name = name.replace("®", "")
            name = name.replace("™", "")
            name = name.replace("©", "")
            name = name.replace("Processor", "")
            name = name.replace("  ", " ")
            name = name.strip()

            try:
                with transaction.atomic():
                    processor: Processor = Processor.objects.get(product_id=_id)
                    processor.name = name
                    processor.save()
                    print(f"Updated {_id} with name {name}")
            except Processor.DoesNotExist:
                print(f"Could not find {_id}")
                continue

        processor = Processor(product_id=_id, **defaults)
        processors_to_update.append(processor)

    if defaults and processors_to_update:
        with transaction.atomic():
            Processor.objects.bulk_update(processors_to_update, fields=list(defaults.keys()))
    else:
        print("No processors to update")


class Command(BaseCommand):
    """Scrape Intel ARK."""

    help: str = __doc__ or ""  # noqa: A003
    requires_migrations_checks = True

    def handle(self: BaseCommand, *args: str, **options: str) -> None:  # noqa: PLR6301, ARG002
        """Handle the command."""
        try:
            for data in get_html():
                process_html(processor_data=data)
        except KeyboardInterrupt:
            msg = "Got keyboard interrupt while scraping Intel ARK"
            raise CommandError(msg) from KeyboardInterrupt
        except Exception as e:  # noqa: BLE001
            raise CommandError(e) from e
