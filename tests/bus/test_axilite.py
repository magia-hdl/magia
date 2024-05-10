from magia import Input, Output
from magia.bus.axilite import axi4lite


class TestAXI4Lite:
    spec = axi4lite()

    def test_master_direction(self):
        master_ports = self.spec.master_ports()
        for ports, direction in [
            (("aclk", "aresetn",), Input),
            (("awready", "arready", "rdata", "rresp", "rvalid", "wready", "bresp", "bvalid",), Input),
            (("awaddr", "awprot", "awvalid", "araddr", "arprot", "arvalid", "rready", "wdata", "wstrb", "wvalid",
              "bready",), Output),
        ]:
            for port in ports:
                assert isinstance(master_ports[port], direction)

    def test_slave_direction(self):
        slave_ports = self.spec.slave_ports()
        for ports, direction in [
            (("aclk", "aresetn",), Input),
            (("awready", "arready", "rdata", "rresp", "rvalid", "wready", "bresp", "bvalid",), Output),
            (("awaddr", "awprot", "awvalid", "araddr", "arprot", "arvalid", "rready", "wdata", "wstrb", "wvalid",
              "bready",), Input),
        ]:
            for port in ports:
                assert isinstance(slave_ports[port], direction)

    def test_monitor_directions(self):
        monitor = self.spec.monitor_ports()
        for ports, direction in [
            (("aclk", "aresetn",), Input),
            (("awready", "arready", "rdata", "rresp", "rvalid", "wready", "bresp", "bvalid",), Input),
            (("awaddr", "awprot", "awvalid", "araddr", "arprot", "arvalid", "rready", "wdata", "wstrb", "wvalid",
              "bready",), Input),
        ]:
            for port in ports:
                assert isinstance(monitor[port], direction)
