# Full solution: Implement a Ring Buffer

This worked implementation demonstrates head, tail, full empty policy. Compare its observable behavior and boundaries with yours; different code is valid when it preserves the same contract.

```c
/* Mission: Implement a Ring Buffer */
#include "task.h"

#include <errno.h>
#include <limits.h>
#include <stdlib.h>
#include <string.h>

bool byte_ring_push(struct byte_ring *ring, uint8_t value) { if (ring == NULL || ring->count == BYTE_RING_CAPACITY) return false; ring->data[ring->head] = value; ring->head = (ring->head + 1U) % BYTE_RING_CAPACITY; ++ring->count; return true; }
bool byte_ring_pop(struct byte_ring *ring, uint8_t *out_value) { if (ring == NULL || out_value == NULL || ring->count == 0U) return false; *out_value = ring->data[ring->tail]; ring->tail = (ring->tail + 1U) % BYTE_RING_CAPACITY; --ring->count; return true; }
```
