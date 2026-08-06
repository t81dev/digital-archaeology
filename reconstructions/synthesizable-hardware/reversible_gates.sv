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
    // FORMAL VERIFICATION PROPERTIES (SVA Friendly Comments)
    // =========================================================================
    //
    // RESET BEHAVIOR:
    // - On asynchronous active-low reset (!rst_n), all registered outputs (X, Y, Z)
    //   must asynchronously clear to 1'b0.
    //
    // FORMAL INVARIANTS (Bijectivity & Self-Inversion):
    // - Self-Inversion: Running the Toffoli or Fredkin configuration twice with
    //   matching outputs routed back must reconstruct the original input triplet.
    //   Since this is a synchronous pipeline, evaluating a self-inverse state
    //   asserts that the logic maps bijective states bi-directionally without loss.
    // - Conservation of Information: Number of high bits in inputs must equal
    //   number of high bits in outputs (essential property of Fredkin gates).
    //   `assert property (@(posedge clk) (en && op == 1'b1) ##1 (X + Y + Z == $past(A + B + C)));`
    // - Control Conservatism: Under both Toffoli and Fredkin configurations, control
    //   line A is preserved exactly.
    //   `assert property (@(posedge clk) en ##1 (X == $past(A)));`
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
