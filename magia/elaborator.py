from __future__ import annotations

from os import PathLike
from pathlib import Path

from .module import Module


class Elaborator:
    """Elaborator is a helper class to elaborate modules."""

    name_to_module: dict[str, Module] = {}

    def __init__(self):
        raise NotImplementedError("Elaborator is a helper class and should not be instantiated.")

    @classmethod
    def to_dict(cls, *modules: Module, top_only: bool = False) -> dict[str, str]:
        """
        Elaborate all modules in the list.

        Each module will be elaborated only once and return the SystemVerilog code, plus a list of submodules
        Duplicated submodules will not be elaborated again.
        The elaboration is done recursively, until all submodules are elaborated.

        :param modules: The modules to be elaborated.
        :param top_only: If True, Elaborator will skip the submodules instantiated by `modules`
        :returns: A dictionary of the SystemVerilog code for each module.
        """
        cls.name_to_module = {}
        modules = list(modules)
        elaborated_modules: dict[str, str] = {}
        while modules:
            mod = modules.pop()
            cls.name_to_module[mod.name] = mod
            if mod.name not in elaborated_modules:
                sv_code, submodules = mod.elaborate()
                elaborated_modules[mod.name] = sv_code
                if not top_only:
                    modules += submodules
        return elaborated_modules

    @classmethod
    def to_string(cls, *modules: Module, top_only: bool = False) -> str:
        """Elaborate all modules in the list and return the SystemVerilog code as a string."""
        return "\n\n".join(cls.to_dict(*modules, top_only=top_only).values())

    @classmethod
    def to_file(cls, filename: PathLike, *modules: Module, top_only: bool = False):
        """Elaborate all modules in the list and write the SystemVerilog code to a file."""
        sv_code = cls.to_string(*modules, top_only=top_only)
        Path(filename).write_text(sv_code)

    @classmethod
    def to_files(
            cls, output_dir: PathLike, /,
            *modules: Module,
            force: bool = False,
            top_only: bool = False
    ) -> list[Path]:
        """
        Elaborate all modules in the list and write the SystemVerilog code to files.

        The files are written to the output directory.

        :param output_dir: The output directory.
        :param modules: The modules to be elaborated.
        :param force: If True, files in the output directory will be overwritten if it exists.
        :param top_only: If True, Elaborator will skip the submodules instantiated by `modules`

        :returns: A list of Path objects of the files written.
        """
        output_dir = Path(output_dir)
        if not force and output_dir.is_dir() and any(output_dir.iterdir()):
            raise FileExistsError(f"Directory {output_dir} already exists and not empty.")
        output_dir.mkdir(parents=True, exist_ok=True)

        result = cls.to_dict(*modules, top_only=top_only)
        result_by_file: dict[str, list[str]] = {}

        # Categorize by output file
        for fname, sv_code in result.items():
            module = cls.name_to_module[fname]
            output_file = f"{fname}.sv" if module.output_file is None else module.output_file

            if output_file not in result_by_file:
                result_by_file[output_file] = []
            result_by_file[output_file].append(sv_code)

        # Write to files
        for fname, sv_codes in result_by_file.items():
            sv_code = "\n\n".join(sv_codes)
            Path(output_dir, fname).write_text(sv_code)

        return [Path(output_dir, fname) for fname in result_by_file]

    @staticmethod
    def file(fname: PathLike):
        """
        Return a class decorator to register the filename of generated code to a Module.

        The effect is employed by the `to_files` method only.

        Example:
        @Elaborator.file("adder.sv")
        class Adder(Module):
            ...

        Elaborator.to_files("/tmp/output", Adder(name="adder1"), Adder(name="adder2"))
        # Result in /tmp/output/adder.sv with 2 adders.
        """

        def decorator(cls: type[Module]):
            cls.output_file = Path(fname)
            return cls

        return decorator
