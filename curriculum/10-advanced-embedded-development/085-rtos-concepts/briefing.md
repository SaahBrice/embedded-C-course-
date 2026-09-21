# Choose When to Use an RTOS

## Your task

Define the interface in `task.c` so this rule holds: The architecture battle gates scheduler startup on ready memory and drivers, checks queue burst capacity and execution-plus-blocking deadlines, then decides whether separate RTOS tasks justify their complexity. The caller will use the return value to distinguish success from failure, so handle invalid inputs deliberately instead of producing a plausible-looking result.

Edit `task.c` (keep the public declarations in `task.h` unchanged) in the attempt directory printed by `./learn status`. Do not edit `task.h`, anything below `curriculum/`, or the trusted test drivers. Do not add `main`; the visible driver supplies `main` while `./learn run` compiles your `task.c` and prints each call and return value. Then run `./learn test`; the sublevel is complete when every required check reports `PASS`.

## Why firmware engineers care

This sublevel turns **task, queue, mutex, priority inversion** into behavior a caller can verify. In firmware, a defect in `startup_services_ready`, `queue_absorbs_burst`, `periodic_load_fits`, `rtos_partition_justified` can corrupt state or hide a hardware failure even when one ordinary example appears correct.

The supplied `task.c` contains a TODO but no definition for `startup_services_ready`, `queue_absorbs_burst`, `periodic_load_fits`, `rtos_partition_justified`. Add the missing code there; keep the declarations and trusted drivers unchanged.

## Read the function signature

```c
bool startup_services_ready(bool memory_ready, bool drivers_ready, bool scheduler_ready);
bool queue_absorbs_burst(size_t producer_burst, size_t consumer_progress, size_t queue_capacity);
bool periodic_load_fits(uint32_t execution_us, uint32_t blocking_us, uint32_t period_us);
bool rtos_partition_justified(unsigned independent_jobs, bool shared_blocking_io, bool cooperative_deadlines_met);
```

Do not change these declarations.

- `memory_ready` from `bool memory_ready`: a true/false input flag.
- `drivers_ready` from `bool drivers_ready`: a true/false input flag.
- `scheduler_ready` from `bool scheduler_ready`: a true/false input flag.
- `startup_services_ready` return type `bool`: returns `true` on success and `false` when the operation is rejected.
- `producer_burst` from `size_t producer_burst`: an input value; its meaningful range is demonstrated below.
- `consumer_progress` from `size_t consumer_progress`: an input value; its meaningful range is demonstrated below.
- `queue_capacity` from `size_t queue_capacity`: an input value; its meaningful range is demonstrated below.
- `queue_absorbs_burst` return type `bool`: returns `true` on success and `false` when the operation is rejected.
- `execution_us` from `uint32_t execution_us`: an input value; its meaningful range is demonstrated below.
- `blocking_us` from `uint32_t blocking_us`: an input value; its meaningful range is demonstrated below.
- `period_us` from `uint32_t period_us`: an input value; its meaningful range is demonstrated below.
- `periodic_load_fits` return type `bool`: returns `true` on success and `false` when the operation is rejected.
- `independent_jobs` from `unsigned independent_jobs`: an input value; its meaningful range is demonstrated below.
- `shared_blocking_io` from `bool shared_blocking_io`: a true/false input flag.
- `cooperative_deadlines_met` from `bool cooperative_deadlines_met`: a true/false input flag.
- `rtos_partition_justified` return type `bool`: returns `true` on success and `false` when the operation is rejected.

## Concrete examples

The following are executable examples of the required behavior. Read each assertion as ‘this call must make the condition true’:

```c
assert(startup_services_ready(true,true,true));assert(!startup_services_ready(true,false,true));assert(queue_absorbs_burst(8U,3U,5U));assert(!queue_absorbs_burst(9U,3U,5U));assert(periodic_load_fits(200U,100U,1000U));assert(!periodic_load_fits(900U,200U,1000U));assert(rtos_partition_justified(3U,true,true));assert(rtos_partition_justified(2U,false,false));assert(!rtos_partition_justified(1U,true,false));assert(!rtos_partition_justified(3U,false,true));
```

## Expected failure behavior

Return `false` for the rejected cases shown above and leave caller-owned output unchanged. Return `true` only after the whole operation is safe and complete.
