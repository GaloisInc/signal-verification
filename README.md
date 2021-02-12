# signal-verification

An effort to start verifying signal, demonstrating the SAW Python frontend in the process.

# Building

First build the signal bitcode with wllvm

From the root (make sure you've updated the submodule)

> $ cd libsignal-protocol-c/

> $ mkdir build

> $ cd build

> $ LLVM_COMPILER=clang cmake -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=wllvm ..

> $ LLVM_COMPILER=clang make

> $ extract-bc src/libsignal-protocol-c.a

I have no idea if we can use that output with SAW

# Python environment

> */signal-verification$ python3 -m venv virtenv

(vscode asks me to add the venv for the environment here. I said yes, either reload the terminal in vscode or)

> . virtenv/bin/activate

then

> pip install -r requirements.txt

this gives me an error about BitVector but I think it's ok

this part needs a better answer...

> pip install -e ../saw-script/deps/argo/python/

> export SAW_SERVER="saw-remote-api socket"

^ I don't know if that's permanent in the virtual environment. Probably not

> python buffer.py