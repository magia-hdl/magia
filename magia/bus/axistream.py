"""
Factory methods that generate BundleSpec for AXI-Stream interface.
Details of the AXI-Stream interface can be found in the AMBA AXI and ACE Protocol Specification.
https://developer.arm.com/documentation/ihi0051/latest/
"""

from magia import BundleSpec, Input, Output
from magia.std.bundles import decoupled_bundle


def axi4stream(
        tdata_width: int,
        tid_width: int = 0,
        tdest_width: int = 0,
        tuser_width: int = 0,
        tlast: bool = False,
        tstrb: bool = False,
        tkeep: bool = False,
) -> BundleSpec:
    """
    Create a BundleSpec for an AXI4-Stream interface.

    :param tdata_width: The width of the data signal.
    :param tid_width: The width of the ID signal, default is 0.
    :param tdest_width: The width of the destination signal, default is 0.
    :param tuser_width: The width of the user signal, default is 0.
    :param tlast: Add a tlast signal, default is False.
    :param tstrb: Add a tstrb signal, default is False.
    :param tkeep: Add a tkeep signal, default is False.
    """

    if tdata_width not in (8, 16, 32, 64, 128, 256, 512, 1024):
        raise ValueError("tdata_width must be a power of 2 between 8 and 1024")

    # Create the BundleSpec with mandatory signals
    spec = decoupled_bundle([
        Output(name="tdata", width=tdata_width, description="Data")
    ], valid="tvalid", ready="tready")
    spec.add_common(Input(name="aclk", width=1, description="Clock"))
    spec.add_common(Input(name="aresetn", width=1, description="Global Async Reset"))

    # Add optional signals
    if tid_width > 0:
        spec += Output(name="tid", width=tid_width, description="Data Stream Identifier")
    if tdest_width > 0:
        spec += Output(name="tdest", width=tdest_width, description="Stream Routing Information")
    if tuser_width > 0:
        spec += Output(name="tuser", width=tuser_width, description="User-defined signal")

    if tlast:
        spec += Output(name="tlast", width=1, description="Last transfer in a packet")
    if tstrb:
        spec += Output(
            name="tstrb", width=tdata_width // 8,
            description="Indicating bytes are valid data (1) or position byte (0).",
        )
    if tkeep:
        spec += Output(
            name="tkeep", width=tdata_width // 8,
            description="Indicating which bytes must be delivered to the destination",
        )

    return spec
