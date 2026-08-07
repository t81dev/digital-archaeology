// formal_assertions_companion.sv
// High-Fidelity SVA (SystemVerilog Assertions) Companion Module
//
// Designed to bind directly to our synthesizable soft-cores.
// These properties mathematically model and verify key physical, security,
// and logic-correctness invariants under formal engines (e.g., SymbiYosys).
//
// To run formal verification with Yosys/SymbiYosys, bind these checkers to their respective modules:
//   bind capability_bounds_checker capability_checker_sva_bind checker_inst (.*);
//   bind stochastic_multiplier stochastic_multiplier_sva_bind checker_inst (.*);
//   bind reversible_gates reversible_gates_sva_bind checker_inst (.*);

// =========================================================================
// 1. CAPABILITY & DESCRIPTOR BOUNDS CHECKER FORMAL INVARIANTS
// =========================================================================
module capability_checker_sva_bind (
    input  logic        clk,
    input  logic        rst_n,
    input  logic        req_valid,
    input  logic [15:0] req_addr,
    input  logic [1:0]  req_op,
    input  logic        desc_mode,
    input  logic [15:0] cap_base,
    input  logic [15:0] cap_limit,
    input  logic [2:0]  cap_perms,
    input  logic        cap_tag,
    input  logic        cap_present,
    input  logic        resp_allowed,
    input  logic        resp_violation_flag,
    input  logic        resp_page_fault,
    input  logic [1:0]  resp_violation_code
);

    // Default clocking block
    default clocking cb_clk @(posedge clk);
    endclocking

    // Property 1: Unforgeability Invariant
    // If the unforgeable tag bit (cap_tag) is 0 and a request is valid,
    // access MUST be denied, and the violation flag must rise on the next clock cycle.
    property p_unforgeability;
        (req_valid && !cap_tag) |=> (!resp_allowed && resp_violation_flag && (resp_violation_code == 2'b01));
    endproperty
    assert_unforgeability: assert property (p_unforgeability);
    cover_unforgeability: cover property (p_unforgeability);

    // Property 2: Spatial Memory Safety (Out of Bounds) Invariant
    // If a request is valid, the capability is tagged, and address is out of bounds
    // (req_addr < cap_base OR req_addr >= cap_limit OR malformed bounds where base > limit),
    // access MUST be denied with OUT_OF_BOUNDS code 2'b10.
    property p_spatial_boundary_safety;
        (req_valid && cap_tag && (req_addr < cap_base || req_addr >= cap_limit || cap_base > cap_limit))
        |=> (!resp_allowed && resp_violation_flag && (resp_violation_code == 2'b10));
    endproperty
    assert_spatial_safety: assert property (p_spatial_boundary_safety);
    cover_spatial_safety: cover property (p_spatial_boundary_safety);

    // Property 3: Page Fault Exception Invariant (Burroughs Mode)
    // In Burroughs descriptor mode, if the descriptor is valid but marked not present (cap_present == 0),
    // a hardware Page Fault exception MUST be triggered on the next cycle, mapping to PERMISSION_DENIED (2'b11).
    property p_descriptor_page_fault;
        (req_valid && cap_tag && desc_mode && !cap_present)
        |=> (!resp_allowed && resp_violation_flag && resp_page_fault && (resp_violation_code == 2'b11));
    endproperty
    assert_descriptor_page_fault: assert property (p_descriptor_page_fault);
    cover_descriptor_page_fault: cover property (p_descriptor_page_fault);

    // Property 4: Complete Access Authorization Invariant
    // If the request is valid, tagged, inside bounds, permission bits match the request op,
    // and present (if in descriptor mode), then access must be ALLOWED on the next cycle.
    property p_access_authorized;
        (req_valid && cap_tag && (req_addr >= cap_base && req_addr < cap_limit && cap_base <= cap_limit) &&
         ((req_op == 2'b00 && cap_perms[0]) ||
          (req_op == 2'b01 && cap_perms[1]) ||
          (req_op == 2'b10 && cap_perms[2])) &&
         (!desc_mode || cap_present))
        |=> (resp_allowed && !resp_violation_flag && !resp_page_fault && (resp_violation_code == 2'b00));
    endproperty
    assert_access_authorized: assert property (p_access_authorized);
    cover_access_authorized: cover property (p_access_authorized);

endmodule


// =========================================================================
// 2. STOCHASTIC MULTIPLIER FORMAL INVARIANTS
// =========================================================================
module stochastic_multiplier_sva_bind (
    input  logic       clk,
    input  logic       rst_n,
    input  logic       enable,
    input  logic [7:0] bin_val,
    input  logic       stream_b,
    input  logic       stream_out,
    input  logic [7:0] lfsr_state
);

    // Property 1: LFSR Non-Zero State Conservation
    // Since 8'h00 is a locking state, the LFSR must never transition to or remain in 8'h00.
    property p_lfsr_nonzero_state;
        @(posedge clk) disable iff (!rst_n) (lfsr_state != 8'h00);
    endproperty
    assert_lfsr_nonzero: assert property (p_lfsr_nonzero_state);

    // Property 2: Dominance of Zero Probability
    // If the unipolar binary input represents exactly 0% probability (bin_val == 0),
    // the output bitstream MUST be 0 on the next cycle when enabled.
    property p_zero_multiplication;
        @(posedge clk) disable iff (!rst_n) (enable && bin_val == 8'd0) |=> (stream_out == 1'b0);
    endproperty
    assert_zero_multiplication: assert property (p_zero_multiplication);

    // Property 3: External Stream B Zero Blocking
    // If external stream B is 0, the product stream_out must be 0 on the next cycle.
    property p_stream_b_zero_blocking;
        @(posedge clk) disable iff (!rst_n) (enable && stream_b == 1'b0) |=> (stream_out == 1'b0);
    endproperty
    assert_stream_b_zero_blocking: assert property (p_stream_b_zero_blocking);

endmodule


// =========================================================================
// 3. REVERSIBLE GATES FORMAL INVARIANTS
// =========================================================================
module reversible_gates_sva_bind (
    input  logic        clk,
    input  logic        rst_n,
    input  logic        en,
    input  logic        op,
    input  logic        A,
    input  logic        B,
    input  logic        C,
    input  logic        X,
    input  logic        Y,
    input  logic        Z
);

    // Property 1: Information Conservation (Fredkin CSWAP)
    // The total number of asserted high rails in inputs must equal the total number of
    // asserted high rails in the output stage on the subsequent clock cycle for CSWAP (op=1).
    property p_fredkin_conservation;
        @(posedge clk) disable iff (!rst_n) (en && op == 1'b1) |=> ((X + Y + Z) == ($past(A + B + C)));
    endproperty
    assert_fredkin_conservation: assert property (p_fredkin_conservation);

    // Property 2: Control Invariance
    // Control rail A is conserved in both Toffoli (op=0) and Fredkin (op=1) logic configurations.
    property p_control_invariance;
        @(posedge clk) disable iff (!rst_n) en |=> (X == $past(A));
    endproperty
    assert_control_invariance: assert property (p_control_invariance);

endmodule
