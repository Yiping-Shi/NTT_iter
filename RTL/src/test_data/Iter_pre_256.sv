// Iterative Preprocessing for 256-degree Polynomial Multiplication
// Input: 256-degree polynomial
//        Stage 0: 1 * 256 --> 3 * 128
//        Stage 1: 3 * 128 --> 9 * 64
//        Stage 2: 9 * 64  --> 27 * 32
//        Stage 3: 27 * 32 --> 81 * 16
//        Stage 4: 81 * 16 --> 243 * 8
//        Stage 5: 243 * 8  --> 729 * 4
//        Stage 6: 729 * 4  --> 2187 * 2
//        Stage 7: 2187 * 2 --> 6561 * 1
// Output: 6561-degree polynomial

`timescale 1ns / 1ps

`include "defines.svh"

module Iter_pre_256(
    input  logic                     clk,
    input  logic                     rst_n,

    input  logic [`DATA_SIZE-1:0]    din,
    output logic [`DATA_SIZE-1:0]    dout,

    input  logic                     load_data,
    input  logic                     start_pre,
    output logic                     done_pre
);

// parameters & control signals
// State Declaration
typedef enum logic [2:0] {
    IDLE,
    LOAD_DATA,
    ITER_PRE,
    OUTPUT_DATA
} state_t;

state_t current_state, next_state;

// Data BRAM1
logic [`RING_DEPTH-1:0] BRAM1_wr_addr;
logic [`RING_DEPTH-1:0] BRAM1_rd_addr;
logic [`DATA_SIZE-1:0]  BRAM1_wr_data;
logic [`DATA_SIZE-1:0]  BRAM1_rd_data;
logic                   BRAM1_wr_en;

// Data BRAM0
logic [`RING_DEPTH-1:0] BRAM0_wr_addr;
logic [`RING_DEPTH-1:0] BRAM0_rd_addr;
logic [`DATA_SIZE-1:0]  BRAM0_wr_data;
logic [`DATA_SIZE-1:0]  BRAM0_rd_data;
logic                   BRAM0_wr_en;

// PU_ICU
logic [`DATA_SIZE-1:0]  ICU_in_1;
logic [`DATA_SIZE-1:0]  ICU_in_0;
logic [`DATA_SIZE-1:0]  ICU_out_2;
logic [`DATA_SIZE-1:0]  ICU_out_1;
logic [`DATA_SIZE-1:0]  ICU_out_0;

// Control signals
logic [2:0]             stage_cnt;
logic [`RING_DEPTH+5:0] sys_cntr;
logic                   iter_finished;


// ------------------------------- BRAMs instantiation
BRAM #(
    .ADDR_WIDTH(`RING_DEPTH),
    .DATA_WIDTH(`DATA_SIZE)
) u_BRAM1 (
    .clk(clk),
    .wr_en(BRAM1_wr_en),
    .wr_addr(BRAM1_wr_addr),
    .wr_data(BRAM1_wr_data),
    .rd_addr(BRAM1_rd_addr),
    .rd_data(BRAM1_rd_data)
); 

BRAM #(
    .ADDR_WIDTH(`RING_DEPTH),
    .DATA_WIDTH(`DATA_SIZE)
) u_BRAM0 (
    .clk(clk),
    .wr_en(BRAM0_wr_en),
    .wr_addr(BRAM0_wr_addr),
    .wr_data(BRAM0_wr_data),
    .rd_addr(BRAM0_rd_addr),
    .rd_data(BRAM0_rd_data)
);

// ------------------------------- ICU instantiation
ICU u_ICU (
    .clk(clk),
    .rst_n(rst_n),
    .ICU_in_0(ICU_in_0),
    .ICU_in_1(ICU_in_1),
    .ICU_out_0(ICU_out_0),
    .ICU_out_1(ICU_out_1),
    .ICU_out_2(ICU_out_2)
);

// ------------------------------- State Machine
always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        current_state <= IDLE;
    end
    else begin
        current_state <= next_state;
    end
end

always_comb begin
    case (current_state)
        IDLE: begin
            if (load_data) begin
                next_state = LOAD_DATA;
            end
            else if (start_pre) begin
                next_state = ITER_PRE;
            end
            else begin
                next_state = IDLE;
            end
        end
        LOAD_DATA: begin
            if (sys_cntr == 14'd256) begin
                next_state = IDLE;
            end
            else begin
                next_state = LOAD_DATA;
            end
        end
        ITER_PRE: begin
            if (iter_finished) begin
                next_state = OUTPUT_DATA;
            end
            else begin
                next_state = ITER_PRE;
            end
        end
        OUTPUT_DATA: begin
            if (sys_cntr == 14'd256) begin
                next_state = IDLE;
            end
            else begin
                next_state = OUTPUT_DATA;
            end
        end
        default: begin
            next_state = IDLE;
        end
    endcase
end

// ------------------------------- sys_cntr
always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        sys_cntr <= 0;
    end
    else begin
        if (current_state == IDLE) begin
            sys_cntr <= 0;
        end
        else if (current_state == LOAD_DATA) begin
            sys_cntr <= sys_cntr + 1;
        end
        else if (current_state == ITER_PRE) begin
            sys_cntr <= 0;
        end
        else if (current_state == OUTPUT_DATA) begin
            sys_cntr <= sys_cntr + 1;
        end
    end
end

// ------------------------------- Load Data
always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        BRAM1_wr_en   <= 0;
        BRAM1_wr_addr <= 0;
        BRAM1_wr_data <= 0;
        BRAM1_rd_addr <= 0;

        BRAM0_wr_en   <= 0;
        BRAM0_wr_addr <= 0;
        BRAM0_wr_data <= 0;
        BRAM0_rd_addr <= 0;
    end
    else begin
        if (next_state == LOAD_DATA) begin
            BRAM1_wr_en   <= sys_cntr[7];
            BRAM1_wr_addr <= sys_cntr - (`RING_SIZE>>1);
            BRAM1_wr_data <= din;
            BRAM1_rd_addr <= 0;

            BRAM0_wr_en   <= !sys_cntr[7];
            BRAM0_wr_addr <= sys_cntr;
            BRAM0_wr_data <= din;
            BRAM0_rd_addr <= 0;
        end
        else begin
            BRAM1_wr_en   <= 0;
            BRAM1_wr_addr <= 0;
            BRAM1_wr_data <= 0;
            BRAM1_rd_addr <= 0;

            BRAM0_wr_en   <= 0;
            BRAM0_wr_addr <= 0;
            BRAM0_wr_data <= 0;
            BRAM0_rd_addr <= 0;
        end
    end
end

endmodule