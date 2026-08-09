# Makefile for Synthesizable Hardware IP Cores
# Handles formal verification via SymbiYosys and physical FPGA compilation via Yosys/nextpnr.

.PHONY: all formal fpga clean help

all: formal fpga

help:
	@echo "Available targets:"
	@echo "  make formal   - Run SymbiYosys formal verification on all cores"
	@echo "  make fpga     - Synthesize, place, and route capability_bounds_checker for iCEbreaker"
	@echo "  make clean    - Remove build artifacts and temporary logs"

formal:
	@echo "================================================================================"
	@echo "                  RUNNING SYMBIYOSYS FORMAL VERIFICATION"
	@echo "================================================================================"
	mkdir -p formal/logs
	@echo "Running capability_bounds_checker proof..."
	sby -f formal/capability_bounds_checker.sby > formal/logs/capability_bounds_checker.log 2>&1 || (echo "FAIL: capability_bounds_checker"; exit 1)
	@echo "Running ternary_alu proof..."
	sby -f formal/ternary_alu.sby > formal/logs/ternary_alu.log 2>&1 || (echo "FAIL: ternary_alu"; exit 1)
	@echo "Running reversible_gates proof..."
	sby -f formal/reversible_gates.sby > formal/logs/reversible_gates.log 2>&1 || (echo "FAIL: reversible_gates"; exit 1)
	@echo "Running stochastic_multiplier proof..."
	sby -f formal/stochastic_multiplier.sby > formal/logs/stochastic_multiplier.log 2>&1 || (echo "FAIL: stochastic_multiplier"; exit 1)
	@echo "All proofs PASSED. Logs stored in reconstructions/synthesizable-hardware/formal/logs/."

fpga:
	@echo "================================================================================"
	@echo "                  COMPILING FPGA BITSTREAM FOR iCEBREAKER"
	@echo "================================================================================"
	mkdir -p fpga/build
	@echo "Synthesizing netlist with Yosys..."
	yosys -p "synth_ice40 -top capability_bounds_checker -json fpga/build/capability_bounds_checker.json" capability_bounds_checker.sv
	@echo "Executing place-and-route with nextpnr-ice40..."
	nextpnr-ice40 --up5k --package sg48 --pcf fpga/icebreaker.pcf --json fpga/build/capability_bounds_checker.json --asc fpga/build/capability_bounds_checker.asc --report fpga/build/capability_bounds_checker_timing.rpt
	@echo "Generating binary bitstream with icepack..."
	icepack fpga/build/capability_bounds_checker.asc fpga/build/capability_bounds_checker.bin
	@echo "FPGA compilation complete!"
	@echo "  Bitstream: fpga/build/capability_bounds_checker.bin"
	@echo "  Timing:    fpga/build/capability_bounds_checker_timing.rpt"

clean:
	rm -rf formal/logs
	rm -rf fpga/build
