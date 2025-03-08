#ifndef _HAL_TYPES_H_
#define _HAL_TYPES_H_

#include <stdint.h>

typedef unsigned char bool_t;
typedef unsigned char u4_t;
typedef unsigned char u5_t;
typedef unsigned char u8_t;
typedef unsigned short u12_t;
typedef unsigned short u13_t;
typedef unsigned int u32_t;
typedef unsigned int timestamp_t; // WARNING: Must be an unsigned type to properly handle wrapping (u32 wraps in around 1h11m when expressed in us)

#endif /* _HAL_TYPES_H_ */
