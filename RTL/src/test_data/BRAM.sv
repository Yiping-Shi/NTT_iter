`timescale 1ns / 1ps

module BRAM #(
    parameter       ADDR_WIDTH = 12,
    parameter       DATA_WIDTH = 30
) (
    input  logic                     clk,
    input  logic                     wr_en,
    input  logic [ADDR_WIDTH-1:0]    wr_addr,
    input  logic [DATA_WIDTH-1:0]    wr_data,
    input  logic [ADDR_WIDTH-1:0]    rd_addr,
    output logic [DATA_WIDTH-1:0]    rd_data
);

// BRAM
(* ram_style="block" *) logic [DATA_WIDTH-1:0] blockram [(1<<ADDR_WIDTH)-1:0];

// Write/Read Operation
always_ff @(posedge clk) begin
    if (wr_en) begin
        blockram[wr_addr] <= wr_data;
    end
    else begin
        rd_data <= blockram[rd_addr];
    end
end

endmodule