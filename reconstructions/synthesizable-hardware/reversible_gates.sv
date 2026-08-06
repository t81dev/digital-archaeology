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
