# Reproducible Hardware Benchmarking Protocol

This repository distinguishes **measured** hardware results from **analytical estimates**. The checked-in FPGA bitstream and timing report are evidence for one iCEbreaker implementation; they do not establish power, area, or timing results for another board, toolchain, PDK, or workload.

## Reproduce a synthesis profile

```bash
python3 -m pip install -r requirements-dev.txt
python3 tools/profile_synthesis.py --module all --output artifacts/profile.json
```

The generated JSON records the Git revision, platform, Python version, tool availability and tool versions. Treat an entry whose `measurement_kind` is `analytical_estimate` as a model output, not a physical measurement.

## Report a physical result

For each result, commit or attach the following alongside the report:

1. RTL revision and exact command line.
2. Board and device/package, constraints file, and clock target.
3. Yosys, nextpnr, OpenLane, and PDK versions as applicable.
4. Input workload, iteration count, and raw timing/area/power artifacts.
5. Measurement instrument, sampling method, ambient conditions, and error bounds for power measurements.

Use `measured_fpga` only for an observed board result and `measured_asic` only for a completed ASIC flow with generated reports. Keep estimates and measurements in separate tables; never compute an average across them.

## Suggested comparison workload

For the current cores, run a fixed 1,000,000-cycle stress workload after reset: capability requests spanning allowed, out-of-bounds, permission-denied, and not-present cases; all ternary operations; all reversible gate input states; and a full stochastic LFSR period. Report throughput, Fmax, LUT/FF or cell area, and board power at the same workload and clock target.
