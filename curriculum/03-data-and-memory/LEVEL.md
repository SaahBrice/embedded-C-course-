# Level 3: Data and Memory

## Main objective

Work safely with arrays, strings, pointers, object lifetime, structured data, byte layouts, and bounded storage.

## What you should know before starting

Complete Level 2; this level builds directly on its C contracts and debugging habits.

## Why these concepts belong together

These sublevels form one progression rather than unrelated topics: each adds a new tool or boundary needed by the final program. You will write and run code at every step, then combine the ideas in **Release: Binary Packet Parser**.

## What you will build and learn

- Use arrays, strings, pointers, and caller-owned output without crossing object bounds
- Reason about lifetime, tagged data, alignment, byte order, and fixed storage
- Release a binary packet parser that validates before committing output

## Ordered sublevels

1. **Work Safely with Arrays** (`arrays`) — Implement `sample_minmax`: The first live element seeds both extrema, and every later index is proven smaller than `count`.
2. **Handle C Strings Explicitly** (`strings`) — Implement `buffer_append`: `buffer_append` first proves that the destination is terminated within capacity and commits only when suffix plus terminator fits.
3. **Read Pointer Relationships** (`pointers`) — Implement `checked_sum`: A pointer and element count share one provenance-safe contract: null is accepted only for zero elements, impossible byte extents are rejected, and iteration never compares unrelated pointers.
4. **Return Results Through Pointers** (`pointer-parameters`) — Implement `decode_u16_le`: The input bytes are read-only, the caller owns the output object, and no byte is read until length is sufficient.
5. **Prevent Lifetime Defects** (`memory-lifetime`) — Implement `snapshot_i16`: The function copies a live value into caller-owned storage instead of returning or retaining a pointer to temporary storage.
6. **Model a Sensor Packet** (`structs-unions-enums`) — Implement `packet_value`: The enum is the union tag: code reads only the member selected by a recognized tag and rejects every unknown value.
7. **Decode Portable Byte Layouts** (`alignment-endianness`) — Implement `decode_u32_be`: Four protocol bytes are decoded in big-endian order without assuming host alignment or byte order.
8. **Set an Allocation Policy** (`dynamic-memory-policy`) — Implement `fixed_pool_acquire`: A boot-allocated fixed pool returns the first free slot and reports exhaustion without dynamic allocation.
9. **Release: Binary Packet Parser** (`packet-parser-release`) — FINAL BATTLE — Implement `packet_header_valid`, `packet_decode_value`, `packet_parse`: The parser release validates the whole frame header, decodes little-endian payload bytes without alignment assumptions, and commits a typed packet only after both stages succeed.

## Topic practice coverage

Each core topic is reinforced through at least five different coding sublevels. The lists are curated by the skill used in the code; they are not automatic neighboring windows or repeated runs of one answer.

- **bounded arrays and storage** is practised in: Work Safely with Arrays, Handle C Strings Explicitly, Read Pointer Relationships, Return Results Through Pointers, Set an Allocation Policy, Release: Binary Packet Parser
- **pointer lifetime and ownership** is practised in: Read Pointer Relationships, Return Results Through Pointers, Prevent Lifetime Defects, Model a Sensor Packet, Set an Allocation Policy, Release: Binary Packet Parser
- **typed and byte-level representation** is practised in: Work Safely with Arrays, Return Results Through Pointers, Model a Sensor Packet, Decode Portable Byte Layouts, Release: Binary Packet Parser

## Final battle

**Release: Binary Packet Parser** is the last required sublevel. It integrates **Read Pointer Relationships**, **Model a Sensor Packet**, **Decode Portable Byte Layouts**. Passing it after all earlier sublevels clears this level and unlocks the next. It remains replayable after completion.
