from collections.abc import Iterable
from enum import Enum
from string import Template
from typing import Optional

from .core import Signal, Synthesizable


class VerifyType(Enum):
    ASSERT = "assert"
    ASSUME = "assume"
    COVER = "cover"


class ManualProperty(Synthesizable):
    """
    Manual property is an SVA property that is written by the user.

    It does not provide any automatic logics like signal tracing in elaboration.
    Developers are expected to have understanding of the SVA syntax.

    Simplification on clocking block is provided.

    The following script is an example of how to use ManualProperty:
    ```python
    from magia import ManualProperty, Module, Signal
    class Design(Module):
        def __init__(self, **kwargs):
            ...
            self.sva = SVABlock()
            with Signal.name_as_str():
                self.sva.add(
                    ManualProperty(
                        # Refer the net name with f-string directly
                        statement=f"{self.io.a} |-> ##[1:2] {self.io.b}",
                        clk=self.io.clk,
                        async_reset=self.io.rst_n,
                    )
                )
            ...

        def post_elaboration(self):
            return self.new_prop.elaborate()
    ```
    """
    property_counts = 0

    _PROP_TEMPLATE = Template(
        "$prop_name: $prop_type property (\n"
        "$clocking  $statement\n"
        ");"
    )

    def __init__(
            self,
            statement: str,
            name: Optional[str] = None,
            clk: Optional[Signal] = None,
            async_reset: Optional[Signal] = None,
            property_type: VerifyType = VerifyType.ASSERT,
            **kwargs
    ):
        if name is None:
            name = f"property_manual_{self.property_counts}"
        self.property_counts += 1
        self.name = {
                        VerifyType.ASSERT: "ap_",
                        VerifyType.ASSUME: "as_",
                        VerifyType.COVER: "cp_"
                    }[self.property_type] + name

        super().__init__(**kwargs)
        self.statement = statement
        self.property_type = property_type
        self.clk = clk
        self.async_reset = async_reset

    @property
    def name(self):
        return self.name

    @property
    def net_name(self):
        return self.name

    def elaborate(self) -> str:
        clocking = ""
        with Signal.name_as_str():
            if self.clk is not None:
                clocking = f"@(posedge {self.clk})"
                if self.async_reset is not None:
                    clocking += f"disable iff (!{self.async_reset})"
        if clocking != "":
            clocking = f"  {clocking}\n"

        return self._PROP_TEMPLATE.substitute(
            prop_name=self.name,
            prop_type=self.property_type.value,
            clocking=clocking,
            statement=self.statement
        )


class SVABlock(Synthesizable):
    """
    Container of SV Assertions.
    Extra warping blocks can be added to the block in later implementation.
    (e.g. `ifdef`, `checker/endchecker`)
    """

    def __init__(
            self,
            clk: Optional[Signal] = None,
            **kwargs,
    ):
        super(self).__init__(**kwargs)
        self.properties = []
        self.property_names = set()
        self.clk = clk

    @property
    def name(self):
        return "To be implemented"

    @property
    def net_name(self):
        return "To be implemented"

    def add(self, new_prop: ManualProperty):
        if new_prop.name in self.property_names:
            raise ValueError(f"Property name {new_prop.name} already exists")

        if new_prop.clk is None and self.clk is not None:
            new_prop.clk = self.clk

        self.properties.append(new_prop)
        self.property_names.add(new_prop.name)

    def __iadd__(self, new_props):
        if not isinstance(new_props, Iterable):
            self.add(new_props)
            return self

        for new_prop in new_props:
            self.add(new_prop)
        return self

    def elaborate(self) -> str:
        return "\n".join([prop.elaborate() for prop in self.properties])
