from typing import Union

from magia import Input, IOBundle, Output


class StdIO:
    @classmethod
    def valid_multi(cls, bundle_name: str, data_spec: dict[str, Union[tuple[int, bool], int]], sep="_") -> IOBundle:
        if not isinstance(data_spec, dict):
            raise TypeError("data_spec must be a dict")
        if len(data_spec) == 0:
            raise ValueError("data_spec must not be empty")
        new_bundle = IOBundle()
        for name, spec in data_spec.items():
            if isinstance(spec, tuple):
                width, signed = spec
            else:
                width, signed = spec, False
            new_bundle += Output(f"{name}", width, signed)
        new_bundle += Output(f"{bundle_name}{sep}valid", 1)
        return new_bundle

    @classmethod
    def decoupled_multi(cls, bundle_name: str, data_spec: dict[str, Union[tuple[int, bool], int]], sep="_") -> IOBundle:
        new_bundle = cls.valid_multi(bundle_name, data_spec, sep)
        new_bundle += Input(f"{bundle_name}ready", 1)
        return new_bundle

    @classmethod
    def valid(cls, name: str, width: int, signed: bool = False, sep="_") -> IOBundle:
        return cls.valid_multi(name, {name: (width, signed)}, sep)

    @classmethod
    def decoupled(cls, name: str, width: int, signed: bool = False, sep="_") -> IOBundle:
        return cls.decoupled_multi(name, {name: (width, signed)}, sep)





class AXI4Stream:
    """
    Define a AXI4 Stream interface factory.
    The factory specializes parameters for the AXI4 Stream interface.
    Using `master` or `slave` will return an IOBundle with the appropriate signal names and directions
    """

    def __init__(
            self,
            tdata_width: int = 32,
            tid_width: int = 0,
            tdest_width: int = 0,
            tuser_width: int = 0,
            **kwargs
    ):
        self.tdata_width = tdata_width
        self.tid_width = tid_width
        self.tdest_width = tdest_width
        self.tuser_width = tuser_width

    def _main_interface(self, **kwargs) -> IOBundle:

        new_bundle = IOBundle()
        new_bundle += Input("aclk", 1)
        new_bundle += Input("aresetn", 1)
        data_spec = {
            "tdata": self.tdata_width,
            "tstrb": self.tdata_width // 8,
            "tkeep": self.tdata_width // 8,
            "tlast": 1,
        }
        if self.tid_width:
            data_spec["tid"] = self.tid_width
        if self.tdest_width:
            data_spec["tdest"] = self.tdest_width
        if self.tuser_width:
            data_spec["tuser"] = self.tuser_width
        new_bundle += StdIO.decoupled_multi("t", data_spec, sep="")

        return new_bundle.with_name(prefix="axis_")

    def master(self, **kwargs) -> IOBundle:
        return self._main_interface(**kwargs)

    def slave(self, **kwargs) -> IOBundle:
        slave_bundle = self._main_interface(**kwargs)
        return slave_bundle.flip(ignore=["aclk, aresetn"])
