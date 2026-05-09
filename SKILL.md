---
name: oura-full-reader
description: Bluetooth and heart-rate reader agent skill for Oura rings and standard BLE Heart Rate Service devices. Use when an agent needs to scan Bluetooth devices, inspect GATT services/characteristics, read/write/subscribe to BLE characteristics, read standard BLE heart-rate measurements, or use Oura's custom latest heart-rate feature protocol from the bundled oura-full-read package.
---

# Oura Full Reader

## Overview

Use this skill to operate the bundled `oura-full-read` Python package as a Bluetooth and heart-rate reader. It supports generic BLE inspection plus two heart-rate paths:

- Standard BLE Heart Rate Service: service `0000180d-0000-1000-8000-00805f9b34fb`, measurement characteristic `00002a37-0000-1000-8000-00805f9b34fb`.
- Oura custom latest-values protocol: Oura service `98ed0001-a541-11e4-b6a0-0002a5d5c51b`, write characteristic `98ed0002-a541-11e4-b6a0-0002a5d5c51b`, read/notify characteristic `98ed0003-a541-11e4-b6a0-0002a5d5c51b`.

The Oura app code uses the standard Heart Rate Service UUID for third-party HR monitors. Oura ring heart-rate values are read through the custom feature protocol, not through standard BLE HR.

## Quick Start

Prefer the bundled wrapper:

```bash
python scripts/oura_full_read.py --help
python scripts/oura_full_read.py scan --timeout 10
python scripts/oura_full_read.py services AA:BB:CC:DD:EE:FF
python scripts/oura_full_read.py hr-standard AA:BB:CC:DD:EE:FF --seconds 30
python scripts/oura_full_read.py hr-oura AA:BB:CC:DD:EE:FF --source daytime-hr
python scripts/oura_full_read.py read-all AA:BB:CC:DD:EE:FF --standard-seconds 20
```

The wrapper runs the bundled source from `assets/oura-full-read/src` without requiring an editable install. Hardware operations require `bleak`, an available Bluetooth adapter, OS Bluetooth permissions, and a device that is connectable from the host.

## Workflow

1. Start with `scan` to identify Oura devices and standard HR monitors.
2. Run `services <address>` before assuming a characteristic exists.
3. For standard HR monitors, use `hr-standard` and expect notifications from `0x2A37`.
4. For Oura rings, use `hr-oura --source daytime-hr`, then try `exercise-hr` or `spo2` if the ring supports those feature latest-values.
5. Use `read-all` when the user wants a broad Bluetooth and heart-rate inventory in one command.
6. Use generic `read`, `write`, and `notify` only when the user provides a characteristic UUID or when a previous `services` run shows the target characteristic.

## Bundled Resources

- `scripts/oura_full_read.py`: wrapper around the bundled CLI.
- `assets/oura-full-read`: complete Python package source, tests, and package metadata.
- `references/protocol.md`: concise UUID and operation reference for the heart-rate and Bluetooth paths.

## Safety And Limits

- Do not claim Oura exposes standard BLE HR. Use `hr-oura` for Oura heart-rate latest values.
- Do not claim live hardware success unless a command was actually run against hardware and returned data.
- Oura feature reads may require bonding, encryption, and a ring state that accepts the request. This skill does not bypass authentication or account-backed authorization.
- Raw BLE writes can change device state. Use generic `write` only when the payload and characteristic are intentional.
