// ICU: Iterative Convolution Unit
// Input:  x, y
// Output: x, (x+y), y

`timescale 1ns / 1ps

`include "defines.svh"

module ICU(
    input  logic                      clk,
    input  logic                      rst_n,

    input  logic [`DATA_SIZE-1:0]     ICU_in_0,
    input  logic [`DATA_SIZE-1:0]     ICU_in_1,

    output logic [`DATA_SIZE-1:0]     ICU_out_0,
    output logic [`DATA_SIZE-1:0]     ICU_out_1,
    output logic [`DATA_SIZE-1:0]     ICU_out_2
);

always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        ICU_out_0 <= 0;
        ICU_out_1 <= 0;
        ICU_out_2 <= 0;
    end
    else begin
        ICU_out_0 <= ICU_in_0;
        ICU_out_1 <= ICU_in_0 + ICU_in_1;
        ICU_out_2 <= ICU_in_1;
    end
end

endmodule