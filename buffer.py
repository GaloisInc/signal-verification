import os
import os.path
from cryptol.cryptoltypes import to_cryptol
from saw import *
from saw.llvm import Contract, void, SetupVal, FreshVar, cryptol, struct
from saw.llvm_types import i8, i32, LLVMType, LLVMArrayType, LLVMAliasType
from env_server import *

dir_path = os.path.dirname(os.path.realpath(__file__))

env_connect_global()
view(LogResults())

path = [dir_path, "libsignal-protocol-c", "build", "src", "libsignal-protocol-c.a.bc"]
bcname = os.path.join(*path)
print(bcname)
mod = llvm_load_module(bcname)

def int_to_32_cryptol(n):
    return llvm.cryptol("`{n}:[32]".format(n=n))

def int_to_64_cryptol(n):
    return llvm.cryptol("`{n}:[64]".format(n=n))

def fresh_signal_buffer(spec:Contract, n):
    buf = spec.alloc(LLVMAliasType("struct.signal_buffer"))
    datav = spec.fresh_var(LLVMArrayType(i8,0),"data")
    #datap = spec.alloc(LLVMArrayType(i8, n))
    #spec.points_to(llvm.field(buf, "len"), llvm.cryptol("`{n}:[32]".format(n=n)))
    #spec.points_to(llvm.field(buf, "data"), datap)
    lenval = int_to_64_cryptol(n)
    spec.points_to(buf, struct(lenval,datav))
    return (buf, datav)


class BufferAllocSpec(Contract):
    def __init__(self, n):
        super().__init__()
        self.n = n

    def specification(self) -> None:
        self.execute_func(int_to_64_cryptol(self.n))
        (buf, _) = fresh_signal_buffer(self, self.n)
        self.returns(buf)

buffer_alloc_ov = llvm_verify(mod, "signal_buffer_alloc", BufferAllocSpec(64))