import os
import os.path

from saw import llvm_verify
from saw.llvm import Contract, elem, field, global_var, null, struct, void
from saw.llvm_types import alias, i8, i32, i64, ptr

from buffer_helpers import *
from curve import *
from load import *
from saw_helpers import *


signal_context_ty = alias("struct.signal_context")

message_version = 3

SIGNAL_MESSAGE_MAC_LENGTH = 8

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
        hmac_context = self.alloc(ptr(i8))
        key          = self.alloc(i8)
        key_len      = self.fresh_var(i64, "key_len")
        self.points_to(field(context, "crypto_provider"), dummy_signal_crypto_provider)

        self.execute_func(context, hmac_context, key, key_len)

        dummy_hmac_context = self.alloc(i8, points_to = int_to_8_cryptol(42))
        self.points_to(hmac_context, dummy_hmac_context)
        self.returns(int_to_32_cryptol(0))

class SignalHmacSha256UpdateSpec(Contract):
    def specification(self) -> None:
        context      = self.alloc(signal_context_ty)
        hmac_context = self.alloc(i8)
        data         = self.alloc(i8)
        data_len     = self.fresh_var(i64, "data_len")
        self.points_to(field(context, "crypto_provider"), dummy_signal_crypto_provider)

        self.execute_func(context, hmac_context, data, data_len)

        self.returns(int_to_32_cryptol(0))

class SignalHmacSha256FinalSpec(Contract):
    def specification(self) -> None:
        context      = self.alloc(signal_context_ty)
        hmac_context = self.alloc(i8)
        output       = self.alloc(ptr(buffer_type(SIGNAL_MESSAGE_MAC_LENGTH)))
        self.points_to(field(context, "crypto_provider"), dummy_signal_crypto_provider)

        self.execute_func(context, hmac_context, output)

        output_buffer = alloc_buffer_aligned(self, SIGNAL_MESSAGE_MAC_LENGTH)
        self.points_to(elem(output_buffer, 0), int_to_64_cryptol(SIGNAL_MESSAGE_MAC_LENGTH), check_target_type = i64)
        self.points_to(output, output_buffer)
        self.returns(int_to_32_cryptol(0))

class SignalHmacSha256CleanupSpec(Contract):
    def specification(self) -> None:
        context      = self.alloc(signal_context_ty)
        hmac_context = self.alloc(i8)
        self.points_to(field(context, "crypto_provider"), dummy_signal_crypto_provider)

        self.execute_func(context, hmac_context)

        self.returns(void)

class SignalMessageGetMacSpec(Contract):
    def specification(self) -> None:
        ec_public_key = alias("struct.ec_public_key")
        buffer_                       = self.alloc(ptr(buffer_type(SIGNAL_MESSAGE_MAC_LENGTH)))
        (_, _, sender_identity_key)   = alloc_ec_public_key(self)
        (_, _, receiver_identity_key) = alloc_ec_public_key(self)
        mac_key                       = self.alloc(i8)
        mac_key_len                   = self.fresh_var(i64, "mac_key_len")
        serialized                    = self.alloc(i8)
        serialized_len                = self.fresh_var(i64, "serialized_len")
        global_context                = self.alloc(signal_context_ty)
        self.points_to(field(global_context, "crypto_provider"), dummy_signal_crypto_provider)

        self.execute_func(buffer_,
                          int_to_8_cryptol(message_version),
                          sender_identity_key,
                          receiver_identity_key,
                          mac_key, mac_key_len,
                          serialized, serialized_len,
                          global_context)

        buffer_buf = alloc_buffer_aligned(self, SIGNAL_MESSAGE_MAC_LENGTH)
        self.points_to(elem(buffer_buf, 0), int_to_64_cryptol(SIGNAL_MESSAGE_MAC_LENGTH), check_target_type = i64)
        self.points_to(buffer_, buffer_buf)
        self.returns(int_to_32_cryptol(0))

signal_hmac_sha256_init_ov    = llvm_verify(mod, "signal_hmac_sha256_init",    SignalHmacSha256InitSpec())
signal_hmac_sha256_update_ov  = llvm_verify(mod, "signal_hmac_sha256_update",  SignalHmacSha256UpdateSpec())
signal_hmac_sha256_final_ov   = llvm_verify(mod, "signal_hmac_sha256_final",   SignalHmacSha256FinalSpec())
signal_hmac_sha256_cleanup_ov = llvm_verify(mod, "signal_hmac_sha256_cleanup", SignalHmacSha256CleanupSpec())
signal_message_get_mac_ov     = llvm_verify(mod, "signal_message_get_mac",     SignalMessageGetMacSpec())
