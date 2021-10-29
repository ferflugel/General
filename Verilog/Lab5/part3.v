module part3(ClockIn, Resetn, Start, Letter, DotDashOut);
input ClockIn;
input Resetn;
input Start;
input [2:0] Letter;
output DotDashOut;
wire clock2;
reg [11:0] q;
divider d1(.clock(ClockIn), .clock2(clock2), .Reset(Resetn));
always@(posedge ClockIn)
begin
	if(Start == 1'b1)
	begin  // I dont know if this way is correct
	case(Letter)
		3'b000: q <= 12'b101110000000;  // A
		3'b001: q <= 12'b111010101000;  // B
		3'b010: q <= 12'b111010111010;  // C
		3'b011: q <= 12'b111010100000;  // D
		3'b100: q <= 12'b100000000000;  // E
		3'b101: q <= 12'b101011101000;  // F
		3'b110: q <= 12'b111011101000;  // G
		3'b111: q <= 12'b101010100000;  // H
		default: q <= 12'b000000000000; // I
	endcase
	end
end
always@(*)
begin
if(Resetn == 1'b0)
q <= 12'b000000000000;
end
shiftreg s1(.Data_IN(q), .Out(DotDashOut), .clock(ClockIn), .clock2(clock2), .reset(Resetn), .Start(Start));


endmodule

module divider(clock, clock2, Reset);
	input clock;
	output reg clock2;
	input Reset;
	reg [8:0] counter = 9'd0;

	// assumes an input of 500 Hz. Returns output of 2 Hz. => we divide by 250
	always@(posedge clock)
	begin
		if(Reset==1'b0)
			counter <= 0;
		counter <= counter + 9'd1;
		if(counter>=9'd249)
			counter <= 9'd0;
		clock2 <= (counter < 9'd125) ? 1'b1:1'b0; // is it 125 or 250
	end

endmodule

module shiftreg(Data_IN, Out, clock, clock2, reset, Start);
	input [11:0] Data_IN;
	output Out;
	input clock;
	input clock2; // different clock (should work based on the counter i.e. only every 0.5 seconds)
	input reset;
	input Start;
	reg [12:0] w;
	assign Out = w[12]; // 12 used to have an extra one at the end which can be loaded
	always@(posedge clock)begin
		if(Start==1'b1)
		begin
			w[0] = Data_IN[0];
			w[1] = Data_IN[1];
			w[2] = Data_IN[2];
			w[3] = Data_IN[3];
			w[4] = Data_IN[4];
			w[5] = Data_IN[5];
			w[6] = Data_IN[6];
			w[7] = Data_IN[7];
			w[8] = Data_IN[8];
			w[9] = Data_IN[9];
			w[10] = Data_IN[10];
			w[11] = Data_IN[11];
			w[12] = 1'b0;
		end
	end
	always@(posedge clock2) begin
		w[12] = w[11];
		w[11] = w[10];
		w[10] = w[9];
		w[9] = w[8];
		w[8] = w[7];
		w[7] = w[6];
		w[6] = w[5];
		w[5] = w[4];
		w[4] = w[3];
		w[3] = w[2];
		w[2] = w[1];
		w[1] = w[0];
		w[0] = w[12]; // verify this
	end
endmodule
