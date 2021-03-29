import os
import os.path

from saw import llvm_verify
from saw.llvm import Contract, field, global_var, null, struct
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

buffer_alloc_ov = llvm_verify(mod, "signal_hmac_sha256_init", SignalHmacSha256InitSpec())
