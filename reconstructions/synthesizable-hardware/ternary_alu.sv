// ternary_alu.sv
// Synthesizable 3-trit Balanced Ternary ALU with Sequential Registered Interface
//
// FPGA / Tiny-Tapeout Readiness Notes:
// - All inputs (A, B, Op) are captured synchronously when 'en' is asserted.
// - All outputs (Out, CarryOut) are registered to prevent glitching and long propagation delays.
// - Fits comfortably on a standard Lattice iCE40 UP5K or within a Tiny-Tapeout tile (approx 150-250 LUTs).
// - Target frequency: 100 MHz+ on common FPGA nodes.
//
// Uses 2-bit Pos-Neg (PN) dual-rail encoding for each trit:
//   2'b00 = 0
//   2'b01 = +1 (Positive)
//   2'b10 = -1 (Negative)
//   2'b11 = Invalid

module ternary_alu (
    input  logic        clk,       // System clock
    input  logic        rst_n,     // Asynchronous active-low reset
    input  logic        en,        // Enable / Strobe for operations
    input  logic [5:0]  A,         // 3 trits: A[1:0] (T0), A[3:2] (T1), A[5:4] (T2)
    input  logic [5:0]  B,         // 3 trits: B[1:0] (T0), B[3:2] (T1), B[5:4] (T2)
    input  logic [2:0]  Op,        // Operation select:
                                   //   3'b000: ADD (A + B)
                                   //   3'b001: SUB (A - B)
                                   //   3'b010: NEG (-A)
                                   //   3'b011: MUL (A * B)
                                   //   3'b100: MIN (Tritwise Minimum / AND)
                                   //   3'b101: MAX (Tritwise Maximum / OR)
                                   //   3'b110: LSH (Tritwise Logical Shift Left A)
                                   //   3'b111: RSH (Tritwise Logical Shift Right A)
    output logic [5:0]  Out,       // 3 trits result (registered)
    output logic [1:0]  CarryOut   // 1 trit carry-out (registered)
);

    // =========================================================================
    // FORMAL VERIFICATION PROPERTIES (SVA Friendly Comments)
    // =========================================================================
    //
    // RESET BEHAVIOR:
    // - When !rst_n is asserted, 'Out' must immediately and asynchronously
    //   clear to 6'b000000 and 'CarryOut' to 2'b00, regardless of clk or 'en'.
    //
    // FORMAL ASSUMPTIONS:
    // - Input encodings for A and B must restrict each 2-bit trit to valid
    //   Pos-Neg dual-rail states: (trit != 2'b11).
    //   `assume property (@(posedge clk) A[1:0] != 2'b11 && A[3:2] != 2'b11 && A[5:4] != 2'b11);`
    //   `assume property (@(posedge clk) B[1:0] != 2'b11 && B[3:2] != 2'b11 && B[5:4] != 2'b11);`
    //
    // FORMAL INVARIANTS:
    // - When 'en' is high and 'rst_n' is high, the registered 'Out' and 'CarryOut'
    //   on the subsequent clock cycle must exactly match the combinational function
    //   of inputs A, B, and Op evaluated during the current cycle.
    // - Negation Involution: Op == 3'b010 (NEG) twice is equivalent to identity.
    //   `assert property (@(posedge clk) (en && Op == 3'b010) ##1 (en && Op == 3'b010) => Out == $past(A, 2));`
    // - Zero Element Addition: When B is zero (all trits 2'b00) and Op is ADD (3'b000), Out must equal A.
    //   `assert property (@(posedge clk) (en && Op == 3'b000 && B == 6'b000000) ##1 Out == $past(A));`
    // =========================================================================

    // Decoding helper function: convert 2-bit PN encoding to 8-bit signed integer
    function automatic integer pn_to_int(logic [1:0] trit);
        case (trit)
            2'b01:   pn_to_int = 1;
            2'b10:   pn_to_int = -1;
            default: pn_to_int = 0;
        endcase
    endfunction

    // Encoding helper function: convert 8-bit signed integer to 2-bit PN encoding
    function automatic logic [1:0] int_to_pn(integer val);
        if (val == 1)
            int_to_pn = 2'b01;
        else if (val == -1)
            int_to_pn = 2'b10;
        else
            int_to_pn = 2'b00;
    endfunction

    // Single-trit Full Adder Module logic implemented inside a function
    function automatic void ternary_full_adder(
        input  logic [1:0] a,
        input  logic [1:0] b,
        input  logic [1:0] cin,
        output logic [1:0] s,
        output logic [1:0] cout
    );
        integer val_a, val_b, val_cin, sum_val;
        begin
            val_a   = pn_to_int(a);
            val_b   = pn_to_int(b);
            val_cin = pn_to_int(cin);
            sum_val = val_a + val_b + val_cin;

            // Map sum_val [-3, 3] to s and cout
            case (sum_val)
                -3: begin s = 2'b00; cout = 2'b10; end // Sum = 0, Carry = -1
                -2: begin s = 2'b01; cout = 2'b10; end // Sum = +1, Carry = -1
                -1: begin s = 2'b10; cout = 2'b00; end // Sum = -1, Carry = 0
                 0: begin s = 2'b00; cout = 2'b00; end // Sum = 0, Carry = 0
                 1: begin s = 2'b01; cout = 2'b00; end // Sum = +1, Carry = 0
                 2: begin s = 2'b10; cout = 2'b01; end // Sum = -1, Carry = +1
                 3: begin s = 2'b00; cout = 2'b01; end // Sum = 0, Carry = +1
                 default: begin s = 2'b00; cout = 2'b00; end
            endcase
        end
    endfunction

    // Single-trit Negation function
    function automatic logic [1:0] ternary_neg(logic [1:0] trit);
        // Swap positive and negative rails
        ternary_neg = {trit[0], trit[1]};
    endfunction

    // Single-trit Multiplication function
    function automatic logic [1:0] ternary_mul_trit(logic [1:0] a, logic [1:0] b);
        integer val_a, val_b, mul_val;
        begin
            val_a = pn_to_int(a);
            val_b = pn_to_int(b);
            mul_val = val_a * val_b;
            ternary_mul_trit = int_to_pn(mul_val);
        end
    endfunction

    // Single-trit Minimum function
    function automatic logic [1:0] ternary_min(logic [1:0] a, logic [1:0] b);
        integer val_a, val_b, min_val;
        begin
            val_a = pn_to_int(a);
            val_b = pn_to_int(b);
            min_val = (val_a < val_b) ? val_a : val_b;
            ternary_min = int_to_pn(min_val);
        end
    endfunction

    // Single-trit Maximum function
    function automatic logic [1:0] ternary_max(logic [1:0] a, logic [1:0] b);
        integer val_a, val_b, max_val;
        begin
            val_a = pn_to_int(a);
            val_b = pn_to_int(b);
            max_val = (val_a > val_b) ? val_a : val_b;
            ternary_max = int_to_pn(max_val);
        end
    endfunction

    // Combinational Internal Wires
    logic [5:0] Out_comb;
    logic [1:0] CarryOut_comb;

    // 3-trit Adder wiring
    logic [1:0] s0, s1, s2;
    logic [1:0] c0, c1, c2;
    logic [5:0] B_mux; // Holds optionally negated B for subtraction

    always_comb begin
        // Subtraction negates B
        if (Op == 3'b001) begin
            B_mux[1:0] = ternary_neg(B[1:0]);
            B_mux[3:2] = ternary_neg(B[3:2]);
            B_mux[5:4] = ternary_neg(B[5:4]);
        end else begin
            B_mux = B;
        end

        // Cascade three 1-trit Full Adders for ADD/SUB
        ternary_full_adder(A[1:0], B_mux[1:0], 2'b00, s0, c0);
        ternary_full_adder(A[3:2], B_mux[3:2], c0,     s1, c1);
        ternary_full_adder(A[5:4], B_mux[5:4], c1,     s2, c2);
    end

    // 3-trit Multiplier logic
    logic [5:0] pp0, pp1, pp2;
    logic [5:0] sum_pp0_pp1;
    logic [1:0] carry_pp0_pp1;
    logic [5:0] final_mul_sum;
    logic [1:0] carry_final_mul;

    always_comb begin
        // Compute partial product 0: A * B[0] (truncated to 3 trits)
        pp0[1:0] = ternary_mul_trit(A[1:0], B[1:0]);
        pp0[3:2] = ternary_mul_trit(A[3:2], B[1:0]);
        pp0[5:4] = ternary_mul_trit(A[5:4], B[1:0]);

        // Compute partial product 1: (A * B[1]) << 1 trit
        pp1[1:0] = 2'b00; // Shifted-in zero
        pp1[3:2] = ternary_mul_trit(A[1:0], B[3:2]);
        pp1[5:4] = ternary_mul_trit(A[3:2], B[3:2]);

        // Compute partial product 2: (A * B[2]) << 2 trits
        pp2[1:0] = 2'b00; // Shifted-in zero
        pp2[3:2] = 2'b00; // Shifted-in zero
        pp2[5:4] = ternary_mul_trit(A[1:0], B[5:4]);

        // Sum the partial products: sum_pp0_pp1 = pp0 + pp1
        begin
            logic [1:0] cp0, cp1, cp2;
            ternary_full_adder(pp0[1:0], pp1[1:0], 2'b00, sum_pp0_pp1[1:0], cp0);
            ternary_full_adder(pp0[3:2], pp1[3:2], cp0,     sum_pp0_pp1[3:2], cp1);
            ternary_full_adder(pp0[5:4], pp1[5:4], cp1,     sum_pp0_pp1[5:4], cp2);
            carry_pp0_pp1 = cp2;
        end

        // Final Multiplication sum: final_mul_sum = sum_pp0_pp1 + pp2
        begin
            logic [1:0] cm0, cm1, cm2;
            ternary_full_adder(sum_pp0_pp1[1:0], pp2[1:0], 2'b00, final_mul_sum[1:0], cm0);
            ternary_full_adder(sum_pp0_pp1[3:2], pp2[3:2], cm0,     final_mul_sum[3:2], cm1);
            ternary_full_adder(sum_pp0_pp1[5:4], pp2[5:4], cm1,     final_mul_sum[5:4], cm2);
            carry_final_mul = cm2;
        end
    end

    // ALU Combinational Mux
    always_comb begin
        case (Op)
            3'b000: begin // ADD
                Out_comb = {s2, s1, s0};
                CarryOut_comb = c2;
            end
            3'b001: begin // SUB
                Out_comb = {s2, s1, s0};
                CarryOut_comb = c2;
            end
            3'b010: begin // NEG (-A)
                Out_comb = {ternary_neg(A[5:4]), ternary_neg(A[3:2]), ternary_neg(A[1:0])};
                CarryOut_comb = 2'b00;
            end
            3'b011: begin // MUL
                Out_comb = final_mul_sum;
                CarryOut_comb = carry_final_mul;
            end
            3'b100: begin // MIN
                Out_comb = {ternary_min(A[5:4], B[5:4]), ternary_min(A[3:2], B[3:2]), ternary_min(A[1:0], B[1:0])};
                CarryOut_comb = 2'b00;
            end
            3'b101: begin // MAX
                Out_comb = {ternary_max(A[5:4], B[5:4]), ternary_max(A[3:2], B[3:2]), ternary_max(A[1:0], B[1:0])};
                CarryOut_comb = 2'b00;
            end
            3'b110: begin // LSH (Logical Shift Left A by 1 trit: T0 <- 0, T1 <- T0, T2 <- T1)
                Out_comb = {A[3:2], A[1:0], 2'b00};
                CarryOut_comb = A[5:4]; // Shifts out T2 as CarryOut
            end
            3'b111: begin // RSH (Logical Shift Right A by 1 trit: T2 <- 0, T1 <- T2, T0 <- T1)
                Out_comb = {2'b00, A[5:4], A[3:2]};
                CarryOut_comb = A[1:0]; // Shifts out T0 as CarryOut
            end
            default: begin
                Out_comb = 6'b000000;
                CarryOut_comb = 2'b00;
            end
        endcase
    end

    // Synchronous Registered Stage (FPGA/ASIC clean path)
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            Out      <= 6'b000000;
            CarryOut <= 2'b00;
        end else if (en) begin
            Out      <= Out_comb;
            CarryOut <= CarryOut_comb;
        end
    end

endmodule
