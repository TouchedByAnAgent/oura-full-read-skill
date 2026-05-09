# Oura Full Reader Protocol Reference

## Standard BLE Heart Rate

- Service UUID: `0000180d-0000-1000-8000-00805f9b34fb`
- Measurement characteristic UUID: `00002a37-0000-1000-8000-00805f9b34fb`
- Body sensor location characteristic UUID: `00002a38-0000-1000-8000-00805f9b34fb`

The measurement parser handles uint8 and uint16 BPM formats, sensor-contact flags, energy-expended, and RR intervals.

## Oura Custom BLE

- Manufacturer ID: `690`
- Service UUID: `98ed0001-a541-11e4-b6a0-0002a5d5c51b`
- Write characteristic UUID: `98ed0002-a541-11e4-b6a0-0002a5d5c51b`
- Read/notify characteristic UUID: `98ed0003-a541-11e4-b6a0-0002a5d5c51b`

Latest-values request format:

```text
2f 02 24 <capability>
```

Expected latest-values response format starts with:

```text
2f <length> 25 <capability> <request_result> <status_mask> <state> <time_since_last_measurement_le16> ...
```

Supported Oura heart-rate sources:

| Source | Capability | Parser output |
| --- | ---: | --- |
| `daytime-hr` | `2` | RR-corrected IBI, derived BPM, CQI, temperature, PQI |
| `exercise-hr` | `3` | signal quality, ACM values, motion frequency, regularity, HR, HR approximation, temperature |
| `spo2` | `4` | signal quality, red/IR perfusion index, SpO2 level, HR level, temperature |

Feature result values:

| Value | Name |
| ---: | --- |
| `0` | `success` |
| `1` | `not_supported` |
| `2` | `not_available` |
| `3` | `not_in_finger` |
| `4` | `message_too_short` |
| `5` | `low_battery` |

Feature state values:

| Value | Name |
| ---: | --- |
| `0` | `idle` |
| `1` | `scanning` |
| `2` | `measuring` |
| `3` | `postprocessing` |
