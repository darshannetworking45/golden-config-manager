# Cisco Golden Configuration Manager

Compares a device configuration with role-specific baseline commands, supports documented exceptions, and calculates a standardization score.

## Main entry points

- `src.manager.GoldenConfigManager` (`register_exception, calculate_standardization_score`)

## Run the tests

```bash
python -m unittest discover -s tests -v
```

The project uses the Python standard library; no third-party package is required.

## Scope

The manager evaluates text configuration. Review its baseline and exception lists before using the score in a change process.
