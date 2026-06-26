*This project has been created as part of the 42 curriculum by amillan-*

# CODEXION

---

## Description

Codexion is a project with a program that a program that manages threads representing coders who must perform different actions based on established conditions.
This project's objetive is understanding how thread processes work and develop over time given instructions. 

---

## Instructions

In order to compile and use this program, yu can use the makefile options:

- make run: compiles the program
- make clean: cleans .o files
- make fclean: cleans .o and executable file

example:
```shell
    /codexion 250 50000 200 200 400 5 100 fifo
```

---

## Blocking Cases Handled

This implementation systematically mitigates classic concurrency pitfalls by designing an explicit, deterministic model for distributed resource allocation:

*   **Deadlock Prevention & Coffman Conditions:** To break the *Circular Wait* condition (one of the four Coffman conditions), a strict global locking hierarchy was implemented via `lock_dongles_ordered`. Regardless of a coder's position, the program mathematically evaluates and locks the dongle with the lowest memory address/ID first. This prevents two threads from holding one resource while eternally waiting for each other's neighboring dongle.
*   **Atomic Resource Acquisition:** Partial resource hoarding is prevented by making the acquisition process completely atomic inside `try_acquire_both`. A coder will only change the dongle's state to `is_taken` if **both** required dongles are simultaneously available, free of cooldowns, and the coder holds the highest priority in their respective queues. If any condition fails, all locks are instantly released.
*   **Starvation Prevention:** Threads that have completed their required number of compilations are systematically routed into a passive sleep loop (`usleep`). This prevents finished threads from flooding the Min-Heap priority queues with stale or obsolete requests, ensuring active coders always get a fair and timely turn to access the table resources.
*   **Cooldown Management:** Resource reuse is throttled by adding a strict `available_at` timestamp check during acquisition. When a coder releases a dongle, the next available timestamp is mathematically offset by the `dongle_cooldown` parameter. Coders waiting in the priority queue will safely ignore the resource until the system clock confirms the cooldown window has closed.
*   **Accurate Burnout Detection:** A dedicated and decoupled supervisor thread (`monitor_routine`) continuously polls the global simulation state with high-frequency micro-sleeps (`usleep(1000)`). It ensures that if any coder exceeds their maximum `time_to_burnout` threshold without compiling, the event is intercepted and logged within a strict sub-10ms tolerance window.
*   **Log Serialization:** To strictly prevent corrupted, interleaved, or mangled output across multiple concurrent threads, all console printing is wrapped inside a dedicated mutex barrier (`log_mutex`). This guarantees that each state transition is written atomically as a single, clean line.

---

## Thread Synchronization Mechanisms

The simulation coordinates access to shared resources using standard POSIX Threads primitives, adhering to a zero-global-variable design:

*   **`pthread_mutex_t` (Mutual Exclusion):** 
    *   **Resource Protection:** Every individual dongle structure contains its own mutex to isolate reads and writes to its availability state (`is_taken`), current owner, and its priority Min-Heap.
    *   **State & Logging Isolation:** A global `state_mutex` protects variables shared between the coders and the monitor (such as `simulation_running`, `compile_count`, and `last_compile_start`). A separate `log_mutex` handles console access.
*   **`pthread_cond_t` (Condition Variables):** Used to eliminate inefficient CPU polling. When a coder finds that a required dongle is busy or cooling down, they suspend their execution context using `pthread_cond_wait`. When a dongle is finally released, `pthread_cond_broadcast` wakes up all suspended threads competing for that specific resource to re-evaluate their priority in the Min-Heap.

### Race Condition Mitigation (Thread-Safe Communication Example)

A critical data race occurs when the Monitor reads a coder's timestamps while the coder thread is actively writing to them. To achieve a perfectly thread-safe architecture, every cross-thread interaction is bound by strict mutex synchronization blocks:

```c
/* Coder Thread: Safely recording the start of a compilation */
pthread_mutex_lock(&coder->env->state_mutex);
coder->last_compile_start = get_time_ms();
coder->compile_count++;
pthread_mutex_unlock(&coder->env->state_mutex);
```

```c
/* Monitor Thread: Safely reading the timestamp to evaluate burnout */
pthread_mutex_lock(&env->state_mutex);
long long last_compile = env->coders[i].last_compile_start;
pthread_mutex_unlock(&env->state_mutex);

if (now - last_compile > env->config.time_burnout) {
    // Handle burnout event immediately...
}
```

By enforcing that both the reading operation (Monitor) and the writing operation (Coder) must acquire the exact same `state_mutex` handle, Helgrind and DRD data-race detectors are completely satisfied, and memory consistency is guaranteed across all execution context switches.

---

## Resources

I used in this project google and AI to understand how to do a main. There is someone that helped me to organize ideas and start the project.
