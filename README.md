# Oura Full Reader Agent Skill

`oura-full-reader` is an agent skill for Bluetooth inspection and heart-rate reading with Oura rings and standard BLE Heart Rate Service devices.

It bundles a Python package named `oura-full-read` and exposes it through a lightweight wrapper at `scripts/oura_full_read.py`. The wrapper lets an agent run the reader directly from this repository without installing the package in editable mode.

## Product Reference

This agent skill was built around the Oura smart ring product family, including Oura Ring 4 devices.

Product link:

- [Browse Oura Ring 4 on Amazon](https://amzn.to/4d9t82s)

Disclosure: As an Amazon Associate, I earn from qualifying purchases.

The Bluetooth reader is not limited to one exact size or finish. It is intended for Oura rings that expose the same custom BLE service and for normal BLE devices that expose the standard Heart Rate Service.

This repository does not use the Oura mobile app, Oura Cloud API, or account-backed app data. It works at the local Bluetooth layer, subject to the ring's pairing, bonding, encryption, firmware, and current device state.

## What It Does

This agent skill supports:

- Scanning nearby Bluetooth Low Energy devices.
- Filtering scans for Oura devices or standard heart-rate monitors.
- Listing GATT services and characteristics.
- Reading, writing, and subscribing to arbitrary BLE characteristics.
- Reading standard BLE Heart Rate Service notifications.
- Reading Oura latest heart-rate feature values through Oura's custom BLE service.
- Running a combined `read-all` workflow that inventories services and attempts both heart-rate paths.

## Important Heart-Rate Distinction

There are two heart-rate paths in this repo:

| Path | Device type | Command | Notes |
| --- | --- | --- | --- |
| Standard BLE Heart Rate Service | Normal BLE heart-rate straps, watches, sensors, and monitors | `hr-standard` | Uses standard service `0x180D` and measurement characteristic `0x2A37`. |
| Oura custom latest-values protocol | Oura rings | `hr-oura` | Uses Oura service `98ed0001-a541-11e4-b6a0-0002a5d5c51b`. |

The Oura ring heart-rate values are not read through the standard BLE Heart Rate Service path in this tool. Use `hr-oura` for Oura ring latest heart-rate values.

## Repository Layout

```text
.
├── SKILL.md
├── agents/
│   └── openai.yaml
├── scripts/
│   └── oura_full_read.py
├── references/
│   └── protocol.md
└── assets/
    └── oura-full-read/
        ├── pyproject.toml
        ├── README.md
        ├── docs/
        │   └── full-reader.md
        ├── src/
        │   └── oura_full_read/
        └── tests/
```

Key files:

- `SKILL.md`: agent-facing instructions and trigger metadata.
- `agents/openai.yaml`: display metadata for the agent skill.
- `scripts/oura_full_read.py`: wrapper around the bundled CLI.
- `references/protocol.md`: UUIDs, request formats, response formats, and Oura capability notes.
- `assets/oura-full-read`: bundled Python package with the actual Bluetooth and parser implementation.

## Requirements

Runtime requirements:

- Python 3.10 or newer.
- `bleak>=0.22`.
- A working Bluetooth Low Energy adapter.
- OS-level Bluetooth permissions for the terminal or agent process.
- A connectable target device.

Hardware operations are environment dependent. Discovery and connection behavior can vary by OS, adapter, pairing state, privacy address rotation, and whether another app is already connected to the device.

## Setup

Install the Python dependency in the environment where the agent will run commands:

```bash
python -m pip install "bleak>=0.22"
```

You can also install the bundled package directly if you want the `oura-full-read` console script:

```bash
cd assets/oura-full-read
python -m pip install -e .
```

Editable installation is optional. The preferred path for the agent skill is the repository wrapper:

```bash
python scripts/oura_full_read.py --help
```

## Quick Start

Scan nearby BLE devices:

```bash
python scripts/oura_full_read.py scan --timeout 10
```

Scan only devices that look like Oura devices:

```bash
python scripts/oura_full_read.py scan --oura-only
```

Scan only devices advertising the standard BLE Heart Rate Service:

```bash
python scripts/oura_full_read.py scan --heart-rate-only
```

List services and characteristics for a device:

```bash
python scripts/oura_full_read.py services AA:BB:CC:DD:EE:FF
```

Read a standard BLE heart-rate monitor:

```bash
python scripts/oura_full_read.py hr-standard AA:BB:CC:DD:EE:FF --seconds 30
```

Read Oura latest daytime heart-rate values:

```bash
python scripts/oura_full_read.py hr-oura AA:BB:CC:DD:EE:FF --source daytime-hr
```

Run a broad inventory and heart-rate attempt:

```bash
python scripts/oura_full_read.py read-all AA:BB:CC:DD:EE:FF --standard-seconds 20
```

## Command Reference

### `scan`

Scans nearby BLE devices and prints JSON rows.

```bash
python scripts/oura_full_read.py scan --timeout 10
python scripts/oura_full_read.py scan --oura-only
python scripts/oura_full_read.py scan --heart-rate-only
```

Options:

- `--timeout`: scan duration in seconds. Default: `10.0`.
- `--oura-only`: return only devices identified as Oura-like.
- `--heart-rate-only`: return only devices advertising standard BLE heart-rate support.

### `services`

Connects to a BLE device and lists GATT services and characteristics.

```bash
python scripts/oura_full_read.py services AA:BB:CC:DD:EE:FF
```

Options:

- `--timeout`: connection timeout in seconds. Default: `20.0`.

### `read`

Reads any characteristic by UUID.

```bash
python scripts/oura_full_read.py read AA:BB:CC:DD:EE:FF 00002a37-0000-1000-8000-00805f9b34fb
```

Arguments:

- `address`: BLE device address.
- `characteristic`: characteristic UUID.

### `write`

Writes a hex payload to any characteristic.

```bash
python scripts/oura_full_read.py write AA:BB:CC:DD:EE:FF 98ed0002-a541-11e4-b6a0-0002a5d5c51b 2f022402 --with-response
```

Arguments:

- `address`: BLE device address.
- `characteristic`: characteristic UUID.
- `hex`: payload bytes as hex.

Options:

- `--with-response`: request a write response.
- `--timeout`: connection timeout in seconds. Default: `20.0`.

Use raw writes carefully. A write can change device state if the payload and characteristic perform a control operation.

### `notify`

Subscribes to notifications from any characteristic.

```bash
python scripts/oura_full_read.py notify AA:BB:CC:DD:EE:FF 00002a37-0000-1000-8000-00805f9b34fb --seconds 30
```

Options:

- `--seconds`: subscription duration. Default: `30.0`.
- `--timeout`: connection timeout in seconds. Default: `20.0`.

### `hr-standard`

Subscribes to standard BLE Heart Rate Measurement notifications and parses them.

```bash
python scripts/oura_full_read.py hr-standard AA:BB:CC:DD:EE:FF --seconds 30
```

Uses:

- Service UUID: `0000180d-0000-1000-8000-00805f9b34fb`
- Measurement characteristic UUID: `00002a37-0000-1000-8000-00805f9b34fb`

Parsed output can include:

- `heart_rate_bpm`
- sensor contact support and detection state
- energy expended
- RR intervals in seconds
- raw notification hex

### `hr-oura`

Reads Oura latest heart-rate feature values through Oura's custom service.

```bash
python scripts/oura_full_read.py hr-oura AA:BB:CC:DD:EE:FF --source daytime-hr
python scripts/oura_full_read.py hr-oura AA:BB:CC:DD:EE:FF --source exercise-hr
python scripts/oura_full_read.py hr-oura AA:BB:CC:DD:EE:FF --source spo2
```

Options:

- `--source`: one of `daytime-hr`, `exercise-hr`, or `spo2`. Default: `daytime-hr`.
- `--timeout`: connection timeout in seconds. Default: `20.0`.
- `--response-timeout`: wait time for the Oura response after writing the request. Default: `5.0`.

Oura UUIDs:

- Service: `98ed0001-a541-11e4-b6a0-0002a5d5c51b`
- Write characteristic: `98ed0002-a541-11e4-b6a0-0002a5d5c51b`
- Read/notify characteristic: `98ed0003-a541-11e4-b6a0-0002a5d5c51b`

Supported sources:

| Source | Capability | Typical parsed values |
| --- | ---: | --- |
| `daytime-hr` | `2` | RR-corrected IBI, derived BPM, CQI, temperature, PQI |
| `exercise-hr` | `3` | signal quality, ACM values, motion frequency, regularity, HR, HR approximation, temperature |
| `spo2` | `4` | signal quality, red and IR perfusion index, SpO2 level, HR level, temperature |

### `read-all`

Runs a combined workflow:

1. Lists services and characteristics.
2. Attempts standard BLE heart-rate notifications.
3. Attempts all supported Oura latest heart-rate sources.

```bash
python scripts/oura_full_read.py read-all AA:BB:CC:DD:EE:FF --standard-seconds 20
```

Options:

- `--standard-seconds`: standard HR notification duration. Set to `0` to skip. Default: `10.0`.
- `--timeout`: connection timeout in seconds. Default: `20.0`.
- `--response-timeout`: Oura response wait time. Default: `5.0`.

## Recommended Agent Workflow

Use this sequence when operating against real hardware:

1. Run `scan --timeout 10`.
2. Pick the target address from the JSON output.
3. Run `services <address>` to confirm the expected services and characteristics.
4. If the device is a standard HR monitor, run `hr-standard <address> --seconds 30`.
5. If the device is an Oura ring, run `hr-oura <address> --source daytime-hr`.
6. If daytime HR is unavailable, try `exercise-hr` or `spo2`.
7. Use `read-all` when the user wants a broad inventory and all heart-rate attempts in one command.

## Output Format

Commands print JSON to stdout. This makes the output suitable for agents, scripts, logs, and downstream tooling.

Example standard HR output:

```json
{
  "energy_expended": null,
  "heart_rate_bpm": 72,
  "raw_hex": "0048",
  "rr_intervals_seconds": [],
  "sensor_contact_detected": null,
  "sensor_contact_supported": false
}
```

Example Oura output shape:

```json
{
  "capability_id": 2,
  "request_result": "success",
  "source": "daytime-hr",
  "state": "idle",
  "time_since_last_measurement": 120,
  "values": {
    "heart_rate_bpm": 68.97
  }
}
```

Actual fields depend on the source, device state, firmware behavior, and response payload.

## Troubleshooting

If scan returns no devices:

- Confirm Bluetooth is enabled.
- Confirm the process has OS Bluetooth permission.
- Increase `--timeout`.
- Move the device closer to the adapter.
- Ensure the target device is advertising.

If connection fails:

- Confirm the address was discovered recently.
- Disconnect the device from other apps when possible.
- Retry after Bluetooth privacy address rotation.
- Pair or bond the device if the OS or device requires it.

If `hr-standard` fails against an Oura ring:

- Use `hr-oura` instead. Oura ring heart-rate values use the custom Oura path in this tool.

If `hr-oura` returns unavailable, unsupported, or times out:

- The ring may require bonding or encryption.
- The ring may not be in a state that has recent values for that source.
- Another app may already be connected.
- The selected source may not be supported by that ring or firmware.

## Validation

Validate the agent skill metadata:

```bash
python3 /path/to/skill-creator/scripts/quick_validate.py .
```

Run the bundled unit tests:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=assets/oura-full-read/src \
  python3 -m unittest discover -s assets/oura-full-read/tests
```

Check wrapper help:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/oura_full_read.py --help
```

These checks validate metadata, parser behavior, and CLI wiring. They do not prove live Bluetooth hardware access unless run against a real device.

## Limits And Safety

- This agent skill does not bypass pairing, bonding, encryption, account-backed authorization, or device permissions.
- Do not treat a timeout as proof that a feature does not exist. It may be a connection, permission, state, or range issue.
- Do not claim live hardware success unless a command was actually run against hardware and returned data.
- Generic BLE writes should only be used when the characteristic and payload are intentional.
- Bluetooth behavior varies significantly across Linux, macOS, Windows, WSL, adapters, and device firmware.

## License

No license file is currently included in this repository.
