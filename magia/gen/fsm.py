import copy
from dataclasses import dataclass, field
from typing import Optional

from magia import Constant, Signal


class FSMLogic:
    @dataclass
    class State:
        name: str
        code: Optional[int]
        signal: Constant = field(repr=False)
        desc: Optional[str] = field(default=None, repr=False)

    @dataclass
    class Transition:
        next: str
        cond: Optional[Signal] = None

    fsm_id = 0

    def __init__(
            self,
            clk: Signal,
            reset_state: str,
            reset: Optional[Signal] = None,
            async_reset: Optional[Signal] = None,
            name: Optional[str] = None,
            **kwargs,
    ):
        if async_reset is None and reset is None:
            raise ValueError("Specify at least one of the reset/async_reset signal")

        self.states: dict[str, FSMLogic.State] = {}
        self.transitions: dict[str, list[FSMLogic.Transition]] = {}
        self.finalized = False

        self.fsm_name = f"{name if name else self.fsm_id}"
        self.fsm_id += 1
        self.gen_id = 0

        self.state_width = 0
        self.reset_state = reset_state
        self._clocking = {
            "clk": clk,
            "reset": reset,
            "async_reset": async_reset,
        }

    @property
    def width(self):
        if not self.finalized:
            raise ValueError("FSM is not finalized")
        return self.state_width

    def add_states(self, **states):
        for name, code in states.items():
            self.add_state(name, code)
        return self

    def add_state(self, name: str, code: Optional[int] = None):
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

    def add_transitions(self, *transitions: tuple[str, str, Optional[Signal]]):
        for src, dst, cond in transitions:
            self.add_transition(src, dst, cond)
        return self

    def _check_transition(self, src: str, dst: str, cond: Optional[Signal] = None):
        if self.finalized:
            raise ValueError("FSM is already finalized")
        if cond is not None and cond.width != 1:
            raise ValueError("All transition condition must have only 1 bit")
        if src not in self.states:
            raise ValueError(f"State {src} is not defined")
        if dst not in self.states:
            raise ValueError(f"State {dst} is not defined")

    def add_transition(self, src: str, dst: str, cond: Optional[Signal] = None):
        self._check_transition(src, dst, cond)
        self.transitions[src].append(self.Transition(dst, cond))
        return self

    def push_transition(self, src: str, dst: str, cond: Optional[Signal] = None):
        self._check_transition(src, dst, cond)
        self.transitions[src].insert(0, self.Transition(dst, cond))
        return self

    def finalize(self):
        if self.finalized:
            raise ValueError("FSM is already finalized")
        self.finalized = True

        # Check if reset state exists
        if self.reset_state not in self.states:
            raise ValueError(f"Reset state {self.reset_state} is not defined")

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
        next_state = Constant(0, self.state_width)
        prev_cond = Constant(0, 1)

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
        new_state = prev_state.case(
            {
                self.states[state].code: next_state
                for state, next_state in new_state_logics.items()
            },
            default=prev_state,
        )
        return new_state

    def generate(self) -> tuple[Signal, Signal]:  # (input, state register)
        if not self.finalized:
            self.finalize()

        register_name = f"fsm_{self.fsm_name}_{self.gen_id}_state"
        input_name = f"fsm_{self.fsm_name}_{self.gen_id}_input"
        self.gen_id += 1

        reset_value = self.states[self.reset_state].code

        state_input = Signal(self.state_width, name=input_name)
        state_register = self._gen_fsm_logic(state_input).reg(
            name=register_name,
            reset_value=reset_value,
            async_reset_value=reset_value,
            **self._clocking,
        )

        return state_input, state_register

    def copy(self, name: Optional[str] = None, **kwargs) -> "FSMLogic":
        new_fsm = FSMLogic(
            **kwargs,
            reset_state=self.reset_state,
            name=name,
            **self._clocking,
        )
        new_fsm.states = copy.deepcopy(self.states)
        new_fsm.transitions = {
            state: [(src, dst, cond) for src, dst, cond in transitions]
            for state, transitions in self.transitions.items()
        }
        return new_fsm


class FSM:
    def __init__(
            self,
            clk: Signal,
            reset_state: str,
            reset: Optional[Signal] = None,
            async_reset: Optional[Signal] = None,
            name: Optional[str] = None,
            fsm_stage: Optional[FSMLogic] = None,
            **kwargs,
    ):
        self.fsm_logic = FSMLogic(
            clk, reset_state, reset, async_reset, name, **kwargs
        ) if fsm_stage is None else fsm_stage
        self.state: Optional[Signal] = None

    @property
    def states(self):
        return self.fsm_logic.states

    @property
    def transitions(self):
        return self.fsm_logic.transitions

    @property
    def width(self):
        if not self.fsm_logic.finalized:
            raise ValueError("FSM is not finalized")
        return self.fsm_logic.state_width

    def add_states(self, **states):
        self.fsm_logic.add_states(**states)
        return self

    def add_state(self, name: str, code: Optional[int] = None):
        self.fsm_logic.add_state(name, code)
        return self

    def add_transitions(self, *transitions: tuple[str, str, Optional[Signal]]):
        self.fsm_logic.add_transitions(*transitions)
        return self

    def add_transition(self, src: str, dst: str, cond: Optional[Signal] = None):
        self.fsm_logic.add_transition(src, dst, cond)
        return self

    def push_transition(self, src: str, dst: str, cond: Optional[Signal] = None):
        self.fsm_logic.push_transition(src, dst, cond)
        return self

    def finalize(self):
        self.fsm_logic.finalize()
        return self

    def generate(self) -> Signal:
        if self.state:
            raise ValueError("FSM has already been generated")

        prev, self.state = self.fsm_logic.generate()
        prev <<= self.state
        return self.state
