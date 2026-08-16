// Tiny Tapeout User Module Wrapper for Digital Archaeology IP Cores
// Wraps ternary_alu, capability_bounds_checker, reversible_gates, and stochastic_multiplier
// into a standardized 8-input / 8-output Tiny Tapeout ASIC pinout.

`default_nettype none

module tt_um_archaeology_cores (
    input  logic [7:0] ui_in,    // Dedicated inputs
    output logic [7:0] uo_out,   // Dedicated outputs
    input  logic [7:0] uio_in,   // IOs: Input path
    output logic [7:0] uio_out,  // IOs: Output path
    output logic [7:0] uio_oe,   // IOs: Enable path (1 = output, 0 = input)
    input  logic       ena,      // Active high enable
    input  logic       clk,      // System clock
    input  logic       rst_n     // Asynchronous active-low reset
);

    // All bidirectional IOs set to output mode for diagnostic/telemetry status
    assign uio_oe = 8'hFF;

    // Mode Selector from uio_in[1:0]:
    // 2'b00: Ternary ALU
    // 2'b01: Capability Bounds Checker
    // 2'b10: Reversible Gates Block
    // 2'b11: Stochastic Multiplier
    wire [1:0] mode_sel = uio_in[1:0];

    // ------------------------------------------------------------------------
    // Core 0: Ternary ALU (3-trit Dual-Rail)
    // ------------------------------------------------------------------------
    wire [5:0] alu_A = ui_in[5:0];
    wire [2:0] alu_Op = {uio_in[2], ui_in[7:6]};
    wire       alu_en = ena;
    wire [5:0] alu_Out;
    wire [1:0] alu_CarryOut;

    ternary_alu alu_inst (
        .clk(clk),
        .rst_n(rst_n),
        .en(alu_en),
        .A(alu_A),
        .B(6'b000001), // Fixed operand +1 for TT demo
        .Op(alu_Op),
        .Out(alu_Out),
        .CarryOut(alu_CarryOut)
    );

    // ------------------------------------------------------------------------
    // Core 1: Capability Bounds Checker
    // ------------------------------------------------------------------------
    wire [15:0] cap_req_addr = {uio_in[7:2], ui_in[7:0], 2'b00};
    wire        cap_resp_allowed;
    wire        cap_resp_violation_flag;
    wire        cap_resp_page_fault;
    wire [1:0]  cap_resp_exception_code;

    capability_bounds_checker bounds_inst (
        .clk(clk),
        .rst_n(rst_n),
        .req_addr(cap_req_addr),
        .req_op(2'b00), // Read op
        .req_valid(ena),
        .cap_base(16'h0010),
        .cap_limit(16'h0100),
        .cap_perms(3'b111),
        .cap_tag(1'b1),
        .cap_present(1'b1),
        .desc_mode(uio_in[2]),
        .resp_allowed(cap_resp_allowed),
        .resp_violation_flag(cap_resp_violation_flag),
        .resp_page_fault(cap_resp_page_fault),
        .resp_exception_code(cap_resp_exception_code)
    );

    // ------------------------------------------------------------------------
    // Core 2: Reversible Logic Gates
    // ------------------------------------------------------------------------
    wire rev_X, rev_Y, rev_Z;
    reversible_gates rev_inst (
        .clk(clk),
        .rst_n(rst_n),
        .en(ena),
        .op(uio_in[2]),
        .A(ui_in[0]),
        .B(ui_in[1]),
        .C(ui_in[2]),
        .X(rev_X),
        .Y(rev_Y),
        .Z(rev_Z)
    );

    // ------------------------------------------------------------------------
    // Core 3: Stochastic Multiplier
    // ------------------------------------------------------------------------
    wire stoch_out;
    wire [7:0] lfsr_state;
    stochastic_multiplier stoch_inst (
        .clk(clk),
        .rst_n(rst_n),
        .enable(ena),
        .bin_val(ui_in[7:0]),
        .stream_b(uio_in[2]),
        .stream_out(stoch_out),
        .lfsr_state(lfsr_state)
    );

    // ------------------------------------------------------------------------
    // Output Multiplexer
    // ------------------------------------------------------------------------
    logic [7:0] out_reg;
    logic [7:0] telemetry_reg;

    always_comb begin
        case (mode_sel)
            2'b00: begin
                out_reg = {alu_CarryOut, alu_Out};
                telemetry_reg = 8'h00;
            end
            2'b01: begin
                out_reg = {3'b000, cap_resp_exception_code, cap_resp_page_fault, cap_resp_violation_flag, cap_resp_allowed};
                telemetry_reg = cap_req_addr[7:0];
            end
            2'b10: begin
                out_reg = {5'b00000, rev_Z, rev_Y, rev_X};
                telemetry_reg = 8'hAA;
            end
            2'b11: begin
                out_reg = {7'b0000000, stoch_out};
                telemetry_reg = lfsr_state;
            end
        endcase
    end

    assign uo_out  = out_reg;
    assign uio_out = telemetry_reg;

endmodule
