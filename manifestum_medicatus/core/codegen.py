"""
Генерация исходного кода Python-модулей manifests_diff/*/get_config() из
обычных словарей (dict), с типами, выведенными из полей Pydantic-моделей.

Используется importer.py при импорте существующих готовых yaml-манифестов
агента в централизованное хранилище manifests_diff.
"""
import typing
from typing import Any, Dict, Type

from pydantic import BaseModel

VAR_NAME_BY_MODEL = {
    "AgentConfig": "agent",
    "CommonConfig": "common",
    "NamespaceConfig": "namespace",
    "IntegrationConfig": "integration",
}

INDENT = "    "


def _unwrap_optional(annotation: Any) -> Any:
    origin = typing.get_origin(annotation)
    if origin is typing.Union:
        args = [a for a in typing.get_args(annotation) if a is not type(None)]
        if len(args) == 1:
            return args[0]
    return annotation


def _render_value(value: Any, annotation: Any, indent: int, used: set) -> str:
    ann = _unwrap_optional(annotation)
    origin = typing.get_origin(ann)
    pad = INDENT * indent
    pad_in = INDENT * (indent + 1)

    if isinstance(value, dict):
        if isinstance(ann, type) and issubclass(ann, BaseModel):
            used.add(ann)
            fields = ann.model_fields
            lines = []
            for key, sub_value in value.items():
                field_ann = fields[key].annotation
                rendered = _render_value(sub_value, field_ann, indent + 1, used)
                lines.append(f"{pad_in}{key}={rendered}")
            if not lines:
                return f"{ann.__name__}()"
            return f"{ann.__name__}(\n" + ",\n".join(lines) + f",\n{pad})"

        if origin is dict:
            _, val_type = typing.get_args(ann)
            lines = []
            for key, sub_value in value.items():
                rendered = _render_value(sub_value, val_type, indent + 1, used)
                lines.append(f"{pad_in}{key!r}: {rendered}")
            if not lines:
                return "{}"
            return "{\n" + ",\n".join(lines) + f",\n{pad}}}"

        # untyped dict fallback (e.g. Dict[str, str] ENV)
        lines = [f"{pad_in}{key!r}: {value[key]!r}" for key in value]
        if not lines:
            return "{}"
        return "{\n" + ",\n".join(lines) + f",\n{pad}}}"

    if isinstance(value, list):
        item_ann = None
        if origin is list:
            (item_ann,) = typing.get_args(ann)
        lines = []
        for item in value:
            rendered = _render_value(item, item_ann, indent + 1, used)
            lines.append(f"{pad_in}{rendered}")
        if not lines:
            return "[]"
        return "[\n" + ",\n".join(lines) + f",\n{pad}]"

    return repr(value)


def render_module(model_class: Type[BaseModel], data: Dict[str, Any], exclude_none: bool = False) -> str:
    """
    Рендерит исходный код модуля manifests_diff-слоя вида:

        from manifestum_medicatus.models.xxx import ModelClass, ...

        def get_config():
            var = ModelClass(
                FIELD=...,
            )
            return var.model_dump(exclude_unset=True[, exclude_none=True])
    """
    used: set = set()
    var_name = VAR_NAME_BY_MODEL.get(model_class.__name__, "config")

    if not data:
        body = f"{model_class.__name__}()"
        used.add(model_class)
    else:
        body = _render_value(data, model_class, 1, used)
        used.add(model_class)

    module_name = model_class.__module__
    class_names = sorted({cls.__name__ for cls in used})
    import_line = f"from {module_name} import {', '.join(class_names)}"

    dump_kwargs = "exclude_unset=True"
    if exclude_none:
        dump_kwargs += ", exclude_none=True"

    lines = [
        import_line,
        "",
        "",
        "def get_config():",
        f"    {var_name} = {body}",
        "",
        f"    return {var_name}.model_dump({dump_kwargs})",
        "",
    ]
    return "\n".join(lines)


def render_empty_module(model_class: Type[BaseModel]) -> str:
    """Валидная заглушка слоя без единого установленного поля."""
    return render_module(model_class, {})
