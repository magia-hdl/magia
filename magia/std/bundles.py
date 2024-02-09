"""
This module provides factory functions to create common BundleSpec objects.
"""

from typing import Union

from magia import BundleSpec, Input, IOPorts, Output, Signal


def valid_bundle(signals: Union[list[Signal], IOPorts], valid: str = "valid") -> BundleSpec:
    """
    Create a BundleSpec with the given signals and a valid signal.

    :param signals: A list of Input/Outputs or an IOPorts object
    :param valid: The name of the valid signal, default is "valid"
    """
    spec = BundleSpec()
    spec += signals
    spec += Output(name=valid, width=1, description="Indicates that the data is valid")
    return spec


def decoupled_bundle(signals: Union[list[Signal], IOPorts], valid: str = "valid", ready: str = "ready") -> BundleSpec:
    """
    Create a BundleSpec with the given signals, a valid signal and a ready signal.

    :param signals: A list of Input/Outputs or an IOPorts object
    :param valid: The name of the valid signal, default is "valid"
    :param ready: The name of the ready signal, default is "ready"
    """
    spec = BundleSpec()
    spec += signals
    spec += Output(name=valid, width=1, description="Indicates that the data from the driver is valid")
    spec += Input(name=ready, width=1, description="Indicates that the data is being accepted by the receiver")
    return spec


def valid_signal(name: str = "data", valid: str = "valid", **kwargs_signal) -> BundleSpec:
    """
    Shortcut to create a BundleSpec with only one data signal and a valid signal.

    :param name: The name of the data signal
    :param valid: The name of the valid signal
    :param kwargs_signal: Additional parameters for the data signal, e.g. width, signed, etc.
    """
    return valid_bundle([Output(name=name, **kwargs_signal)], valid=valid)


def decoupled_signal(name: str = "data", valid: str = "valid", ready: str = "ready", **kwargs_signal) -> BundleSpec:
    """
    Shortcut to create a BundleSpec with only one data signal, a valid signal and a ready signal.

    :param name: The name of the data signal
    :param valid: The name of the valid signal
    :param ready: The name of the ready signal
    :param kwargs_signal: Additional parameters for the data signal, e.g. width, signed, etc.
    """
    return decoupled_bundle([Output(name=name, **kwargs_signal)], valid=valid, ready=ready)
