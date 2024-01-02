"""AMD models.

Current models:
    - Processor
        A AMD processor.
"""

from __future__ import annotations

import typing

from django.db import models


class Processor(models.Model):
    """A AMD processor."""

    model = models.TextField(
        help_text="Processor model",
        null=True,
        blank=True,
    )
    family = models.TextField(
        help_text="Processor family",
        null=True,
        blank=True,
    )
    line = models.TextField(
        help_text="Processor line",
        null=True,
        blank=True,
    )
    platform = models.TextField(
        help_text="Processor platform",
        null=True,
        blank=True,
    )
    product_id_tray = models.TextField(
        help_text="Product ID Tray",
        null=True,
        blank=True,
    )
    product_id_boxed = models.TextField(
        help_text="Product ID Boxed",
        null=True,
        blank=True,
    )
    product_id_mpk = models.TextField(
        help_text="Product ID MPK",
        null=True,
        blank=True,
    )
    launch_date = models.DateField(
        help_text="Processor launch date",
        null=True,
        blank=True,
    )
    cpu_core_count = models.IntegerField(
        help_text="Number of CPU cores",
        null=True,
        blank=True,
    )
    thread_count = models.IntegerField(
        help_text="Number of threads",
        null=True,
        blank=True,
    )
    gpu_core_count = models.IntegerField(
        help_text="Number of graphics core",
        null=True,
        blank=True,
    )
    base_clock = models.BigIntegerField(
        help_text="Base clock speed in hertz",
        null=True,
        blank=True,
    )
    max_boost_clock = models.BigIntegerField(
        help_text="Max. Boost Clock in hertz",
        null=True,
        blank=True,
    )
    all_core_boost_speed = models.BigIntegerField(
        help_text="All Core Boost Speed in hertz",
        null=True,
        blank=True,
    )
    l1_cache = models.BigIntegerField(
        help_text="L1 Cache in bytes",
        null=True,
        blank=True,
    )
    l2_cache = models.BigIntegerField(
        help_text="L2 Cache in bytes",
        null=True,
        blank=True,
    )
    l3_cache = models.BigIntegerField(
        help_text="L3 Cache in bytes",
        null=True,
        blank=True,
    )
    _1ku_pricing = models.BigIntegerField(
        help_text="1kU Pricing in dollar cents",
        null=True,
        blank=True,
    )
    unlocked_for_overclocking = models.BooleanField(
        help_text="Unlocked for Overclocking",
        null=True,
        blank=True,
    )
    processor_technology = models.TextField(
        help_text="Processor Technology for CPU Cores",
        null=True,
        blank=True,
    )
    cpu_socket = models.TextField(
        help_text="CPU Socket",
        null=True,
        blank=True,
    )
    socket_count = models.TextField(
        help_text="Socket Count",
        null=True,
        blank=True,
    )
    pci_express_version = models.TextField(
        help_text="PCI Express® Version",
        null=True,
        blank=True,
    )
    thermal_solution_pib = models.TextField(
        help_text="Thermal Solution PIB",
        null=True,
        blank=True,
    )
    recommended_cooler = models.TextField(
        help_text="Recommended Cooler",
        null=True,
        blank=True,
    )
    thermal_solution_mpk = models.TextField(
        help_text="Thermal Solution MPK",
        null=True,
        blank=True,
    )
    default_tdp = models.TextField(
        help_text="Default TDP",
        null=True,
        blank=True,
    )
    configurable_tdp = models.TextField(
        help_text="AMD Configurable TDP (cTDP)",
        null=True,
        blank=True,
    )
    max_temps = models.TextField(
        help_text="Max. Operating Temperature (Tjmax)",
        null=True,
        blank=True,
    )
    os_support = models.TextField(
        help_text="Operating System Support",
        null=True,
        blank=True,
    )
    max_memory_speed = models.TextField(
        help_text="System Memory Specification",
        null=True,
        blank=True,
    )
    system_memory_type = models.TextField(
        help_text="System Memory Type",
        null=True,
        blank=True,
    )
    memory_channels = models.IntegerField(
        help_text="Memory Channels",
        null=True,
        blank=True,
    )
    per_socket_mem_bw = models.TextField(
        help_text="Per Socket Mem BW",
        null=True,
        blank=True,
    )
    gpu_clock_speed = models.FloatField(
        help_text="Graphics Frequency",
        null=True,
        blank=True,
    )
    graphics_model = models.TextField(
        help_text="Graphics Model",
        null=True,
        blank=True,
    )
    supported_technologies = models.TextField(
        help_text="Supported Technologies",
        null=True,
        blank=True,
    )
    workload_affinity = models.TextField(
        help_text="Workload Affinity",
        null=True,
        blank=True,
    )
    amd_ryzen_ai = models.TextField(
        help_text="AMD Raven™ AI",
        null=True,
        blank=True,
    )
    fips_certification = models.TextField(
        help_text="FIPS Certification",
        null=True,
        blank=True,
    )
    fips_certification_links = models.TextField(
        help_text="FIPS Certification Links",
        null=True,
        blank=True,
    )

    class Meta:
        """https://docs.djangoproject.com/en/5.0/ref/models/options/."""

        ordering: typing.ClassVar[list[str]] = ["launch_date"]
        verbose_name: str = "Processor"
        verbose_name_plural: str = "Processors"
        db_table: str = "amd_processors"
        db_table_comment: str = "AMD Processors and their specifications"

    def __str__(self: Processor) -> str:
        """Return the CPU model."""
        return self.model or "No model found"
