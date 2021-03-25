#include <stdint.h>

#include "signal_protocol_internal.h"

// Type signatures taken from
// https://github.com/signalapp/libsignal-protocol-c/blob/3a83a4f4ed2302ff6e68ab569c88793b50c22d28/src/signal_protocol.h#L276
int dummy_random_func(uint8_t *data, size_t len, void *user_data) {
    return 0;
}

int dummy_hmac_sha256_init_func(void **hmac_context, const uint8_t *key, size_t key_len, void *user_data) {
    return 0;
}

int dummy_hmac_sha256_update_func(void *hmac_context, const uint8_t *data, size_t data_len, void *user_data) {
    return 0;
}

int dummy_hmac_sha256_final_func(void *hmac_context, signal_buffer **output, void *user_data) {
    return 0;
}

void dummy_hmac_sha256_cleanup_func(void *hmac_context, void *user_data) {}

int dummy_sha512_digest_init_func(void **digest_context, void *user_data) {
    return 0;
}

int dummy_sha512_digest_update_func(void *digest_context, const uint8_t *data, size_t data_len, void *user_data) {
    return 0;
}

int dummy_sha512_digest_final_func(void *digest_context, signal_buffer **output, void *user_data) {
    return 0;
}

void dummy_sha512_digest_cleanup_func(void *digest_context, void *user_data) {}

int dummy_encrypt_func(signal_buffer **output,
        int cipher,
        const uint8_t *key, size_t key_len,
        const uint8_t *iv, size_t iv_len,
        const uint8_t *plaintext, size_t plaintext_len,
        void *user_data) {
    return 0;
}

int dummy_decrypt_func(signal_buffer **output,
        int cipher,
        const uint8_t *key, size_t key_len,
        const uint8_t *iv, size_t iv_len,
        const uint8_t *ciphertext, size_t ciphertext_len,
        void *user_data) {
    return 0;
}
