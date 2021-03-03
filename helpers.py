from typing import Tuple

from saw import *
from saw.llvm import Contract, FreshVar, SetupVal
from saw.llvm_types import LLVMType


def ptr_to_fresh(spec : Contract, ty : LLVMType, name : Optional[str] = None) -> Tuple[FreshVar, SetupVal]:
    """Add to``Contract`` ``spec`` an allocation of a pointer of type ``ty`` initialized to an unknown fresh value.

    :returns A fresh variable bound to the pointers initial value and the newly allocated pointer. (The fresh
             variable will be assigned ``name`` if provided/available.)"""
    var = spec.fresh_var(ty, name)
    ptr = spec.alloc(ty, points_to = var)
    return (var, ptr)
