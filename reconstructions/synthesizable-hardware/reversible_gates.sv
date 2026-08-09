// reversible_gates.sv
// Synthesizable 3-bit Reversible Logic Gate Block (Toffoli CCNOT & Fredkin CSWAP)
//
// FPGA / Tiny-Tapeout Readiness Notes:
// - Outputs are synchronously registered on the rising clock edge when enabled.
// - Complies with standard Lattice iCE40 and Tiny-Tapeout synthesizable parameters.
// - Can be used as a primitive cell for classical reversible computation.

module reversible_gates (
    input  logic        clk,     // System clock
    input  logic        rst_n,   // Asynchronous active-low reset
    input  logic        en,      // Enable strobe
    input  logic        op,      // Operation select: 0 = Toffoli (CCNOT), 1 = Fredkin (CSWAP)
    input  logic        A,       // Input A (Control 1 / Fredkin Control)
    input  logic        B,       // Input B (Control 2 / Fredkin Input 1)
    input  logic        C,       // Input C (Toffoli Target / Fredkin Input 2)
    output logic        X,       // Output X (registered)
    output logic        Y,       // Output Y (registered)
    output logic        Z        // Output Z (registered)
);

    // =========================================================================
    // FORMAL VERIFICATION PROPERTIES (SVA Block)
    // =========================================================================
    `ifdef FORMAL
        // Immediate Reset Behavior
        always @(*) begin
            if (!rst_n) begin
                assert(X == 1'b0);
                assert(Y == 1'b0);
                assert(Z == 1'b0);
            end
        end

        // Control Conservatism Invariant
        // Under both Toffoli and Fredkin configurations, control line A is preserved exactly.
        property p_control_preservation;
            @(posedge clk) disable iff (!rst_n)
            en |=> (X == $past(A));
        endproperty
        assert_control_preservation: assert property(p_control_preservation);

        // Conservation of Information Invariant (Fredkin/CSWAP)
        // Number of high bits in inputs must equal number of high bits in outputs.
        property p_fredkin_conservation;
            @(posedge clk) disable iff (!rst_n)
            (en && op == 1'b1) |=> (X + Y + Z == $past(A) + $past(B) + $past(C));
        endproperty
        assert_fredkin_conservation: assert property(p_fredkin_conservation);

        // Control B Preservation Invariant (Toffoli/CCNOT)
        // Under Toffoli configuration, control line B is preserved exactly.
        property p_toffoli_control_b;
            @(posedge clk) disable iff (!rst_n)
            (en && op == 1'b0) |=> (Y == $past(B));
        endproperty
        assert_toffoli_control_b: assert property(p_toffoli_control_b);

        // Target Inversion Invariant (Toffoli/CCNOT)
        // Z is inverted under Toffoli if A and B are both high.
        property p_toffoli_inversion;
            @(posedge clk) disable iff (!rst_n)
            (en && op == 1'b0 && A && B) |=> (Z == !$past(C));
        endproperty
        assert_toffoli_inversion: assert property(p_toffoli_inversion);

        // Target Preservation Invariant (Toffoli/CCNOT)
        // Z is preserved under Toffoli if A or B is low.
        property p_toffoli_no_inversion;
            @(posedge clk) disable iff (!rst_n)
            (en && op == 1'b0 && !(A && B)) |=> (Z == $past(C));
        endproperty
        assert_toffoli_no_inversion: assert property(p_toffoli_no_inversion);

        // Fredkin No Swap Invariant (Fredkin/CSWAP)
        // If control A is low, Y == B and Z == C.
        property p_fredkin_no_swap;
            @(posedge clk) disable iff (!rst_n)
            (en && op == 1'b1 && !A) |=> (Y == $past(B) && Z == $past(C));
        endproperty
        assert_fredkin_no_swap: assert property(p_fredkin_no_swap);

        // Fredkin Swap Invariant (Fredkin/CSWAP)
        // If control A is high, Y == C and Z == B.
        property p_fredkin_swap;
            @(posedge clk) disable iff (!rst_n)
            (en && op == 1'b1 && A) |=> (Y == $past(C) && Z == $past(B));
        endproperty
        assert_fredkin_swap: assert property(p_fredkin_swap);
    `endif
    // =========================================================================

    logic X_comb, Y_comb, Z_comb;

    always_comb begin
        if (op == 1'b0) begin
            // Toffoli (CCNOT) Gate
            // X = A
            // Y = B
            // Z = C ^ (A & B)
            X_comb = A;
            Y_comb = B;
            Z_comb = C ^ (A & B);
        end else begin
            // Fredkin (CSWAP) Gate
            // X = A
            // Y = A ? C : B
            // Z = A ? B : C
            X_comb = A;
            Y_comb = A ? C : B;
            Z_comb = A ? B : C;
        end
    end

    // Sequential Registered Stage
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            X <= 1'b0;
            Y <= 1'b0;
            Z <= 1'b0;
        end else if (en) begin
            X <= X_comb;
            Y <= Y_comb;
            Z <= Z_comb;
        end
    end

endmodule
