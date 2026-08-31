
/***********************************  FROM_PART80 **************************************/

// ref component/and2b.v
assign FROM_PART80  = (~Wire_145 ) & Wire_146 ;

// ref component/dfrtp.v
dfrtp dfrtp_28 (
  .CLK(clk),
  .D(Wire_152),
  .Q(Wire_145),
  .RESET_B(rst_n)
);

// ref component/dfrtp.v
dfrtp dfrtp_25 (
  .CLK(clk),
  .D(Wire_693),
  .Q(Wire_146),
  .RESET_B(rst_n)
);

assign Wire_152  = ((Wire_146  | Wire_150 ) & Wire_141 );
assign Wire_693  = ~((~Wire_146 ) & Wire_150 ); // Syntax?
assign Wire_141  = Wire_145  | (I  & Wire_140 );
assign Wire_150  = ~(I  & Wire_145  & Wire_140 );
assign Wire_140  = ( ~ FROM_BLOB1  & ~ FROM_BLOB2  ) & FROM_BLOB3  & FROM_BLOB0  ;



/***********************************  FROM_PART81 **************************************/

// ref component/and2b.v
assign FROM_PART81  = (~Wire_147 ) & Wire_148 ;

// ref component/dfrtp.v
dfrtp dfrtp_29 (
  .CLK(clk),
  .D(Wire_149),
  .Q(Wire_147),
  .RESET_B(rst_n)
);

// ref component/dfrtp.v
dfrtp dfrtp_26 (
  .CLK(clk),
  .D(Wire_151),
  .Q(Wire_148),
  .RESET_B(rst_n)
);

assign Wire_149  = ((Wire_148  | Wire_159 ) & Wire_155 );
assign Wire_151  = ~((~Wire_148 ) & Wire_159 ); // Syntax?
assign Wire_159  = ~(I  & Wire_147  & Wire_131 );
assign Wire_155  = Wire_147  | (I  & Wire_131 );
assign Wire_131  = (~FROM_BLOB0  & ~FROM_BLOB2 ) & FROM_BLOB3  & FROM_BLOB1 ;

/***********************************  FROM_PART82 **************************************/

// ref component/and2b.v
assign FROM_PART82  = (~Wire_205 ) & Wire_179 ;

// ref component/dfrtp.v
dfrtp dfrtp_76 (
  .CLK(clk),
  .D(Wire_198),
  .Q(Wire_205),
  .RESET_B(rst_n)
);
// ref component/dfrtp.v
dfrtp dfrtp_80 (
  .CLK(clk),
  .D(Wire_170),
  .Q(Wire_179),
  .RESET_B(rst_n)
);

assign Wire_198  = ((Wire_179  | Wire_194 ) & Wire_201 );
assign Wire_170  = ~((~Wire_179 ) & Wire_194 ); // Syntax?
assign Wire_194  = ~(I  & Wire_205  & Wire_199 );
assign Wire_201  = Wire_205  | (I  & Wire_199 );
assign Wire_199  = ( ~ FROM_BLOB3  & ~ FROM_BLOB2  ) & FROM_BLOB0  & FROM_BLOB1  ;

/***********************************  FROM_PART83 **************************************/

// ref component/and2b.v
assign FROM_PART83  = (~Wire_224 ) & Wire_225 ;

// ref component/dfrtp.v
dfrtp dfrtp_84 (
  .CLK(clk),
  .D(Wire_206),
  .Q(Wire_224),
  .RESET_B(rst_n)
);

// ref component/dfrtp.v
dfrtp dfrtp_70 (
  .CLK(clk),
  .D(Wire_226),
  .Q(Wire_225),
  .RESET_B(rst_n)
);
assign Wire_206  = ((Wire_225  | Wire_228 ) & Wire_208 );
assign Wire_226  = ~((~Wire_225 ) & Wire_228 ); // Syntax?
assign Wire_228  = ~(I  & Wire_224  & Wire_207 );
assign Wire_208  = Wire_224  | (I  & Wire_207 );
assign Wire_207  = ~ ( FROM_BLOB1  | FROM_BLOB0  | FROM_BLOB3  | FROM_BLOB2  ) ;

/***********************************  FROM_PART84 **************************************/

// ref component/and2b.v
assign FROM_PART84  = (~Wire_167 ) & Wire_182 ;

// ref component/dfrtp.v
dfrtp dfrtp_79 (
  .CLK(clk),
  .D(Wire_181),
  .Q(Wire_167),
  .RESET_B(rst_n)
);


// ref component/dfrtp.v
dfrtp dfrtp_72 (
  .CLK(clk),
  .D(Wire_185),
  .Q(Wire_182),
  .RESET_B(rst_n)
);

assign Wire_181  = ((Wire_182  | Wire_186 ) & Wire_169 );
assign Wire_185  = ~((~Wire_182 ) & Wire_186 ); // Syntax?
assign Wire_186  = ~(I  & Wire_167  & Wire_168 );
assign Wire_169  = Wire_167  | (I  & Wire_168 );
assign Wire_168  = ( ~ FROM_BLOB0  & ~ FROM_BLOB3  ) & FROM_BLOB2  & FROM_BLOB1  ;

/***********************************  FROM_PART85 **************************************/

// ref component/and2.v
assign FROM_PART85  = ~Wire_190 & Wire_180;

// ref component/dfrtp.v
dfrtp dfrtp_77 (
  .CLK(clk),
  .D(Wire_171),
  .Q(Wire_190),
  .RESET_B(rst_n)
);

// ref component/dfrtp.v
dfrtp dfrtp_71 (
  .CLK(clk),
  .D(Wire_172),
  .Q(Wire_180),
  .RESET_B(rst_n)
);

assign Wire_171  = ((Wire_190  | Wire_192 ) & Wire_176 );
assign Wire_172  = Wire_180  | (Wire_190  & Wire_192 );
assign Wire_192  = (~Wire_174  & I ); // Syntax?
assign Wire_176  = Wire_180  | ~Wire_190  | Wire_174  | ~I ;
assign Wire_174  = FROM_BLOB1  | FROM_BLOB0  | FROM_BLOB3  | ( ~ FROM_BLOB2  ) ;

/***********************************  FROM_PART86 **************************************/

// ref component/and2.v
assign FROM_PART86  = ~Wire_156 & Wire_157;

// ref component/dfrtp.v
dfrtp dfrtp_30 (
  .CLK(clk),
  .D(Wire_135),
  .Q(Wire_156),
  .RESET_B(rst_n)
);

// ref component/dfrtp.v
dfrtp dfrtp_32 (
  .CLK(clk),
  .D(Wire_136),
  .Q(Wire_157),
  .RESET_B(rst_n)
);

assign Wire_135  = ((Wire_156  | Wire_139 ) & Wire_154 );
assign Wire_136  = Wire_157  | (Wire_156  & Wire_139 );
assign Wire_139  = (~Wire_153  & I ); // Syntax?
assign Wire_154  = Wire_157  | ~Wire_156  | Wire_153  | ~I ;
assign Wire_153  = FROM_BLOB1  | FROM_BLOB0  | FROM_BLOB2  | ( ~ FROM_BLOB3  ) ;

/***********************************  FROM_PART87 **************************************/

// ref component/and2.v
assign FROM_PART87  = ~Wire_202 & Wire_203;

// ref component/dfrtp.v
dfrtp dfrtp_83 (
  .CLK(clk),
  .D(Wire_213),
  .Q(Wire_202),
  .RESET_B(rst_n)
);

// ref component/dfrtp.v
dfrtp dfrtp_82 (
  .CLK(clk),
  .D(Wire_218),
  .Q(Wire_203),
  .RESET_B(rst_n)
);

assign Wire_213  = ((Wire_202  | Wire_211 ) & Wire_214 );
assign Wire_218  = Wire_203  | (Wire_202  & Wire_211 );
assign Wire_211  = (~Wire_209  & I ); // Syntax?
assign Wire_214  = Wire_203  | ~Wire_202  | Wire_209  | ~I ;
assign Wire_209  = FROM_BLOB1  | FROM_BLOB3  | FROM_BLOB2  | ( ~ FROM_BLOB0  ) ;

/***********************************  FROM_PART88 **************************************/

// ref component/and2.v
assign FROM_PART88  = ~Wire_204 & Wire_220;

// ref component/dfrtp.v
dfrtp dfrtp_75 (
  .CLK(clk),
  .D(Wire_215),
  .Q(Wire_204),
  .RESET_B(rst_n)
);


// ref component/dfrtp.v
dfrtp dfrtp_81 (
  .CLK(clk),
  .D(Wire_212),
  .Q(Wire_220),
  .RESET_B(rst_n)
);

assign Wire_215  = ((Wire_204  | Wire_217 ) & Wire_431 );
assign Wire_212  = Wire_220  | (Wire_204  & Wire_217 );
assign Wire_217  = (~Wire_222  & I ); // Syntax?
assign Wire_431  = Wire_220  | ~Wire_204  | Wire_222  | ~I ;
assign Wire_222  = FROM_BLOB0  | FROM_BLOB3  | FROM_BLOB2  | ( ~ FROM_BLOB1  ) ;

/***********************************  FROM_PART88 **************************************/

// ref component/and2b.v
assign FROM_PART89  = (~Wire_166 ) & Wire_130 ;

// ref component/dfrtp.v
dfrtp dfrtp_78 (
  .CLK(clk),
  .D(Wire_177),
  .Q(Wire_166),
  .RESET_B(rst_n)
);

// ref component/dfrtp.v
dfrtp dfrtp_73 (
  .CLK(clk),
  .D(Wire_184),
  .Q(Wire_130),
  .RESET_B(rst_n)
);

assign Wire_177  = ((Wire_130  | Wire_164 ) & Wire_187 );
assign Wire_184  = ~((~Wire_130 ) & Wire_164 ); // Syntax?
assign Wire_164  = ~(I  & Wire_166  & Wire_178 );
assign Wire_187  = Wire_166  | (I  & Wire_178 );
assign Wire_178  = ( ~ FROM_BLOB1  & ~ FROM_BLOB3  ) & FROM_BLOB2  & FROM_BLOB0  ;

/***********************************  FROM_PART88 **************************************/

// ref component/and2b.v
assign FROM_PART810  = (~Wire_142 ) & Wire_143 ;

// ref component/dfrtp.v
dfrtp dfrtp_31 (
  .CLK(clk),
  .D(Wire_132),
  .Q(Wire_142),
  .RESET_B(rst_n)
);

// ref component/dfrtp.v
dfrtp dfrtp_74 (
  .CLK(clk),
  .D(Wire_133),
  .Q(Wire_143),
  .RESET_B(rst_n)
);

assign Wire_132  = ((Wire_143  | Wire_134 ) & Wire_163 );
assign Wire_133  = ~((~Wire_143 ) & Wire_134 ); // Syntax?
assign Wire_134  = ~(I  & Wire_142  & Wire_162 );
assign Wire_163  = Wire_142  | ( I  & S  & Wire_162  ) ;
assign Wire_162  = ( ~ FROM_BLOB3  ) & FROM_BLOB2  & FROM_BLOB0  & FROM_BLOB1  ;
