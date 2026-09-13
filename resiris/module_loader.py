from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ModuleInfo:
    """Python-side prototype metadata for a loaded Resiris module."""

    name: str
    functions: str
    variables: str


class ModuleLoader:
    """Minimal Python-side Resiris module loader prototype."""

    def __init__(self, modules_dir: Path | str = "Modules"):
        self.modules_dir = Path(modules_dir)
        self.loaded: dict[str, object] = {}
        self.info: dict[str, ModuleInfo] = {}

    def load(self, module_name: str):
        if module_name in self.loaded:
            raise RuntimeErrorResirisModule(
                f'{module_name} is already included. Error code:"SameModuleMultiCall"'
            )

        module_path = self.modules_dir / f"{module_name}.py"
        if not module_path.is_file():
            raise RuntimeErrorResirisModule(
                f'{module_name} not found! Error code:"MissingModule"'
            )

        internal_name = f"_resiris_module_{module_name}"
        spec = importlib.util.spec_from_file_location(internal_name, module_path)
        if spec is None or spec.loader is None:
            raise RuntimeErrorResirisModule(
                f"{module_name}: module could not be loaded"
            )

        module = importlib.util.module_from_spec(spec)
        sys.modules[internal_name] = module
        try:
            spec.loader.exec_module(module)
            init = getattr(module, "_INIT_", None)
            if not callable(init):
                raise RuntimeErrorResirisModule(
                    f"{module_name}: _INIT_ function is required"
                )
            init()

            name = self._read_string_constant(module, module_name, "NAME")
            functions = self._read_string_constant(module, module_name, "FUNCTIONS")
            variables = self._read_string_constant(module, module_name, "VARIABLES")

            if name != module_name:
                raise RuntimeErrorResirisModule(
                    f'{module_name}: NAME constant must be "{module_name}"'
                )

            self.info[module_name] = ModuleInfo(
                name=name,
                functions=functions,
                variables=variables,
            )
        except Exception:
            self.info.pop(module_name, None)
            sys.modules.pop(internal_name, None)
            raise

        self.loaded[module_name] = module
        return module

    @staticmethod
    def _read_string_constant(module, module_name: str, constant_name: str) -> str:
        if not hasattr(module, constant_name):
            raise RuntimeErrorResirisModule(
                f'{module_name}: required constant "{constant_name}" is missing'
            )

        value = getattr(module, constant_name)
        if not isinstance(value, str):
            raise RuntimeErrorResirisModule(
                f'{module_name}: "{constant_name}" must be a string'
            )

        return value


class RuntimeErrorResirisModule(Exception):
    """Internal module-loading error; converted by the Interpreter."""
