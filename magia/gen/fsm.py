from collections import UserDict
from dataclasses import dataclass, field
from typing import Optional

from magia import Constant, Register, Signal


class FSM:
    @dataclass
    class State:
        name: str
        code: int
        signal: Constant = field(repr=False)

    @dataclass
    class Transition:
        next: str
        cond: Optional[Signal] = None
        desc: str = ""

        def __post_init__(self):
            if self.cond is not None and self.cond.width != 1:
                raise ValueError("All transition condition must have only 1 bit")

    fsm_id = 0

    def __init__(
            self,
            clk: Signal,
            states: dict[str, int],
            transitions: dict[str, list],
            reset_state: str,
            reset: Optional[Signal] = None,
            async_reset: Optional[Signal] = None,
            description: Optional[str] = None,
            name: Optional[str] = None,
    ):
        if async_reset is None and reset is None:
            raise ValueError("Specify at least one of the reset/async_reset signal")
        if reset_state not in states:
            raise ValueError(f"Reset state is not defined in states {reset_state=}")

        self.name = f"{name if name else self.fsm_id}"
        self.name_signal = f"fsm_{self.name}"
        self.fsm_id += 1
        self.description = description

        self._states, state_width = self._init_states(states)

        _update_state = Signal(1)
        self._state = Register(
            name=f"{self.name_signal}_state",
            width=state_width,
            clk=clk,
            enable=_update_state,
            reset=reset, async_reset=async_reset,
            reset_value=self.states[reset_state].code,
            async_reset_value=self.states[reset_state].code,
        )

        self.transitions = {
            state: [
                self.Transition(**trans) if not isinstance(trans, self.Transition) else trans
                for trans in trans_list
            ]
            for state, trans_list in transitions.items()
        }
        self._validate_transitions()

        next_state, update_state = self._gen_fsm_signals()
        self._state <<= next_state
        _update_state <<= update_state

    @property
    def state(self):
        return self._state

    @property
    def states(self):
        return self._states

    @property
    def width(self):
        return self.state.width

    def case(self, default=None, **cases):
        cases = {
            self.states[state].code: signal
            for state, signal in cases.items()
        }
        return self.state.case(cases, default)

    def _one_state_signals(self, transitions) -> tuple[Signal, Signal]:
        next_state = Constant(0, self.state_width)
        update_state = Constant(0, 1)
        prev_cond = Constant(0, 1)

        for i, trans in enumerate(transitions):
            if trans.cond:
                next_state |= self.states[trans.next].signal.when((~prev_cond) & trans.cond, else_=0)
                update_state |= trans.cond
                prev_cond |= trans.cond
            else:
                if i != len(transitions) - 1:
                    raise ValueError("Unconditional transition can only be the last entry")
                next_state |= self.states[trans.next].signal.when(~prev_cond, else_=0)
                update_state = Constant(1, 1)

        return next_state, update_state

    def _gen_fsm_signals(self) -> tuple[Signal, Signal]:
        next_and_update = {
            state: self._one_state_signals(transitions)  # next_state, update_state
            for state, transitions in self.transitions.items()
        }
        next_state = self.state.case(
            {
                self.states[state].code: next_up[0]
                for state, next_up in next_and_update.items()
            },
            default=self.state
        )
        update_state = self.state.case(
            {
                self.states[state].code: next_up[1]
                for state, next_up in next_and_update.items()
            },
            default=0
        )
        return next_state, update_state

    def _validate_transitions(self):
        for src_state, trans_lists in self.transitions.items():
            if src_state not in self.states:
                raise ValueError("State in transitions is undefined: {src_state}")
            for transition in trans_lists:
                if transition.next not in self.states:
                    raise ValueError("State in transitions is undefined: {transition.next_state}")

    def _init_states(self, states: dict[str, int]) -> tuple[dict[str, State], int]:
        max_code = max(states.values())
        state_width = max_code.bit_length()
        states_in_fsm = UserDict(**{
            name: self.State(
                name=name,
                code=code,
                signal=Constant(
                    name=f"const_{self.name_signal}_state_{name}",
                    value=code, width=state_width,
                )
            )
            for name, code in states.items()
        })
        for name in states:
            setattr(states_in_fsm, name, states_in_fsm[name])
        return states_in_fsm, state_width
