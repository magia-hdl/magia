from dataclasses import dataclass, field

from magia import Constant, Signal


class FSM:
    """
    A Finite State Machine (FSM) generator.

    Developers can define the states and transitions of the FSM using the add_states and add_transitions methods.
    The state logic and output state can be generated using the generate methods.

    Once the state logic is generated, the FSM is finalized and no more states or transitions can be added.
    """

    @dataclass
    class State:
        name: str
        code: None | int
        signal: Constant = field(repr=False)

    @dataclass
    class Transition:
        next: str
        cond: None | Signal = None

    fsm_id = 0

    def __init__(
            self,
            name: None | str = None,
            **kwargs,
    ):
        self.states: dict[str, FSM.State] = {}
        self.transitions: dict[str, list[FSM.Transition]] = {}
        self.finalized = False

        self.fsm_name = f"{name if name is not None else FSM.fsm_id}"
        FSM.fsm_id += 1
        self.gen_id = 0

        self.state_width = 0

    @property
    def fsm_name_prefix(self):
        return f"fsm_{self.fsm_name}_{self.gen_id}"

    @property
    def width(self):
        """
        Returns the width of the state signal.

        It is only available after the FSM is finalized.
        """
        if not self.finalized:
            raise ValueError("FSM is not finalized")
        return self.state_width

    def add_states(self, **states):
        """
        Add multiple states to the FSM.

        The code name are specified as the key of the arguments.
        Code will be automatically assigned if None is passed as the value.
        """
        for name, code in states.items():
            self.add_state(name, code)
        return self

    def add_state(self, name: str, code: None | int = None):
        """
        Add a state to the FSM.

        :param name: The name of the state
        :param code: The code of the state, if None, it will be automatically assigned
        """
        if self.finalized:
            raise ValueError("FSM is already finalized")

        if name in self.states:
            raise ValueError(f"State {name} already exists")
        if code is not None:
            existing_code = {state.code for state in self.states.values() if state.code is not None}
            if code in existing_code:
                raise ValueError(f"Code {code} already exists")

        self.states[name] = self.State(name, code, None)
        self.transitions[name] = []

        return self

    def add_transitions(self, *transitions: tuple[str, str, None | Signal]):
        """
        Add multiple transitions to the FSM.

        :param transitions: Tuples contain the source state, destination state, and the transition condition
        """
        for src, dst, cond in transitions:
            self.add_transition(src, dst, cond)
        return self

    def add_transition(self, src: str, dst: str, cond: None | Signal = None):
        """
        Add a transition to the FSM.

        :param src: The source state
        :param dst: The destination state
        :param cond: A single bit transition condition. None for unconditional transition.
        """
        if self.finalized:
            raise ValueError("FSM is already finalized")

        self._check_transition(src, dst, cond)
        self.transitions[src].append(self.Transition(dst, cond))
        return self

    def _check_transition(self, src: str, dst: str, cond: None | Signal = None):
        if self.finalized:
            raise ValueError("FSM is already finalized")
        if cond is not None and cond.width != 1:
            raise ValueError("All transition condition must have only 1 bit")
        if src not in self.states:
            raise ValueError(f"State {src} is not defined")
        if dst not in self.states:
            raise ValueError(f"State {dst} is not defined")

    def _finalize(self):
        if self.finalized:
            raise ValueError("FSM is already finalized")
        self.finalized = True

        # Fill in missing codes
        existing_code = {state.code for state in self.states.values() if state.code is not None}
        for state in self.states.values():
            if state.code is None:
                if len(existing_code) == 0:
                    state.code = 0
                else:
                    max_code = max(existing_code) if len(existing_code) else 0
                    free_codes = [c for c in range(max_code + 1) if c not in existing_code]
                    state.code = min(free_codes) if len(free_codes) else (max_code + 1)
                existing_code.add(state.code)

        # Generate states Constant signals
        self.state_width = max(state.code for state in self.states.values()).bit_length()
        for state_name, state in self.states.items():
            state.signal = Constant(
                state.code, width=self.state_width,
                name=f"const_{self.fsm_name}_state_{state_name}",
            )

        return self

    def _fsm_logic_one_state(self, transitions, prev_state) -> Signal:
        next_state: Signal = Constant(0, self.state_width)
        prev_cond: Signal = Constant(0, 1)

        for i, trans in enumerate(transitions):
            if trans.cond:
                next_state |= self.states[trans.next].signal.when((~prev_cond) & trans.cond, else_=0)
                prev_cond |= trans.cond
            else:
                if i != len(transitions) - 1:
                    raise ValueError("Unconditional transition can only be the last entry")
                next_state |= self.states[trans.next].signal.when(~prev_cond, else_=0)
                prev_cond = Constant(1, 1)
        next_state |= prev_state.when(~prev_cond, else_=0)

        return next_state

    def _gen_fsm_logic(self, prev_state: Signal) -> Signal:
        new_state_logics = {
            state: self._fsm_logic_one_state(transitions, prev_state)
            for state, transitions in self.transitions.items()
        }
        return prev_state.case(
            {
                self.states[state].code: next_state
                for state, next_state in new_state_logics.items()
            },
            default=prev_state,
        )

    def generate(
            self,
            reset_state: str, clk: Signal,
            reset: None | Signal = None,
            async_reset: None | Signal = None,
    ) -> Signal:
        """
        Generate the FSM and return the current state signal.

        :param reset_state: The initial state of the FSM
        :param clk: The clock signal
        :param reset: The synchronous reset signal
        :param async_reset: The asynchronous reset signal
        :returns: The current state signal
        """
        input_state, state = self.generate_unrolled(
            reset_state=reset_state,
            clk=clk,
            reset=reset,
            async_reset=async_reset,
        )
        input_state <<= state
        return state

    def generate_unrolled(
            self,
            reset_state: None | str = None,
            clk: None | Signal = None,
            reset: None | Signal = None,
            async_reset: None | Signal = None,
    ) -> tuple[Signal, Signal]:  # Input state, Next state
        """
        Generate the FSM logic and optionally register the output state in an unrolled manner.

        If clk is provided, the output state is registered and either reset or async_reset must be provided.
        The reset_state must be provided as well to specify the initial state of the FSM.

        If clk is not provided, only the next state logic is generated but not the output register.
        In this case, reset_state and reset signals are not required.

        :param reset_state: The initial state of the FSM
        :param clk: The clock signal
        :param reset: The synchronous reset signal
        :param async_reset: The asynchronous reset signal
        :returns: The input state and the next state
        """
        reg_output = clk is not None
        if reg_output:
            if async_reset is None and reset is None:
                raise ValueError("Specify at least one of the reset/async_reset signal")
            if reset_state is None:
                raise ValueError("Specify the reset state")
            if reset_state not in self.states:
                raise ValueError(f"Reset state {reset_state} is not defined")

        if not self.finalized:
            self._finalize()

        output_name = f"{self.fsm_name_prefix}_next"
        input_name = f"{self.fsm_name_prefix}_input"
        reg_name = f"{self.fsm_name_prefix}_state"
        self.gen_id += 1

        state_input = Signal(self.state_width, name=input_name)
        next_state = self._gen_fsm_logic(state_input)
        next_state.set_name(output_name)

        if reg_output:
            reset_value = self.states[reset_state].code
            next_state = next_state.reg(
                clk, name=reg_name,
                reset=reset, async_reset=async_reset,
                reset_value=reset_value, async_reset_value=reset_value,
            )

        return state_input, next_state
