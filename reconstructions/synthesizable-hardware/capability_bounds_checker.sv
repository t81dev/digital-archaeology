// capability_bounds_checker.sv
// Synthesizable Hardware Tagged RAM Capability Bounds Checker
//
// Performs inline hardware check of memory requests against loaded capability bounds.
// Asserts violation flags and precise error codes if unauthorized accesses occur.

module capability_bounds_checker (
    input  logic        clk,
    input  logic        rst_n,

    // Memory Access Request
    input  logic        req_valid,
    input  logic [15:0] req_addr,
    input  logic [1:0]  req_op,     // 2'b00: READ, 2'b01: WRITE, 2'b10: EXECUTE

    // Capability register inputs
    input  logic [15:0] cap_base,   // Lower bound of valid segment (inclusive)
    input  logic [15:0] cap_limit,  // Upper bound of valid segment (exclusive)
    input  logic [2:0]  cap_perms,  // [0]: Read, [1]: Write, [2]: Execute
    input  logic        cap_tag,    // 1-bit unforgeable validity tag

    // Access Response
    output logic        resp_allowed,
    output logic        resp_violation_flag,
    output logic [1:0]  resp_violation_code // 2'b00: NO_VIOLATION
                                             // 2'b01: INVALID_CAP (tag is 0)
                                             // 2'b10: OUT_OF_BOUNDS (addr < base OR addr >= limit)
                                             // 2'b11: PERMISSION_DENIED
);

    logic tag_fault;
    logic bounds_fault;
    logic perm_fault;

    always_comb begin
        tag_fault    = 1'b0;
        bounds_fault = 1'b0;
        perm_fault   = 1'b0;

        if (req_valid) begin
            // 1. Tag validity check
            if (!cap_tag) begin
                tag_fault = 1'b1;
            end
            // 2. Bounds check (inclusive base, exclusive limit)
            else if (req_addr < cap_base || req_addr >= cap_limit) begin
                bounds_fault = 1'b1;
            end
            // 3. Permissions check
            else begin
                case (req_op)
                    2'b00: if (!cap_perms[0]) perm_fault = 1'b1; // Read Denied
                    2'b01: if (!cap_perms[1]) perm_fault = 1'b1; // Write Denied
                    2'b10: if (!cap_perms[2]) perm_fault = 1'b1; // Execute Denied
                    default: perm_fault = 1'b1;
                endcase
            end
        end
    end

    // Sequential output registering to represent real-time pipeline stage
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            resp_allowed         <= 1'b0;
            resp_violation_flag  <= 1'b0;
            resp_violation_code  <= 2'b00;
        end else begin
            if (req_valid) begin
                if (tag_fault) begin
                    resp_allowed         <= 1'b0;
                    resp_violation_flag  <= 1'b1;
                    resp_violation_code  <= 2'b01;
                end else if (bounds_fault) begin
                    resp_allowed         <= 1'b0;
                    resp_violation_flag  <= 1'b1;
                    resp_violation_code  <= 2'b10;
                end else if (perm_fault) begin
                    resp_allowed         <= 1'b0;
                    resp_violation_flag  <= 1'b1;
                    resp_violation_code  <= 2'b11;
                end else begin
                    resp_allowed         <= 1'b1;
                    resp_violation_flag  <= 1'b0;
                    resp_violation_code  <= 2'b00;
                end
            end else begin
                resp_allowed         <= 1'b0;
                resp_violation_flag  <= 1'b0;
                resp_violation_code  <= 2'b00;
            end
        end
    end

endmodule
