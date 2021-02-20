# signal-verification

An effort to start verifying signal, demonstrating the SAW Python frontend in the process.

# Building `libsignal`

First build the signal bitcode with `wllvm`

From the root (make sure you've updated the submodule):

```
$ make
```

If that doesn't work, you can try running each of the commands in the `Makefile` individually:

```
$ cd libsignal-protocol-c/
$ mkdir build
$ cd build
$ LLVM_COMPILER=clang cmake -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=wllvm ..
$ LLVM_COMPILER=clang make
$ extract-bc -b src/libsignal-protocol-c.a
```

# Python environment

## [Poetry](https://python-poetry.org/)

First, [install `poetry`](https://python-poetry.org/docs/#installation) and then run:

```
$ poetry install
```

You should now be able to typecheck and run the files in this repo, e.g.,

```
$ poetry run mypy buffer.py
$ poetry run python buffer.py
```

## `virtualenv`

You'll need at least python 3.8 installed, be sure that the command below
uses python 3.8, not something lower.

```
*/signal-verification$ python3 -m venv virtenv
```

(vscode asks me to add the venv for the environment here. I said yes, either reload the terminal in vscode or)

```
$ . virtenv/bin/activate
```

install dependencies

```
/signal-verification$ pip install -r galois-py-toolkit/requirements.txt
```

BitVector failure in red, ignore

```
pip install -e galois-py-toolkit/
```

# Python environment

```
*/signal-verification$ python3 -m venv virtenv
```



then

```
$ pip install -r requirements.txt
```

this gives me an error about BitVector but I think it's ok

this part needs a better answer...

```
$ pip install -e ../saw-script/deps/argo/python/
$ export SAW_SERVER="saw-remote-api socket"
```

^ I don't know if that's permanent in the virtual environment. Probably not

```
$ python buffer.py
```
