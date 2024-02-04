from magia.bus.axilite import axi4lite
from magia.constants import SignalType


class TestAXI4Lite:
    spec = axi4lite()

    def test_master_direction(self):
        master_ports = self.spec.master_ports()
        for ports, direction in [
            (("aclk", "aresetn",), SignalType.INPUT),
            (("awready", "arready", "rdata", "rresp", "rvalid", "wready", "bresp", "bvalid",), SignalType.INPUT),
            (("awaddr", "awprot", "awvalid", "araddr", "arprot", "arvalid", "rready", "wdata", "wstrb", "wvalid",
              "bready",), SignalType.OUTPUT),
        ]:
            for port in ports:
                assert master_ports[port].type == direction

    def test_slave_direction(self):
        slave_ports = self.spec.slave_ports()
        for ports, direction in [
            (("aclk", "aresetn",), SignalType.INPUT),
            (("awready", "arready", "rdata", "rresp", "rvalid", "wready", "bresp", "bvalid",), SignalType.OUTPUT),
            (("awaddr", "awprot", "awvalid", "araddr", "arprot", "arvalid", "rready", "wdata", "wstrb", "wvalid",
              "bready",), SignalType.INPUT),
        ]:
            for port in ports:
                assert slave_ports[port].type == direction

    def test_monitor_directions(self):
        monitor = self.spec.monitor_ports()
        for ports, direction in [
            (("aclk", "aresetn",), SignalType.INPUT),
            (("awready", "arready", "rdata", "rresp", "rvalid", "wready", "bresp", "bvalid",), SignalType.INPUT),
            (("awaddr", "awprot", "awvalid", "araddr", "arprot", "arvalid", "rready", "wdata", "wstrb", "wvalid",
              "bready",), SignalType.INPUT),
        ]:
            for port in ports:
                assert monitor[port].type == direction
