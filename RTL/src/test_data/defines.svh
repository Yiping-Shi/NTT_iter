`timescale 1ns / 1ps

// --------------------------------------
// User-defined parameters
// -- K: DATA_SIZE
// -- n: RING_SIZE

`define DATA_SIZE 30
`define RING_SIZE 256

// --------------------------------------
// parameter depth
`define RING_DEPTH      ($clog2(`RING_SIZE))