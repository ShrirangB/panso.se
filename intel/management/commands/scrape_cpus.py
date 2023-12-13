from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from functools import lru_cache
from itertools import batched
from typing import TYPE_CHECKING, Any

import hishel
from django.core.management.base import BaseCommand, CommandError
from loguru import logger
from selectolax.lexbor import LexborHTMLParser, LexborNode

from intel.management.commands.product_ids import product_ids

if TYPE_CHECKING:
    from collections.abc import Generator

    from httpx import Response

storage = hishel.FileStorage(
    ttl=60 * 60 * 24 * 7,  # 1 week
)


@dataclass(frozen=True)
class ProcessorData:
    """Data about a processor."""

    html: str
    ids: str


def get_html() -> Generator[ProcessorData, Any, None]:
    """Get the HTML from Intel ARK so we can parse it."""
    # Split the URLs into batches of 100
    for batch in list(batched(product_ids, 100)):
        ids: str = ",".join(batch)
        url: str = f"https://www.intel.com/content/www/us/en/products/compare.html?productIds={ids}"
        logger.info(f"Visiting {url}")
        with hishel.CacheClient(storage=storage) as client:
            response: Response = client.get(url)
            processor_data: ProcessorData = ProcessorData(html=response.text, ids=ids)
            yield processor_data


@lru_cache
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


@lru_cache
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


@lru_cache
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


@lru_cache
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


@lru_cache
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


@lru_cache
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


def add_to_database(data: list[LexborNode], _id: str) -> dict | None:  # noqa: PLR0912, C901, PLR0915
    """Add the processor to the database."""
    node: LexborNode
    defaults: dict | None = {}
    for node in data:
        node_attributes: dict[str, str | None] = node.attributes
        if not node_attributes:
            logger.info(f"Could not find attributes for {_id}")
            return None
        if "data-key" in node_attributes:
            data_key: str | None = node_attributes["data-key"]
            if not data_key:
                logger.info(f"Could not find data-key for {_id}")
                return None

            if data_key == "ProductGroup":  # Intel® Xeon® D Processor
                defaults["product_collection"] = node.text(strip=True) or None

            if data_key == "MarketSegment":  # Server
                defaults["vertical_segment"] = node.text(strip=True) or None

            if data_key == "ProcessorNumber":  # D-2738
                defaults["processor_number"] = node.text(strip=True) or None

            if data_key == "Lithography":  # 10 nm
                defaults["Lithography"] = node.text(strip=True) or None

            if data_key == "CertifiedUseConditions":  # Automotive, Base Transceiver Station
                defaults["use_conditions"] = node.text(strip=True) or None

            # TODO: Add l3_cache
            # TODO: Add recommended_customer_price. We should check if the value starts with "$" and then remove it
            if data_key == "CoreCount":  # 8
                defaults["total_cores"] = int(node.text(strip=True)) or None

            if data_key == "PerfCoreCount":  # 8
                defaults["performance_cores"] = int(node.text(strip=True)) or None

            if data_key == "ThreadCount":  # 16
                defaults["total_threads"] = int(node.text(strip=True)) or None

            if data_key == "ClockSpeedMax":  # 2.8 GHz -> 2800000000
                defaults["max_turbo_frequency"] = hertz_an_hertz(node.text(strip=True))

            if data_key == "ClockSpeed":  # 2.2 GHz -> 2200000000
                defaults["base_frequency"] = hertz_an_hertz(node.text(strip=True))

            if data_key == "Cache":  # 16.5 MB
                defaults["cache"] = node.text(strip=True) or None

            if data_key == "UltraPathInterconnectLinks":  # 0
                defaults["upi_links"] = int(node.text(strip=True)) or None

            if data_key == "MaxTDP":  # 65 W -> 65
                defaults["tdp"] = watt_to_watt(node.text(strip=True))

            if data_key == "DeepLearningBoostVersion":  # Yes -> True
                defaults["dl_boost_version"] = bool_to_bool(node.text(strip=True))

            if data_key == "EffCoreCount":  # 8
                defaults["efficiency_cores"] = int(node.text(strip=True)) or None

            if data_key == "TurboBoostMaxTechMaxFreq":  # 4.8 GHz -> 4800000000
                defaults["turbo_boost_max_technology_3_0_frequency"] = hertz_an_hertz(node.text(strip=True))

            if data_key == "PCoreTurboFreq":  # 4.8 GHz -> 4800000000
                defaults["single_performance_core_turbo_frequency"] = hertz_an_hertz(node.text(strip=True))

            if data_key == "ECoreTurboFreq":  # 4.5 GHz -> 4500000000
                defaults["single_efficiency_core_turbo_frequency"] = hertz_an_hertz(node.text(strip=True))

            if data_key == "ProcessorBasePower":  # 15 W -> 15
                defaults["processor_base_power"] = watt_to_watt(node.text(strip=True))

            if data_key == "MaxTurboPower":  # 64 W -> 64
                defaults["max_turbo_power"] = watt_to_watt(node.text(strip=True))

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
                    datetime_object: datetime = datetime.strptime(date_string, "%m/%d/%Y %I:%M:%S %p").astimezone()
                    date_part = datetime_object.date()
                    defaults["end_of_servicing_updates_date"] = date_part
                else:
                    defaults["end_of_servicing_updates_date"] = None

            if data_key == "MaxMem":  # 1 TB -> 1000000000000
                defaults["max_memory_size"] = bytes_to_bytes(node.text(strip=True))

            if data_key == "MemoryTypes":  # DDR4
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
                defaults["physical_address_extensions"] = node.text(strip=True) or None

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

            if data_key == "PackageSize":
                defaults["package_size"] = node.text(strip=True) or None

            if data_key == "MaxCPUs":
                defaults["max_cpu_configuration"] = int(node.text(strip=True)) or None

            if data_key == "OperatingTemperature":
                defaults["operating_temperature_range"] = node.text(strip=True) or None

            if data_key == "OperatingTemperatureMax":
                defaults["operating_temperature_max"] = int(node.text(strip=True)) or None

            if data_key == "OperatingTemperatureMin":
                defaults["operating_temperature_min"] = int(node.text(strip=True)) or None

            if data_key == "ThermalSolutionSpecification":
                defaults["thermal_solution_specification"] = node.text(strip=True) or None

            if data_key == "TCase":
                defaults["t_case"] = node.text(strip=True) or None

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

            if data_key == "DeepLearningBoostVersion":
                defaults["deep_learning_boost"] = bool_to_bool(node.text(strip=True))

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

            for key, value in defaults.items():
                if not value:
                    continue
                if not isinstance(value, str):
                    continue
                defaults[key] = value.replace("®", "")
                defaults[key] = value.replace("™", "")
                defaults[key] = value.replace("©", "")

    return defaults


def parse_html(processor_data: ProcessorData) -> None:
    """Parse the HTML from Intel ARK."""
    html: str = processor_data.html
    ids: str = processor_data.ids
    parser: LexborHTMLParser = LexborHTMLParser(html=html)
    for _id in ids.split(","):
        selector = f'[data-product-id="{_id}"]'
        data: list[LexborNode] = parser.css(selector)
        if not data:
            logger.info(f"Could not find {_id}")
            continue

        add_to_database(data, _id=_id)


class Command(BaseCommand):
    """Scrape Intel ARK."""

    help: str = __doc__ or ""  # noqa: A003
    requires_migrations_checks = True

    def handle(self: BaseCommand, *args: str, **options: str) -> None:  # noqa: PLR6301, ARG002
        """Handle the command."""
        try:
            for data in get_html():
                parse_html(processor_data=data)
        except KeyboardInterrupt:
            msg = "Got keyboard interrupt while scraping Intel ARK"
            raise CommandError(msg) from KeyboardInterrupt
        except Exception as e:  # noqa: BLE001
            raise CommandError(e) from e
