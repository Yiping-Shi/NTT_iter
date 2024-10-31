`timescale 1ns / 1ps
`include "defines.svh"

module tb_Iter_pre_256;

    // Clock and Reset
    logic                     clk;
    logic                     rst_n;

    // Data
    logic [`DATA_SIZE-1:0]    din;
    logic [`DATA_SIZE-1:0]    dout;

    // Control signals
    logic                     load_data;
    logic                     start_pre;
    logic                     done_pre;

    // ------------------------------- Instantiate DUT
    Iter_pre_256 u_Iter_pre_256 (
        .clk(clk),
        .rst_n(rst_n),
        .din(din),
        .dout(dout),
        .load_data(load_data),
        .start_pre(start_pre),
        .done_pre(done_pre)
    );

    // ------------------------------- Clock generation
    always begin
        #5 clk = ~clk;
    end

    // ------------------------------- TXT data
    logic [`DATA_SIZE-1:0]  ntt_pin [0:`RING_SIZE-1];

    initial begin
        $readmemh("D:/FHE/IDEA/RTL_code/prj_iter/prj_iter.srcs/test_data/NTT_DIN.txt", ntt_pin);
    end

    // ------------------------------- TEST case

    integer k;

    initial begin: CLK_RST_INIT
        clk   = 0;
        rst_n = 1;

        #20; 
        rst_n = 0;

        #20;
        rst_n = 1;
    end

    initial begin: LOAD_DATA
        load_data = 0;
        start_pre = 0;
        din       = 0;

        #100;

        // state == LOAD_DATA
        load_data = 1;
        #10;
        load_data = 0;

        for (k=0; k<`RING_SIZE; k=k+1) begin
            din = ntt_pin[k];
            #10;
        end

        #50;

        $stop;
    end
    
endmodule