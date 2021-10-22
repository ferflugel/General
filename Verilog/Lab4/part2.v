// Main circuit
module part2(Clock, Reset_b, Data, Function, ALUout);

    input Clock, Reset_b;
    input [3:0] Data;
    input [2:0] Function;
    output reg [7:0] ALUout;
    reg [7:0] ALU;              // Wire for the ALU

    // Wires for the data and ALUout[3:0]
    wire [3:0] A, B;
    assign A = Data;
    assign B = ALUout[3:0];

    // Adder from other lab, also creating the sum and carry
    wire [3:0] s1, c1;
    fourBitAdder adder(.a(A), .b(B), .c_in(0), .s(s1), .c_out(c1));

    // Selector based on function passed
    always @(*)
    begin
        case (Function)
            0: ALU = {c1[3], s1};
            1: ALU = A+B;
            2: ALU = {{4{B[3]}} , B};
            3: ALU = |{A,B} ? 8'b00000001 : 8'b00000000;
            4: ALU = &{A,B} ? 8'b00000001 : 8'b00000000;
            5: ALU = B << A;
            6: ALU = A*B;
            7: ALU = ALU;
            default: ALU = 8'b00000000;
        endcase
    end

    always @(posedge Clock)
    begin
        if (Reset_b == 1'b0)
            ALUout <= 0;
        else
            ALUout <= ALU;
    end

endmodule


// ---------------------- Old labs from here on

// Four Bit Adder
module fourBitAdder(a, b, c_in, s, c_out);
  input [3:0] a, b;
  input c_in;
  output [3:0] s, c_out; // 3-bit c_out!!!
  FA U1(.A(a[0]), .B(b[0]), .C_in(c_in), .S(s[0]), .C_out(c_out[0]));
  FA U2(.A(a[1]), .B(b[1]), .C_in(c_out[0]), .S(s[1]), .C_out(c_out[1]));
  FA U3(.A(a[2]), .B(b[2]), .C_in(c_out[1]), .S(s[2]), .C_out(c_out[2]));
  FA U4(.A(a[3]), .B(b[3]), .C_in(c_out[2]), .S(s[3]), .C_out(c_out[3]));
endmodule

// Full Adder
module FA(A, B, C_in, S, C_out);
  input A, B, C_in;
  output S;
  output reg C_out;
  wire w1;
  assign w1 = A ^ B;
  always @(*)
    begin
      if (w1)
        C_out = C_in;
      else
        C_out = B;
    end
  assign S = C_in ^ w1;
endmodule