# signal-verification

An effort to start verifying signal, demonstrating the SAW Python frontend in the process.

# Note to readers

The contents of this repo have been folded into
[`saw-demos`](https://github.com/GaloisInc/saw-demos), so go there for the
latest code. The contents of this repo are mostly of historical interest.

# Building dependencies

First, install the following prerequisites:

* [Clang](https://clang.llvm.org/)
* [CMake](https://cmake.org/)
* [GHC](https://www.haskell.org/ghc/) (8.6 or later) and [`cabal`](https://www.haskell.org/cabal/)
* [Python](https://www.python.org/) (3.8 or later) and [Poetry](https://python-poetry.org/)
* [WLLVM](https://github.com/travitch/whole-program-llvm)

The following is optional, but highly recommended:

* [`direnv`](https://direnv.net/)

Next, you will need to clone the submodules:

```
$ git submodule update --init
```

Then, you can build all of the dependencies with:

```
$ make
```

Alternatively, if you want to be more explicit, you can run:

```
$ make libsignal
$ make saw-haskell
$ make saw-python-poetry
```

This will build all of the C, Haskell, and Python dependencies, respectively.
Refer to the following sections for more details on what this entails.

## Building `libsignal`

First, you will need to build the `libsignal-protocol-c` library using
[`wllvm`](https://github.com/travitch/whole-program-llvm).

From the root (make sure you've updated the submodule):

```
$ make libsignal
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

## Building `saw` and `saw-remote-api`.

You will need a development version of `saw` and `saw-remote-api`. To do so:

```
$ make saw-haskell
```

Alternatively, if you want to be more explicit:

```
$ (cd saw-script && ./build)
```

This will produce binaries under the `saw-script/bin/` directory, which will
used when invoking the Python code.

## Building a Python environment

There are two ways of building a Python environment:

* [Poetry](https://python-poetry.org/) (recommended)
* `virtualenv`

### Poetry

Run the following command:

```
$ make saw-python
```

Alternatively:

```
$ poetry install
```

You should now be able to typecheck and the files in this repo as a sanity
check:

```
$ poetry run mypy python/main.py
```

### `virtualenv`

As an alternative to Poetry, you can install the Python dependencies in a
`virtualenv`. To build an appropriate `virtualenv`, run the following script:

```
$ ./build-virtenv.sh
```

And then activate it with:

```
$ source virtenv/bin/activate
```

Alternatively, run the following steps. First, create the `virtualenv`:

```
$ python3 -m venv virtenv
```

(vscode asks me to add the venv for the environment here. I said yes, either reload the terminal in vscode or)

Next, activate it with:

```
$ source virtenv/bin/activate
```

Now install the Cryptol and SAW bindings' dependencies:

```
$ pip install -r saw-script/deps/cryptol/cryptol-remote-api/python/requirements.txt
$ pip install -r saw-script/saw/saw-remote-api/python/requirements.txt
```

(Note that installing `BitVector` will appear to fail with a red error message,
but in actuality, the overall installation will succeed. You can safely ignore
the scary-looking red error message bit.)

Now install the libraries themselves:

```
$ pip install -e saw-script/deps/cryptol/cryptol-remote-api/python/
$ pip install -e saw-script/saw/saw-remote-api/python/
```

To leave the `virtualenv`, run:

```
$ deactivate
```

# Running

First, you will need to run the following to ensure that the appropriate
environment variables are set:

```
$ source .envrc
```

Note that if you have [`direnv`](https://direnv.net/) installed, this step will
automatically happen behind the scenes.

In order to invoke the Python specifications, run the following:

```
$ poetry run python python/main.py
```

This repo also comes with a SAWScript equivalent of `main.py`, which can be
run with:

```
$ $SAW_EXE saw/main.saw
```
