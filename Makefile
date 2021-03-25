LIBSIGNAL_DIR=libsignal-protocol-c
LIBSIGNAL_BUILD_DIR=$(LIBSIGNAL_DIR)/build

all: libsignal saw-haskell saw-python-poetry

libsignal: c/libsignal-everything.bc

$(LIBSIGNAL_BUILD_DIR)/src/libsignal-protocol-c.a:
	mkdir -p $(LIBSIGNAL_BUILD_DIR)
	(cd $(LIBSIGNAL_BUILD_DIR) && \
	LLVM_COMPILER=clang cmake -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=wllvm .. && \
	LLVM_COMPILER=clang make)

$(LIBSIGNAL_BUILD_DIR)/src/libsignal-protocol-c.a.bc: $(LIBSIGNAL_BUILD_DIR)/src/libsignal-protocol-c.a
	(cd $(LIBSIGNAL_BUILD_DIR) && \
	extract-bc -b src/libsignal-protocol-c.a)

c/libsignal-everything.bc: $(LIBSIGNAL_BUILD_DIR)/src/libsignal-protocol-c.a.bc c/dummy_signal_crypto_provider.bc
	llvm-link $^ -o $@

c/dummy_signal_crypto_provider.bc: c/dummy_signal_crypto_provider.c
	clang -g -c -emit-llvm $< -o $@ -I$(LIBSIGNAL_DIR)/src

.PHONY: saw-haskell
saw-haskell:
	(cd saw-script && ./build.sh)

.PHONY: saw-python-poetry
saw-python-poetry:
	poetry install

.PHONY: saw-python-virtualenv
saw-python-virtualenv:
	./build-virtenv.sh

.PHONY: clean
clean:
	rm -rf $(LIBSIGNAL_BUILD_DIR)
