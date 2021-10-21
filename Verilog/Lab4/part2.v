// Main circuit
module part2_internal(Clock, Reset_b, Data, Function, ALUout);

    input Clock, Reset_b;
    input [3:0] Data;
    input [2:0] Function;
    output [7:0] ALUout;

    wire [3:0] A;
    wire [3:0] B;
    reg [7:0] regIn;
    wire [3:0] s1,c1;

    assign A = Data;
    assign B = ALUout[3:0];

    pos_ff flipRegister(.clk(Clock), .Reset_b(Reset_b), .q(ALUout), .d(regIn));
    fourBitAdder adder(.a(A), .b(B), .c_in(0), .s(s1), .c_out(c1)); // Output is max 5 bits

    always @(*)
    begin
        case (Function)
            0: regIn = {c1[3], s1};
            1: regIn = A+B;
            2: regIn = {{4{B[3]}} , B};
            3: regIn = |{A,B} ? 8'b00000001 : 8'b00000000;
            4: regIn = &{A,B} ? 8'b00000001 : 8'b00000000;
            5: regIn = B << A;
            6: regIn = A*B;
            7: regIn = ALUout;
            default: regIn = 8'b00000000;
        endcase
    end

endmodule


// Register
module pos_ff(q, d, clk, Reset_b);
    input [7:0] d;
    input clk, Reset_b;
    output reg [7:0] q;

    always @(posedge clk)
    begin
        if (Reset_b == 1'b0)
            q <= 0;
        else
            q <= d;
    end
endmodule
