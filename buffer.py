import os
import os.path
from cryptol.cryptoltypes import to_cryptol
from saw import *
from saw.llvm import Contract, void, SetupVal, FreshVar, cryptol
from saw.llvm_types import i8, i32, LLVMType, LLVMArrayType
from env_server import *

dir_path = os.path.dirname(os.path.realpath(__file__))

env_connect_global()
view(LogResults())

bcname = os.path.join(dir_path, 'salsa20.bc')
