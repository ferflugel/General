module part2(ClockIn, Reset, Speed, CounterValue);

    // Inputs, outputs, and wires
    input ClockIn, Reset;
    input [1:0] Speed;
    output reg [3:0] CounterValue;
    reg Enable;
    reg [10:0] RateDivider;

    // For every cycle (of the 500 Hz clock)
    always @(posedge ClockIn)
    begin

        // Resetting the counter
        if (Reset)
        begin
            CounterValue <= 0;
            RateDivider <= 0;
        end

        // Not resetting the counter
        else
        begin
            if (RateDivider == 0)
            begin
                Enable <= 1;
                case(Speed)
                    0: RateDivider <= 11'd0;
                    1: RateDivider <= 11'd499;
                    2: RateDivider <= 11'd999;
                    3: RateDivider <= 11'd1999;
                endcase
                CounterValue <= (CounterValue == 4'b1111) ? 0 : CounterValue + 1;
            end
            else
            begin
                Enable <= 0;
                RateDivider <= RateDivider - 1;
            end
        end
   end
endmodule
