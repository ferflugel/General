// Main module, which connects the T-flip-flops
module part1(Clock, Enable, Clear_b, CounterValue);

    // Inputs, outputs, and wires
    input Clock, Enable, Clear_b;
    output [7:0] CounterValue;
    wire T7, T6, T5, T4, T3, T1, T0;

    // Wiring the circuit with and gates
    assign T0 = Enable;
    assign T1 = CounterValue[0] & T0;
    assign T2 = CounterValue[1] & T1;
    assign T3 = CounterValue[2] & T2;
    assign T4 = CounterValue[3] & T3;
    assign T5 = CounterValue[4] & T4;
    assign T6 = CounterValue[5] & T5;
    assign T7 = CounterValue[6] & T6;

    // Instantiating the T-flip-flops
    tFlipFlop BIT0(.T(T0), .clk(Clock), .reset(Clear_b), .Q(CounterValue[0]));
    tFlipFlop BIT1(.T(T1), .clk(Clock), .reset(Clear_b), .Q(CounterValue[1]));
    tFlipFlop BIT2(.T(T2), .clk(Clock), .reset(Clear_b), .Q(CounterValue[2]));
    tFlipFlop BIT3(.T(T3), .clk(Clock), .reset(Clear_b), .Q(CounterValue[3]));
    tFlipFlop BIT4(.T(T4), .clk(Clock), .reset(Clear_b), .Q(CounterValue[4]));
    tFlipFlop BIT5(.T(T5), .clk(Clock), .reset(Clear_b), .Q(CounterValue[5]));
    tFlipFlop BIT6(.T(T6), .clk(Clock), .reset(Clear_b), .Q(CounterValue[6]));
    tFlipFlop BIT7(.T(T7), .clk(Clock), .reset(Clear_b), .Q(CounterValue[7]));
endmodule

// Code for the T-flip-flop
module tFlipFlop(T, clk, reset, Q);
    input T, clk, reset;
    output reg Q;
    always @(posedge clk)
    begin
        Q <= (!reset) ? 0 : T^Q; // Reset is active-low
    end
endmodule
