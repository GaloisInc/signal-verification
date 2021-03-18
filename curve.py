from saw import llvm_verify
from saw.llvm import Contract, struct
from saw.llvm_types import alias, array, i8, ptr, struct_type

from buffer_helpers import *
from load import mod
from saw_helpers import *

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

ec_public_key_serialize_ov = llvm_verify(mod, "ec_public_key_serialize", ECPublicKeySerializeSpec())
