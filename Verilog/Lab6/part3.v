//  - input data port
// Resetn - synchronous reset
// Go signal starts things
// DataResult - register at output of ALU

module part3(Clock, Resetn, Go, Divisor, Dividend, Quotient, Remainder);
    input Clock;
    input Resetn;
    input Go;
    input [3:0] Divisor;    // from piazza apparently its 4 bit
    input [3:0] Dividend;
    output [3:0] Quotient;
    output [4:0] Remainder;

    // lots of wires to connect our datapath and control
    wire ld_a, ld_b, ld_c, ld_r;
	 wire RegA;
	 wire [4:0] result1;
	 wire [3:0] result2;
    wire [4:0] div; // new divisor being used
    assign div= {1'b0, Divisor};
	 wire [3:0] dostuff;
    control C0(
        .clk(Clock),
        .resetn(Resetn),

        .go(Go),
        .ld_a(ld_a),
        .ld_b(ld_b),
        .ld_c(ld_c),
        .ld_r(ld_r),
		  .dostuff(dostuff)
    );

    datapath D0(
        .clk(Clock),
        .resetn(Resetn),
        .ld_x(ld_x),
        .ld_a(ld_a),
        .ld_b(ld_b),
        .ld_c(ld_c),
        .ld_r(ld_r),
        .Divisor(div),
		  .RegA(RegA),
		  .Dividend(Dividend),
        .a(Remainder),
		  .b(Quotient), // replace with result1, result2 if needed. change .a, .b to result1, result2 also if needed
		  .dostuff(dostuff)
    );

 endmodule


module control(
    input clk,
    input resetn,
    input go,

    output reg  ld_a, ld_b, ld_c, ld_r,
	 output reg [3:0] dostuff
    );

    reg [5:0] current_state, next_state;
	 //wire dostuff;
	 //wire setstuff;

    localparam  S_LOAD_A        = 5'd0,
                S_LOAD_A_WAIT   = 5'd1,
                S_LOAD_B        = 5'd2,
                S_LOAD_B_WAIT   = 5'd3,
                S_LOAD_C        = 5'd4,
                S_LOAD_C_WAIT   = 5'd5,
                S_LOAD_X        = 5'd6,
                S_LOAD_X_WAIT   = 5'd7,
                S_CYCLE_0       = 5'd8,
                S_CYCLE_1       = 5'd9,
                S_CYCLE_2       = 5'd10,
					 S_CYCLE_3       = 5'd11,
					 S_CYCLE_4       = 5'd12;

    // Next state logic aka our state table
    always@(*)
    begin: state_table
            case (current_state)
                S_LOAD_A: next_state = go ? S_LOAD_A_WAIT : S_LOAD_A; // Loop in current state until value is input
                S_LOAD_A_WAIT: next_state = go ? S_LOAD_A_WAIT : S_CYCLE_0; // Loop in current state until go signal goes low
                S_CYCLE_0: next_state = S_CYCLE_1;
                S_CYCLE_1: next_state = S_CYCLE_2;
					 S_CYCLE_2: next_state = S_CYCLE_3;
					 S_CYCLE_3: next_state = S_CYCLE_4;
					 S_CYCLE_4: next_state = S_LOAD_A;   // Last cycle will be to assign remainder and quotient to RegA and Divided

            default:     next_state = S_LOAD_A;
        endcase
    end // state_table


    // Output logic aka all of our datapath control signals
    always @(*)
    begin: enable_signals
        // By default make all our signals 0
        ld_a = 1'b0;
        ld_b = 1'b0;
        ld_c = 1'b0;
        ld_r = 1'b0;
		  dostuff = 4'b0;
		  //setstuff = 1'b0;

        case (current_state)
				S_LOAD_A: begin   // not being used.
                ld_a = 1'b0;
                end
            S_LOAD_A_WAIT: begin
                ld_a = 1'b1;
                end
            S_LOAD_B: begin   // not being used.
                ld_b = 1'b1;
                end
            S_LOAD_C: begin
                ld_c = 1'b1;
                end
            S_CYCLE_0: begin // Cycle 0
					 dostuff = 4'b0001;
            end
            S_CYCLE_1: begin
					 dostuff = 4'b0010;
            end
				S_CYCLE_2: begin
					 dostuff = 4'b0100;
            end
				S_CYCLE_3: begin
					 dostuff = 4'b1000;
            end
				S_CYCLE_4: begin // when we set
					 dostuff = 4'b0;
					 ld_r = 1'b1; // load values in the reg.
					 //setstuff = 1'b1;
            end
        // default:    // don't need default since we already made sure all of our outputs were assigned a value at the start of the always block
        endcase
    end // enable_signals

    // current_state registers
    always@(posedge clk)
    begin: state_FFs
        if(!resetn)
            current_state <= S_LOAD_A;
        else
            current_state <= next_state;
    end // state_FFS
endmodule

module datapath(
    input clk,
    input resetn,
    input [4:0] Divisor,
	 input [4:0] RegA,
	 input [3:0] Dividend,
    input ld_x, ld_a, ld_b, ld_c,
    input ld_r,
	 input [3:0] dostuff,
	 output reg [4:0] a,
	 output reg [3:0] b);
//    output reg [4:0] result1,
//	 output reg [3:0] result2
//    );

    // input registers
//	 reg [4:0] a; // Register A
//	 reg [3:0] b; // Dividend
	 reg [4:0] c; // Divisor

//	 result1 = a;
//	 result2 = b;

    // Registers a, b, c, x with respective input logic
    always@(posedge clk) begin
        if(!resetn) begin
            a = 5'b0;
            b = 4'b0;
            c = 5'b0;
        end
        else begin  // ld_a, ld_b and ld_c only set at the beginning to load the initial values to the registers
            if(ld_a)
					 begin
                a =  5'b0; // load alu_out if load_alu_out signal is high, otherwise load from data_in
					 b = Dividend;
					 c = Divisor;
					 end
        end
    end

	 // To run the steps inside one cycle
	 always@(*)
	 begin
		case (dostuff)
			4'b0001: begin
				a = {a[3:0], b[3]};
				//a = a << 1;
				//a = a + b[3];
				b = b << 1;
				a = a-Divisor;
				if(a[4])
				begin
					a = a + Divisor;
					b[0] = 1'b0;
				end
				else
				begin
					b[0] = 1'b1;
				end
			end
			4'b0010: begin
				a = {a[3:0], b[3]};
//				a = a << 1;
//				a = a + b[3];
				b = b << 1;
				a = a-Divisor;
				if(a[4])
				begin
					a = a + Divisor;
					b[0] = 1'b0;
				end
				else
				begin
					b[0] = 1'b1;
				end
			end
			4'b0100: begin
			a = {a[3:0], b[3]};
//				a = a << 1;
//				a = a + b[3];
				b = b << 1;
				a = a-Divisor;
				if(a[4])
				begin
					a = a + Divisor;
					b[0] = 1'b0;
				end
				else
				begin
					b[0] = 1'b1;
				end
			end
			4'b1000: begin
			a = {a[3:0], b[3]};
//				a = a << 1;
//				a = a + b[3];
				b = b << 1;
				a = a-Divisor;
				if(a[4])
				begin
					a = a + Divisor;
					b[0] = 0;
				end
				else
				begin
					b[0] = 1;
				end
			end
			4'b0000: begin
				a = a;
				b = b;
			end
		endcase

	 end

endmodule
