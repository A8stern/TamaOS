# Hardware bring-up procedure

Use this procedure for an actual wiring, measurement, first-power, or hardware-diagnosis task. Adapt the detail to the risk, but do not skip an unresolved safety boundary.

## 1. Identify the exact hardware

- Ask for or inspect clear photos of both sides, connector labels, jumpers, chip markings, and board revision.
- Match primary documentation to those markings. State any mismatch between the listing, reference board, and received item.
- Record orientation using visible labels or landmarks; do not rely only on left/right positions in a photo.

## 2. Build the electrical contract

For every connection, determine:

- source and destination pin labels;
- power rail or signal direction;
- allowed voltage and logic level;
- expected idle state and pull-up/pull-down behavior where relevant;
- load current path and whether a driver or protection element is required;
- evidence source and remaining uncertainty.

Do not assign a GPIO until its boot, flash/PSRAM, USB, and peripheral constraints are checked for the exact board configuration.

## 3. Pre-power inspection

With all power disconnected:

1. Confirm breadboard rail segmentation and intended rail bridges.
2. Confirm that 3.3 V and 5 V rails are not shorted together.
3. Confirm the common-ground path.
4. Check for shorts from each powered rail to ground and inspect connector orientation.
5. Verify switch contact pairs, unknown connector continuity, and driver-board jumpers when relevant.
6. Reconcile the physical assembly against the wiring table connection by connection.

Use resistance readings rather than an audible-continuity assumption when the available DT830B has no buzzer.

## 4. First power

- Begin with the controller and power distribution, without optional loads when practical.
- Measure rails relative to the verified ground before attaching signal wires or loads.
- Add only one peripheral or functional path at a time.
- Use the simplest diagnostic behavior for that peripheral; do not combine display, inputs, and sound in the first test.
- Disconnect power before every wiring change.

## 5. Evidence and failure handling

For each step record: configuration, expected observation, actual observation, measurement and meter range if used, and pass/fail.

On failure, return to the last known-good configuration. Check power, ground, orientation, continuity, and signal assignment before changing firmware or replacing parts. A failed test does not prove a component is defective.

Promote a planned connection to verified only after the exact assembly passes its stated physical check. Keep firmware build evidence and hardware behavior evidence separate.
