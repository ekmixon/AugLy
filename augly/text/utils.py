#!/usr/bin/env python3
# Copyright (c) Facebook, Inc. and its affiliates.

from copy import deepcopy
from typing import Any, Dict, List, Optional

import augly.text.intensity as txtintensity


def get_func_kwargs(
    metadata: Optional[List[Dict[str, Any]]], local_kwargs: Dict[str, Any], **kwargs
) -> Dict[str, Any]:
    if metadata is None:
        return {}
    func_kwargs = deepcopy(local_kwargs)
    func_kwargs.pop("metadata")
    func_kwargs.update(**kwargs)
    return func_kwargs


def get_metadata(
    metadata: Optional[List[Dict[str, Any]]],
    function_name: str,
    texts: Optional[List[str]] = None,
    aug_texts: Optional[List[str]] = None,
    **kwargs,
) -> None:
    if metadata is None:
        return

    assert isinstance(
        metadata, list
    ), "Expected `metadata` to be set to None or of type list"
    assert (
        texts is not None
    ), "Expected `texts` to be passed in if metadata was provided"
    assert (
        aug_texts is not None
    ), "Expected `aug_texts` to be passed in if metadata was provided"

    metadata.append(
        {
            "name": function_name,
            "input_type": "list" if isinstance(texts, list) else "string",
            "src_length": len(texts) if isinstance(texts, list) else 1,
            "dst_length": len(aug_texts),
            **kwargs,
        }
    )

    intensity_kwargs = {"metadata": metadata[-1], **kwargs}
    metadata[-1]["intensity"] = getattr(
        txtintensity, f"{function_name}_intensity", lambda **_: 0.0
    )(**intensity_kwargs)