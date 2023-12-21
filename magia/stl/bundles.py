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


