# PlantPulse

## Message format

| Field | Example | Meaning |
| --- | --- | --- |
| `schema` | `1` | Format version |
| `sensor_id` | `motor-0042` | Which motor (letters, digits, `-`, `_` only) |
| `site` | `plant-02` | Which factory |
| `ts` | `1763400000000` | When, as milliseconds since 1 Jan 1970 (UTC) |
| `seq` | `17` | This motor's reading number: 1, 2, 3... |
| `temperature_c` | `48.2` | Temperature in °C |
| `vibration_mm_s` | `1.1` | Vibration in mm/s |
