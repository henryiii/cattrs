"""Preconfigured converters for the stdlib json."""
from base64 import b85decode, b85encode
from datetime import datetime

from .._compat import Counter, Set
from ..converters import Converter, GenConverter


def configure_converter(converter: Converter):
    """
    Configure the converter for use with the stdlib json module.

    * bytes are serialized as base64 strings
    * datetimes are serialized as ISO 8601
    * counters are serialized as dicts
    * sets are serialized as lists
    """
    converter.register_unstructure_hook(
        bytes, lambda v: (b85encode(v) if v else b"").decode("utf8")
    )
    converter.register_structure_hook(bytes, lambda v, _: b85decode(v))
    converter.register_unstructure_hook(datetime, lambda v: v.isoformat())
    converter.register_structure_hook(datetime, lambda v, _: datetime.fromisoformat(v))


def make_converter(*args, **kwargs) -> GenConverter:
    kwargs["unstruct_collection_overrides"] = {
        **kwargs.get("unstruct_collection_overrides", {}),
        Set: list,
        Counter: dict,
    }
    res = GenConverter(*args, **kwargs)
    configure_converter(res)

    return res
