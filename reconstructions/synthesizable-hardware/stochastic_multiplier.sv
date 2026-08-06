/*
 * Stochastic Computing Multiplier
 * Synthesizable unipolar stochastic multiplier with integrated 8-bit LFSR.
 * Multiplies an input 8-bit binary value with a stochastic bitstream.
 *
 * FPGA / Tiny-Tapeout Readiness Notes:
 * - Output stream_out is registered to avoid logic-cone delays and glitching.
 * - LFSR state-register uses synchronous enable clocking with active-low async reset.
 * - Clock speed target: 300 MHz+ on common open-source toolchains.
 *
 * Interface Definition:
 * - clk: System reference clock.
 * - rst_n: Active-low asynchronous reset.
 * - enable: Clock enable for LFSR state transitions and multiplier registration.
 * - bin_val: Unipolar 8-bit binary value [0, 255] representing target probability.
 * - stream_b: Incoming external stochastic bitstream (unipolar probability).
 * - stream_out: Outgoing synchronized product stochastic bitstream (Y = A * B).
 */

module stochastic_multiplier (
    input  logic       clk,           // Master system clock
    input  logic       rst_n,         // Active-low asynchronous reset
    input  logic       enable,        // High-active clock enable
    input  logic [7:0] bin_val,       // 8-bit unipolar binary value
    input  logic       stream_b,      // External stochastic bitstream B
    output logic       stream_out     // Output product stochastic bitstream
);

    logic [7:0] lfsr_state;
    logic       stream_a;

    // 8-bit LFSR with primitive polynomial: x^8 + x^6 + x^5 + x^4 + 1
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            lfsr_state <= 8'h01; // Avoid lock-up state
        end else if (enable) begin
            lfsr_state <= {lfsr_state[6:0], lfsr_state[7] ^ lfsr_state[5] ^ lfsr_state[4] ^ lfsr_state[3]};
        end
    end

    // Unipolar Stochastic Generation: comparator output stream_a
    always_comb begin
        stream_a = (lfsr_state < bin_val) ? 1'b1 : 1'b0;
    end

    // Stochastic Multiplication (Unipolar AND gate)
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            stream_out <= 1'b0;
        end else if (enable) begin
            stream_out <= stream_a & stream_b;
        end else begin
            stream_out <= 1'b0;
        end
    end

endmodule
