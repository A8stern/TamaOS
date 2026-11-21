# TamaOS architecture

Status: initial architecture for discussion. Hardware-dependent details are provisional until the delivered modules are inspected.

Shared decision principles and the language-start checkpoint are defined in [architecture-principles.md](architecture-principles.md). Each implementation language must supply its own architect skill; the common coordinator does not replace language expertise.

## 1. Architectural drivers

The first version optimizes for:

- a reliable boot-to-main-screen path;
- safe bring-up of each physical component in isolation;
- deterministic virtual-pet behavior that can be tested on a computer;
- a small binary and understandable control flow;
- incremental delivery on one ESP32-S3 board.

It does not initially optimize for runtime-loaded games, multiple boards, networking, battery operation, or a general-purpose operating system.

## 2. Recommended starting point

Start with a bare-metal `no_std` firmware using `esp-hal`, a single cooperative event loop, `embedded-graphics`, and an ST7789-compatible `mipidsi` driver. This is a provisional recommendation, not a locked decision.

Reconsider ESP-IDF only if a near-term requirement needs facilities that materially outweigh its added build and runtime complexity—for example Wi-Fi/Bluetooth integration, an RTOS-based third-party component, or a supported system service unavailable in the bare-metal stack.

Record the final choice as the first ADR after a minimal toolchain spike builds and flashes successfully.

## 3. Runtime model

Use one explicit loop for the first milestone:

```text
read monotonic time
  -> sample inputs and emit semantic events
  -> advance pet/game state with elapsed time
  -> update navigation and UI state
  -> render only invalidated regions or the current frame
  -> execute queued audio commands
  -> persist at defined checkpoints
```

Interrupts should do the minimum necessary and hand data to the main loop. Avoid shared mutable application state inside interrupt handlers.

The initial event vocabulary should be semantic (`RotateLeft`, `RotateRight`, `Confirm`, `Back`, `Tick`) rather than tied to GPIO edges. Debouncing and quadrature decoding belong in input adapters.

## 4. Module boundaries

```text
apps/firmware
  |- board       ESP32-S3 clocks, pins, SPI, timers, boot
  |- drivers     ST7789, controls, buzzer, flash adapter
  |- services    input, clock, renderer, audio, persistence ports
  |- ui          navigation, screens, view state
  `- domain      pet model, rules, commands, save schema
```

When host tests become useful, extract portable crates rather than simulating the entire board:

```text
crates/tama-domain   pure state transitions and time-based rules
crates/tama-ui       navigation/view state independent of the display bus
apps/firmware        board integration and embedded entry point
```

Do not create this workspace split until the first portable logic exists.

## 5. State and persistence

The pet model should be a serializable state plus pure transitions. Time-based behavior receives elapsed time explicitly; it must not read hardware clocks directly.

Persistence should use a versioned save envelope with:

- schema version;
- payload;
- integrity check;
- a write strategy resilient to power loss.

The exact flash/NVS implementation remains open until the platform choice is confirmed. Saving on every frame is forbidden; use meaningful checkpoints and bounded periodic saves.

## 6. Rendering and assets

Keep scene/view state separate from display I/O. Begin with primitive graphics and a small compiled-in asset set. Establish memory budgets before adding large sprites or frame buffers.

Use partial redraws only after a simple full-screen or region-based implementation is measured. PSRAM availability must be detected and verified rather than assumed solely from the board listing.

## 7. Audio

Represent sound as commands such as frequency, duration, and silence. A hardware adapter maps them to PWM. Keep melody sequencing out of the interrupt path and avoid software busy-wait tone generation.

The ULN2003 and buzzer wiring remains unverified until module markings and continuity checks are available.

## 8. Verification strategy

Use three levels:

1. Host tests: domain rules, navigation, save migration, and input decoding with recorded sequences.
2. Build checks: formatting, linting where supported, firmware compilation, size report, and documentation checks.
3. Hardware checks: one repeatable bring-up checklist per peripheral, with observed results recorded in the related issue or PR.

“Builds” and “works on hardware” are separate statuses.

## 9. Delivery slices

1. Toolchain spike: build, flash, log, and identify the exact board memory configuration.
2. Display slice: solid colors, orientation, color order, and basic text.
3. Input slice: encoder and buttons produce semantic events with debouncing.
4. Audio slice: safe PWM tone through the verified buzzer circuit.
5. Shell slice: boot screen, menu, navigation, and diagnostics page.
6. Pet slice: deterministic needs, actions, time progression, and save/restore.
7. Mini-game slice: one compiled-in game using the same input/rendering boundaries.

Each slice should leave a runnable firmware state and a documented hardware result.

## 10. Open decisions

- `esp-hal` bare metal versus ESP-IDF.
- Exact ESP32-S3 board revision, USB port roles, flash mode, and PSRAM mode.
- Safe GPIO assignment after module inspection.
- Display pin labels, backlight power path, offsets, color order, and orientation.
- Number and meaning of standalone buttons.
- Persistence backend and save frequency.
- Frame-rate and RAM/flash budgets.
- Whether networking is in scope at all.

Do not close these decisions by guessing.
