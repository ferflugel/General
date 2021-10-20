module sub_circuit(left, right, LoadLeft, D, LoadN, clk, reset, q);
    input left, right, LoadLeft, D, LoadN, clk, reset;
    output q;
    wire mux1_output, mux2_output;
    multiplexer MUX1(.a(left), .b(right), .s(LoadLeft), .out(mux1_output));
    multiplexer MUX2(.a(mux1_output), .b(D), .s(LoadN), .out(mux2_output));
    flip_flop FF(.clk(clk), .d(mux2_output), .reset(reset), .q(q));
endmodule

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

module multiplexer(a, b, s, out);
    input a, b, out;
    output reg out;
    always @(*)
    begin
        if(reset == 1'b0)
            out <= a;
        else
            out <= b;
    end
endmodule
