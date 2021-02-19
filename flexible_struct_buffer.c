#include <stdlib.h>
#include <stdint.h>

typedef struct buffer {
    size_t len;
    uint8_t data[];
} buffer;

size_t get_length(buffer *buffer){
    return buffer->len;
}