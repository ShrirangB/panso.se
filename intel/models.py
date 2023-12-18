from __future__ import annotations

import typing

from django.db import models
from simple_history.models import HistoricalRecords


class ArkFilterData(models.Model):
    """The data from https://ark.intel.com/content/www/us/en/ark/search/featurefilter.html."""

    json_data = models.JSONField(verbose_name="Intel ARK Filter Data")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(
        table_name="ark_filter_data_history",
        excluded_fields=["created", "updated"],
    )

    class Meta:
        """Django metadata."""

        ordering: typing.ClassVar[list[str]] = ["-created"]
        verbose_name: str = "Intel ARK Filter Data"
        verbose_name_plural: str = "Intel ARK Filter Data"
        db_table: str = "ark_filter_data"
        db_table_comment: str = "Table storing Intel ARK Filter Data"

    def __str__(self: ArkFilterData) -> str:
        """Return the string representation of the model."""
        return f"Intel ARK Filter Data ({self.created})"


class Processor(models.Model):
    """The data from https://ark.intel.com/content/www/us/en/ark/search/featurefilter.html."""

    product_id = models.IntegerField(
        verbose_name="Product ID",
        help_text="The product ID of the processor.",
        primary_key=True,
    )

    name = models.TextField(
        verbose_name="Name",
        help_text="The name of the processor.",
        blank=True,
        null=True,
    )

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(
        table_name="ark_processors_history",
        excluded_fields=["created", "updated"],
    )

    # Essentials
    product_collection = models.TextField(
        verbose_name="Product Collection",
        help_text="The product family the processor belongs to.",
        blank=True,
        null=True,
    )
    vertical_segment = models.TextField(
        verbose_name="Vertical Segment",
        help_text="The vertical segment the processor belongs to.",
        blank=True,
        null=True,
    )
    processor_number = models.TextField(
        verbose_name="Processor Number",
        help_text="Server, Mobile, Desktop",
        blank=True,
        null=True,
    )
    lithography = models.TextField(
        verbose_name="Lithography",
        help_text="Die size",
        blank=True,
        null=True,
    )
    use_conditions = models.TextField(
        verbose_name="Use Conditions",
        help_text="The use conditions the processor is designed for.",
        blank=True,
        null=True,
    )
    recommended_customer_price = models.TextField(
        verbose_name="Recommended Customer Price",
        help_text="The recommended customer price for the processor.",
        blank=True,
        null=True,
    )

    # CPU Specifications
    total_cores = models.IntegerField(
        verbose_name="Total Cores",
        help_text="The number of cores the processor has.",
        blank=True,
        null=True,
    )
    total_threads = models.IntegerField(
        verbose_name="Total Threads",
        help_text="The number of threads the processor has.",
        blank=True,
        null=True,
    )
    max_turbo_frequency = models.BigIntegerField(
        verbose_name="Max Turbo Frequency",
        help_text="The maximum turbo frequency the processor can reach. In hertz.",
        blank=True,
        null=True,
    )
    base_frequency = models.BigIntegerField(
        verbose_name="Base Frequency",
        help_text="The base frequency the processor can reach. In hertz.",
        blank=True,
        null=True,
    )
    cache = models.TextField(
        verbose_name="Cache",
        help_text="The cache the processor has.",
        blank=True,
        null=True,
    )
    l2_cache = models.TextField(
        verbose_name="L2 Cache",
        help_text="The L2 cache the processor has.",
        blank=True,
        null=True,
    )

    upi_links = models.IntegerField(
        verbose_name="UPI Links",
        help_text="The number of Intel Ultra Path Interconnect links the processor has.",
        blank=True,
        null=True,
    )
    tdp = models.IntegerField(
        verbose_name="TDP",
        help_text="The Thermal Design Power of the processor. In watts.",
        blank=True,
        null=True,
    )
    turbo_boost_2_0_frequency = models.BigIntegerField(
        verbose_name="Turbo Boost 2.0 Frequency",
        help_text="The maximum turbo frequency the processor can reach. In hertz.",
        blank=True,
        null=True,
    )
    turbo_boost_max_technology_3_0_frequency = models.BigIntegerField(
        verbose_name="Turbo Boost Max Technology 3.0 Frequency",
        help_text="The maximum turbo frequency the processor can reach. In hertz.",
        blank=True,
        null=True,
    )
    single_performance_core_turbo_frequency = models.BigIntegerField(
        verbose_name="Single P-core Turbo Frequency",
        help_text="How many hertz a single P-core can reach.",
        blank=True,
        null=True,
    )
    single_efficiency_core_turbo_frequency = models.BigIntegerField(
        verbose_name="Single E-core Turbo Frequency",
        help_text="How many hertz a single E-core can reach.",
        blank=True,
        null=True,
    )

    number_of_qpi_links = models.IntegerField(
        verbose_name="Number of QPI Links",
        help_text="The number of Intel QuickPath Interconnect links the processor has.",
        blank=True,
        null=True,
    )
    bus_speed = models.TextField(
        verbose_name="Bus Speed",
        help_text="The bus speed of the processor. In giga-transfers per second.",
        blank=True,
        null=True,
    )
    configurable_tdp_down_frequency = models.BigIntegerField(
        verbose_name="Configurable TDP-down Frequency",
        help_text="The configurable TDP-down frequency of the processor. In hertz.",
        blank=True,
        null=True,
    )
    configurable_tdp_down = models.IntegerField(
        verbose_name="Configurable TDP-down",
        help_text="The configurable TDP-down of the processor. In watts.",
        blank=True,
        null=True,
    )
    thermal_velocity_boost_frequency = models.BigIntegerField(
        verbose_name="Thermal Velocity Boost Frequency",
        help_text="The thermal velocity boost frequency of the processor. In hertz.",
        blank=True,
        null=True,
    )
    # TODO: Should this be converted to a BigIntegerField?
    upi_speed = models.TextField(
        verbose_name="UPI Speed",
        help_text="The UPI speed of the processor. In giga-transfers per second.",
        blank=True,
        null=True,
    )
    speedstep_max_frequency = models.IntegerField(
        verbose_name="SpeedStep Max Frequency",
        help_text="The maximum SpeedStep frequency of the processor. In hertz.",
        blank=True,
        null=True,
    )
    performance_cores = models.IntegerField(
        verbose_name="Performance Cores",
        help_text="The number of performance cores the processor has.",
        blank=True,
        null=True,
    )
    efficiency_cores = models.IntegerField(
        verbose_name="Efficiency Cores",
        help_text="The number of efficiency cores the processor has.",
        blank=True,
        null=True,
    )
    configurable_tdp_up_frequency = models.IntegerField(
        verbose_name="Configurable TDP-up Frequency",
        help_text="The configurable TDP-up frequency of the processor. In hertz.",
        blank=True,
        null=True,
    )
    configurable_tdp_up = models.IntegerField(
        verbose_name="Configurable TDP-up",
        help_text="The configurable TDP-up of the processor. In watts.",
        blank=True,
        null=True,
    )
    p_core_base_frequency = models.BigIntegerField(
        verbose_name="P-Core Base Frequency",
        help_text="The base frequency of the P-Core. In hertz.",
        blank=True,
        null=True,
    )
    e_core_base_frequency = models.BigIntegerField(
        verbose_name="E-Core Base Frequency",
        help_text="The base frequency of the E-Core. In hertz.",
        blank=True,
        null=True,
    )
    min_assured_power = models.IntegerField(
        verbose_name="Minimum Assured Power",
        help_text="The minimum assured power of the processor. In watts.",
        blank=True,
        null=True,
    )
    max_assured_power = models.IntegerField(
        verbose_name="Maximum Assured Power",
        help_text="The maximum assured power of the processor. In watts.",
        blank=True,
        null=True,
    )

    # TODO: Is this the same as Intel Deep Learning Boost on CPU?
    deep_learning_boost = models.BooleanField(
        verbose_name="Intel Deep Learning Boost (Intel DL Boost)",
        help_text="Whether Intel Deep Learning Boost (Intel DL Boost) is supported.",
        blank=True,
        null=True,
    )
    processor_base_power = models.IntegerField(
        verbose_name="Processor Base Power",
        help_text="The processor base power. In watts.",
        blank=True,
        null=True,
    )
    maximum_turbo_power = models.IntegerField(
        verbose_name="Maximum Turbo Power",
        help_text="The maximum turbo power. In watts.",
        blank=True,
        null=True,
    )

    # Supplemental Information
    marketing_status = models.TextField(
        verbose_name="Marketing Status",
        help_text="The marketing status of the processor.",
        blank=True,
        null=True,
    )
    launch_date = models.TextField(
        verbose_name="Launch Date",
        help_text="The launch date of the processor.",
        blank=True,
        null=True,
    )
    servicing_status = models.TextField(
        verbose_name="Servicing Status",
        help_text="The servicing status of the processor.",
        blank=True,
        null=True,
    )
    end_of_servicing_updates_date = models.DateField(
        verbose_name="End of Servicing Updates Date",
        help_text="The end of servicing updates date of the processor.",
        blank=True,
        null=True,
    )
    end_of_interactive_support_date = models.DateField(
        verbose_name="End of Interactive Support Date",
        help_text="The end of interactive support date of the processor.",
        blank=True,
        null=True,
    )
    embedded_options_available = models.BooleanField(
        verbose_name="Embedded Options Available",
        help_text="Whether embedded options are available.",
        blank=True,
        null=True,
    )
    datasheet = models.URLField(
        verbose_name="Datasheet",
        help_text="The datasheet of the processor.",
        blank=True,
        null=True,
    )
    product_brief_url = models.URLField(
        verbose_name="Product Brief URL",
        help_text="The product brief URL of the processor.",
        blank=True,
        null=True,
    )
    product_brief = models.FileField(
        verbose_name="Product Brief",
        help_text="The product brief of the processor.",
        blank=True,
        null=True,
    )
    additional_information_url = models.URLField(
        verbose_name="Additional Information URL",
        help_text="The additional information URL of the processor.",
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name="Description",
        help_text="The description of the processor.",
        blank=True,
        null=True,
    )
    included_items = models.TextField(
        verbose_name="Included Items",
        help_text="The included items of the processor.",
        blank=True,
        null=True,
    )
    extended_temperature_options = models.TextField(
        verbose_name="Extended Temperature Options",
        help_text="The extended temperature options of the processor.",
        blank=True,
        null=True,
    )

    # Memory Specifications
    max_memory_size = models.BigIntegerField(
        verbose_name="Max Memory Size",
        help_text="The maximum memory size the processor supports.",
        blank=True,
        null=True,
    )
    memory_types = models.TextField(
        verbose_name="Memory Types",
        help_text="The memory types the processor supports.",
        blank=True,
        null=True,
    )
    max_memory_speed = models.BigIntegerField(
        verbose_name="Max Memory Speed",
        help_text="The maximum memory speed the processor supports. In hertz.",
        blank=True,
        null=True,
    )
    max_number_of_memory_channels = models.IntegerField(
        verbose_name="Max Number of Memory Channels",
        help_text="The maximum number of memory channels the processor supports.",
        blank=True,
        null=True,
    )
    max_hbm_memory_size = models.TextField(
        verbose_name="Max HBM Memory Size",
        help_text="The maximum HBM memory size the processor supports.",
        blank=True,
        null=True,
    )
    ecc_memory_supported = models.BooleanField(
        verbose_name="ECC Memory Supported",
        help_text="Whether ECC memory is supported.",
        blank=True,
        null=True,
    )
    max_memory_bandwidth = models.BigIntegerField(
        verbose_name="Max Memory Bandwidth",
        help_text="The maximum memory bandwidth the processor supports. In bytes per second.",
        blank=True,
        null=True,
    )
    physical_address_extensions = models.IntegerField(
        verbose_name="Physical Address Extensions",
        help_text="The physical address extensions the processor supports.",
        blank=True,
        null=True,
    )

    # Expansion Options
    scalability = models.TextField(
        verbose_name="Scalability",
        help_text="The scalability of the processor.",
        blank=True,
        null=True,
    )
    pci_express_revision = models.TextField(
        verbose_name="PCI Express Revision",
        help_text="The PCI Express revision the processor supports.",
        blank=True,
        null=True,
    )
    max_amount_of_pci_express_lanes = models.IntegerField(
        verbose_name="Max Amount of PCI Express Lanes",
        help_text="The maximum amount of PCI Express lanes the processor supports.",
        blank=True,
        null=True,
    )
    pci_express_configurations = models.TextField(
        verbose_name="PCI Express Configurations",
        help_text="The PCI Express configurations the processor supports.",
        blank=True,
        null=True,
    )
    microprocessor_pcie_revision = models.TextField(
        verbose_name="Microprocessor PCIe Revision",
        help_text="The microprocessor PCIe revision the processor supports.",
        blank=True,
        null=True,
    )
    thunderbolt_4_support = models.BooleanField(
        verbose_name="Thunderbolt 4 Support",
        help_text="Whether Thunderbolt 4 is supported.",
        blank=True,
        null=True,
    )
    chipset_pch_pcie_revision = models.TextField(
        verbose_name="Chipset PCH PCIe Revision",
        help_text="The chipset PCH PCIe revision the processor supports.",
        blank=True,
        null=True,
    )
    direct_media_interface_revision = models.TextField(
        verbose_name="Direct Media Interface Revision",
        help_text="The direct media interface revision the processor supports.",
        blank=True,
        null=True,
    )
    max_amount_of_direct_media_interface_lanes = models.IntegerField(
        verbose_name="Max Amount of Direct Media Interface Lanes",
        help_text="The maximum amount of direct media interface lanes the processor supports.",
        blank=True,
        null=True,
    )

    # Package Specifications
    sockets_supported = models.TextField(
        verbose_name="Sockets Supported",
        help_text="Sockets the processor supports.",
        blank=True,
        null=True,
    )
    digital_thermal_sensor_temperature_max = models.FloatField(
        verbose_name="Digital Thermal Sensor (DTS) max temperature",
        help_text="Digital Thermal Sensor (DTS) max temperature. In celsius.",
        blank=True,
        null=True,
    )
    t_case = models.DecimalField(
        verbose_name="T Case",
        help_text="The maximum temperature allowed at the processor Integrated Heat Spreader (IHS).",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    package_size = models.TextField(
        verbose_name="Package Size",
        help_text="The package size of the processor.",
        blank=True,
        null=True,
    )
    max_cpu_configuration = models.TextField(
        verbose_name="Max CPU Configuration",
        help_text="How many CPUs you can have in a configuration.",
        blank=True,
        null=True,
    )
    t_junction = models.DecimalField(
        verbose_name="T Junction",
        help_text="The highest temperature the processor can reach without damaging it. In celsius.",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    thermal_solution_specification = models.TextField(
        verbose_name="Thermal Solution Specification",
        help_text="The thermal solution specification of the processor.",
        blank=True,
        null=True,
    )
    thermal_velocity_boost_temperature = models.DecimalField(
        verbose_name="Thermal Velocity Boost Temperature",
        help_text="The thermal velocity boost temperature of the processor. In celsius.",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    operating_temperature_max = models.DecimalField(
        verbose_name="Operating Temperature Max",
        help_text="The maximum operating temperature of the processor. In celsius.",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    operating_temperature_min = models.DecimalField(
        verbose_name="Operating Temperature Min",
        help_text="The minimum operating temperature of the processor. In celsius.",
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )
    package_carrier = models.TextField(
        verbose_name="Package Carrier",
        help_text="The package carrier of the processor.",
        blank=True,
        null=True,
    )
    dts_max = models.IntegerField(
        verbose_name="DTS Max",
        help_text="The Digital Thermal Sensors max of the processor. In celsius.",
        blank=True,
        null=True,
    )
    operating_temperature_range = models.TextField(
        verbose_name="Operating Temperature Range",
        help_text="The operating temperature range of the processor.",
        blank=True,
        null=True,
    )

    # Advanced Technologies
    deep_learning_boost_version = models.TextField(
        verbose_name="Intel Deep Learning Boost (Intel DL Boost) version",
        help_text="The Intel Deep Learning Boost (Intel DL Boost) version the processor supports.",
        blank=True,
        null=True,
    )

    optane_supported = models.BooleanField(
        verbose_name="Intel Optane supported",
        help_text="Whether Intel Optane is supported.",
        blank=True,
        null=True,
    )
    speed_shift_technology = models.BooleanField(
        verbose_name="Speed Shift Technology",
        help_text="Whether speed shift technology is supported.",
        blank=True,
        null=True,
    )
    turbo_boost_max_technology_3_0 = models.BooleanField(
        verbose_name="Turbo Boost Max Technology 3.0",
        help_text="Whether turbo boost max technology 3.0 is supported.",
        blank=True,
        null=True,
    )
    turbo_boost_technology = models.TextField(
        verbose_name="Intel Turbo Boost version",
        help_text="Intel Turbo Boost version used",
        blank=True,
        null=True,
    )
    hyper_threading_technology = models.BooleanField(
        verbose_name="Hyper-Threading Technology",
        help_text="Whether hyper-threading technology is supported.",
        blank=True,
        null=True,
    )
    transactional_synchronization_extensions = models.BooleanField(
        verbose_name="Intel TSX-NI",
        help_text="Whether Intel TSX-NI is supported.",
        blank=True,
        null=True,
    )
    _64_bit = models.BooleanField(
        verbose_name="64-bit",
        help_text="Whether 64-bit is supported. Also called EM64T (Extended Memory 64 Technology).",
        blank=True,
        null=True,
    )
    instruction_set_extensions = models.TextField(
        verbose_name="Instruction Set Extensions",
        help_text="The instruction set extensions the processor supports.",
        blank=True,
        null=True,
    )
    avx_512_fma_units = models.IntegerField(
        verbose_name="AVX-512 FMA Units",
        help_text="The number of AVX-512 FMA units the processor has.",
        blank=True,
        null=True,
    )
    enhanced_speedstep_technology = models.BooleanField(
        verbose_name="Enhanced Intel SpeedStep Technology",
        help_text="Allows the clock speed to be dynamically changed (to different P-states) by software.",
        blank=True,
        null=True,
    )
    volume_management_device = models.BooleanField(
        verbose_name="Intel Volume Management Device (VMD)",
        help_text="Enables direct control and management of NVMe SSDs from the PCIe bus without additional hardware adaptors",  # noqa: E501
        blank=True,
        null=True,
    )
    instruction_set = models.TextField(
        verbose_name="Instruction Set",
        help_text="The instruction set the processor supports.",
        blank=True,
        null=True,
    )
    idle_states = models.BooleanField(
        verbose_name="Idle States",
        help_text="Whether idle states are supported.",
        blank=True,
        null=True,
    )
    thermal_monitoring_technologies = models.BooleanField(
        verbose_name="Thermal Monitoring Technologies",
        help_text="Allows the processor to maintain optimal temperature by regulating voltage and frequency.",
        blank=True,
        null=True,
    )
    integrated_quick_assist_technology = models.BooleanField(
        verbose_name="Integrated Quick Assist Technology",
        help_text="Whether Integrated Quick assist technology is supported.",
        blank=True,
        null=True,
    )
    management_engine_firmware_version = models.TextField(
        verbose_name="Management Engine Firmware Version",
        help_text="The management engine firmware version the processor supports.",
        blank=True,
        null=True,
    )
    quiet_system_technology = models.BooleanField(
        verbose_name="Quiet System Technology",
        help_text="Whether quiet system technology is supported.",
        blank=True,
        null=True,
    )
    my_wifi_technology = models.BooleanField(
        verbose_name="My WiFi Technology",
        help_text="Whether My WiFi technology is supported.",
        blank=True,
        null=True,
    )
    flex_memory_access = models.BooleanField(
        verbose_name="Flex Memory Access",
        help_text="Whether flex memory access is supported.",
        blank=True,
        null=True,
    )
    identity_protection_technology = models.BooleanField(
        verbose_name="Intel Identity Protection Technology",
        help_text="Intel Identity Protection Technology generates a unique PC number and a six-digit code for web authentication.",  # noqa: E501
        blank=True,
        null=True,
    )
    speed_select_technology_performance_profile = models.BooleanField(
        verbose_name="Speed Select Technology Performance Profile",
        help_text="Whether speed select technology performance profile is supported.",
        blank=True,
        null=True,
    )
    speed_select_technology_base_frequency = models.BooleanField(
        verbose_name="Speed Select Technology Base Frequency",
        help_text="Whether speed select technology base frequency is supported.",
        blank=True,
        null=True,
    )
    resource_director_technology = models.BooleanField(
        verbose_name="Intel Resource Director Technology (Intel RDT)",
        help_text="Whether Intel Resource Director Technology (Intel RDT) is supported.",
        blank=True,
        null=True,
    )
    demand_based_switching = models.BooleanField(
        verbose_name="Intel Demand Based Switching",
        help_text="Whether Intel Demand Based Switching is supported.",
        blank=True,
        null=True,
    )
    thermal_velocity_boost = models.BooleanField(
        verbose_name="Intel Thermal Velocity Boost",
        help_text="Whether Intel Thermal Velocity Boost is supported.",
        blank=True,
        null=True,
    )
    speed_select_technology_core_power = models.BooleanField(
        verbose_name="Speed Select Technology Core Power",
        help_text="Whether speed select technology core power is supported.",
        blank=True,
        null=True,
    )
    speed_select_technology_turbo_frequency = models.BooleanField(
        verbose_name="Speed Select Technology Turbo Frequency",
        help_text="Whether speed select technology turbo frequency is supported.",
        blank=True,
        null=True,
    )
    gaussian_neural_accelerator = models.BooleanField(
        verbose_name="Intel Gaussian & Neural Accelerator",
        help_text="Whether gaussian & neural accelerator is supported.",
        blank=True,
        null=True,
    )
    thread_director = models.BooleanField(
        verbose_name="Intel Thread Director",
        help_text="Monitors the runtime instruction mix of each thread and the state of each core with nanosecond precision.",  # noqa: E501
        blank=True,
        null=True,
    )
    high_priority_cores = models.BooleanField(
        verbose_name="High Priority Cores",
        help_text="Whether high priority cores is supported.",
        blank=True,
        null=True,
    )
    high_priority_cores_frequency = models.BooleanField(
        verbose_name="High Priority Cores Frequency",
        help_text="Whether high priority cores frequency is supported.",
        blank=True,
        null=True,
    )
    low_priority_cores = models.BooleanField(
        verbose_name="Low Priority Cores",
        help_text="Whether low priority cores is supported.",
        blank=True,
        null=True,
    )
    low_priority_cores_frequency = models.BooleanField(
        verbose_name="Low Priority Cores Frequency",
        help_text="Whether low priority cores frequency is supported.",
        blank=True,
        null=True,
    )
    image_processing_unit = models.BooleanField(
        verbose_name="Intel Image Processing Unit",
        help_text="Whether Intel Image Processing Unit is supported.",
        blank=True,
        null=True,
    )
    smart_sound_technology = models.BooleanField(
        verbose_name="Intel Smart Sound Technology",
        help_text="Whether Intel Smart Sound Technology is supported.",
        blank=True,
        null=True,
    )
    wake_on_voice = models.BooleanField(
        verbose_name="Intel Wake on Voice",
        help_text="Whether Intel Wake on Voice is supported.",
        blank=True,
        null=True,
    )
    high_definition_audio = models.BooleanField(
        verbose_name="Intel High Definition Audio",
        help_text="Whether Intel High Definition Audio is supported.",
        blank=True,
        null=True,
    )
    adaptix_technology = models.BooleanField(
        verbose_name="Adaptix Technology",
        help_text="Whether Adaptix technology is supported.",
        blank=True,
        null=True,
    )
    time_coordinated_computing = models.BooleanField(
        verbose_name="Intel Time Coordinated Computing (Intel TCC)",
        help_text="Whether Intel Time Coordinated Computing (Intel TCC) is supported.",
        blank=True,
        null=True,
    )
    mipi_soundwire_version = models.FloatField(
        verbose_name="MIPI SoundWire Version",
        help_text="The MIPI SoundWire version the processor supports.",
        blank=True,
        null=True,
    )
    on_demand_feature_activation = models.BooleanField(
        verbose_name="On-Demand Feature Activation",
        help_text="Whether on-demand feature activation is supported.",
        blank=True,
        null=True,
    )
    data_streaming_accelerator = models.BooleanField(
        verbose_name="Data Streaming Accelerator (DSA)",
        help_text="Whether Data Streaming Accelerator (DSA) is supported.",
        blank=True,
        null=True,
    )
    advanced_matrix_extensions = models.BooleanField(
        verbose_name="Advanced Matrix Extensions",
        help_text="Whether advanced matrix extensions is supported.",
        blank=True,
        null=True,
    )
    # TODO: Is this the same as the other QuickAssist?
    quick_assist_technology = models.BooleanField(
        verbose_name="Quick Assist Technology",
        help_text="Whether quick assist technology is supported.",
        blank=True,
        null=True,
    )
    dynamic_load_balancer = models.BooleanField(
        verbose_name="Dynamic Load Balancer (DLB)",
        help_text="Whether Dynamic Load Balancer (DLB) is supported.",
        blank=True,
        null=True,
    )
    in_memory_analytics_accelerator = models.BooleanField(
        verbose_name="In-Memory Analytics Accelerator (IAA)",
        help_text="Whether In-Memory Analytics Accelerator (IAA) is supported.",
        blank=True,
        null=True,
    )
    vran_boost = models.BooleanField(
        verbose_name="VRAN Boost",
        help_text="Whether VRAN Boost is supported.",
        blank=True,
        null=True,
    )
    adaptive_boost_technology = models.BooleanField(
        verbose_name="Intel Adaptive Boost Technology",
        help_text="Whether Intel Adaptive Boost Technology is supported.",
        blank=True,
        null=True,
    )

    # Security & Reliability
    vpro_eligibility = models.TextField(
        verbose_name="Intel vPro Eligibility",
        help_text="Whether Intel vPro is supported.",
        blank=True,
        null=True,
    )
    quick_assist_software_acceleration = models.BooleanField(
        verbose_name="Intel QuickAssist Software Acceleration",
        help_text="Offloads data compression and decompression, encrypt and decrypt, and public key data encryption tasks from the CPU cores",  # noqa: E501
        blank=True,
        null=True,
    )
    aes_new_instructions = models.BooleanField(
        verbose_name="Intel AES New Instructions",
        help_text="Whether Intel AES New Instructions is supported.",
        blank=True,
        null=True,
    )
    trusted_execution_technology = models.BooleanField(
        verbose_name="Intel Trusted Execution Technology (Intel TXT, formerly known as LaGrande Technology)",
        help_text="Whether Intel Trusted Execution Technology (Intel TXT, formerly known as LaGrande Technology) is supported.",  # noqa: E501
        blank=True,
        null=True,
    )
    # TODO: Intel.com has "Newer processors such as 11th Generation Intel® Core™ Processors consider the Execute Disable Bit feature to be Legacy and thus it may not be listed in the processor specification page (ARK). However, it is still supported." # noqa: E501
    #   Should we set this to True for all newer processors?
    execute_disable_bit = models.BooleanField(
        verbose_name="Execute Disable Bit",
        help_text="The Execute Disable Bit is a hardware-based security feature that can reduce exposure to viruses and malicious-code attacks, and prevent harmful software from executing and propagating on the server or network.",  # noqa: E501
        blank=True,
        null=True,
    )
    run_sure_technology = models.BooleanField(
        verbose_name="Run Sure Technology",
        help_text="Whether run sure technology is supported.",
        blank=True,
        null=True,
    )
    mode_based_execute_control = models.BooleanField(
        verbose_name="Mode-based Execute Control (MBE)",
        help_text="Whether Mode-based Execute Control (MBE) is supported.",
        blank=True,
        null=True,
    )
    virtualization_technology = models.BooleanField(
        verbose_name="Intel Virtualization Technology (VT-x)",
        help_text="Whether Intel Virtualization Technology (VT-x) is supported.",
        blank=True,
        null=True,
    )
    virtualization_technology_for_directed_io = models.BooleanField(
        verbose_name="Virtualization Technology for Directed I/O (VT-d)",
        help_text="Whether Virtualization Technology for Directed I/O (VT-d) is supported.",
        blank=True,
        null=True,
    )
    virtualization_technology_with_extended_page_tables = models.BooleanField(
        verbose_name="Virtualization Technology with Extended Page Tables (EPT)",
        help_text="Whether Virtualization Technology with Extended Page Tables (EPT) is supported.",
        blank=True,
        null=True,
    )
    secure_key = models.BooleanField(
        verbose_name="Secure Key",
        help_text="Whether secure key is supported.",
        blank=True,
        null=True,
    )
    os_guard = models.BooleanField(
        verbose_name="Intel OS Guard",
        help_text="Whether Intel OS Guard is supported.",
        blank=True,
        null=True,
    )
    # TODO: Software Guard Extensions is "Yes with Intel® SPS" or "No"
    #   Should this be a boolean and a separate field with what it supports?
    #   Is it always with Intel SPS?
    software_guard_extensions = models.TextField(
        verbose_name="Intel Software Guard Extensions (Intel SGX)",
        help_text="Whether Intel Software Guard Extensions (Intel SGX) is supported.",
        blank=True,
        null=True,
    )
    boot_guard = models.BooleanField(
        verbose_name="Intel Boot Guard",
        help_text="Whether Intel Boot Guard is supported.",
        blank=True,
        null=True,
    )
    memory_protection_extensions = models.BooleanField(
        verbose_name="Memory Protection Extensions (MPX)",
        help_text="Whether Memory Protection Extensions (MPX) is supported.",
        blank=True,
        null=True,
    )
    stable_image_platform_program = models.BooleanField(
        verbose_name="Stable Image Platform Program (SIPP)",
        help_text="Whether Stable Image Platform Program (SIPP) is supported.",
        blank=True,
        null=True,
    )
    maximum_enclave_size_for_sgx = models.BigIntegerField(
        verbose_name="Default Maximum Enclave Page Cache (EPC) Size for Intel SGX",
        help_text="How many bytes the Enclave Page Cache (EPC) can be.",
        blank=True,
        null=True,
    )
    crypto_acceleration = models.BooleanField(
        verbose_name="Intel Crypto Acceleration",
        help_text="Whether Intel Crypto Acceleration is supported.",
        blank=True,
        null=True,
    )
    platform_firmware_resilience = models.BooleanField(
        verbose_name="Intel Platform Firmware Resilience Support (Intel PFR)",
        help_text="Whether Intel Platform Firmware Resilience Support (Intel PFR) is supported.",
        blank=True,
        null=True,
    )
    total_memory_encryption = models.BooleanField(
        verbose_name="Intel Total Memory Encryption (Intel TME)",
        help_text="Whether Intel Total Memory Encryption (Intel TME) is supported.",
        blank=True,
        null=True,
    )
    control_flow_enforcement_technology = models.BooleanField(
        verbose_name="Intel Control-flow Enforcement Technology",
        help_text="Whether Intel Control-flow Enforcement Technology is supported.",
        blank=True,
        null=True,
    )
    threat_detection_technology = models.BooleanField(
        verbose_name="Intel Threat Detection Technology (TDT)",
        help_text="Whether Intel Threat Detection Technology (TDT) is supported.",
        blank=True,
        null=True,
    )
    active_management_technology = models.BooleanField(
        verbose_name="Intel Active Management Technology (AMT)",
        help_text="Whether Intel Active Management Technology (AMT) is supported.",
        blank=True,
        null=True,
    )
    standard_manageability = models.BooleanField(
        verbose_name="Intel Standard Manageability (ISM)",
        help_text="Whether Intel Standard Manageability (ISM) is supported.",
        blank=True,
        null=True,
    )
    remote_platform_erase = models.BooleanField(
        verbose_name="Intel Remote Platform Erase (RPE)",
        help_text="Whether Intel Remote Platform Erase (RPE) is supported.",
        blank=True,
        null=True,
    )
    one_click_recovery = models.BooleanField(
        verbose_name="Intel One-click Recovery",
        help_text="Whether Intel One-click Recovery is supported.",
        blank=True,
        null=True,
    )
    hardware_shield = models.BooleanField(
        verbose_name="Intel Hardware Shield Eligibility",
        help_text="Whether Intel Hardware Shield is supported.",
        blank=True,
        null=True,
    )
    total_memory_encryption_multi_key = models.BooleanField(
        verbose_name="Intel Total Memory Encryption - Multi Key",
        help_text="Whether Intel Total Memory Encryption - Multi Key is supported.",
        blank=True,
        null=True,
    )
    virtualization_technology_with_redirect_protection = models.BooleanField(
        verbose_name="Intel Virtualization Technology with Redirect Protection (VT-rp)",
        help_text="Whether Intel Virtualization Technology with Redirect Protection (VT-rp) is supported.",
        blank=True,
        null=True,
    )

    # I/O Specifications
    number_of_usb_ports = models.IntegerField(
        verbose_name="Number of USB Ports",
        help_text="The number of USB ports the processor has.",
        blank=True,
        null=True,
    )
    usb_revision = models.TextField(
        verbose_name="USB Revision",
        help_text="The USB revision the processor supports.",
        blank=True,
        null=True,
    )
    number_of_sata_ports = models.IntegerField(
        verbose_name="Number of SATA Ports",
        help_text="The number of SATA ports the processor has.",
        blank=True,
        null=True,
    )
    integrated_lan = models.BooleanField(
        verbose_name="Integrated LAN",
        help_text="Whether integrated LAN is supported.",
        blank=True,
        null=True,
    )
    general_purpose_io = models.BooleanField(
        verbose_name="General Purpose I/O",
        help_text="Whether general purpose I/O is supported.",
        blank=True,
        null=True,
    )
    uart = models.TextField(  # This is Yes, No or 3 :thinking:
        verbose_name="UART",
        help_text="Universal asynchronous receiver-transmitter",
        blank=True,
        null=True,
    )
    number_of_sata_6_0_ports = models.IntegerField(
        verbose_name="Number of SATA 6.0 Gb/s Ports",
        help_text="The number of SATA 6.0 Gb/s ports the processor has.",
        blank=True,
        null=True,
    )
    usb_configuration = models.TextField(
        verbose_name="USB Configuration",
        help_text="The amount and generation the CPU supports.",
        blank=True,
        null=True,
    )
    integrated_ide = models.BooleanField(
        verbose_name="Integrated IDE",
        help_text="Integrated development environment",
        blank=True,
        null=True,
    )

    # Networking Specifications
    interfaces_supported = models.TextField(
        verbose_name="Interfaces Supported",
        help_text="The interfaces supported by the processor.",
        blank=True,
        null=True,
    )

    # GPU Specifications
    processor_graphics = models.TextField(
        verbose_name="Processor Graphics",
        help_text="The processor graphics the processor has.",
        blank=True,
        null=True,
    )
    graphics_base_frequency = models.BigIntegerField(
        verbose_name="Graphics Base Frequency",
        help_text="The graphics base frequency the processor has. In hertz.",
        blank=True,
        null=True,
    )
    graphics_max_dynamic_frequency = models.BigIntegerField(
        verbose_name="Graphics Max Dynamic Frequency",
        help_text="The graphics max dynamic frequency the processor has. In hertz.",
        blank=True,
        null=True,
    )
    graphics_video_max_memory = models.TextField(
        verbose_name="Graphics Video Max Memory",
        help_text="The graphics video max memory the processor has.",
        blank=True,
        null=True,
    )
    graphics_output = models.TextField(
        verbose_name="Graphics Output",
        help_text="The graphics output the processor has.",
        blank=True,
        null=True,
    )
    _4k_support = models.TextField(
        verbose_name="4K Support",
        help_text="Whether 4K is supported.",
        blank=True,
        null=True,
    )
    max_resolution_hdmi = models.TextField(
        verbose_name="Max Resolution (HDMI)",
        help_text="The maximum resolution (HDMI) the processor supports.",
        blank=True,
        null=True,
    )
    max_resolution_dp = models.TextField(
        verbose_name="Max Resolution (DP)",
        help_text="The maximum resolution (DP) the processor supports.",
        blank=True,
        null=True,
    )
    max_resolution_edp_integrated_flat_panel = models.TextField(
        verbose_name="Max Resolution (eDP - Integrated Flat Panel)",
        help_text="The maximum resolution (eDP - Integrated Flat Panel) the processor supports.",
        blank=True,
        null=True,
    )
    max_resolution_vga = models.TextField(
        verbose_name="Max Resolution (VGA)",
        help_text="The maximum resolution (VGA) the processor supports.",
        blank=True,
        null=True,
    )
    # TODO: Should this be a float?
    directx_support = models.TextField(
        verbose_name="DirectX Support",
        help_text="The DirectX support the processor has.",
        blank=True,
        null=True,
    )
    opengl_support = models.TextField(
        verbose_name="OpenGL Support",
        help_text="The OpenGL support the processor has.",
        blank=True,
        null=True,
    )
    opencl_support = models.TextField(
        verbose_name="OpenCL Support",
        help_text="The OpenCL support the processor has.",
        blank=True,
        null=True,
    )
    intel_quick_sync_video = models.BooleanField(
        verbose_name="Intel Quick Sync Video",
        help_text="Whether Intel Quick Sync Video is supported.",
        blank=True,
        null=True,
    )
    intel_in_tru_3d_technology = models.BooleanField(
        verbose_name="Intel InTru 3D Technology",
        help_text="Whether Intel InTru 3D Technology is supported.",
        blank=True,
        null=True,
    )
    intel_clear_video_hd_technology = models.BooleanField(
        verbose_name="Intel Clear Video HD Technology",
        help_text="Whether Intel Clear Video HD Technology is supported.",
        blank=True,
        null=True,
    )
    intel_clear_video_technology = models.BooleanField(
        verbose_name="Intel Clear Video Technology",
        help_text="Whether Intel Clear Video Technology is supported.",
        blank=True,
        null=True,
    )
    number_of_displays_supported = models.IntegerField(
        verbose_name="Number of Displays Supported",
        help_text="The number of displays supported by the processor.",
        blank=True,
        null=True,
    )
    device_id = models.TextField(
        verbose_name="Device ID",
        help_text="The device ID of the processor.",
        blank=True,
        null=True,
    )
    execution_units = models.IntegerField(
        verbose_name="Execution Units",
        help_text="The number of execution units the processor has.",
        blank=True,
        null=True,
    )
    multi_format_codec_engines = models.IntegerField(
        verbose_name="Multi-format Codec Engines",
        help_text="The number of multi-format codec engines the processor has.",
        blank=True,
        null=True,
    )

    # Intel On Demand Available Upgrades
    intel_on_demand_available_upgrades = models.TextField(
        verbose_name="Intel On Demand Available Upgrades",
        help_text="The Intel On Demand available upgrades the processor has.",
        blank=True,
        null=True,
    )

    # Networking Specifications
    network_interfaces = models.TextField(
        verbose_name="Network Interfaces",
        help_text="The network interfaces the processor has.",
        blank=True,
        null=True,
    )

    class Meta:
        """Meta options for the Processor model."""

        ordering: typing.ClassVar[list[str]] = ["-created"]
        verbose_name: str = "Intel processor"
        verbose_name_plural: str = "Intel processors"
        db_table: str = "intel_processors"
        db_table_comment: str = "Intel processors and their specifications"

    def __str__(self: Processor) -> str:
        """Return CPU name."""
        return f"{self.pk} - {self.name}"
