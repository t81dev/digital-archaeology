`/*
 * Stochastic Computing Multiplier
 * Represents a synthesizable stochastic multiplier with an integrated LFSR.
 * Multiplies an input 8-bit binary value with a stochastic bitstream.
 */

module stochastic_multiplier (
    input  logic       clk,
    input  logic       rst_n,
    input  logic       enable,
    input  logic [7:0] bin_val,       // Unipolar binary target value [0, 255]
    input  logic       stream_b,      // External stochastic stream (e.g. from weight)
    output logic       stream_out     // Output product stream
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
