import os
import os.path

from saw import LogResults, llvm_load_module, view

from env_server import env_connect_global

dir_path = os.path.dirname(os.path.realpath(__file__))

env_connect_global()
view(LogResults())

path = [dir_path, "libsignal-protocol-c", "build", "src", "libsignal-protocol-c.a.bc"]
bcname = os.path.join(*path)
print(bcname)
mod = llvm_load_module(bcname)
