from contextlib import contextmanager

current_clock_stack = []


@contextmanager
def clock(clk: "Input"):
    """
    Set current clock signal to `clk`
    Other modules will use this clock signal as default
    by invoking `get_cur_clock()`
    :param clk: Clock signal to be used
    """
    current_clock_stack.append(clk)
    yield clk
    current_clock_stack.pop()


def get_cur_clock():
    """
    Get current clock signal.
    :return:
    """
    if len(current_clock_stack) == 0:
        return None
    return current_clock_stack[-1]
