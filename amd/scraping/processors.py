from __future__ import annotations

from typing import TYPE_CHECKING

import hishel
from django.core.management.base import CommandError
from selectolax.lexbor import LexborHTMLParser, LexborNode

from data_converters import bytes_to_bytes, dollar_to_cents, hertz_an_hertz

if TYPE_CHECKING:
    from httpx import Response

storage = hishel.FileStorage(ttl=60 * 60 * 24 * 7)  # 1 week


def get_processor_data() -> None:  # noqa: C901, PLR0915, PLR0912
    """Get all processor data from AMD's website."""
    url = "https://www.amd.com/en/products/specifications/processors"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"
    with hishel.CacheClient(storage=storage) as client:
        response: Response = client.get(url=url, timeout=5, headers={"User-Agent": user_agent})

    if response.is_client_error:
        msg: str = f"Got client error while getting processor data. {response.text}"
        raise CommandError(msg)

    if not response.text:
        msg: str = f"Got empty response while getting processor data. {response.text}"
        raise CommandError(msg)

    parser = LexborHTMLParser(response.text)
    data: list[LexborNode] = parser.css("tr")
    for row in data:
        defaults: dict | None = {}
        # Loop through all the table rows and get the data
        for cell in row.css("td"):
            if not cell.attributes:
                continue

            header: str | None = cell.attributes["headers"]
            if not header:
                continue

            if "view-name-table-column" in header:
                # TODO: Remove (OEM Only) from the name?
                # TODO: There are several processors with "Microsoft Surface® Edition" in the name. Should we remove that and add it as a separate field?  # noqa: E501
                defaults["name"] = cell.text(strip=True) or None

            elif "view-product-type-table-column" in header:
                defaults["family"] = cell.text(strip=True) or None

            elif "view-name-table-column" in header:
                defaults["model"] = cell.text(strip=True) or None

            elif "view-product-type-table-column" in header:
                defaults["family"] = cell.text(strip=True) or None

            elif "view-product-type-1-table-column" in header:
                defaults["line"] = cell.text(strip=True) or None

            elif "view-platform-table-column" in header:
                defaults["platform"] = cell.text(strip=True) or None

            elif "view-field-opn-tray-table-column" in header:
                defaults["product_id_tray"] = cell.text(strip=True) or None

            elif "view-field-opn-pib-table-column" in header:
                defaults["product_id_boxed"] = cell.text(strip=True) or None

            elif "view-field-opn-mpk-table-column" in header:
                defaults["product_id_mpk"] = cell.text(strip=True) or None

            elif "view-field-launch-date-table-column" in header:
                defaults["launch_date"] = cell.text(strip=True) or None

            elif "view-field-cpu-core-count-table-column" in header:
                defaults["cpu_core_count"] = int(cell.text(strip=True)) if cell.text(strip=True) else None

            elif "view-field-thread-count-table-column" in header:
                defaults["thread_count"] = int(cell.text(strip=True)) if cell.text(strip=True) else None

            elif "view-field-gpu-core-count-table-column" in header:
                defaults["gpu_core_count"] = int(cell.text(strip=True)) if cell.text(strip=True) else None

            elif "view-field-cpu-clock-speed-table-column" in header:
                defaults["base_clock"] = hertz_an_hertz(cell.text(strip=True))

            elif "view-field-max-cpu-clock-speed-table-column" in header:
                defaults["max_boost_clock"] = hertz_an_hertz(cell.text(strip=True))

            elif "view-field-all-core-boost-speed-table-column" in header:
                defaults["all_core_boost_speed"] = hertz_an_hertz(cell.text(strip=True))

            elif "view-field-total-l1-cache-table-column" in header:
                defaults["l1_cache"] = bytes_to_bytes(cell.text(strip=True))

            elif "view-field-total-l2-cache-table-column" in header:
                defaults["l2_cache"] = bytes_to_bytes(cell.text(strip=True))

            elif "view-field-total-l3-cache-table-column" in header:
                defaults["l3_cache"] = bytes_to_bytes(cell.text(strip=True))

            elif "view-field-1ku-pricing-table-column" in header:
                defaults["_1ku_pricing"] = dollar_to_cents(cell.text(strip=True))

            elif "view-field-unlocked-table-column" in header:
                defaults["unlocked_for_overclocking"] = cell.text(strip=True).lower() == "yes"

            elif "view-field-cmos-table-column" in header:
                defaults["processor_technology"] = cell.text(strip=True) or None

            elif "view-field-socket-table-column" in header:
                defaults["cpu_socket"] = cell.text(strip=True) or None

            elif "view-field-socket-count-table-column" in header:
                defaults["socket_count"] = cell.text(strip=True) or None

            elif "view-product-type-4-table-column" in header:
                defaults["pci_express_version"] = cell.text(strip=True) or None

            elif "view-field-thermal-solution-table-column" in header:
                defaults["thermal_solution_pib"] = cell.text(strip=True) or None

            elif "view-recommended-cooler-table-column" in header:
                defaults["recommended_cooler"] = cell.text(strip=True) or None

            elif "view-field-thermal-solution-mpk-table-column" in header:
                defaults["thermal_solution_mpk"] = cell.text(strip=True) or None

            elif "view-field-default-tdp-table-column" in header:
                defaults["default_tdp"] = cell.text(strip=True) or None

            elif "view-field-ctdp-table-column" in header:
                defaults["configurable_tdp"] = cell.text(strip=True) or None

            elif "view-field-max-temps-table-column" in header:
                defaults["max_temps"] = cell.text(strip=True) or None

            elif "view-field-os-support-table-column" in header:
                defaults["os_support"] = cell.text(strip=True) or None

            elif "view-field-max-memory-speed-table-column" in header:
                defaults["max_memory_speed"] = cell.text(strip=True) or None

            elif "view-product-type-6-table-column" in header:
                defaults["system_memory_type"] = cell.text(strip=True) or None

            elif "view-field-memory-channels-table-column" in header:
                defaults["memory_channels"] = int(cell.text(strip=True)) if cell.text(strip=True) else None

            elif "view-field-per-socket-mem-bw-table-column" in header:
                defaults["per_socket_mem_bw"] = cell.text(strip=True) or None

            elif "view-field-gpu-clock-speed-table-column" in header:
                defaults["gpu_clock_speed"] = hertz_an_hertz(cell.text(strip=True))

            elif "view-product-type-2-table-column" in header:
                defaults["graphics_model"] = cell.text(strip=True) or None

            elif "view-supported-technologies-table-column" in header:
                defaults["supported_technologies"] = cell.text(strip=True) or None

            elif "view-field-workload-affinity-table-column" in header:
                defaults["workload_affinity"] = cell.text(strip=True) or None

            elif "view-amd-ryzen-ai-table-column" in header:
                defaults["amd_ryzen_ai"] = cell.text(strip=True) or None

            elif "view-field-fips-certification-table-column" in header:
                defaults["fips_certification"] = cell.text(strip=True) or None

            elif "view-field-fips-certification-links-table-column" in header:
                defaults["fips_certification_links"] = cell.text(strip=True) or None

            for key, value in defaults.items():
                if not value:
                    continue
                if not isinstance(value, str):
                    continue
                defaults[key] = value.replace("®", "")
                defaults[key] = value.replace("™", "")
                defaults[key] = value.replace("©", "")
                defaults[key] = value.strip()

        if defaults:
            # Print the data
            pass
