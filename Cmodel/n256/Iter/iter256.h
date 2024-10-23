#ifndef __ITER256_H
#define __ITER256_H

#include <stdint.h>

extern void iter_preprocess_256(int32_t *a, int32_t *a_pre);

extern void iter_postprocess_256(int32_t *c_pre, int32_t *c_post);

extern void iter_concat_256(int32_t *c_post, int32_t *c);

extern void elementwise_product(int32_t *c, uint32_t n, const int32_t *a, const int32_t *b);

#endif /* __ITER256_H */