LIBSIGNAL_BUILD_DIR=libsignal-protocol-c/build

all: $(LIBSIGNAL_BUILD_DIR)/src/libsignal-protocol-c.a.bc

$(LIBSIGNAL_BUILD_DIR)/src/libsignal-protocol-c.a:
	mkdir -p $(LIBSIGNAL_BUILD_DIR)
	(cd $(LIBSIGNAL_BUILD_DIR) && \
	LLVM_COMPILER=clang cmake -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=wllvm .. && \
	LLVM_COMPILER=clang make)

$(LIBSIGNAL_BUILD_DIR)/src/libsignal-protocol-c.a.bc: $(LIBSIGNAL_BUILD_DIR)/src/libsignal-protocol-c.a
	(cd $(LIBSIGNAL_BUILD_DIR) && \
	extract-bc -b src/libsignal-protocol-c.a)

.PHONY: clean
clean:
	rm -rf $(LIBSIGNAL_BUILD_DIR)
