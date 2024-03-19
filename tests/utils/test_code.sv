module top (
  input clk, rst,
  output reg [3:0] cnt
);
  initial cnt = 0;

  always @(posedge clk) begin
    if (rst)
      cnt <= 0;
    else
      cnt <= cnt + 4'd 1;
  end

  always @(posedge clk) begin
    assume (cnt != 10);
    assert (cnt != 15);
  end
endmodule
module foo (input logic a, input logic b, output logic c);
  // Magic happens here...
endmodule

module bar (input a, input b, output c);
  assign c = a ^ b;
endmodule

module top ();
  logic u, v, w;
  foo foo_i (.a (u), .b (v), .c (w));

  // // bind foo bar bound_i (.*);

  always_comb begin
    assert(w == u ^ v);
  end
endmodule
module foo (input logic a0, input logic b0, output logic c0,
            input logic a1, input logic b1, output logic c1);
  // Magic happens here...
endmodule

module bar (input a, input b, output c);
  assign c = a ^ b;
endmodule

module top ();
  logic u0, v0, w0;
  logic u1, v1, w1;

  foo foo0 (.a0 (u0), .b0 (v0), .c0 (w0),
            .a1 (u1), .b1 (v1), .c1 (w1));

  // // bind foo bar bar0 (.a(a0), .b(b0), .c(c0)), bar1 (.a(a1), .b(b1), .c(c1));

  always_comb begin
    assert(w0 == u0 ^ v0);
    assert(w1 == u1 ^ v1);
  end
endmodule
module foo (input logic a, input logic b, output logic c);
  // Magic happens here...
endmodule

module bar (input a, input b, output c);
  assign c = a ^ b;
endmodule

module top ();
  logic u, v, w;
  foo foo_i (.a (u), .b (v), .c (w));

  always_comb begin
    assert(w == u ^ v);
  end
endmodule

// // bind $root.top.foo_i bar bound_i (.*);
module foo (input logic a, input logic b, output logic c);
  // Magic happens here...
endmodule

module bar (input a, input b, output c);
  assign c = a ^ b;
endmodule

module top ();
  logic u0, v0, w0;
  logic u1, v1, w1;

  foo foo0 (.a (u0), .b (v0), .c (w0));
  foo foo1 (.a (u1), .b (v1), .c (w1));

  // // bind foo : foo0, foo1 bar bound_i (.*);

  always_comb begin
    assert(w0 == u0 ^ v0);
    assert(w1 == u1 ^ v1);
  end
endmodule
module foo (input logic a, input logic b, output logic c);
  parameter doit = 1;

  // Magic happens here...
endmodule

module bar (input a, input b, output c);
  parameter doit = 1;

  assign c = doit ? a ^ b : 0;
endmodule

module top (input u0, input v0, output w0,
            input u1, input v1, output w1);
  foo #(.doit (0)) foo0 (.a (u0), .b (v0), .c (w0));
  foo #(.doit (1)) foo1 (.a (u1), .b (v1), .c (w1));

  // bind foo bar #(.doit (doit)) bound_i (.*);

  always_comb begin
    assert (w0 == '0);
    assert (w1 == u1 ^ v1);
  end
endmodule
module foo (input logic a, input logic b, output logic c);
  // Magic happens here...
endmodule

module bar (input a, input b, output c);
  assign c = a ^ b;
endmodule

module top ();
  logic u, v, w;
  foo foo_i (.a (u), .b (v), .c (w));

  always_comb begin
    assert(w == u ^ v);
  end
endmodule

// bind top.foo_i bar bound_i (.*);
module functions01;

wire t;
wire [5:2]x;
wire [3:0]y[2:7];
wire [3:0]z[7:2][2:9];

//wire [$size(x)-1:0]x_size;
//wire [$size({x, x})-1:0]xx_size;
//wire [$size(y)-1:0]y_size;
//wire [$size(z)-1:0]z_size;

assert property ($dimensions(t) == 1);
assert property ($dimensions(x) == 1);
assert property ($dimensions({3{x}}) == 1);
assert property ($dimensions(y) == 2);
assert property ($dimensions(y[2]) == 1);
assert property ($dimensions(z) == 3);
assert property ($dimensions(z[3]) == 2);
assert property ($dimensions(z[3][3]) == 1);

assert property ($unpacked_dimensions(t) == 0);
assert property ($unpacked_dimensions(x) == 0);
assert property ($unpacked_dimensions({3{x}}) == 0);
assert property ($unpacked_dimensions(y) == 1);
assert property ($unpacked_dimensions(y[2]) == 0);
assert property ($unpacked_dimensions(z) == 2);
assert property ($unpacked_dimensions(z[3]) == 1);
assert property ($unpacked_dimensions(z[3][3]) == 0);

assert property ($size(t) == 1);
assert property ($size(x) == 4);
assert property ($size({3{x}}) == 3*4);
assert property ($size(y) == 6);
assert property ($size(y, 1) == 6);
assert property ($size(y, (1+1)) == 4);
assert property ($size(y[2], 1) == 4);
// This is unsupported at the moment
//assert property ($size(y[2][1], 1) == 1);

assert property ($size(z) == 6);
assert property ($size(z, 1) == 6);
assert property ($size(z, 2) == 8);
assert property ($size(z, 3) == 4);
assert property ($size(z[3], 1) == 8);
assert property ($size(z[3][3], 1) == 4);
// This is unsupported at the moment
//assert property ($size(z[3][3][3], 1) == 1);
// This should trigger an error if enabled (it does).
//assert property ($size(z, 4) == 4);

//wire [$bits(x)-1:0]x_bits;
//wire [$bits({x, x})-1:0]xx_bits;

assert property ($bits(t) == 1);
assert property ($bits(x) == 4);
assert property ($bits(y) == 4*6);
assert property ($bits(z) == 4*6*8);

assert property ($high(x) == 5);
assert property ($high(y) == 7);
assert property ($high(y, 1) == 7);
assert property ($high(y, (1+1)) == 3);

assert property ($high(z) == 7);
assert property ($high(z, 1) == 7);
assert property ($high(z, 2) == 9);
assert property ($high(z, 3) == 3);
assert property ($high(z[3]) == 9);
assert property ($high(z[3][3]) == 3);
assert property ($high(z[3], 2) == 3);

assert property ($low(x) == 2);
assert property ($low(y) == 2);
assert property ($low(y, 1) == 2);
assert property ($low(y, (1+1)) == 0);

assert property ($low(z) == 2);
assert property ($low(z, 1) == 2);
assert property ($low(z, 2) == 2);
assert property ($low(z, 3) == 0);
assert property ($low(z[3]) == 2);
assert property ($low(z[3][3]) == 0);
assert property ($low(z[3], 2) == 0);

assert property ($left(x) == 5);
assert property ($left(y) == 2);
assert property ($left(y, 1) == 2);
assert property ($left(y, (1+1)) == 3);

assert property ($left(z) == 7);
assert property ($left(z, 1) == 7);
assert property ($left(z, 2) == 2);
assert property ($left(z, 3) == 3);
assert property ($left(z[3]) == 2);
assert property ($left(z[3][3]) == 3);
assert property ($left(z[3], 2) == 3);

assert property ($right(x) == 2);
assert property ($right(y) == 7);
assert property ($right(y, 1) == 7);
assert property ($right(y, (1+1)) == 0);

assert property ($right(z) == 2);
assert property ($right(z, 1) == 2);
assert property ($right(z, 2) == 9);
assert property ($right(z, 3) == 0);
assert property ($right(z[3]) == 9);
assert property ($right(z[3][3]) == 0);
assert property ($right(z[3], 2) == 0);

assert property ($increment(x) == 1);
assert property ($increment(y) == -1);
assert property ($increment(y, 1) == -1);
assert property ($increment(y, (1+1)) == 1);

assert property ($increment(z) == 1);
assert property ($increment(z, 1) == 1);
assert property ($increment(z, 2) == -1);
assert property ($increment(z, 3) == 1);
assert property ($increment(z[3]) == -1);
assert property ($increment(z[3][3]) == 1);
assert property ($increment(z[3], 2) == 1);
endmodule
module uut_arrays02(clock, we, addr, wr_data, rd_data);

input clock, we;
input [3:0] addr, wr_data;
output [3:0] rd_data;
reg [3:0] rd_data;

reg [3:0] memory [16];

always @(posedge clock) begin
	if (we)
		memory[addr] <= wr_data;
	rd_data <= memory[addr];
end

endmodule
typedef logic [0:3][7:0] reg2dim_t;
typedef logic  [7:0] reg8_t;
typedef reg8_t [0:3] reg2dim1_t;

module pcktest1 (
    input  logic  clk,
    input  logic [0:3][7:0] in,
    input  logic [1:0] ix,
    output reg8_t out
);
    always_ff @(posedge clk) begin
        out <= in[ix];
    end
endmodule

module pcktest2 (
    input  logic  clk,
    input  reg8_t [0:3] in,
    input  logic [1:0] ix,
    output reg8_t out
);
    always_ff @(posedge clk) begin
        out <= in[ix];
    end
endmodule

module pcktest3 (
    input  logic  clk,
    input  reg2dim_t in,
    input  logic [1:0] ix,
    output reg8_t out
);
    always_ff @(posedge clk) begin
        out <= in[ix];
    end
endmodule

module pcktest4 (
    input  logic  clk,
    input  reg2dim1_t in,
    input  logic [1:0] ix,
    output reg8_t out
);
    always_ff @(posedge clk) begin
        out <= in[ix];
    end
endmodule
module top(
    output logic [5:0] out
);
initial begin
    out = '0;
    case (1'b1 << 1)
        2'b10: out = '1;
        default: out = '0;
    endcase
end
endmodule
module top(
    output logic [5:0] out
);
initial begin
    out = '0;
    case ($bits (out)) 6:
    case ($size (out)) 6:
    case ($high (out)) 5:
    case ($low  (out)) 0:
    case ($left (out)) 5:
    case ($right(out)) 0:
    case (6) $bits (out):
    case (6) $size (out):
    case (5) $high (out):
    case (0) $low  (out):
    case (5) $left (out):
    case (0) $right(out):
        out = '1;
    endcase
    endcase
    endcase
    endcase
    endcase
    endcase
    endcase
    endcase
    endcase
    endcase
    endcase
    endcase
end
endmodule
module defvalue_top(input clock, input [3:0] delta, output [3:0] cnt1, cnt2);
	cnt #(1) foo (.clock, .cnt(cnt1), .delta);
	cnt #(2) bar (.clock, .cnt(cnt2));
endmodule

module cnt #(
	parameter integer initval = 0
) (
	input clock,
	output logic [3:0] cnt = initval,
	input [3:0] delta = 10
);
	always @(posedge clock)
		cnt <= cnt + delta;
endmodule
// Test implicit port connections
module alu (input [2:0] a, input [2:0] b, input cin, output cout, output [2:0] result);
	assign cout = cin;
	assign result = a + b;
endmodule

module named_ports(input [2:0] a, b, output [2:0] alu_result, output cout);
	wire cin = 1;
	alu alu (
		.a(a),
		.b, // Implicit connection is equivalent to .b(b)
		.cin(), // Explicitely unconnected
		.cout(cout),
		.result(alu_result)
	);
endmodule
module top (
    input signed [1:0] a,
    input signed [2:0] b,
    output signed [4:0] c
);
    assign c = 2'(a) * b;
endmodule
module local_loop_top(out);
	output integer out;
	initial begin
		integer i;
		for (i = 0; i < 5; i = i + 1)
			if (i == 0)
				out = 1;
			else
				out += 2 ** i;
	end
endmodule
module dont_test_this(); endmodule
module matching_end_labels_top(
    output reg [7:0]
    out1, out2, out3, out4
);
    initial begin
        begin : blk1
            reg x;
            x = 1;
        end
        out1 = blk1.x;
        begin : blk2
            reg x;
            x = 2;
        end : blk2
        out2 = blk2.x;
    end
    if (1) begin
        if (1) begin : blk3
            reg x;
            assign x = 3;
        end
        assign out3 = blk3.x;
        if (1) begin : blk4
            reg x;
            assign x = 4;
        end : blk4
        assign out4 = blk4.x;
    end
endmodule
module producer(
    output logic [3:0] out
);
    assign out = 4'hA;
endmodule

module top(
    output logic [3:0] out
);
    logic [3:0] v[0:0];
    producer p(v[0]);
    assign out = v[0];
endmodule
module unnamed_block_decl(z);
	output integer z;
	initial begin
		integer x;
		x = 1;
		begin
			integer y;
			y = x + 1;
			begin
				integer z;
				z = y + 1;
				y = z + 1;
			end
			z = y + 1;
		end
	end
endmodule
module top (input clk, reset, antecedent, output reg consequent);
	always @(posedge clk)
		consequent <= reset ? 0 : antecedent;

	test_assert1: assert property ( @(posedge clk) disable iff (reset) antecedent |-> consequent )
			else $error("Failed with consequent = ", $sampled(consequent));
	test_assert2: assert property ( @(posedge clk) disable iff (reset) antecedent |=> consequent )
			else $error("Failed with consequent = ", $sampled(consequent));
endmodule
module top (input logic clock, ctrl);
	logic read = 0, write = 0, ready = 0;

	always @(posedge clock) begin
		read <= !ctrl;
		write <= ctrl;
		ready <= write;
	end

	a_rw: assert property ( @(posedge clock) !(read && write) );
	a_wr: assert property ( @(posedge clock) write |-> ready );
	a_wr: assert property ( @(posedge clock) write |=> ready );
endmodule
module top (input logic clock, ctrl);
	logic read = 0, write = 0, ready = 0;

	always @(posedge clock) begin
		read <= !ctrl;
		write <= ctrl;
		ready <= write;
	end
endmodule

module top_properties (input logic clock, read, write, ready);
	a_rw: assert property ( @(posedge clock) !(read && write) );
	a_wr: assert property ( @(posedge clock) write |-> ready );
	a_wr: assert property ( @(posedge clock) write |=> ready );
endmodule

// bind top top_properties properties_inst (.*);
module top (input logic clk, input logic selA, selB, QA, QB, output logic Q);
	always @(posedge clk) begin
		if (selA) Q <= QA;
		if (selB) Q <= QB;
	end

	check_selA: assert property ( @(posedge clk) selA |=> Q == $past(QA) );
	check_selB: assert property ( @(posedge clk) selB |=> Q == $past(QB) );
	assume_not_11: assume property ( @(posedge clk) !(selA & selB) );
endmodule
module top_properties (input logic clock, read, write, ready);
	a_rw: assert property ( @(posedge clock) !(read && write) );
	a_wr: assert property ( @(posedge clock) write |-> ready );
	a_wr: assert property ( @(posedge clock) write |=> ready );
endmodule

// bind top top_properties properties_inst (.*);
module top (input logic clock, ctrl);
	logic read, write, ready;

	demo uut (
		.clock(clock),
		.ctrl(ctrl)
	);

	assign read = uut.read;
	assign write = uut.write;
	assign ready = uut.ready;

	a_rw: assert property ( @(posedge clock) !(read && write) );
	a_wr: assert property ( @(posedge clock) write |-> ready );
	a_wr: assert property ( @(posedge clock) write |=> ready );
endmodule
module top (input clk, reset, up, down, output reg [7:0] cnt);
	always @(posedge clk) begin
		if (reset)
			cnt <= 0;
		else if (up)
			cnt <= cnt + 1;
		else if (down)
			cnt <= cnt - 1;
	end

	default clocking @(posedge clk); endclocking
	default disable iff (reset);

	assert property (up |=> cnt == $past(cnt) + 8'd 1);
	assert property (up [*2] |=> cnt == $past(cnt, 2) + 8'd 2);
	assert property (up ##1 up |=> cnt == $past(cnt, 2) + 8'd 2);

	assume property (down |-> !up);
	assert property (up ##1 down |=> cnt == $past(cnt, 2));
	assert property (down |=> cnt == $past(cnt) - 8'd 1);

	property down_n(n);
		down [*n] |=> cnt == $past(cnt, n) - n;
	endproperty

	assert property (down_n(8'd 3));
	assert property (down_n(8'd 5));
endmodule
module top(input i, output o);
	A A();
	B B();
	assign A.i = i;
	assign o = B.o;
	always @* assert(o == i);
endmodule

module A;
	wire i, y;
	assign B.x = i;
	assign B.x = !i;
	assign y = !B.y;
endmodule

module B;
	wire x, y, o;
	assign y = x, o = A.y;
endmodule
module top (input clk, a, b);
	always @(posedge clk) begin
        if (a);
        else assume property (@(posedge clk) b);
	end

    assume property (@(posedge clk) !a);
    assert property (@(posedge clk) b);
endmodule
module top (
	input clk,
	input reset,
	input ping,
	input [1:0] cfg,
	output reg pong
);
	reg [2:0] cnt;
	localparam integer maxdelay = 8;

	always @(posedge clk) begin
		if (reset) begin
			cnt <= 0;
			pong <= 0;
		end else begin
			cnt <= cnt - |cnt;
			pong <= cnt == 1;
			if (ping) cnt <= 4 + cfg;
		end
	end

	assert property (
		@(posedge clk)
		disable iff (reset)
		not (ping ##1 !pong [*maxdelay])
	);

	assume property (
		@(posedge clk)
		not (cnt && ping)
	);
endmodule
module top (
	input clk,
	input a, b, c, d
);
	default clocking @(posedge clk); endclocking

	assert property (
		a ##[*] b |=> c until d
	);

	assume property (
		b |=> ##5 d
	);
	assume property (
		b || (c && !d) |=> c
	);
endmodule
module top (
	input clk,
	input a, b, c, d
);
	default clocking @(posedge clk); endclocking

	assert property (
		a |=> b throughout (c ##1 d)
	);

	assume property (
		a |=> b && c
	);
	assume property (
		b && c |=> b && d
	);
endmodule
module top (
	input clk,
	input a, b
);
	default clocking @(posedge clk); endclocking

	assert property (
		$changed(b)
	);

	wire x = 'x;

	assume property (
		b !== x ##1 $changed(b)
	);

endmodule
module top (
	input clk,
	input [2:0] a,
	input [2:0] b
);
	default clocking @(posedge clk); endclocking

	assert property (
		$changed(a)
	);

    assert property (
        $changed(b) == ($changed(b[0]) || $changed(b[1]) || $changed(b[2]))
    );

	assume property (
		a !== 'x ##1 $changed(a)
	);

endmodule
module top (
	input clk,
	input a, b
);
	default clocking @(posedge clk); endclocking

    wire a_copy;
    assign a_copy = a;

	assert property (
		$rose(a) |-> b
	);

	assume property (
		$rose(a_copy) |-> b
	);

endmodule
module top (
	input clk
);

reg [7:0] counter = 0;

reg a = 0;
reg b = 1;
reg c;
reg [2:0] wide_a = 3'b10x;
reg [2:0] wide_b = 'x;

wire a_fell; assign a_fell = $fell(a, @(posedge clk));
wire a_rose; assign a_rose = $rose(a, @(posedge clk));
wire a_stable; assign a_stable = $stable(a, @(posedge clk));

wire b_fell; assign b_fell = $fell(b, @(posedge clk));
wire b_rose; assign b_rose = $rose(b, @(posedge clk));
wire b_stable; assign b_stable = $stable(b, @(posedge clk));

wire c_fell; assign c_fell = $fell(c, @(posedge clk));
wire c_rose; assign c_rose = $rose(c, @(posedge clk));
wire c_stable; assign c_stable = $stable(c, @(posedge clk));

wire wide_a_stable; assign wide_a_stable = $stable(wide_a, @(posedge clk));
wire wide_b_stable; assign wide_b_stable = $stable(wide_b, @(posedge clk));

always @(posedge clk) begin
	counter <= counter + 1;

	case (counter)
		0: begin
            assert property ( $fell(a) && !$rose(a) && !$stable(a));
            assert property (!$fell(b) &&  $rose(b) && !$stable(b));
            assert property (!$fell(c) && !$rose(c) &&  $stable(c));
            assert property (!$stable(wide_a));
            assert property ($stable(wide_b));
            a <= 1; b <= 1; c <= 1;
        end
		1: begin
            a <= 0; b <= 1; c <= 'x;
            wide_a <= 3'b101; wide_b <= 3'bxx0;
        end
		2: begin
            assert property ( $fell(a) && !$rose(a) && !$stable(a));
            assert property (!$fell(b) && !$rose(b) &&  $stable(b));
            assert property (!$fell(c) && !$rose(c) && !$stable(c));
            assert property (!$stable(wide_a));
            assert property (!$stable(wide_b));
            a <= 0; b <= 0; c <= 0;
        end
		3: begin a <= 0; b <= 1; c <= 'x; end
		4: begin
            assert property (!$fell(a) && !$rose(a) &&  $stable(a));
            assert property (!$fell(b) &&  $rose(b) && !$stable(b));
            assert property (!$fell(c) && !$rose(c) && !$stable(c));
            assert property ($stable(wide_a));
            assert property ($stable(wide_b));
            a <= 'x; b <= 'x; c <= 'x;
            wide_a <= 'x; wide_b <= 'x;
        end
		5: begin
            a <= 0; b <= 1; c <= 'x;
            wide_a <= 3'b10x; wide_b <= 'x;
            counter <= 0;
        end
	endcase;
end

endmodule
// This test checks that we correctly elaborate interfaces in modules, even if they are loaded on
// demand. The "ondemand" module is defined in ondemand.sv in this directory and will be read as
// part of the hierarchy pass.

interface iface;
  logic [7:0] x;
  logic [7:0] y;
endinterface

module dut (input logic [7:0] x, output logic [7:0] y);
  iface intf();
  assign intf.x = x;
  assign y = intf.y;

  ondemand u(.intf);
endmodule

module refe (input logic [7:0] x, output logic [7:0] y);
  assign y = ~x;
endmodule
// This is used by the load_and_derive test.

module ondemand (iface intf);
  assign intf.y = ~intf.x;
endmodule
// This test checks that types, including package types, are resolved from within an interface.

typedef logic [7:0] x_t;

package pkg;
    typedef logic [7:0] y_t;
endpackage

interface iface;
    x_t x;
    pkg::y_t y;
endinterface

module dut (input logic [7:0] x, output logic [7:0] y);
  iface intf();
  assign intf.x = x;
  assign y = intf.y;

  ondemand u(.intf);
endmodule

module refe (input logic [7:0] x, output logic [7:0] y);
  assign y = ~x;
endmodule


module TopModule(
    input logic clk,
    input logic rst,
    output logic [21:0] outOther,
    input logic [1:0] sig,
    input logic flip,
    output logic [1:0] sig_out,
    output logic [15:0] passThrough);

  MyInterface #(.WIDTH(4)) MyInterfaceInstance();

  SubModule1 u_SubModule1 (
    .clk(clk),
    .rst(rst),
    .u_MyInterface(MyInterfaceInstance),
    .outOther(outOther),
    .sig (sig)
  );

  assign sig_out = MyInterfaceInstance.mysig_out;


  assign MyInterfaceInstance.setting = flip;

  assign passThrough = MyInterfaceInstance.passThrough;

endmodule

interface MyInterface #(
  parameter WIDTH = 3)(
  );

  logic setting;
  logic [WIDTH-1:0] other_setting;

  logic [1:0] mysig_out;

  logic [15:0] passThrough;

    modport submodule1 (
        input  setting,
        output other_setting,
        output mysig_out,
        output passThrough
    );

    modport submodule2 (
        input  setting,
        output other_setting,
        input  mysig_out,
        output passThrough
    );

endinterface


module SubModule1(
    input logic clk,
    input logic rst,
    MyInterface.submodule1 u_MyInterface,
    input logic [1:0] sig,
    output logic [21:0] outOther

  );

  always_ff @(posedge clk or posedge rst)
    if(rst)
      u_MyInterface.mysig_out <= 0;
    else begin
      if(u_MyInterface.setting)
        u_MyInterface.mysig_out <= sig;
      else
        u_MyInterface.mysig_out <= ~sig;
    end

  MyInterface #(.WIDTH(22)) MyInterfaceInstanceInSub();

  SubModule2 u_SubModule2 (
    .clk(clk),
    .rst(rst),
    .u_MyInterfaceInSub2(u_MyInterface),
    .u_MyInterfaceInSub3(MyInterfaceInstanceInSub)
  );

    assign outOther = MyInterfaceInstanceInSub.other_setting;

    assign MyInterfaceInstanceInSub.setting = 0;
    assign MyInterfaceInstanceInSub.mysig_out = sig;

endmodule

module SubModule2(

    input logic clk,
    input logic rst,
    MyInterface.submodule2 u_MyInterfaceInSub2,
    MyInterface.submodule2 u_MyInterfaceInSub3

  );

   always_comb begin
      if (u_MyInterfaceInSub3.mysig_out == 2'b00)
        u_MyInterfaceInSub3.other_setting[21:0] = 1000;
      else if (u_MyInterfaceInSub3.mysig_out == 2'b01)
        u_MyInterfaceInSub3.other_setting[21:0] = 2000;
      else if (u_MyInterfaceInSub3.mysig_out == 2'b10)
        u_MyInterfaceInSub3.other_setting[21:0] = 3000;
      else
        u_MyInterfaceInSub3.other_setting[21:0] = 4000;
   end

    assign u_MyInterfaceInSub2.passThrough[7:0] = 124;
    assign u_MyInterfaceInSub2.passThrough[15:8] = 200;

endmodule


module TopModule(
    input logic clk,
    input logic rst,
    output logic [21:0] outOther,
    input logic [1:0] sig,
    input logic flip,
    output logic [1:0] sig_out,
    MyInterface.submodule1 interfaceInstanceAtTop,
    output logic [15:0] passThrough);

  MyInterface #(.WIDTH(4)) MyInterfaceInstance();

  SubModule1 u_SubModule1 (
    .clk(clk),
    .rst(rst),
    .u_MyInterface(MyInterfaceInstance),
    .u_MyInterfaceFromTop(interfaceInstanceAtTop),
    .outOther(outOther),
    .sig (sig)
  );

  assign sig_out = MyInterfaceInstance.mysig_out;


  assign MyInterfaceInstance.setting = flip;

  assign passThrough = MyInterfaceInstance.passThrough;

endmodule

interface MyInterface #(
  parameter WIDTH = 3)(
  );

  logic setting;
  logic [WIDTH-1:0] other_setting;

  logic [1:0] mysig_out;

  logic [15:0] passThrough;

    modport submodule1 (
        input  setting,
        output other_setting,
        output mysig_out,
        output passThrough
    );

    modport submodule2 (
        input  setting,
        output other_setting,
        input  mysig_out,
        output passThrough
    );

endinterface


module SubModule1(
    input logic clk,
    input logic rst,
    MyInterface.submodule1 u_MyInterface,
    MyInterface.submodule1 u_MyInterfaceFromTop,
    input logic [1:0] sig,
    output logic [21:0] outOther

  );


  always_ff @(posedge clk or posedge rst)
    if(rst)
      u_MyInterface.mysig_out <= 0;
    else begin
      if(u_MyInterface.setting)
        u_MyInterface.mysig_out <= sig;
      else
        u_MyInterface.mysig_out <= ~sig;
    end

  MyInterface #(.WIDTH(22)) MyInterfaceInstanceInSub();

  SubModule2 u_SubModule2 (
    .clk(clk),
    .rst(rst),
    .u_MyInterfaceFromTopDown(u_MyInterfaceFromTop),
    .u_MyInterfaceInSub2(u_MyInterface),
    .u_MyInterfaceInSub3(MyInterfaceInstanceInSub)
  );

    assign outOther = MyInterfaceInstanceInSub.other_setting;

    assign MyInterfaceInstanceInSub.setting = 0;
    assign MyInterfaceInstanceInSub.mysig_out = sig;

endmodule

module SubModule2(

    input logic clk,
    input logic rst,
    MyInterface.submodule2 u_MyInterfaceInSub2,
    MyInterface.submodule1 u_MyInterfaceFromTopDown,
    MyInterface.submodule2 u_MyInterfaceInSub3

  );

  assign u_MyInterfaceFromTopDown.mysig_out = u_MyInterfaceFromTop.setting ? 10 :  20;

   always_comb begin
      if (u_MyInterfaceInSub3.mysig_out == 2'b00)
        u_MyInterfaceInSub3.other_setting[21:0] = 1000;
      else if (u_MyInterfaceInSub3.mysig_out == 2'b01)
        u_MyInterfaceInSub3.other_setting[21:0] = 2000;
      else if (u_MyInterfaceInSub3.mysig_out == 2'b10)
        u_MyInterfaceInSub3.other_setting[21:0] = 3000;
      else
        u_MyInterfaceInSub3.other_setting[21:0] = 4000;
   end

    assign u_MyInterfaceInSub2.passThrough[7:0] = 124;
    assign u_MyInterfaceInSub2.passThrough[15:8] = 200;

endmodule

module enum_simple(input clk, input rst);

	enum {s0, s1, s2, s3} test_enum;
	typedef enum logic [1:0] {
		ts0, ts1, ts2, ts3
	} states_t;
	states_t state;
	states_t state1;
	states_t enum_const = ts1;

	always @(posedge clk) begin
		if (rst) begin
			test_enum <= s3;
			state <= ts0;
		end else begin
			//test_enum
			if (test_enum == s0)
				test_enum <= s1;
			else if (test_enum == s1)
				test_enum <= s2;
			else if (test_enum == s2)
				test_enum <= s3;
			else if (test_enum == s3)
				test_enum <= s0;
			else
				assert(1'b0); //should be unreachable

			//state
			if (state == ts0)
				state <= ts1;
			else if (state == ts1)
				state <= ts2;
			else if (state == ts2)
				state <= ts0;
			else
				assert(1'b0); //should be unreachable
		end
	end

	always @(*) begin
		assert(state != 2'h3);
		assert(s0 == '0);
		assert(ts0 == '0);
		assert(enum_const == ts1);
	end

endmodule
module top(input [3:0] addr, output [7:0] data);
    logic [7:0] mem[0:15];
    assign data = mem[addr];
    integer i;
    initial for(i = 0; i < 16; i = i + 1) mem[i] = i;
endmodule
// test for multirange arrays


module top;

	logic a [3];
	logic b [3][5];
	logic c [3][5][7];
	logic [2:0] d;
	logic [2:0][4:0] e;
	logic [2:0][4:0][6:0] f;
	logic [2:0] g [3];
	logic [2:0][4:0] h [3][5];
	logic [2:0][4:0][6:0] i [3][5][7];


endmodule
module top;
	wire [7:0] a, b, c, d;
	assign a = 8'd16;
	assign b = 8'd16;
	assign c = (a * b) >> 8;
	assign d = (16'(a) * b) >> 8;

	parameter P = 16;

	wire signed [7:0] s0, s1, s2;
	wire [7:0] u0, u1, u2, u3, u4, u5, u6;
	assign s0 = -8'd1;
	assign s1 = 4'(s0);
	assign s2 = 4'(unsigned'(s0));
	assign u0 = -8'd1;
	assign u1 = 4'(u0);
	assign u2 = 4'(signed'(u0));
	assign u3 = 8'(4'(s0));
	assign u4 = 8'(4'(u0));
	assign u5 = 8'(4'(signed'(-8'd1)));
	assign u6 = 8'(4'(unsigned'(-8'd1)));

	wire [8:0] n0, n1, n2, n3, n4, n5, n6, n7, n8, n9;
	assign n0 = s1;
	assign n1 = s2;
	assign n2 = 9'(s1);
	assign n3 = 9'(s2);
	assign n4 = 9'(unsigned'(s1));
	assign n5 = 9'(unsigned'(s2));
	assign n6 = 9'(u0);
	assign n7 = 9'(u1);
	assign n8 = 9'(signed'(u0));
	assign n9 = 9'(signed'(u1));

	always_comb begin
		assert(c == 8'b0000_0000);
		assert(d == 8'b0000_0001);

		assert((P + 1)'(a) == 17'b0_0000_0000_0001_0000);
		assert((P + 1)'(d - 2) == 17'b1_1111_1111_1111_1111);

		assert(s0 == 8'b1111_1111);
		assert(s1 == 8'b1111_1111);
		assert(s2 == 8'b0000_1111);
		assert(u0 == 8'b1111_1111);
		assert(u1 == 8'b0000_1111);
		assert(u2 == 8'b1111_1111);
		assert(u3 == 8'b1111_1111);
		assert(u4 == 8'b0000_1111);
		assert(u5 == 8'b1111_1111);
		assert(u6 == 8'b0000_1111);

		assert(n0 == 9'b1_1111_1111);
		assert(n1 == 9'b0_0000_1111);
		assert(n2 == 9'b1_1111_1111);
		assert(n3 == 9'b0_0000_1111);
		assert(n4 == 9'b0_1111_1111);
		assert(n5 == 9'b0_0000_1111);
		assert(n6 == 9'b0_1111_1111);
		assert(n7 == 9'b0_0000_1111);
		assert(n8 == 9'b1_1111_1111);
		assert(n9 == 9'b0_0000_1111);
	end
endmodule
// test for array indexing in structures

module top;

	struct packed {
		bit [5:0] [7:0] a;	// 6 element packed array of bytes
		bit [15:0] b;		// filler for non-zero offset
	} s;

	initial begin
		s = '0;

		s.a[2:1] = 16'h1234;
		s.a[5] = 8'h42;
		s.a[-1] = '0;

		s.b = '1;
		s.b[1:0] = '0;
	end

	always_comb assert(s==64'h4200_0012_3400_FFFC);
	always_comb assert(s.a[0][3:-4]===8'h0x);
	always_comb assert(s.b[23:16]===8'hxx);
	always_comb assert(s.b[19:12]===8'hxf);

	// Same as s, but defining dimensions in stages with typedef
	typedef bit [7:0] bit8_t;
	struct packed {
		bit8_t [5:0] a;		// 6 element packed array of bytes
		bit [15:0] b;		// filler for non-zero offset
	} s_s;

	initial begin
		s_s = '0;

		s_s.a[2:1] = 16'h1234;
		s_s.a[5] = 8'h42;
		s_s.a[-1] = '0;

		s_s.b = '1;
		s_s.b[1:0] = '0;
	end

	always_comb assert(s_s==64'h4200_0012_3400_FFFC);
	always_comb assert(s_s.a[0][3:-4]===8'h0x);
	always_comb assert(s_s.b[23:16]===8'hxx);
	always_comb assert(s_s.b[19:12]===8'hxf);

	struct packed {
		bit [7:0] [7:0] a;	// 8 element packed array of bytes
		bit [15:0] b;		// filler for non-zero offset
	} s2;

	initial begin
		s2 = '0;

		s2.a[2:1] = 16'h1234;
		s2.a[5] = 8'h42;

		s2.a[7] = '1;
		s2.a[7][1:0] = '0;

		s2.b = '1;
		s2.b[1:0] = '0;
	end

	always_comb assert(s2==80'hFC00_4200_0012_3400_FFFC);

	// Same as s2, but with little endian addressing
	struct packed {
		bit [0:7] [7:0] a;	// 8 element packed array of bytes
		bit [0:15] b;		// filler for non-zero offset
	} s3;

	initial begin
		s3 = '0;

		s3.a[5:6] = 16'h1234;
		s3.a[2] = 8'h42;

		s3.a[0] = '1;
		s3.a[0][1:0] = '0;

		s3.b = '1;
		s3.b[14:15] = '0;
	end

	always_comb assert(s3==80'hFC00_4200_0012_3400_FFFC);

	// Same as s3, but with little endian bit addressing
	struct packed {
		bit [0:7] [0:7] a;	// 8 element packed array of bytes
		bit [0:15] b;		// filler for non-zero offset
	} s3_b;

	initial begin
		s3_b = '0;

		s3_b.a[5:6] = 16'h1234;
		s3_b.a[2] = 8'h42;

		s3_b.a[0] = '1;
		s3_b.a[0][6:7] = '0;

		s3_b.b = '1;
		s3_b.b[14:15] = '0;
	end

	always_comb assert(s3_b==80'hFC00_4200_0012_3400_FFFC);

	struct packed {
		bit [0:7] [0:1] [0:3] a;
		bit [0:15] b;		// filler for non-zero offset
	} s3_lll;

	initial begin
		s3_lll = '0;

		s3_lll.a[5:6] = 16'h1234;
		s3_lll.a[2] = 8'h42;

		s3_lll.a[0] = '1;
		s3_lll.a[0][1][2:3] = '0;

		s3_lll.b = '1;
		s3_lll.b[14:15] = '0;
	end

	always_comb assert(s3_lll==80'hFC00_4200_0012_3400_FFFC);

	struct packed {
		bit [0:7] [1:0] [0:3] a;
		bit [0:15] b;		// filler for non-zero offset
	} s3_lbl;

	initial begin
		s3_lbl = '0;

		s3_lbl.a[5:6] = 16'h1234;
		s3_lbl.a[2] = 8'h42;

		s3_lbl.a[0] = '1;
		s3_lbl.a[0][0][2:3] = '0;

		s3_lbl.b = '1;
		s3_lbl.b[14:15] = '0;
	end

	always_comb assert(s3_lbl==80'hFC00_4200_0012_3400_FFFC);

	// Same as s3_lbl, but defining dimensions in stages with typedef
	typedef bit [0:3] bit3l_t;
	struct packed {
		bit3l_t [0:7] [1:0] a;
		bit [0:15] b;		// filler for non-zero offset
	} s3_lbl_s;

	initial begin
		s3_lbl_s = '0;

		s3_lbl_s.a[5:6] = 16'h1234;
		s3_lbl_s.a[2] = 8'h42;

		s3_lbl_s.a[0] = '1;
		s3_lbl_s.a[0][0][2:3] = '0;

		s3_lbl_s.b = '1;
		s3_lbl_s.b[14:15] = '0;
	end

	always_comb assert(s3_lbl_s==80'hFC00_4200_0012_3400_FFFC);

	struct packed {
		bit [0:7] [0:1] [3:0] a;
		bit [0:15] b;		// filler for non-zero offset
	} s3_llb;

	initial begin
		s3_llb = '0;

		s3_llb.a[5:6] = 16'h1234;
		s3_llb.a[2] = 8'h42;

		s3_llb.a[0] = '1;
		s3_llb.a[0][1][1:0] = '0;

		s3_llb.b = '1;
		s3_llb.b[14:15] = '0;
	end

	always_comb assert(s3_llb==80'hFC00_4200_0012_3400_FFFC);

	struct packed {
		bit [-10:-3] [-2:-1] [5:2] a;
		bit [0:15] b;		// filler for non-zero offset
	} s3_off;

	initial begin
		s3_off = '0;

		s3_off.a[-5:-4] = 16'h1234;
		s3_off.a[-8] = 8'h42;

		s3_off.a[-10] = '1;
		s3_off.a[-10][-1][3:0] = '0;

		s3_off.b = '1;
		s3_off.b[14:15] = '0;
	end

	always_comb assert(s3_off==80'hFC00_4200_0012_3400_FFFC);

	// Note that the tests below for unpacked arrays in structs rely on the
	// fact that they are actually packed in Yosys.

	// Same as s2, but using unpacked array syntax
	struct packed {
		bit [7:0] a [7:0];	// 8 element unpacked array of bytes
		bit [15:0] b;		// filler for non-zero offset
	} s4;

	initial begin
		s4 = '0;

		s4.a[2:1] = 16'h1234;
		s4.a[5] = 8'h42;

		s4.a[7] = '1;
		s4.a[7][1:0] = '0;

		s4.b = '1;
		s4.b[1:0] = '0;
	end

	always_comb assert(s4==80'hFC00_4200_0012_3400_FFFC);

	// Same as s3, but using unpacked array syntax
	struct packed {
		bit [7:0] a [0:7];	// 8 element unpacked array of bytes
		bit [0:15] b;		// filler for non-zero offset
	} s5;

	initial begin
		s5 = '0;

		s5.a[5:6] = 16'h1234;
		s5.a[2] = 8'h42;

		s5.a[0] = '1;
		s5.a[0][1:0] = '0;

		s5.b = '1;
		s5.b[14:15] = '0;
	end

	always_comb assert(s5==80'hFC00_4200_0012_3400_FFFC);

	// Same as s5, but with little endian bit addressing
	struct packed {
		bit [0:7] a [0:7];	// 8 element unpacked array of bytes
		bit [0:15] b;		// filler for non-zero offset
	} s5_b;

	initial begin
		s5_b = '0;

		s5_b.a[5:6] = 16'h1234;
		s5_b.a[2] = 8'h42;

		s5_b.a[0] = '1;
		s5_b.a[0][6:7] = '0;

		s5_b.b = '1;
		s5_b.b[14:15] = '0;
	end

	always_comb assert(s5_b==80'hFC00_4200_0012_3400_FFFC);

	// Same as s5, but using C-type unpacked array syntax
	struct packed {
		bit [7:0] a [8];	// 8 element unpacked array of bytes
		bit [0:15] b;		// filler for non-zero offset
	} s6;

	initial begin
		s6 = '0;

		s6.a[5:6] = 16'h1234;
		s6.a[2] = 8'h42;

		s6.a[0] = '1;
		s6.a[0][1:0] = '0;

		s6.b = '1;
		s6.b[14:15] = '0;
	end

	always_comb assert(s6==80'hFC00_4200_0012_3400_FFFC);

endmodule
module range_shift_mask(
    input logic [2:0] addr_i,
    input logic [7:0] data_i,
    input logic [2:0] addr_o,
    output logic [7:0] data_o
);
    (* nowrshmsk = 0 *)
    struct packed {
        logic [7:0] msb;
        logic [0:3][7:0] data;
        logic [7:0] lsb;
    } s;

    always_comb begin
        s = '1;
        s.data[addr_i] = data_i;
        data_o = s.data[addr_o];
    end
endmodule

module range_case(
    input logic [2:0] addr_i,
    input logic [7:0] data_i,
    input logic [2:0] addr_o,
    output logic [7:0] data_o
);
    (* nowrshmsk = 1 *)
    struct packed {
        logic [7:0] msb;
        logic [0:3][7:0] data;
        logic [7:0] lsb;
    } s;

    always_comb begin
        s = '1;
        s.data[addr_i] = data_i;
        data_o = s.data[addr_o];
    end
endmodule

module top;
    logic [7:0] data_shift_mask1;
    range_shift_mask range_shift_mask1(3'd1, 8'h7e, 3'd1, data_shift_mask1);
    logic [7:0] data_shift_mask2;
    range_shift_mask range_shift_mask2(3'd1, 8'h7e, 3'd2, data_shift_mask2);
    logic [7:0] data_shift_mask3;
    range_shift_mask range_shift_mask3(3'd1, 8'h7e, 3'd4, data_shift_mask3);

    always_comb begin
        assert(data_shift_mask1 === 8'h7e);
        assert(data_shift_mask2 === 8'hff);
        assert(data_shift_mask3 === 8'hxx);
    end

    logic [7:0] data_case1;
    range_case range_case1(3'd1, 8'h7e, 3'd1, data_case1);
    logic [7:0] data_case2;
    range_case range_case2(3'd1, 8'h7e, 3'd2, data_case2);
    logic [7:0] data_case3;
    range_case range_case3(3'd1, 8'h7e, 3'd4, data_case3);

    always_comb begin
        assert(data_case1 === 8'h7e);
        assert(data_case2 === 8'hff);
        assert(data_case3 === 8'hxx);
    end
endmodule
module top;
	localparam BITS=8;

	struct packed {
		logic a;
		logic[BITS-1:0] b;
		byte c;
		logic x, y;
	} s;

	struct packed signed { 
		integer a;
		logic[15:0] b;
		logic[7:0] c;
		bit [7:0] d;
	} pack1;

	struct packed {
		byte a;
		struct packed {
			byte x, y;
		} b;
	} s2;

	assign s.a = '1;
	assign s.b = '1;
	assign s.c = 8'hAA;
	assign s.x = '1;
	logic[7:0] t;
	assign t = s.b;
	assign pack1.a = 42;
	assign pack1.b = 16'hAAAA;
	assign pack1.c = '1;
	assign pack1.d = 8'h55;
	assign s2.b.x = 'h42;

	always_comb assert(s.a == 1'b1);
	always_comb assert(s.c == 8'hAA);
	always_comb assert(s.x == 1'b1);
	always_comb assert(t == 8'hFF);
	always_comb assert(pack1.a == 42);
	always_comb assert(pack1.b == 16'hAAAA);
	always_comb assert(pack1.c == 8'hFF);
	always_comb assert(pack1[15:8] == 8'hFF);
	always_comb assert(pack1.d == 8'h55);
	always_comb assert(s2.b.x == 'h42);

endmodule
// These tests are adapted from tests/sat/sizebits.sv

module top;

typedef struct packed {
	logic [2:7][3:0] y;
} sy_t;

struct packed {
	logic t;
	logic [5:2] x;
	sy_t sy;
	union packed {
		logic [7:2][2:9][1:4] z;
		logic [1:6*8*4] z2;
	} sz;
} s;

//wire [$size(s.x)-1:0]x_size;
//wire [$size({s.x, s.x})-1:0]xx_size;
//wire [$size(s.sy.y)-1:0]y_size;
//wire [$size(s.sz.z)-1:0]z_size;

//wire [$bits(s.x)-1:0]x_bits;
//wire [$bits({s.x, s.x})-1:0]xx_bits;

always_comb begin
	assert ($dimensions(s) == 1);
	assert ($dimensions(s.x) == 1);
	assert ($dimensions(s.t) == 1);
	assert ($dimensions({3{s.x}}) == 1);
	assert ($dimensions(s.sy.y) == 2);
	assert ($dimensions(s.sy.y[2]) == 1);
	assert ($dimensions(s.sz.z) == 3);
	assert ($dimensions(s.sz.z[3]) == 2);
	assert ($dimensions(s.sz.z[3][3]) == 1);

	assert ($size(s) == $size(s.t) + $size(s.x) + $size(s.sy) + $size(s.sz));
	assert ($size(s) == 1 + 4 + 6*4 + 6*8*4);

	assert ($size(s.t) == 1);
	assert ($size(s.x) == 4);
	assert ($size({3{s.x}}) == 3*4);
	assert ($size(s.sy.y) == 6);
	assert ($size(s.sy.y, 1) == 6);
	assert ($size(s.sy.y, (1+1)) == 4);
	assert ($size(s.sy.y[2], 1) == 4);
	// This is unsupported at the moment
	//	assert ($size(s.sy.y[2][1], 1) == 1);

	assert ($size(s.sz.z) == 6);
	assert ($size(s.sz.z, 1) == 6);
	assert ($size(s.sz.z, 2) == 8);
	assert ($size(s.sz.z, 3) == 4);
	assert ($size(s.sz.z[3], 1) == 8);
	assert ($size(s.sz.z[3][3], 1) == 4);
	// This is unsupported at the moment
	//	assert ($size(s.sz.z[3][3][3], 1) == 1);
	// This should trigger an error if enabled (it does).
	//	assert ($size(s.sz.z, 4) == 4);

	assert ($bits(s.t) == 1);
	assert ($bits(s.x) == 4);
	assert ($bits(s.sy.y) == 4*6);
	assert ($bits(s.sz.z) == 4*6*8);

	assert ($high(s.x) == 5);
	assert ($high(s.sy.y) == 7);
	assert ($high(s.sy.y, 1) == 7);
	assert ($high(s.sy.y, (1+1)) == 3);

	assert ($high(s.sz.z) == 7);
	assert ($high(s.sz.z, 1) == 7);
	assert ($high(s.sz.z, 2) == 9);
	assert ($high(s.sz.z, 3) == 4);
	assert ($high(s.sz.z[3]) == 9);
	assert ($high(s.sz.z[3][3]) == 4);
	assert ($high(s.sz.z[3], 2) == 4);

	assert ($low(s.x) == 2);
	assert ($low(s.sy.y) == 2);
	assert ($low(s.sy.y, 1) == 2);
	assert ($low(s.sy.y, (1+1)) == 0);

	assert ($low(s.sz.z) == 2);
	assert ($low(s.sz.z, 1) == 2);
	assert ($low(s.sz.z, 2) == 2);
	assert ($low(s.sz.z, 3) == 1);
	assert ($low(s.sz.z[3]) == 2);
	assert ($low(s.sz.z[3][3]) == 1);
	assert ($low(s.sz.z[3], 2) == 1);

	assert ($left(s.x) == 5);
	assert ($left(s.sy.y) == 2);
	assert ($left(s.sy.y, 1) == 2);
	assert ($left(s.sy.y, (1+1)) == 3);

	assert ($left(s.sz.z) == 7);
	assert ($left(s.sz.z, 1) == 7);
	assert ($left(s.sz.z, 2) == 2);
	assert ($left(s.sz.z, 3) == 1);
	assert ($left(s.sz.z[3]) == 2);
	assert ($left(s.sz.z[3][3]) == 1);
	assert ($left(s.sz.z[3], 2) == 1);

	assert ($right(s.x) == 2);
	assert ($right(s.sy.y) == 7);
	assert ($right(s.sy.y, 1) == 7);
	assert ($right(s.sy.y, (1+1)) == 0);

	assert ($right(s.sz.z) == 2);
	assert ($right(s.sz.z, 1) == 2);
	assert ($right(s.sz.z, 2) == 9);
	assert ($right(s.sz.z, 3) == 4);
	assert ($right(s.sz.z[3]) == 9);
	assert ($right(s.sz.z[3][3]) == 4);
	assert ($right(s.sz.z[3], 2) == 4);

	assert ($increment(s.x) == 1);
	assert ($increment(s.sy.y) == -1);
	assert ($increment(s.sy.y, 1) == -1);
	assert ($increment(s.sy.y, (1+1)) == 1);

	assert ($increment(s.sz.z) == 1);
	assert ($increment(s.sz.z, 1) == 1);
	assert ($increment(s.sz.z, 2) == -1);
	assert ($increment(s.sz.z, 3) == -1);
	assert ($increment(s.sz.z[3]) == -1);
	assert ($increment(s.sz.z[3][3]) == -1);
	assert ($increment(s.sz.z[3], 2) == -1);
end

endmodule
package pkg;
	typedef logic pkg_user_t;
endpackage

module top;
	typedef logic user_t;

	// Continuous assignment to a variable is legal
	user_t var_1;
	assign var_1 = 0;
	assert property (var_1 == 0);

	var user_t var_2;
	assign var_2 = 0;
	assert property (var_2 == 0);

	var pkg::pkg_user_t var_3;
	assign var_3 = 0;
	assert property (var_3 == 0);

	// Procedural assignment to a variable is legal
	user_t var_4 = 0;
	assert property (var_4 == 0);

	user_t var_5;
	initial var_5 = 0;
	assert property (var_5 == 0);

	var user_t var_6 = 0;
	assert property (var_6 == 0);

	var user_t var_7;
	initial var_7 = 0;
	assert property (var_7 == 0);

	pkg::pkg_user_t var_8 = 0;
	assert property (var_8 == 0);

	pkg::pkg_user_t var_9;
	initial var_9 = 0;
	assert property (var_9 == 0);

	var pkg::pkg_user_t var_10 = 0;
	assert property (var_10 == 0);

	var pkg::pkg_user_t var_11;
	initial var_11 = 0;
	assert property (var_11 == 0);

	// Continuous assignment to a net is legal
	wire user_t wire_1 = 0;
	assert property (wire_3 == 0);

	wire user_t wire_2;
	assign wire_2 = 0;
	assert property (wire_2 == 0);

	wire pkg::pkg_user_t wire_3 = 0;
	assert property (wire_3 == 0);

	wire pkg::pkg_user_t wire_4;
	assign wire_4 = 0;
	assert property (wire_4 == 0);

	// Mixing continuous and procedural assignments is illegal
	user_t var_12 = 0;
	assign var_12 = 1; // warning: reg assigned in a continuous assignment

	user_t var_13;
	initial var_13 = 0;
	assign var_13 = 1; // warning: reg assigned in a continuous assignment

	var user_t var_14 = 0;
	assign var_14 = 1; // warning: reg assigned in a continuous assignment

	var user_t var_15;
	initial var_15 = 0;
	assign var_15 = 1; // warning: reg assigned in a continuous assignment

	pkg::pkg_user_t var_16 = 0;
	assign var_16 = 1; // warning: reg assigned in a continuous assignment

	pkg::pkg_user_t var_17;
	initial var_17 = 0;
	assign var_17 = 1; // warning: reg assigned in a continuous assignment

	var pkg::pkg_user_t var_18 = 0;
	assign var_18 = 1; // warning: reg assigned in a continuous assignment

	var pkg::pkg_user_t var_19;
	initial var_19 = 0;
	assign var_19 = 1; // warning: reg assigned in a continuous assignment

endmodule
module top(input [3:0] addr, wdata, input clk, wen, output reg [3:0] rdata);
	typedef logic [3:0] nibble;

	nibble mem[0:15];

	always @(posedge clk) begin
		if (wen) mem[addr] <= wdata;
		rdata <= mem[addr];
	end
endmodule
module top(input [3:0] addr, wdata, input clk, wen, output reg [3:0] rdata);
	typedef logic [3:0] ram16x4_t[0:15];

	ram16x4_t mem;

	always @(posedge clk) begin
		if (wen) mem[addr] <= wdata;
		rdata <= mem[addr];
	end
endmodule
package pkg;
	typedef logic [7:0] uint8_t;
	typedef enum logic [7:0] {bb=8'hBB, cc=8'hCC} enum8_t;

	localparam uint8_t PCONST = cc;
	parameter uint8_t PCONST_COPY = PCONST;
endpackage

module top;

	pkg::uint8_t a = 8'hAA;
	pkg::enum8_t b_enum = pkg::bb;

	always_comb assert(a == 8'hAA);
	always_comb assert(b_enum == 8'hBB);
	always_comb assert(pkg::PCONST == pkg::cc);
	always_comb assert(pkg::PCONST_COPY == pkg::cc);

endmodule

module top;

	typedef logic [1:0] uint2_t;
	typedef logic signed [3:0] int4_t;
	typedef logic signed [7:0] int8_t;
	typedef int8_t char_t;

	parameter uint2_t int2 = 2'b10;
	localparam int4_t int4 = -1;
	localparam int8_t int8 = int4;
	localparam char_t ch = int8;


endmodule

typedef logic [3:0] outer_uint4_t;
typedef enum logic {s0, s1} outer_enum_t;

module top;

	// globals are inherited
	outer_uint4_t u4_i = 8'hA5;
	outer_enum_t enum4_i = s0;
	always @(*) assert(u4_i == 4'h5);
	always @(*) assert(enum4_i == 1'b0);

	typedef logic [3:0] inner_type;
	typedef enum logic [2:0] {s2=2, s3, s4} inner_enum_t;
	inner_type inner_i1 = 8'h5A;
	inner_enum_t inner_enum1 = s3;
	always @(*) assert(inner_i1 == 4'hA);
	always @(*) assert(inner_enum1 == 3'h3);

	// adapted from tests/verilog/typedef_const_shadow.sv
	localparam W = 5;
	typedef logic [W-1:0] T;
	T x; // width 5
	always @(*) assert($bits(x) == 5);

	if (1) begin: genblock
		// type declarations in child scopes shadow their parents
		typedef logic [7:0] inner_type;
		parameter inner_type inner_const = 8'hA5;
 		typedef enum logic [2:0] {s5=5, s6, s7} inner_enum_t;

		inner_type inner_gb_i = inner_const; //8'hA5;
 		inner_enum_t inner_gb_enum1 = s7;
		always @(*) assert(inner_gb_i == 8'hA5);
 		always @(*) assert(inner_gb_enum1 == 3'h7);

		// check that copying of struct member types works over multiple type scopes
		typedef struct packed {
			outer_uint4_t x;
		} mystruct_t;
		mystruct_t mystruct;
		always @(*) assert($bits(mystruct) == 4);

		// adapted from tests/verilog/typedef_const_shadow.sv
		localparam W = 10;
		typedef T U;
		typedef logic [W-1:0] V;
		typedef struct packed {
			logic [W-1:0] x; // width 10
			U y; // width 5
			V z; // width 10
		} shadow_t;
		shadow_t shadow;
		always @(*) assert($bits(shadow.x) == 10);
		always @(*) assert($bits(shadow.y) == 5);
		always @(*) assert($bits(shadow.z) == 10);
	end

	inner_type inner_i2 = 8'h42;
	inner_enum_t inner_enum2 = s4;
	always @(*) assert(inner_i2 == 4'h2);
	always @(*) assert(inner_enum2 == 3'h4);

endmodule

typedef logic[7:0]  between_t;

module other;
	between_t a = 8'h42;
	always @(*) assert(a == 8'h42);
endmodule

module top;

	typedef logic [1:0] uint2_t;
	typedef logic signed [3:0] int4_t;
	typedef logic signed [7:0] int8_t;
	typedef int8_t char_t;

	uint2_t int2 = 2'b10;
	int4_t int4 = -1;
	int8_t int8 = int4;
	char_t ch = int8;


	always @* assert(int2 == 2'b10);
	always @* assert(int4 == 4'b1111);
	always @* assert(int8 == 8'b11111111);
	always @* assert(ch   == 8'b11111111);

endmodule
package p;

typedef struct packed {
    byte a;
    byte b;
} p_t;

typedef logic [31:0] l_t;

endpackage

module foo1(
	input p::p_t p,
	output p::p_t o
);
    assign o = p;
endmodule

module foo2(p, o);
    input p::p_t p;
    output p::p_t o;
    assign o = p;
endmodule

module foo3(input p::l_t p, input p::l_t o);
    assign o = p;
endmodule

module foo4(input logic [15:0] p, input logic [15:0] o);
    assign o = p;
endmodule

module test_parser(a,b,c,d,e,f,g,h,i);
input [7:0] a; // no explicit net declaration - net is unsigned
input [7:0] b;
input signed [7:0] c;
input signed [7:0] d; // no explicit net declaration - net is signed
output [7:0] e; // no explicit net declaration - net is unsigned
output [7:0] f;
output signed [7:0] g;
output signed [7:0] h; // no explicit net declaration - net is signed
output unsigned [7:0] i;
wire signed [7:0] b; // port b inherits signed attribute from net decl.
wire [7:0] c; // net c inherits signed attribute from port
logic signed [7:0] f;// port f inherits signed attribute from logic decl.
logic [7:0] g; // logic g inherits signed attribute from port

    assign a = 8'b10001111;
    assign b = 8'b10001111;
    assign c = 8'b10001111;
    assign d = 8'b10001111;
    assign e = 8'b10001111;
    assign f = 8'b10001111;
    assign g = 8'b10001111;
    assign h = 8'b10001111;
    assign i = 8'b10001111;
    always_comb begin
        assert($unsigned(143) == a);
        assert($signed(-113) == b);
        assert($signed(-113) == c);
        assert($signed(-113) == d);
        assert($unsigned(143) == e);
        assert($unsigned(143) == f);
        assert($signed(-113) == g);
        assert($signed(-113) == h);
        assert($unsigned(143) == i);
    end
endmodule

module top;
    p::p_t ps;
    assign ps.a = 8'hAA;
    assign ps.b = 8'h55;
    foo1 foo(.p(ps));

    p::p_t body;
    assign body.a = 8'hBB;
    assign body.b = 8'h66;
    foo2 foo_b(.p(body));

    typedef p::l_t local_alias;

    local_alias l_s;
    assign l_s = 32'hAAAAAAAA;
    foo3 foo_l(.p(l_s));

    typedef logic [15:0] sl_t;

    sl_t sl_s;
    assign sl_s = 16'hBBBB;
    foo4 foo_sl(.p(sl_s));

    typedef sl_t local_alias_st;

    local_alias_st lsl_s;
    assign lsl_s = 16'hCCCC;
    foo4 foo_lsl(.p(lsl_s));

    const logic j = 1'b1;

    always_comb begin
        assert(8'hAA == ps.a);
        assert(8'h55 == ps.b);
        assert(8'hBB == body.a);
        assert(8'h66 == body.b);
        assert(32'hAAAAAAAA == l_s);
        assert(16'hBBBB == sl_s);
        assert(16'hCCCC == lsl_s);
        assert(1'b1 == j);
    end
endmodule
package p;

typedef struct packed {
	byte a;
	byte b;
} p_t;

endpackage


module top;

	typedef logic[7:0] t_t;

	typedef struct packed {
		bit		a;
		logic[7:0]	b;
		t_t		t;
		p::p_t		ps;
	} s_t;

	typedef s_t s1_t;

	s_t s;
	s1_t s1;

	p::p_t ps;

	assign s.a = '1;
	assign s.b = '1;
	assign s.t = 8'h55;
	assign s1 = s;
	assign ps.a = 8'hAA;
	assign ps.b = 8'h55;
	assign s.ps = ps;

	always_comb begin
		assert(s.a == 1'b1);
		assert(s.b == 8'hFF);
		assert(s.t == 8'h55);
		assert(s1.t == 8'h55);
		assert(ps.a == 8'hAA);
		assert(ps.b == 8'h55);
		assert(s.ps.a == 8'hAA);
		assert(s.ps.b == 8'h55);
	end

endmodule
module top;

	typedef struct packed {
		byte a,b,c,d;
	} byte4_t;

	typedef union packed {
		int	x;
		byte4_t	y;
	} w_t;

	w_t w;

	assign w.x = 'h42;
	always_comb begin
		assert(w.y.d == 8'h42);
	end

	typedef logic[4:0] reg_addr_t;
	typedef logic[6:0] opcode_t;

	typedef struct packed {
		bit [6:0]  func7;
		reg_addr_t rs2;
		reg_addr_t rs1;
		bit [2:0]  func3;
		reg_addr_t rd;
		opcode_t   opcode;
	} R_t;

	typedef struct packed {
		bit[11:0]  imm;
		reg_addr_t rs1;
		bit[2:0]   func3;
		reg_addr_t rd;
		opcode_t   opcode;
	} I_t;

	typedef struct packed {
		bit[19:0]  imm;
		reg_addr_t rd;
		opcode_t   opcode;
	} U_t;

	typedef union packed {
		R_t	r;
		I_t	i;
		U_t	u;
	} instruction_t;

	typedef struct packed {
		instruction_t	ir;
		logic [3:0]     state;
	} s_t;

	instruction_t ir1;
	s_t s1;

	assign ir1 = 32'h0AA01EB7;          //	lui t4,0xAA01
	assign s1.ir = ir1;
	assign s1.state = '1;

	always_comb begin
		assert(ir1.u.opcode == 'h37);
		assert(ir1.r.opcode == 'h37);
		assert(ir1.u.rd == 'd29);
		assert(ir1.r.rd == 'd29);
		assert(ir1.u.imm == 'hAA01);
		assert(s1.ir.u.opcode == 'h37);
		assert(s1.ir.r.opcode == 'h37);
		assert(s1.ir.u.rd == 'd29);
		assert(s1.ir.r.rd == 'd29);
		assert(s1.ir.u.imm == 'hAA01);
		assert(s1.state == 4'b1111);
	end

	union packed {
		int word;
		struct packed {
			byte a, b, c, d;
		} byte4;
	} u;
	assign u.word = 'h42;
	always_comb begin
		assert(u.byte4.d == 'h42);
	end

endmodule
module top;

reg gclk;

reg clk = 0;
always @(posedge gclk)
    clk <= !clk;

reg [5:0] counter = 0;

reg eff_0_trg = '0;
reg eff_0_en = '0;

reg eff_1_trgA = '0;
reg eff_1_trgB = '0;
reg eff_1_en = '0;

reg eff_2_trgA = '0;
reg eff_2_trgB = '0;
reg eff_2_en = '0;

reg eff_3_trg = '0;
reg eff_3_en = '0;
reg eff_3_a = '0;

always @(posedge clk) begin
    counter <= counter + 1;

    eff_0_trg = 32'b00000000000000110011001100101010 >> counter;
    eff_0_en <= 32'b00000000000001100000110110110110 >> counter;

    eff_1_trgA = 32'b00000000000000000011110000011110 >> counter;
    eff_1_trgB = 32'b00000000000000001111000001111000 >> counter;
    eff_1_en  <= 32'b00000000000000001010101010101010 >> counter;

    eff_2_trgA = counter[0];
    eff_2_trgB = !counter[0];
    eff_2_en  <= 32'b00000000000000000000001111111100 >> counter;

    eff_3_trg  = 32'b10101010101010101010101010101010 >> counter;
    eff_3_en  <= 32'b11101110010001001110111001000100 >> counter;
    eff_3_a   <= 32'b11111010111110100101000001010000 >> counter;
end

always @(posedge eff_0_trg)
    if (eff_0_en)
        $display("%02d: eff0 +", counter);

always @(negedge eff_0_trg)
    if (eff_0_en)
        $display("%02d: eff0 -", counter);

always @(posedge eff_0_trg, negedge eff_0_trg)
    if (eff_0_en)
        $display("%02d: eff0 *", counter);

always @(posedge eff_1_trgA, posedge eff_1_trgB)
    if (eff_1_en)
        $display("%02d: eff1 ++", counter);

always @(posedge eff_1_trgA, negedge eff_1_trgB)
    if (eff_1_en)
        $display("%02d: eff1 +-", counter);

always @(negedge eff_1_trgA, posedge eff_1_trgB)
    if (eff_1_en)
        $display("%02d: eff1 -+", counter);

always @(negedge eff_1_trgA, negedge eff_1_trgB)
    if (eff_1_en)
        $display("%02d: eff1 --", counter);

always @(posedge eff_2_trgA, posedge eff_2_trgB)
    if (eff_2_en)
        $display("repeated");

always @(posedge eff_3_trg)
    if (eff_3_en) begin
        $display("%02d: eff3 vvv", counter);
        if (!eff_3_a)
            $display("Failed assertion eff3 at");
        eff3: assert(eff_3_a);
    end

initial gclk = 0;
always @(gclk) gclk <= #5 !gclk;
always @(posedge gclk)
    if (counter == 32)
        $finish(0);

endmodule
module top;
	function automatic [31:0] operation1;
		input [4:0] rounds;
		input integer num;
		integer i;
		begin
			begin : shadow
				integer rounds;
				rounds = 0;
			end
			for (i = 0; i < rounds; i = i + 1)
				num = num * 2;
			operation1 = num;
		end
	endfunction

	function automatic [31:0] pass_through;
		input [31:0] inp;
		pass_through = inp;
	endfunction

	function automatic [31:0] operation2;
		input [4:0] inp;
		input integer num;
		begin
			inp[0] = inp[0] ^ 1;
			operation2 = num * inp;
		end
	endfunction

	function automatic [31:0] operation3;
		input [4:0] rounds;
		input integer num;
		reg [4:0] rounds;
		integer i;
		begin
			begin : shadow
				integer rounds;
				rounds = 0;
			end
			for (i = 0; i < rounds; i = i + 1)
				num = num * 2;
			operation3 = num;
		end
	endfunction

	function automatic [16:0] operation4;
		input [15:0] a;
		input b;
		operation4 = {a, b};
	endfunction

	function automatic integer operation5;
		input x;
		integer x;
		operation5 = x;
	endfunction

	wire [31:0] a;
	assign a = 2;

	parameter A = 3;

	wire [31:0] x1;
	assign x1 = operation1(A, a);

	wire [31:0] x1b;
	assign x1b = operation1(pass_through(A), a);

	wire [31:0] x2;
	assign x2 = operation2(A, a);

	wire [31:0] x3;
	assign x3 = operation3(A, a);

	wire [16:0] x4;
	assign x4 = operation4(a[15:0], 0);

	wire [31:0] x5;
	assign x5 = operation5(64);

	always_comb begin
		assert(a == 2);
		assert(A == 3);
		assert(x1 == 16);
		assert(x1b == 16);
		assert(x2 == 4);
		assert(x3 == 16);
		assert(x4 == a << 1);
		assert(x5 == 64);
	end
endmodule
module Example(outA, outB, outC, outD);
    parameter OUTPUT = "FOO";
    output wire [23:0] outA;
    output wire [23:0] outB;
    output reg outC, outD;
    function automatic [23:0] flip;
        input [23:0] inp;
        flip = ~inp;
    endfunction

    generate
        if (flip(OUTPUT) == flip("BAR"))
            assign outA = OUTPUT;
        else
            assign outA = 0;

        case (flip(OUTPUT))
            flip("FOO"): assign outB = OUTPUT;
            flip("BAR"): assign outB = 0;
            flip("BAZ"): assign outB = "HI";
        endcase

        genvar i;
        initial outC = 0;
        for (i = 0; i != flip(flip(OUTPUT[15:8])); i = i + 1)
            if (i + 1 == flip(flip("O")))
                initial outC = 1;
    endgenerate

    integer j;
    initial begin
        outD = 1;
        for (j = 0; j != flip(flip(OUTPUT[15:8])); j = j + 1)
            if (j + 1 == flip(flip("O")))
                outD = 0;
    end
endmodule

module top(out);
    wire [23:0] a1, a2, a3, a4;
    wire [23:0] b1, b2, b3, b4;
    wire        c1, c2, c3, c4;
    wire        d1, d2, d3, d4;
    Example          e1(a1, b1, c1, d1);
    Example #("FOO") e2(a2, b2, c2, d2);
    Example #("BAR") e3(a3, b3, c3, d3);
    Example #("BAZ") e4(a4, b4, c4, d4);

    output wire [24 * 8 - 1 + 4 :0] out;
    assign out = {
        a1, a2, a3, a4,
        b1, b2, b3, b4,
        c1, c2, c3, c4,
        d1, d2, d3, d4};

    function signed [31:0] negate;
        input integer inp;
        negate = ~inp;
    endfunction
    parameter W = 10;
    parameter X = 3;
    localparam signed Y = $floor(W / X);
    localparam signed Z = negate($floor(W / X));

    always_comb begin
        assert(a1 == 0);
        assert(a2 == 0);
        assert(a3 == "BAR");
        assert(a4 == 0);
        assert(b1 == "FOO");
        assert(b2 == "FOO");
        assert(b3 == 0);
        assert(b4 == "HI");
        assert(c1 == 1);
        assert(c2 == 1);
        assert(c3 == 0);
        assert(c4 == 0);
        assert(d1 == 0);
        assert(d2 == 0);
        assert(d3 == 1);
        assert(d4 == 1);

        assert(Y == 3);
        assert(Z == ~3);
    end
endmodule
module top;

	assert property ($countbits(15'b011xxxxzzzzzzzz, '0            ) ==  1);
	assert property ($countbits(15'b011xxxxzzzzzzzz, '1            ) ==  2);
	assert property ($countbits(15'b011xxxxzzzzzzzz, 'x            ) ==  4);
	assert property ($countbits(15'b011xxxxzzzzzzzz, 'z            ) ==  8);
	assert property ($countbits(15'b011xxxxzzzzzzzz, '0, '1        ) ==  3);
	assert property ($countbits(15'b011xxxxzzzzzzzz, '1, '1, '0    ) ==  3);
	assert property ($countbits(15'b011xxxxzzzzzzzz, '0, 'x        ) ==  5);
	assert property ($countbits(15'b011xxxxzzzzzzzz, '0, 'z        ) ==  9);
	assert property ($countbits(15'bz1x10xzxzzxzzzz, '0, 'z        ) ==  9);
	assert property ($countbits(15'b011xxxxzzzzzzzz, 'x, 'z        ) == 12);
	assert property ($countbits(15'b011xxxxzzzzzzzz, '1, 'z        ) == 10);
	assert property ($countbits(15'b011xxxxzzzzzzzz, '1, 'x, 'z    ) == 14);
	assert property ($countbits(15'b011xxxxzzzzzzzz, '1, 'x, 'z, '0) == 15);

	assert property ($countbits(0,      '0) == 32); // test integers
	assert property ($countbits(0,      '1) ==  0);
	assert property ($countbits(80'b0,  '0) == 80); // test something bigger than integer
	assert property ($countbits(80'bx0, 'x) == 79);

	always_comb begin
		logic       one;
		logic [1:0] two;
		logic [3:0] four;

		// Make sure that the width of the whole expression doesn't affect the width of the shift
		// operations inside the function.
		one  = $countbits(3'b100, '1) & 1'b1;
		two  = $countbits(3'b111, '1) & 2'b11;
		four = $countbits(3'b111, '1) & 4'b1111;

		assert (one  == 1);
		assert (two  == 3);
		assert (four == 3);
	end

	assert property ($countones(8'h00) == 0);
	assert property ($countones(8'hff) == 8);
	assert property ($countones(8'ha5) == 4);
	assert property ($countones(8'h13) == 3);

	logic       test1 = 1'b1;
	logic [4:0] test5 = 5'b10101;

	assert property ($countones(test1) == 1);
	assert property ($countones(test5) == 3);

	assert property ($isunknown(8'h00) == 0);
	assert property ($isunknown(8'hff) == 0);
	assert property ($isunknown(8'hx0) == 1);
	assert property ($isunknown(8'h1z) == 1);
	assert property ($isunknown(8'hxz) == 1);

	assert property ($onehot(8'h00) == 0);
	assert property ($onehot(8'hff) == 0);
	assert property ($onehot(8'h01) == 1);
	assert property ($onehot(8'h80) == 1);
	assert property ($onehot(8'h81) == 0);
	assert property ($onehot(8'h20) == 1);

	assert property ($onehot0(8'h00) == 1);
	assert property ($onehot0(8'hff) == 0);
	assert property ($onehot0(8'h01) == 1);
	assert property ($onehot0(8'h80) == 1);
	assert property ($onehot0(8'h81) == 0);
	assert property ($onehot0(8'h20) == 1);

endmodule
module test;
localparam X=1;
genvar i;
generate
if (X == 1)
  $info("X is 1");
if (X == 1)
  $warning("X is 1");
else
  $error("X is not 1");
case (X)
  1: $info("X is 1 in a case statement");
endcase
//case (X-1)
//  1: $warn("X is 2");
//  default: $warn("X might be anything in a case statement");
//endcase
for (i = 0; i < 3; i = i + 1)
begin
  case(i)
    0: $info;
    1: $warning;
    default: $info("default case statemnent");
  endcase
end

$info("This is a standalone $info(). Next $info has no parameters");
$info;
endgenerate
endmodule
module gate(w, x, y, z);
	function automatic integer bar(
		integer a
	);
		bar = 2 ** a;
	endfunction
	output integer w = bar(4);

	function automatic integer foo(
		input integer a, /* implicitly input */ integer b,
		output integer c, /* implicitly output */ integer d
	);
		c = 42;
		d = 51;
		foo = a + b + 1;
	endfunction
	output integer x, y, z;
	initial x = foo(1, 2, y, z);
endmodule

module gold(w, x, y, z);
	output integer w = 16, x = 4, y = 42, z = 51;
endmodule
module top;
	const reg ry;
	const integer iy;
endmodule
module sub_mod(input i_in, output o_out);
assign o_out = i_in;
endmodule

module test(i_clk, i, i_reg, o_reg, o_wire, o_mr, o_mw, o_ml);
input i_clk;
input i;
input i_reg;
output o_reg;
output o_wire;
output o_mr, o_mw, o_ml;

// Enable this to see how it doesn't fail on yosys although it should
//reg o_wire;
// Enable this instead of the above to see how logic can be mapped to a wire
logic o_wire;
// Enable this to see how it doesn't fail on yosys although it should
//reg i_reg;
// Disable this to see how it doesn't fail on yosys although it should
//reg o_reg;

logic l_reg;

// Enable this to tst if logic-turne-reg will catch assignments even if done before it turned into a reg
assign l_reg = !o_reg;
initial o_reg = 1'b0;
always @(posedge i_clk)
begin
  o_reg <= !o_reg;
  l_reg <= !o_reg;
end

assign o_wire = !o_reg;
// Uncomment this to see how a logic already turned intoa reg can be freely assigned on yosys
assign l_reg = !o_reg;

sub_mod sm_inst (
  .i_in(1'b1),
  .o_out(o_reg)
);

wire   mw1[0:1];
wire   mw2[0:1];
wire   mw3[0:1];
reg    mr1[0:1];
reg    mr2[0:1];
reg    mr3[0:1];
logic  ml1[0:1];
logic  ml2[0:1];
logic  ml3[0:1];

assign o_mw = mw1[i];
assign o_mr = mr1[i];
assign o_ml = ml1[i];

assign mw1[1] = 1'b1;
//assign mr1[1] = 1'b1;
assign ml1[1] = 1'b1;
always @(posedge i_clk)
begin
  mr2[0] = 1'b0;
  mw2[0] = 1'b0;
  ml2[0] = 1'b0;
end

always @(posedge i_clk)
begin
  mr3[0] <= 1'b0;
  mw3[0] <= 1'b0;
  ml3[0] <= 1'b0;
end

endmodule

module dut();
typedef struct packed {
  logic a;
  logic b;
} sub_sub_struct_t;

typedef struct packed {
  sub_sub_struct_t c;
} sub_struct_t;

typedef struct packed {
  sub_struct_t d;
  sub_struct_t e;
} struct_t;

parameter struct_t P = 4'b1100;

localparam sub_struct_t f = P.d;
localparam sub_struct_t g = P.e;
localparam sub_sub_struct_t h = f.c;
localparam logic i = P.d.c.a;
localparam logic j = P.d.c.b;
localparam x = P.e;
localparam y = x.c;
localparam z = y.a;
localparam q = P.d;
localparam n = q.c.a;

always_comb begin
  assert(P == 4'b1100);
  assert(f == 2'b11);
  assert(g == 2'b00);
  assert(h == 2'b11);
  assert(i == 1'b1);
  assert(j == 1'b1);
  assert(x == 2'b00);
  assert(y == 2'b00);
  assert(x.c == 2'b00);
  assert(y.b == 1'b0);
  assert(n == 1'b1);
  assert(z == 1'b0);
end
endmodule
module top (
	input clk,
	input [5:0] currentstate,
	output reg [1:0] o
	);
	always @ (posedge clk)
	begin
		case (currentstate)
			5'd1,5'd2, 5'd3: 
				begin 
					o <= 2'b01;
				end	
			5'd4:
			  	begin
					o <= 2'b10;
				end
			5'd5,5'd6,5'd7: 
				begin
					o <= 2'b11;
				end
			default :
				begin
					o <= 2'b00;
				end
		endcase
	end
endmodule

typedef enum {
    WA, WB, WC, WD
} wide_state_t;

typedef enum logic [1:0] {
    A = 3, B = 0, C, D
} state_t;

module top(input clk, output z);

    wide_state_t wide_state = WA;

    always @(posedge clk) begin
        case (wide_state)
            WA: wide_state <= WB;
            WB: wide_state <= WC;
            WC: wide_state <= WD;
            default: wide_state <= WA;
        endcase
    end

    (* some_attribute = shortint'(42) *)
    (* another_attribute = -1 *)
    state_t state = A;

    always @(posedge clk) begin
        case (state)
            A: state <= B;
            B: state <= C;
            C: state <= D;
            default: state <= A;
        endcase
    end

    assign z = (wide_state == WB) ^ (state == B);

endmodule
module top(input clk, input signed [3:0] sel_w , output reg out);

always @ (posedge clk)
begin
    case (sel_w) inside
        [-4:3] : out <= 1'b1;
        [4:5] : out <= 1'b0;
    endcase
end

endmodule
module top;
    integer x, y, z;
    task check;
        input integer a, b, c;
        assert (x == a);
        assert (y == b);
        assert (z == c);
    endtask
    always_comb begin
        x = 0; y = 0; z = 0;
        check(0, 0, 0);

        // post-increment/decrement statements
        x++;
        check(1, 0, 0);
        (* bar *) y (* foo *) ++;
        check(1, 1, 0);
        z--;
        check(1, 1, -1);
        (* bar *) z (* foo *) --;
        check(1, 1, -2);

        // pre-increment/decrement statements are equivalent
        ++z;
        check(1, 1, -1);
        (* bar *) ++ (* foo *) z;
        check(1, 1, 0);
        --x;
        check(0, 1, 0);
        (* bar *) -- (* foo *) y;
        check(0, 0, 0);

        // procedural pre-increment/decrement expressions
        z = ++x;
        check(1, 0, 1);
        z = ++ (* foo *) x;
        check(2, 0, 2);
        y = --x;
        check(1, 1, 2);
        y = -- (* foo *) x;

        // procedural post-increment/decrement expressions
        // T O D O: support attributes on post-increment/decrement
        check(0, 0, 2);
        y = x++;
        check(1, 0, 2);
        y = x--;
        check(0, 1, 2);

        // procedural assignment expressions
        x = (y = (z = 99) + 1) + 1;
        check(101, 100, 99);
        x = (y *= 2);
        check(200, 200, 99);
        x = (z >>= 2) * 4;
        check(96, 200, 24);
        y = (z >>= 1'sb1) * 2; // shift is implicitly cast to unsigned
        check(96, 24, 12);

        // check width of post-increment expressions
        z = (y = 0);
        begin
            byte w;
            w = 0;
            x = {1'b1, ++w};
            check(257, 0, 0);
            assert (w == 1);
            x = {2'b10, w++};
            check(513, 0, 0);
            assert (w == 2);
        end
    end
endmodule
module gate(x);
	output reg [15:0] x;
	if (1) begin : gen
		integer x;
		initial begin
			for (integer x = 5; x < 10; x++)
				if (x == 5)
					gen.x = 0;
				else
					gen.x += 2 ** x;
			x = x * 2;
		end
	end
	initial x = gen.x;
endmodule

module gold(x);
	output reg [15:0] x;
	if (1) begin : gen
		integer x;
		integer z;
		initial begin
			for (z = 5; z < 10; z++)
				if (z == 5)
					x = 0;
				else
					x += 2 ** z;
			x = x * 2;
		end
	end
	initial x = gen.x;
endmodule
module top;
    function automatic [30:0] func;
        input integer inp;
        func = { // self-determined context
            (
                inp == 0
                ? -1 // causes whole ternary to be 32 bits
                : func(inp - 1) // 31 bits, unsigned
            ) >> 2};
    endfunction
    function automatic signed [3:0] dunk;
        input integer inp;
        dunk = (
                inp == 0
                ? 4'hF
                // shouldn't make the ternary signed
                : dunk(inp - 1)
            ) == -1;
    endfunction
    localparam A = func(0);
    localparam B = func(1);
    localparam C = func(2);
    localparam D = func(3);
    localparam X = dunk(0);
    localparam Y = dunk(1);
    initial begin
        assert(A == 31'h3F_FFFFFF);
        assert(B == 31'h0F_FFFFFF);
        assert(C == 31'h03_FFFFFF);
        assert(D == 31'h00_FFFFFF);
        assert(X == 0);
        assert(Y == 0);
    end
    initial begin
        logic x;
        case (1'b1)
            dunk(0): x = 0;
            default: x = 1;
        endcase
        assert(x);
    end
endmodule
typedef logic [1:0] T;

package P;
    typedef logic [3:0] S;
endpackage

module gate(
    output wire [31:0] out1, out2
);
    function automatic T func1;
        input reg signed inp;
        func1 = inp;
    endfunction
    assign out1 = func1(1);
    function automatic P::S func2;
        input reg signed inp;
        func2 = inp;
    endfunction
    assign out2 = func2(1);
endmodule

module gold(
    output wire [31:0] out1, out2
);
    function automatic [1:0] func1;
        input reg signed inp;
        func1 = inp;
    endfunction
    assign out1 = func1(1);
    function automatic [3:0] func2;
        input reg signed inp;
        func2 = inp;
    endfunction
    assign out2 = func2(1);
endmodule
module gate(a);
	for (genvar i = 0; i < 2; i++)
		wire [i:0] x = '1;

	output wire [32:0] a;
	assign a = {1'b0, genblk1[0].x, 1'b0, genblk1[1].x, 1'b0};
endmodule

module gold(a);
	genvar i;
	for (i = 0; i < 2; i++)
		wire [i:0] x = '1;

	output wire [32:0] a;
	assign a = {1'b0, genblk1[0].x, 1'b0, genblk1[1].x, 1'b0};
endmodule
module top;
    reg [0:7] mem [0:2];

    initial mem[1] = '1;
    wire [31:0] a, b, c, d;
    assign a = mem[1];
    assign b = mem[-1];
    assign c = mem[-1][0];
    assign d = mem[-1][0:1];

    always @* begin

    	assert ($countbits(a, '0) == 24);
    	assert ($countbits(a, '1) == 8);
    	assert ($countbits(a, 'x) == 0);

    	assert ($countbits(b, '0) == 24);
    	assert ($countbits(b, 'x) == 8);

    	assert ($countbits(c, '0) == 31);
    	assert ($countbits(c, 'x) == 1);

    	assert ($countbits(d, '0) == 30);
    	assert ($countbits(d, 'x) == 2);

    end
endmodule
module top;
    wire logic wire_logic_0; assign wire_logic_0 = 0;
    wire logic wire_logic_1; assign wire_logic_1 = 1;
    wand logic wand_logic_0; assign wand_logic_0 = 0; assign wand_logic_0 = 1;
    wand logic wand_logic_1; assign wand_logic_1 = 1; assign wand_logic_1 = 1;
    wor logic wor_logic_0; assign wor_logic_0 = 0; assign wor_logic_0 = 0;
    wor logic wor_logic_1; assign wor_logic_1 = 1; assign wor_logic_1 = 0;

    wire integer wire_integer; assign wire_integer = 4'b1001;
    wand integer wand_integer; assign wand_integer = 4'b1001; assign wand_integer = 4'b1010;
    wor integer wor_integer; assign wor_integer = 4'b1001; assign wor_integer = 4'b1010;

    typedef logic [3:0] typename;
    wire typename wire_typename; assign wire_typename = 4'b1001;
    wand typename wand_typename; assign wand_typename = 4'b1001; assign wand_typename = 4'b1010;
    wor typename wor_typename; assign wor_typename = 4'b1001; assign wor_typename = 4'b1010;

    always @* begin
        assert (wire_logic_0 == 0);
        assert (wire_logic_1 == 1);
        assert (wand_logic_0 == 0);
        assert (wand_logic_1 == 1);
        assert (wor_logic_0 == 0);
        assert (wor_logic_1 == 1);

        assert (wire_integer == 4'b1001);
        assert (wand_integer == 4'b1000);
        assert (wor_integer == 4'b1011);

        assert (wire_typename == 4'b1001);
        assert (wand_typename == 4'b1000);
        assert (wor_typename == 4'b1011);
    end
endmodule
package P;
    localparam Y = 2;
    localparam X = Y + 1;
    task t;
        output integer x;
        x = Y;
    endtask
    function automatic integer f;
        input integer i;
        f = i * X;
    endfunction
    function automatic integer g;
        input integer i;
        g = i == 0 ? 1 : Y * g(i - 1);
    endfunction
    localparam Z = g(4);
endpackage

module top;
    integer a;
    initial P::t(a);
    integer b = P::f(3);
    integer c = P::g(3);
    integer d = P::Z;

    assert property (a == 2);
    assert property (b == 9);
    assert property (c == 8);
    assert property (d == 16);
endmodule
module gate(out);
    parameter integer a = -1;
    parameter int b = -2;
    parameter shortint c = -3;
    parameter longint d = -4;
    parameter byte e = -5;
    output wire [1023:0] out;
    assign out = {a, b, c, d, e};
endmodule

module gold(out);
    integer a = -1;
    int b = -2;
    shortint c = -3;
    longint d = -4;
    byte e = -5;
    output wire [1023:0] out;
    assign out = {a, b, c, d, e};
endmodule
module example #(
    parameter w,
    parameter x = 1,
    parameter byte y,
    parameter byte z = 3
) (
    output a, b,
    output byte c, d
);
    assign a = w;
    assign b = x;
    assign c = y;
    assign d = z;
endmodule

module top;
    wire a1, b1;
    wire a2, b2;
    wire a3, b3;
    wire a4, b4;
    byte c1, d1;
    byte c2, d2;
    byte c3, d3;
    byte c4, d4;

    example #(0, 1, 2) e1(a1, b1, c1, d1);
    example #(.w(1), .y(4)) e2(a2, b2, c2, d2);
    example #(.x(0), .w(1), .y(5)) e3(a3, b3, c3, d3);
    example #(1, 0, 9, 10) e4(a4, b4, c4, d4);

    always @* begin
        assert (a1 == 0);
        assert (b1 == 1);
        assert (c1 == 2);
        assert (d1 == 3);

        assert (a2 == 1);
        assert (b2 == 1);
        assert (c2 == 4);
        assert (d3 == 3);

        assert (a3 == 1);
        assert (b3 == 0);
        assert (c3 == 5);
        assert (d3 == 3);

        assert (a4 == 1);
        assert (b4 == 0);
        assert (c4 == 9);
        assert (d4 == 10);
    end
endmodule
module top;
    genvar i, j;
    if (1) begin : blk1
        integer a = 1;
        for (i = 0; i < 2; i = i + 1) begin : blk2
            integer b = i;
            for (j = 0; j < 2; j = j + 1) begin : blk3
                integer c = j;
                localparam x = i;
                localparam y = j;
                always @* begin
                    assert (1 == a);
                    assert (1 == blk1.a);
                    assert (1 == top.blk1.a);
                    assert (i == b);
                    assert (i == blk2[i].b);
                    assert (i == blk1.blk2[i].b);
                    assert (i == top.blk1.blk2[i].b);
                    assert (i == blk2[x].b);
                    assert (i == blk1.blk2[x].b);
                    assert (i == top.blk1.blk2[x].b);
                    assert (j == c);
                    assert (j == blk3[j].c);
                    assert (j == blk2[x].blk3[j].c);
                    assert (j == blk1.blk2[x].blk3[j].c);
                    assert (j == top.blk1.blk2[x].blk3[j].c);
                    assert (j == c);
                    assert (j == blk3[y].c);
                    assert (j == blk2[x].blk3[y].c);
                    assert (j == blk1.blk2[x].blk3[y].c);
                    assert (j == top.blk1.blk2[x].blk3[y].c);
                    assert (j == top.blk1.blk2[x].blk3[y].c[0]);
                    assert (0 == top.blk1.blk2[x].blk3[y].c[1]);
                    assert (0 == top.blk1.blk2[x].blk3[y].c[j]);
                end
            end
            always @* begin
                assert (1 == a);
                assert (1 == blk1.a);
                assert (1 == top.blk1.a);
                assert (i == b);
                assert (i == blk2[i].b);
                assert (i == blk1.blk2[i].b);
                assert (i == top.blk1.blk2[i].b);
                assert (0 == blk3[0].c);
                assert (0 == blk2[i].blk3[0].c);
                assert (0 == blk1.blk2[i].blk3[0].c);
                assert (0 == top.blk1.blk2[i].blk3[0].c);
                assert (1 == blk3[1].c);
                assert (1 == blk2[i].blk3[1].c);
                assert (1 == blk1.blk2[i].blk3[1].c);
                assert (1 == top.blk1.blk2[i].blk3[1].c);
            end
        end
        always @* begin
            assert (1 == a);
            assert (1 == blk1.a);
            assert (1 == top.blk1.a);
            assert (0 == blk2[0].b);
            assert (0 == blk1.blk2[0].b);
            assert (0 == top.blk1.blk2[0].b);
            assert (1 == blk2[1].b);
            assert (1 == blk1.blk2[1].b);
            assert (1 == top.blk1.blk2[1].b);
            assert (0 == blk2[0].blk3[0].c);
            assert (0 == blk1.blk2[0].blk3[0].c);
            assert (0 == top.blk1.blk2[0].blk3[0].c);
            assert (1 == blk2[0].blk3[1].c);
            assert (1 == blk1.blk2[0].blk3[1].c);
            assert (1 == top.blk1.blk2[0].blk3[1].c);
            assert (0 == blk2[1].blk3[0].c);
            assert (0 == blk1.blk2[1].blk3[0].c);
            assert (0 == top.blk1.blk2[1].blk3[0].c);
            assert (1 == blk2[1].blk3[1].c);
            assert (1 == blk1.blk2[1].blk3[1].c);
            assert (1 == top.blk1.blk2[1].blk3[1].c);
        end
    end
    always @* begin
        assert (1 == blk1.a);
        assert (1 == top.blk1.a);
        assert (0 == blk1.blk2[0].b);
        assert (0 == top.blk1.blk2[0].b);
        assert (1 == blk1.blk2[1].b);
        assert (1 == top.blk1.blk2[1].b);
        assert (0 == blk1.blk2[0].blk3[0].c);
        assert (0 == top.blk1.blk2[0].blk3[0].c);
        assert (1 == blk1.blk2[0].blk3[1].c);
        assert (1 == top.blk1.blk2[0].blk3[1].c);
        assert (0 == blk1.blk2[1].blk3[0].c);
        assert (0 == top.blk1.blk2[1].blk3[0].c);
        assert (1 == blk1.blk2[1].blk3[1].c);
        assert (1 == top.blk1.blk2[1].blk3[1].c);
    end
endmodule
module top;
    logic L1b0 = 0;
    logic L1b1 = 1;

    logic signed L1sb0 = 0;
    logic signed L1sb1 = 1;

    logic [1:0] L2b00 = 0;
    logic [1:0] L2b01 = 1;
    logic [1:0] L2b10 = 2;
    logic [1:0] L2b11 = 3;

    logic signed [1:0] L2sb00 = 0;
    logic signed [1:0] L2sb01 = 1;
    logic signed [1:0] L2sb10 = 2;
    logic signed [1:0] L2sb11 = 3;

    logic y = 1;

    always @* begin

        assert (1'(L1b0  ) == 1'b0);
        assert (1'(L1b1  ) == 1'b1);
        assert (1'(L1sb0 ) == 1'b0);
        assert (1'(L1sb1 ) == 1'b1);
        assert (1'(L2b00 ) == 1'b0);
        assert (1'(L2b01 ) == 1'b1);
        assert (1'(L2b10 ) == 1'b0);
        assert (1'(L2b11 ) == 1'b1);
        assert (1'(L2sb00) == 1'b0);
        assert (1'(L2sb01) == 1'b1);
        assert (1'(L2sb10) == 1'b0);
        assert (1'(L2sb11) == 1'b1);

        assert (2'(L1b0  ) == 2'b00);
        assert (2'(L1b1  ) == 2'b01);
        assert (2'(L1sb0 ) == 2'b00);
        assert (2'(L1sb1 ) == 2'b11);
        assert (2'(L2b00 ) == 2'b00);
        assert (2'(L2b01 ) == 2'b01);
        assert (2'(L2b10 ) == 2'b10);
        assert (2'(L2b11 ) == 2'b11);
        assert (2'(L2sb00) == 2'b00);
        assert (2'(L2sb01) == 2'b01);
        assert (2'(L2sb10) == 2'b10);
        assert (2'(L2sb11) == 2'b11);

        assert (3'(L1b0  ) == 3'b000);
        assert (3'(L1b1  ) == 3'b001);
        assert (3'(L1sb0 ) == 3'b000);
        assert (3'(L1sb1 ) == 3'b111);
        assert (3'(L2b00 ) == 3'b000);
        assert (3'(L2b01 ) == 3'b001);
        assert (3'(L2b10 ) == 3'b010);
        assert (3'(L2b11 ) == 3'b011);
        assert (3'(L2sb00) == 3'b000);
        assert (3'(L2sb01) == 3'b001);
        assert (3'(L2sb10) == 3'b110);
        assert (3'(L2sb11) == 3'b111);

        assert (3'(L1b0   | '1) == 3'b111);
        assert (3'(L1b1   | '1) == 3'b111);
        assert (3'(L1sb0  | '1) == 3'b111);
        assert (3'(L1sb1  | '1) == 3'b111);
        assert (3'(L2b00  | '1) == 3'b111);
        assert (3'(L2b01  | '1) == 3'b111);
        assert (3'(L2b10  | '1) == 3'b111);
        assert (3'(L2b11  | '1) == 3'b111);
        assert (3'(L2sb00 | '1) == 3'b111);
        assert (3'(L2sb01 | '1) == 3'b111);
        assert (3'(L2sb10 | '1) == 3'b111);
        assert (3'(L2sb11 | '1) == 3'b111);

        assert (3'(L1b0   | '0) == 3'b000);
        assert (3'(L1b1   | '0) == 3'b001);
        assert (3'(L1sb0  | '0) == 3'b000);
        assert (3'(L1sb1  | '0) == 3'b001);
        assert (3'(L2b00  | '0) == 3'b000);
        assert (3'(L2b01  | '0) == 3'b001);
        assert (3'(L2b10  | '0) == 3'b010);
        assert (3'(L2b11  | '0) == 3'b011);
        assert (3'(L2sb00 | '0) == 3'b000);
        assert (3'(L2sb01 | '0) == 3'b001);
        assert (3'(L2sb10 | '0) == 3'b010);
        assert (3'(L2sb11 | '0) == 3'b011);

        assert (3'(y ? L1b0   : '1) == 3'b000);
        assert (3'(y ? L1b1   : '1) == 3'b001);
        assert (3'(y ? L1sb0  : '1) == 3'b000);
        assert (3'(y ? L1sb1  : '1) == 3'b001);
        assert (3'(y ? L2b00  : '1) == 3'b000);
        assert (3'(y ? L2b01  : '1) == 3'b001);
        assert (3'(y ? L2b10  : '1) == 3'b010);
        assert (3'(y ? L2b11  : '1) == 3'b011);
        assert (3'(y ? L2sb00 : '1) == 3'b000);
        assert (3'(y ? L2sb01 : '1) == 3'b001);
        assert (3'(y ? L2sb10 : '1) == 3'b010);
        assert (3'(y ? L2sb11 : '1) == 3'b011);

        assert (3'(y ? L1b0   : '0) == 3'b000);
        assert (3'(y ? L1b1   : '0) == 3'b001);
        assert (3'(y ? L1sb0  : '0) == 3'b000);
        assert (3'(y ? L1sb1  : '0) == 3'b001);
        assert (3'(y ? L2b00  : '0) == 3'b000);
        assert (3'(y ? L2b01  : '0) == 3'b001);
        assert (3'(y ? L2b10  : '0) == 3'b010);
        assert (3'(y ? L2b11  : '0) == 3'b011);
        assert (3'(y ? L2sb00 : '0) == 3'b000);
        assert (3'(y ? L2sb01 : '0) == 3'b001);
        assert (3'(y ? L2sb10 : '0) == 3'b010);
        assert (3'(y ? L2sb11 : '0) == 3'b011);

        assert (3'(y ? L1b0   : 1'sb0) == 3'b000);
        assert (3'(y ? L1b1   : 1'sb0) == 3'b001);
        assert (3'(y ? L1sb0  : 1'sb0) == 3'b000);
        assert (3'(y ? L1sb1  : 1'sb0) == 3'b111);
        assert (3'(y ? L2b00  : 1'sb0) == 3'b000);
        assert (3'(y ? L2b01  : 1'sb0) == 3'b001);
        assert (3'(y ? L2b10  : 1'sb0) == 3'b010);
        assert (3'(y ? L2b11  : 1'sb0) == 3'b011);
        assert (3'(y ? L2sb00 : 1'sb0) == 3'b000);
        assert (3'(y ? L2sb01 : 1'sb0) == 3'b001);
        assert (3'(y ? L2sb10 : 1'sb0) == 3'b110);
        assert (3'(y ? L2sb11 : 1'sb0) == 3'b111);

        assert (3'(y ? L1b0   : 1'sb1) == 3'b000);
        assert (3'(y ? L1b1   : 1'sb1) == 3'b001);
        assert (3'(y ? L1sb0  : 1'sb1) == 3'b000);
        assert (3'(y ? L1sb1  : 1'sb1) == 3'b111);
        assert (3'(y ? L2b00  : 1'sb1) == 3'b000);
        assert (3'(y ? L2b01  : 1'sb1) == 3'b001);
        assert (3'(y ? L2b10  : 1'sb1) == 3'b010);
        assert (3'(y ? L2b11  : 1'sb1) == 3'b011);
        assert (3'(y ? L2sb00 : 1'sb1) == 3'b000);
        assert (3'(y ? L2sb01 : 1'sb1) == 3'b001);
        assert (3'(y ? L2sb10 : 1'sb1) == 3'b110);
        assert (3'(y ? L2sb11 : 1'sb1) == 3'b111);

    end
endmodule
module top;
    localparam W = 5;
    typedef logic [W-1:0] T;
    T x; // width 5
    if (1) begin : blk
        localparam W = 10;
        typedef T U;
        typedef logic [W-1:0] V;
        U y; // width 5
        V z; // width 10
    end
endmodule
module pass_through(
    input [63:0] inp,
    output [63:0] out
);
    assign out = inp;
endmodule

module top;
    logic [63:0] s0c, s1c, sxc, s0d, s1d, sxd, d;

    pass_through pt(8, d);

    assign s0c = '0 << 8;
    assign s1c = '1 << 8;
    assign sxc = 'x << 8;
    assign s0d = '0 << d;
    assign s1d = '1 << d;
    assign sxd = 'x << d;

    always @* begin
        assert (s0c === 64'h0000_0000_0000_0000);
        assert (s1c === 64'hFFFF_FFFF_FFFF_FF00);
        assert (sxc === 64'hxxxx_xxxx_xxxx_xx00);
        assert (s0d === 64'h0000_0000_0000_0000);
        assert (s1d === 64'hFFFF_FFFF_FFFF_FF00);
        assert (sxd === 64'hxxxx_xxxx_xxxx_xx00);
    end
endmodule
module pass_through(
    input [63:0] inp,
    output [63:0] out
);
    assign out = inp;
endmodule

module top;
    logic [63:0]
        o01, o02, o03, o04,
        o05, o06, o07, o08,
        o09, o10, o11, o12,
        o13, o14, o15, o16;
    assign o01 = '0;
    assign o02 = '1;
    assign o03 = 'x;
    assign o04 = 'z;
    assign o05 = 3'('0);
    assign o06 = 3'('1);
    assign o07 = 3'('x);
    assign o08 = 3'('z);
    pass_through pt09('0, o09);
    pass_through pt10('1, o10);
    pass_through pt11('x, o11);
    pass_through pt12('z, o12);
    always @* begin
        assert (o01 === {64 {1'b0}});
        assert (o02 === {64 {1'b1}});
        assert (o03 === {64 {1'bx}});
        assert (o04 === {64 {1'bz}});
        assert (o05 === {61'b0, 3'b000});
        assert (o06 === {61'b0, 3'b111});
        assert (o07 === {61'b0, 3'bxxx});
        assert (o08 === {61'b0, 3'bzzz});
        assert (o09 === {64 {1'b0}});
        assert (o10 === {64 {1'b1}});
        assert (o11 === {64 {1'bx}});
        assert (o12 === {64 {1'bz}});
    end
endmodule
module pass_through #(
	parameter WIDTH = 1
) (
	input logic [WIDTH-1:0] inp,
	output logic [WIDTH-1:0] out
);
	assign out = inp;
endmodule

module gate (
	input logic inp,
	output logic [63:0]
		out1, out2, out3, out4
);
	pass_through #(40) pt1('1, out1);
	pass_through #(40) pt2(inp ? '1 : '0, out2);
	pass_through #(40) pt3(inp ? '1 : 2'b10, out3);
	pass_through #(40) pt4(inp ? '1 : inp, out4);
endmodule

module gold (
	input logic inp,
	output logic [63:0]
		out1, out2, out3, out4
);
	localparam ONES = 40'hFF_FFFF_FFFF;
	pass_through #(40) pt1(ONES, out1);
	pass_through #(40) pt2(inp ? ONES : 0, out2);
	pass_through #(40) pt3(inp ? ONES : 2'sb10, out3);
	pass_through #(40) pt4(inp ? ONES : inp, out4);
endmodule
// This test is taken directly from Section 27.6 of IEEE 1800-2017

module top;
	parameter genblk2 = 0;
	genvar i;

	// The following generate block is implicitly named genblk1

	if (genblk2) logic a; // top.genblk1.a
	else logic b; // top.genblk1.b

	// The following generate block is implicitly named genblk02
	// as genblk2 is already a declared identifier

	if (genblk2) logic a; // top.genblk02.a
	else logic b; // top.genblk02.b

	// The following generate block would have been named genblk3
	// but is explicitly named g1

	for (i = 0; i < 1; i = i + 1) begin : g1 // block name
		// The following generate block is implicitly named genblk1
		// as the first nested scope inside g1
		if (1) logic a; // top.g1[0].genblk1.a
	end

	// The following generate block is implicitly named genblk4 since
	// it belongs to the fourth generate construct in scope "top".
	// The previous generate block would have been
	// named genblk3 if it had not been explicitly named g1

	for (i = 0; i < 1; i = i + 1)
		// The following generate block is implicitly named genblk1
		// as the first nested generate block in genblk4
		if (1) logic a; // top.genblk4[0].genblk1.a

	// The following generate block is implicitly named genblk5
	if (1) logic a; // top.genblk5.a
endmodule
