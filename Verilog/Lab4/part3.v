// Main circuit
module part3(clock, reset, ParallelLoadn, RotateRight, ASRight, Data_IN, Q);

    // inputs, outputs, and wires
    input clock, reset, ParallelLoadn, RotateRight, ASRight;
    input [7: 0] Data_IN;
    output [7: 0] Q;

    // Using the ASR functionality
    wire ASR_result;
    multiplexer MUX(.a(Q[7]), .b(Q[0]), .s(ASRight), .out(ASR_result));

    // connecting the circuits
    sub_circuit C0(.left(Q[1]), .right(Q[7]), .LoadLeft(RotateRight), .D(Data_IN[0]), .LoadN(ParallelLoadn), .clk(clock), .reset(reset), .q(Q[0]));
    sub_circuit C1(.left(Q[2]), .right(Q[0]), .LoadLeft(RotateRight), .D(Data_IN[1]), .LoadN(ParallelLoadn), .clk(clock), .reset(reset), .q(Q[1]));
    sub_circuit C2(.left(Q[3]), .right(Q[1]), .LoadLeft(RotateRight), .D(Data_IN[2]), .LoadN(ParallelLoadn), .clk(clock), .reset(reset), .q(Q[2]));
    sub_circuit C3(.left(Q[4]), .right(Q[2]), .LoadLeft(RotateRight), .D(Data_IN[3]), .LoadN(ParallelLoadn), .clk(clock), .reset(reset), .q(Q[3]));
    sub_circuit C4(.left(Q[5]), .right(Q[3]), .LoadLeft(RotateRight), .D(Data_IN[4]), .LoadN(ParallelLoadn), .clk(clock), .reset(reset), .q(Q[4]));
    sub_circuit C5(.left(Q[6]), .right(Q[4]), .LoadLeft(RotateRight), .D(Data_IN[5]), .LoadN(ParallelLoadn), .clk(clock), .reset(reset), .q(Q[5]));
    sub_circuit C6(.left(Q[7]), .right(Q[5]), .LoadLeft(RotateRight), .D(Data_IN[6]), .LoadN(ParallelLoadn), .clk(clock), .reset(reset), .q(Q[6]));
    sub_circuit C7(.left(ASR_result), .right(Q[6]), .LoadLeft(RotateRight), .D(Data_IN[7]), .LoadN(ParallelLoadn), .clk(clock), .reset(reset), .q(Q[7]));

endmodule


// Sub circuit
module sub_circuit(left, right, LoadLeft, D, LoadN, clk, reset, q);
    input left, right, LoadLeft, D, LoadN, clk, reset;
    output q;
    wire mux1_output, mux2_output;
    multiplexer MUX1(.a(left), .b(right), .s(LoadLeft), .out(mux1_output));
    multiplexer MUX2(.a(mux1_output), .b(D), .s(LoadN), .out(mux2_output));
    flip_flop FF(.clk(clk), .d(mux2_output), .reset(reset), .q(q));
endmodule


// Flip flop
module flip_flop(clk, d, reset, q);
    input d, clk, reset;
    output reg q;
    always @(posedge clk)
    begin
        if(reset == 1'b0)
            q <= 0;
        else
            q <= d;
    end
endmodule


// Multiplexer
module multiplexer(a, b, s, out);
    input a, b, s;
    output reg out;
    always @(*)
    begin
        if(s == 1'b0)
            out <= a;
        else
            out <= b;
    end
endmodule
