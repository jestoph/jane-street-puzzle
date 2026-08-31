
/************************************ FROM_PART7C0 ********************************/

assign FROM_PART7C0  = ( ~ Wire_544  ) & Wire_548  ;

  // ref component/dfrtp.v
  dfrtp dfrtp_24 (
    .CLK(clk),
    .D(Wire_554),
    .Q(Wire_544),
    .RESET_B(rst_n)
  );

  // ref component/dfrtp.v
  dfrtp dfrtp_27 (
    .CLK(clk),
    .D(Wire_549),
    .Q(Wire_548),
    .RESET_B(rst_n)
  );

assign Wire_554  = ( ( Wire_548  | Wire_545  ) & Wire_543  ) ;
assign Wire_549  = ~ ( ( ~ Wire_548  ) & Wire_545  ) ;
assign Wire_545  = ~ ( I  & Wire_544  & Wire_999  ) ;
assign Wire_543  = Wire_544  | ( I  & Wire_999  ) ;
assign Wire_999  = ~ ( FROM_PART21  | FROM_PART22  | FROM_PART23  | FROM_PART20  ) ;

/************************************ FROM_PART7A0 ********************************/

assign FROM_PART7A0  = ( ~ Wire_43  ) & Wire_127  ;

  // ref component/dfrtp.v
  dfrtp dfrtp_11 (
    .CLK(clk),
    .D(Wire_144),
    .Q(Wire_43),
    .RESET_B(rst_n)
  );
  // ref component/dfrtp.v
  dfrtp dfrtp_16 (
    .CLK(clk),
    .D(Wire_102),
    .Q(Wire_127),
    .RESET_B(rst_n)
  );

assign Wire_144  = ( ( Wire_127  | Wire_75  ) & Wire_158  ) ;
assign Wire_102  = ~ ( ( ~ Wire_127  ) & Wire_75  ) ;
assign Wire_75  = ~ ( I  & Wire_43  & Wire_518  ) ;
assign Wire_158  = Wire_43  | ( I  & Wire_518  ) ;
assign Wire_518  = ( ~ FROM_PART22  & ~ FROM_PART20  ) & FROM_PART23  & FROM_PART21  ;

/************************************ FROM_PART7A1 ********************************/

// ref component/and2.v
assign FROM_PART7A1  = Wire_64  & (~Wire_53)  ;
  // ref component/dfrtp.v
  dfrtp dfrtp_15 (
    .CLK(clk),
    .D(Wire_36),
    .Q(Wire_64),
    .RESET_B(rst_n)
  );

  // ref component/dfrtp.v
  dfrtp dfrtp_12 (
    .CLK(clk),
    .D(Wire_521),
    .Q(Wire_53),
    .RESET_B(rst_n)
  );

  // ref component/a21o.v
assign Wire_36  = Wire_64  | ( Wire_53  & Wire_516  ) ;
  // ref component/o21a.v
assign Wire_521  = ( ( Wire_53  | Wire_516  ) & Wire_4  ) ;
  // ref component/nor2.v
assign Wire_516  = ~ ( Wire_514  | (~I)  ) ;
  // ref component/or4.v
assign Wire_4  = Wire_64  | (~Wire_53)  | Wire_514  | (~I)  ;
// ref component/or4b.v
assign Wire_514  = FROM_PART21  | FROM_PART22  | FROM_PART20  | ( ~ FROM_PART23  ) ;

/************************************ FROM_PART7A2 ********************************/

// ref component/and2b.v
assign FROM_PART7A2  = ( ~ Wire_517  ) & Wire_25  ;

  // ref component/dfrtp.v
  dfrtp dfrtp_10 (
    .CLK(clk),
    .D(Wire_86),
    .Q(Wire_517),
    .RESET_B(rst_n)
  );
  // ref component/dfrtp.v
  dfrtp dfrtp_14 (
    .CLK(clk),
    .D(Wire_519),
    .Q(Wire_25),
    .RESET_B(rst_n)
  );

  // ref component/o21a.v
assign Wire_86  = ( ( Wire_25  | Wire_17  ) & Wire_114  ) ;
  // ref component/nand2b.v
assign Wire_519  = ~ ( ( ~ Wire_25  ) & Wire_17  ) ;
  // ref component/nand4.v
assign Wire_17  = ~ ( I  & Wire_517  & Wire_407  ) ;
  // ref component/a31o.v
assign Wire_114  = Wire_517  | ( I  & Wire_407  ) ;
// ref component/and4bb.v
assign Wire_407  = ( ~ FROM_PART21  & ~ FROM_PART20  ) & FROM_PART23  & FROM_PART22  ;

/************************************ FROM_PART7B1 ********************************/

// ref component/and2.v
assign FROM_PART7B1  = Wire_436  & (~Wire_552)  ;
  // ref component/dfrtp.v
  dfrtp dfrtp_7 (
    .CLK(clk),
    .D(Wire_538),
    .Q(Wire_436),
    .RESET_B(rst_n)
  );

  // ref component/dfrtp.v
  dfrtp dfrtp_22 (
    .CLK(clk),
    .D(Wire_409),
    .Q(Wire_552),
    .RESET_B(rst_n)
  );

  // ref component/a21o.v
assign Wire_538  = Wire_436  | ( Wire_552  & Wire_542  ) ;
  // ref component/o21a.v
assign Wire_409  = ( ( Wire_552  | Wire_542  ) & Wire_410  ) ;
  // ref component/or4.v
assign Wire_410  = Wire_436  | (~Wire_552)  | Wire_540  | (~I)  ;
  // ref component/nor2.v
assign Wire_542  = ~ ( Wire_540  | (~I)  ) ;
// ref component/or4b.v
assign Wire_540  = FROM_PART22  | FROM_PART23  | FROM_PART20  | ( ~ FROM_PART21  ) ;

/************************************ FROM_PART7B2 ********************************/

// ref component/and2.v
assign FROM_PART7B2  = Wire_551  & (~Wire_408)  ;
  // ref component/dfrtp.v
  dfrtp dfrtp_23 (
    .CLK(clk),
    .D(Wire_547),
    .Q(Wire_551),
    .RESET_B(rst_n)
  );

  // ref component/dfrtp.v
  dfrtp dfrtp_8 (
    .CLK(clk),
    .D(Wire_546),
    .Q(Wire_408),
    .RESET_B(rst_n)
  );

  // ref component/a21o.v
assign Wire_547  = Wire_551  | ( Wire_408  & Wire_537  ) ;
  // ref component/o21a.v
assign Wire_546  = ( ( Wire_408  | Wire_537  ) & Wire_707  ) ;
  // ref component/nor2.v
assign Wire_537  = ~ ( Wire_550  | (~I)  ) ;
  // ref component/or4.v
assign Wire_707  = Wire_551  | (~Wire_408)  | Wire_550  | (~I)  ;
// ref component/or4b.v
assign Wire_550  = FROM_PART21  | FROM_PART23  | FROM_PART20  | ( ~ FROM_PART22  ) ;

/************************************ FROM_PART7B3 ********************************/

// ref component/and2b.v
assign FROM_PART7B3  = ( ~ Wire_280  ) & Wire_197  ;
  // ref component/dfrtp.v
  dfrtp dfrtp_9 (
    .CLK(clk),
    .D(Wire_200),
    .Q(Wire_280),
    .RESET_B(rst_n)
  );

  // ref component/dfrtp.v
  dfrtp dfrtp_17 (
    .CLK(clk),
    .D(Wire_313),
    .Q(Wire_197),
    .RESET_B(rst_n)
  );

  // ref component/o21a.v
assign Wire_200  = ( ( Wire_197  | Wire_195  ) & Wire_189  ) ;
  // ref component/nand2b.v
assign Wire_313  = ~ ( ( ~ Wire_197  ) & Wire_195  ) ;
  // ref component/nand4.v
assign Wire_195  = ~ ( I & Wire_280  & Wire_321  ) ;
  // ref component/a31o.v
assign Wire_189  = Wire_280  | ( I  & Wire_321  ) ;
// ref component/and4b.v
assign Wire_321  = ( ~ FROM_PART23  ) & FROM_PART20  & FROM_PART22  & FROM_PART21  ;

/************************************ FROM_PART7B4 ********************************/

// ref component/and2b.v
assign FROM_PART7B4  = ( ~ Wire_511  ) & Wire_482  ;
  // ref component/dfrtp.v
  dfrtp dfrtp_4 (
    .CLK(clk),
    .D(Wire_534),
    .Q(Wire_511),
    .RESET_B(rst_n)
  );

  // ref component/dfrtp.v
  dfrtp dfrtp_18 (
    .CLK(clk),
    .D(Wire_520),
    .Q(Wire_482),
    .RESET_B(rst_n)
  );

  // ref component/o21a.v
assign Wire_534  = ( ( Wire_482  | Wire_524  ) & Wire_523  ) ;
  // ref component/nand2b.v
assign Wire_520  = ~ ( ( ~ Wire_482  ) & Wire_524  ) ;
  // ref component/nand4.v
assign Wire_524  = ~ ( I  & Wire_511  & Wire_508  ) ;
  // ref component/a31o.v
assign Wire_523  = Wire_511  | ( I  & Wire_508  ) ;
// ref component/and4bb.v
assign Wire_508  = ( ~ FROM_PART21  & ~ FROM_PART23  ) & FROM_PART20  & FROM_PART22  ;

/************************************ FROM_PART7B5 ********************************/

// ref component/and2b.v
assign FROM_PART7B5  = ( ~ Wire_227  ) & Wire_360  ;

  // ref component/dfrtp.v
  dfrtp dfrtp_6 (
    .CLK(clk),
    .D(Wire_381),
    .Q(Wire_227),
    .RESET_B(rst_n)
  );
  // ref component/dfrtp.v
  dfrtp dfrtp_20 (
    .CLK(clk),
    .D(Wire_525),
    .Q(Wire_360),
    .RESET_B(rst_n)
  );

  // ref component/o21a.v
assign Wire_381  = ( ( Wire_360  | Wire_345  ) & Wire_433  ) ;
  // ref component/nand2b.v
assign Wire_525  = ~ ( ( ~ Wire_360  ) & Wire_345  ) ;
  // ref component/nand4.v
assign Wire_345  = ~ ( I  & Wire_227  & Wire_377  ) ;
  // ref component/a31o.v
assign Wire_433  = Wire_227  | ( I  & Wire_377  ) ;
// ref component/and4bb.v
assign Wire_377  = ( ~ FROM_PART22  & ~ FROM_PART23  ) & FROM_PART20  & FROM_PART21  ;

/************************************ FROM_PART7B6 ********************************/

// ref component/and2b.v
assign FROM_PART7B6  = ( ~ Wire_532  ) & Wire_452  ;
  // ref component/dfrtp.v
  dfrtp dfrtp_13 (
    .CLK(clk),
    .D(Wire_526),
    .Q(Wire_532),
    .RESET_B(rst_n)
  );

  // ref component/dfrtp.v
  dfrtp dfrtp_21 (
    .CLK(clk),
    .D(Wire_464),
    .Q(Wire_452),
    .RESET_B(rst_n)
  );

  // ref component/o21a.v
assign Wire_526  = ( ( Wire_452  | Wire_529  ) & Wire_528  ) ;
  // ref component/nand2b.v
assign Wire_464  = ~ ( ( ~ Wire_452  ) & Wire_529  ) ;
  // ref component/nand4.v
assign Wire_529  = ~ ( I  & Wire_532  & Wire_527  ) ;
  // ref component/a31o.v
assign Wire_528  = Wire_532  | ( I  & Wire_527  ) ;
// ref component/and4bb.v
assign Wire_527  = ( ~ FROM_PART23  & ~ FROM_PART20  ) & FROM_PART22  & FROM_PART21  ;

/************************************ FROM_PART7B7 ********************************/

// ref component/and2.v
assign FROM_PART7B7  = Wire_445  & (~Wire_454)  ;
  // ref component/dfrtp.v
  dfrtp dfrtp_5 (
    .CLK(clk),
    .D(Wire_531),
    .Q(Wire_445),
    .RESET_B(rst_n)
  );

  // ref component/dfrtp.v
  dfrtp dfrtp_19 (
    .CLK(clk),
    .D(Wire_530),
    .Q(Wire_454),
    .RESET_B(rst_n)
  );

  // ref component/a21o.v
assign Wire_531  = Wire_445  | ( Wire_454  & Wire_455  ) ;
  // ref component/o21a.v
assign Wire_530  = ( ( Wire_454  | Wire_455  ) & Wire_533  ) ;
  // ref component/or4.v
assign Wire_533  = Wire_445  | (~Wire_454)  | Wire_492  | (~I)  ;
  // ref component/nor2.v
assign Wire_455  = ~ ( Wire_492  | (~I)  ) ;
// ref component/or4b.v
assign Wire_492  = FROM_PART21  | FROM_PART22  | FROM_PART23  | ( ~ FROM_PART20  ) ;
