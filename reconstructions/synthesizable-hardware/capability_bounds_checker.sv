// capability_bounds_checker.sv
// Synthesizable Hardware Tagged RAM Capability & Descriptor Bounds Checker
//
// FPGA / Tiny-Tapeout Readiness Notes:
// - Pipelined synchronous outputs representation for precise timing constraints.
// - Fits cleanly within standard Lattice, Cyclone, or Artix FPGA logic slices (~120 LUTs).
// - Designed to integrate with standard SoC busses (e.g., Wishbone, TileLink, or AXI-Lite).
// - Easily fits in a single Tiny-Tapeout digital layout tile at 50 MHz+.
//
// Performs inline hardware check of memory requests against loaded capability or Burroughs descriptor bounds.
// Asserts violation flags, precise error codes, and virtual memory page-fault triggers if unauthorized accesses occur.
//
// Interface Definition:
// - clk: Master system clock.
// - rst_n: Active-low asynchronous reset.
// - req_valid: Asserted when a new memory request is active.
// - req_addr: 16-bit target memory address.
// - req_op: Operation type: 2'b00: READ, 2'b01: WRITE, 2'b10: EXECUTE, 2'b11: INVALID_OP.
// - desc_mode: 1-bit control select. If 1'b1, uses Burroughs Descriptor mode; if 1'b0, uses pure Capability mode.
// - cap_base: 16-bit segment base address (inclusive lower bound).
// - cap_limit: 16-bit segment limit address (exclusive upper bound).
// - cap_perms: 3-bit permissions: [0] Read allowed, [1] Write allowed, [2] Execute allowed.
// - cap_tag: 1-bit unforgeable validity tag bit (must be 1 for any access).
// - cap_present: 1-bit presence descriptor bit (if desc_mode is active and this is 0, triggers page fault).
//
// Outputs (Synchronous pipelined):
// - resp_allowed: High if memory access is fully authorized and valid.
// - resp_violation_flag: High if any hardware violation occurs.
// - resp_page_fault: High if a Descriptor Not Present (Page Fault) is triggered.
// - resp_violation_code: 2-bit error status code:
//     - 2'b00: NO_VIOLATION
//     - 2'b01: INVALID_CAP_OR_DESC (tag bit is 0)
//     - 2'b10: OUT_OF_BOUNDS (addr < base OR addr >= limit, OR malformed bounds)
//     - 2'b11: PERMISSION_DENIED (or read-only / invalid requested op)

module capability_bounds_checker (
    input  logic        clk,
    input  logic        rst_n,

    // Memory Access Request
    input  logic        req_valid,
    input  logic [15:0] req_addr,
    input  logic [1:0]  req_op,     // 2'b00: READ, 2'b01: WRITE, 2'b10: EXECUTE, 2'b11: INVALID_OP

    // Control parameters
    input  logic        desc_mode,   // 1'b1: Burroughs Descriptor mode, 1'b0: Capability mode

    // Capability / Descriptor register inputs
    input  logic [15:0] cap_base,    // Lower bound of valid segment (inclusive)
    input  logic [15:0] cap_limit,   // Upper bound of valid segment (exclusive)
    input  logic [2:0]  cap_perms,   // [0]: Read, [1]: Write, [2]: Execute
    input  logic        cap_tag,     // 1-bit unforgeable validity tag
    input  logic        cap_present, // 1-bit presence bit (Burroughs VM / page fault support)

    // Access Response (Synchronous registered pipeline output)
    output logic        resp_allowed,
    output logic        resp_violation_flag,
    output logic        resp_page_fault,
    output logic [1:0]  resp_violation_code
);

    logic tag_fault;
    logic pres_fault;
    logic bounds_fault;
    logic perm_fault;

    always_comb begin
        tag_fault    = 1'b0;
        pres_fault   = 1'b0;
        bounds_fault = 1'b0;
        perm_fault   = 1'b0;

        if (req_valid) begin
            // 1. Tag validity check
            if (!cap_tag) begin
                tag_fault = 1'b1;
            end
            // 2. Presence bit check (Burroughs page fault simulation in descriptor mode)
            else if (desc_mode && !cap_present) begin
                pres_fault = 1'b1;
            end
            // 3. Bounds check (inclusive base, exclusive limit, plus malformed bounds safety check)
            else if (req_addr < cap_base || req_addr >= cap_limit || cap_base > cap_limit) begin
                bounds_fault = 1'b1;
            end
            // 4. Permissions check
            else begin
                case (req_op)
                    2'b00: if (!cap_perms[0]) perm_fault = 1'b1; // Read Denied
                    2'b01: if (!cap_perms[1]) perm_fault = 1'b1; // Write Denied (or read-only descriptor)
                    2'b10: if (!cap_perms[2]) perm_fault = 1'b1; // Execute Denied
                    default:                  perm_fault = 1'b1; // Any undefined/invalid op (e.g. 2'b11) raises permission fault
                endcase
            end
        end
    end

    // Sequential output registering to represent real-time pipeline stage
    always_ff @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            resp_allowed         <= 1'b0;
            resp_violation_flag  <= 1'b0;
            resp_page_fault      <= 1'b0;
            resp_violation_code  <= 2'b00;
        end else begin
            if (req_valid) begin
                if (tag_fault) begin
                    resp_allowed         <= 1'b0;
                    resp_violation_flag  <= 1'b1;
                    resp_page_fault      <= 1'b0;
                    resp_violation_code  <= 2'b01;
                end else if (pres_fault) begin
                    resp_allowed         <= 1'b0;
                    resp_violation_flag  <= 1'b1;
                    resp_page_fault      <= 1'b1; // Trigger hardware page fault / MCP interrupt
                    resp_violation_code  <= 2'b11; // Maps under access permission/denied block
                end else if (bounds_fault) begin
                    resp_allowed         <= 1'b0;
                    resp_violation_flag  <= 1'b1;
                    resp_page_fault      <= 1'b0;
                    resp_violation_code  <= 2'b10;
                end else if (perm_fault) begin
                    resp_allowed         <= 1'b0;
                    resp_violation_flag  <= 1'b1;
                    resp_page_fault      <= 1'b0;
                    resp_violation_code  <= 2'b11;
                end else begin
                    resp_allowed         <= 1'b1;
                    resp_violation_flag  <= 1'b0;
                    resp_page_fault      <= 1'b0;
                    resp_violation_code  <= 2'b00;
                end
            end else begin
                resp_allowed         <= 1'b0;
                resp_violation_flag  <= 1'b0;
                resp_page_fault      <= 1'b0;
                resp_violation_code  <= 2'b00;
            end
        end
    end

endmodule
