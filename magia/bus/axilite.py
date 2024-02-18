"""
Factory methods that generate BundleSpec for AXI-Lite interface.
Details of the AXI-Lite interface can be found in the AMBA AXI and ACE Protocol Specification.
https://developer.arm.com/documentation/ihi0022/latest/
https://developer.arm.com/-/media/Arm%20Developer%20Community/PDF/IHI0022H_amba_axi_protocol_spec.pdf
"""
from magia import BundleSpec, Input, Output
from magia.std.bundles import decoupled_bundle


def axi4lite(
        data_width: int = 32,
        addr_width: int = 32,
) -> BundleSpec:
    """
    Create a BundleSpec for an AXI4-Lite interface.
    :param data_width: The width of the data signal, default is 32.
    :param addr_width: The width of the address signal, default is 32.
    """
    if data_width not in (32, 64):
        raise ValueError("data_width must be either 32 or 64")

    # Define the AXI4-Lite signals
    aw = decoupled_bundle([
        Output(name="addr", width=addr_width, description="Write address"),
        Output(name="prot", width=3, description="Write Protection type"),
    ])

    ar = decoupled_bundle([
        Output(name="addr", width=addr_width, description="Read address"),
        Output(name="prot", width=3, description="Read Protection type"),
    ])

    r = decoupled_bundle([
        Output(name="data", width=data_width, description="Read Data"),
        Output(name="resp", width=2, description="Read response"),
    ])

    w = decoupled_bundle([
        Output(name="data", width=data_width, description="Write Data"),
        Output(name="strb", width=data_width // 8, description="Write strobes"),
    ])

    b = decoupled_bundle([
        Output(name="resp", width=2, description="Write response"),
    ])

    # Create the BundleSpec and merge the signals
    spec = BundleSpec()
    spec += aw.master_ports(prefix="aw")
    spec += ar.master_ports(prefix="ar")
    spec += r.slave_ports(prefix="r")  # R Channel is driven by the slave
    spec += w.master_ports(prefix="w")
    spec += b.slave_ports(prefix="b")  # B Channel is driven by the slave

    # Add Clock and Reset
    spec.add_common(Input(name="aclk", width=1, description="Clock"))
    spec.add_common(Input(name="aresetn", width=1, description="Global Async Reset"))

    return spec
