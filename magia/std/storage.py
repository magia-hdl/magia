from magia import Constant, Input, Module, Register, Signal

from .bundles import StdIO


class Queue(Module):
    def __init__(self, width, depth, **kwargs):
        super().__init__(**kwargs)
        self.register_module_doc(locals())

        self.width = width
        self.depth = depth
        self.pointer_width = depth

        self.io += Input("clk", 1)
        self.io += Input("reset", 1)

        self.io += StdIO.decoupled("din", width).flip()
        self.io += StdIO.decoupled("dout", width)

        self.implementation()

    def implementation(self):
        def fifo_ptr(width, name):
            adv_signal = Signal(1, name=f"{name}_adv")
            ptr = Register(width, name=name, clk=self.io.clk, enable=adv_signal, reset=self.io.reset, reset_value=1)
            next_ptr = ptr[-2:0, -1]
            ptr <<= next_ptr
            return ptr, next_ptr, adv_signal

        # Write Pointer
        write_ptr, next_write_ptr, write_adv = fifo_ptr(self.pointer_width, "write_ptr")
        write_en = write_ptr.when(write_adv)

        # Read Pointer
        read_ptr, next_read_ptr, read_adv = fifo_ptr(self.pointer_width, "read_ptr")

        queue_empty = write_ptr == read_ptr
        queue_full = next_write_ptr == read_ptr

        memory = [
            self.io.din.reg(
                clk=self.io.clk,
                enable=write_en[i],
                reset=self.io.reset,
            ).set_name(f"mem_{i}")
            for i in range(self.depth)
        ]
        self.io.din_ready <<= ~queue_full

        write_adv <<= self.io.din_valid & ~queue_full
        read_adv <<= self.io.dout_ready & ~queue_empty

        output = Constant(0, self.width)
        for i in range(self.depth):
            output |= memory[i].when(read_ptr[i])
        self.io.dout <<= output.reg(clk=self.io.clk, enable=read_adv)
        self.io.dout_valid <<= (~queue_empty).reg(clk=self.io.clk)
