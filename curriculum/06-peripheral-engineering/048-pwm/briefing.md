# Control Output with PWM

## Your task

Define the interface in `task.c` so this rule holds: Widening prevents multiplication overflow, 0 and 100 percent map to the endpoints, and invalid percentages are rejected. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **frequency, duty cycle, timer period** into behavior a caller can verify. In firmware, a defect in `pwm_compare` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `pwm_compare`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool pwm_compare(uint32_t period_ticks, uint8_t duty_percent, uint32_t *out_compare);
```

Do not change these declarations.

- `period_ticks` from `uint32_t period_ticks`: an input value; its meaningful range is demonstrated below.
- `duty_percent` from `uint8_t duty_percent`: an input value; its meaningful range is demonstrated below.
- `out_compare` from `uint32_t *out_compare`: caller-owned destination written only when the operation succeeds.
- `pwm_compare` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
uint32_t compare=0U; assert(pwm_compare(1000U,0U,&compare)&&compare==0U); assert(pwm_compare(1000U,25U,&compare)&&compare==250U); assert(pwm_compare(UINT32_MAX,100U,&compare)&&compare==UINT32_MAX); assert(!pwm_compare(10U,101U,&compare));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
