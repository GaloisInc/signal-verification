import os
import os.path

from saw import llvm_verify
from saw.llvm import Contract, field, global_var, null, struct, void
from saw.llvm_types import alias, i8, i32, i64, ptr

from buffer_helpers import *
from load import *
from saw_helpers import *


hmac_context_ty   = alias("struct.hmac_context")
signal_context_ty = alias("struct.signal_context")

message_version = 3

dummy_signal_crypto_provider = struct( global_var("dummy_random_func")
                                     , global_var("dummy_hmac_sha256_init_func")
                                     , global_var("dummy_hmac_sha256_update_func")
                                     , global_var("dummy_hmac_sha256_final_func")
                                     , global_var("dummy_hmac_sha256_cleanup_func")
                                     , global_var("dummy_sha512_digest_init_func")
                                     , global_var("dummy_sha512_digest_update_func")
                                     , global_var("dummy_sha512_digest_final_func")
                                     , global_var("dummy_sha512_digest_cleanup_func")
                                     , global_var("dummy_encrypt_func")
                                     , global_var("dummy_decrypt_func")
                                     , null()
                                     )

class SignalHmacSha256InitSpec(Contract):
    def specification(self) -> None:
        context      = self.alloc(signal_context_ty)
        hmac_context = self.alloc(ptr(hmac_context_ty))
        key          = self.alloc(i8)
        key_len      = self.fresh_var(i64, "key_len")
        self.points_to(field(context, "crypto_provider"), dummy_signal_crypto_provider)

        self.execute_func(context, hmac_context, key, key_len)

        res = self.fresh_var(i32, "res")
        self.returns(res)

class SignalHmacSha256UpdateSpec(Contract):
    def specification(self) -> None:
        context      = self.alloc(signal_context_ty)
        hmac_context = self.alloc(ptr(hmac_context_ty))
        data         = self.alloc(i8)
        data_len     = self.fresh_var(i64, "data_len")
        self.points_to(field(context, "crypto_provider"), dummy_signal_crypto_provider)

        self.execute_func(context, hmac_context, data, data_len)

        res = self.fresh_var(i32, "res")
        self.returns(res)

class SignalHmacSha256FinalSpec(Contract):
    output_length: int

    def __init__(self, output_length: int):
        super().__init__()
        self.output_length = output_length

    def specification(self) -> None:
        context      = self.alloc(signal_context_ty)
        hmac_context = self.alloc(ptr(hmac_context_ty))
        output       = self.alloc(ptr(buffer_type(self.output_length)))
        self.points_to(field(context, "crypto_provider"), dummy_signal_crypto_provider)

        self.execute_func(context, hmac_context, output)

        res = self.fresh_var(i32, "res")
        self.returns(res)

class SignalHmacSha256CleanupSpec(Contract):
    def specification(self) -> None:
        context      = self.alloc(signal_context_ty)
        hmac_context = self.alloc(ptr(hmac_context_ty))
        self.points_to(field(context, "crypto_provider"), dummy_signal_crypto_provider)

        self.execute_func(context, hmac_context)

        self.returns(void)

signal_hmac_sha256_init_ov    = llvm_verify(mod, "signal_hmac_sha256_init",    SignalHmacSha256InitSpec())
signal_hmac_sha256_update_ov  = llvm_verify(mod, "signal_hmac_sha256_update",  SignalHmacSha256UpdateSpec())
signal_hmac_sha256_final_ov   = llvm_verify(mod, "signal_hmac_sha256_final",   SignalHmacSha256FinalSpec(31))
signal_hmac_sha256_cleanup_ov = llvm_verify(mod, "signal_hmac_sha256_cleanup", SignalHmacSha256CleanupSpec())
