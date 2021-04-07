import os
import os.path

from saw import llvm_verify
from saw.llvm import Contract, cryptol, elem, field, global_var, struct, void
from saw.llvm_types import alias, array, i8, i64, ptr, struct_type

from buffer_helpers import *
from load import mod
from saw_helpers import *


class BufferAllocSpec(Contract):
    length: int

    def __init__(self, length: int):
        super().__init__()
        self.length = length

    def specification(self) -> None:
        n_val = int_to_64_cryptol(self.length)

        self.execute_func(n_val)

        buf = alloc_buffer_aligned(self, self.length)
        self.points_to(elem(buf, 0), n_val, check_target_type = i64)
        self.returns(buf)

class BufferCreateSpec(Contract):
    length: int

    def __init__(self, length: int):
        super().__init__()
        self.length = length

    def specification(self) -> None:
        (data, datap) = ptr_to_fresh(self, array(self.length, i8), name = "data")

        self.execute_func(datap, int_to_64_cryptol(self.length))

        buf = alloc_pointsto_buffer(self, self.length, data)
        self.returns(buf)

class BufferCopySpec(Contract):
    length: int

    def __init__(self, length: int):
        super().__init__()
        self.length = length

    def specification(self) -> None:
        data = self.fresh_var(array(self.length, i8), "data")
        buf  = alloc_pointsto_buffer_readonly(self, self.length, data)

        self.execute_func(buf)

        new_buf = alloc_pointsto_buffer(self, self.length, data)
        self.returns(new_buf)

class BufferCopyNSpec(Contract):
    length: int
    n: int

    def __init__(self, length: int, n: int):
        super().__init__()
        self.length = length
        self.n = n

    def specification(self) -> None:
        data = self.fresh_var(array(self.length, i8), "data")
        buf  = alloc_pointsto_buffer_readonly(self, self.length, data)

        self.execute_func(buf, int_to_64_cryptol(self.n))

        new_length = min(self.length, self.n)

        new_buf = alloc_pointsto_buffer(self, new_length, cryptol("take`{i} data".format(i=new_length)))
        self.returns(new_buf)

class BufferAppendSpec(Contract):
    buf_length: int
    additional_length: int

    def __init__(self, buf_length: int, additional_length: int):
        super().__init__()
        self.buf_length = buf_length
        self.additional_length = additional_length

    def specification(self) -> None:
        buf_data = self.fresh_var(array(self.buf_length, i8), "buffer_data")
        buf      = alloc_pointsto_buffer(self, self.buf_length, buf_data)

        (additional_data, additional_datap) = ptr_to_fresh(self, array(self.additional_length, i8),
                                                           name = "additional_data")

        self.execute_func(buf, additional_datap, int_to_64_cryptol(self.additional_length))

        new_length = self.buf_length + self.additional_length;
        new_buf    = alloc_pointsto_buffer(self, new_length,
                                           cryptol(f"{buf_data.name()} # {additional_data.name()}"))
        self.returns(new_buf)

class ConstantMemcmpSpec(Contract):
    n: int

    def __init__(self, n: int):
        super().__init__()
        self.n = n

    def specification(self) -> None:
        (s1, s1p) = ptr_to_fresh(self, array(self.n, i8), name = "s1")
        (s2, s2p) = ptr_to_fresh(self, array(self.n, i8), name = "s2")
        nval = int_to_64_cryptol(self.n)

        self.execute_func(s1p, s2p, nval)

        self.returns(cryptol(f"zext`{{32}} (foldl (||) zero (zipWith (^) {s1.name()} {s2.name()}))"))

DJB_TYPE = 0x05
DJB_KEY_LEN = 32

class ECPublicKeySerializeSpec(Contract):
    def specification(self) -> None:
        length = DJB_KEY_LEN + 1
        signal_type_base_ty = alias("struct.signal_type_base")
        djb_array_ty = array(DJB_KEY_LEN, i8)
        buffer_ = self.alloc(ptr(buffer_type(length)))
        key_base = self.fresh_var(signal_type_base_ty, "key_base")
        key_data = self.fresh_var(djb_array_ty, "key_data")
        key = self.alloc(struct_type(signal_type_base_ty, djb_array_ty),
                         points_to = struct(key_base, key_data))

        self.execute_func(buffer_, key)

        buf = alloc_pointsto_buffer(self, length,
                                    cryptol(f"[`({DJB_TYPE})] # {key_data.name()} : [{length}][8]"))
        self.points_to(buffer_, buf)
        self.returns(int_to_32_cryptol(0))

class SignalTypeInitSpec(Contract):
    def specification(self) -> None:
        instance = self.alloc(alias("struct.signal_type_base"))
        destroy_func = global_var("signal_message_destroy")

        self.execute_func(instance, destroy_func)

        self.points_to(field(instance, "ref_count"), int_to_32_cryptol(1))
        self.points_to(field(instance, "destroy"), destroy_func)
        self.returns(void)

buffer_alloc_ov     = llvm_verify(mod, "signal_buffer_alloc",    BufferAllocSpec(64))
buffer_create_ov    = llvm_verify(mod, "signal_buffer_create",   BufferCreateSpec(64))
buffer_copy_ov      = llvm_verify(mod, "signal_buffer_copy",     BufferCopySpec(63))
buffer_copy_n_ov    = llvm_verify(mod, "signal_buffer_n_copy",   BufferCopyNSpec(64, 31))
buffer_append_ov    = llvm_verify(mod, "signal_buffer_append",   BufferAppendSpec(63, 31))
constant_memcmp_ov  = llvm_verify(mod, "signal_constant_memcmp", ConstantMemcmpSpec(63))
signal_type_init_ov = llvm_verify(mod, "signal_type_init",       SignalTypeInitSpec())