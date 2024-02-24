from magia import Elaborator, Input, Module, Output
from magia.std.edges import edge_detector


class ALlEdges(Module):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.io += [
            Input("clk", 1),
            Input("reset", 1),
            Input("rst_n", 1),
            Input("event", 1),
            Output("rising", 1),
            Output("falling", 1),
            Output("both", 1),
            Output("rising_unreg", 1),
            Output("falling_unreg", 1),
            Output("both_unreg", 1),
            Output("rising_async", 1),
            Output("falling_async", 1),
            Output("both_async", 1),
            Output("rising_async_unreg", 1),
            Output("falling_async_unreg", 1),
            Output("both_async_unreg", 1),
        ]

        sync_clock = {
            "clk": self.io.clk,
            "reset": self.io.reset,
        }
        sync_clock_unreg = {
            **sync_clock,
            "registered": False,
        }
        async_clock = {
            "clk": self.io.clk,
            "async_reset": self.io.rst_n,
        }
        async_clock_unreg = {
            **async_clock,
            "registered": False,
        }

        self.io.rising <<= edge_detector(self.io.event, edge="rising", **sync_clock)
        self.io.falling <<= edge_detector(self.io.event, edge="falling", **sync_clock)
        self.io.both <<= edge_detector(self.io.event, edge="both", **sync_clock)
        self.io.rising_unreg <<= edge_detector(self.io.event, edge="rising", **sync_clock_unreg)
        self.io.falling_unreg <<= edge_detector(self.io.event, edge="falling", **sync_clock_unreg)
        self.io.both_unreg <<= edge_detector(self.io.event, edge="both", **sync_clock_unreg)

        self.io.rising_async <<= edge_detector(self.io.event, edge="rising", **async_clock)
        self.io.falling_async <<= edge_detector(self.io.event, edge="falling", **async_clock)
        self.io.both_async <<= edge_detector(self.io.event, edge="both", **async_clock)
        self.io.rising_async_unreg <<= edge_detector(self.io.event, edge="rising", **async_clock_unreg)
        self.io.falling_async_unreg <<= edge_detector(self.io.event, edge="falling", **async_clock_unreg)
        self.io.both_async_unreg <<= edge_detector(self.io.event, edge="both", **async_clock_unreg)


def test_edge_detector_smoke():
    Elaborator.to_string(ALlEdges(name="Top"))
