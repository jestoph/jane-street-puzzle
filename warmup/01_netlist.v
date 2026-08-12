module adder_demo (A,
    B,
    S,
    clk,
    en,
    rst_n);
 input A;
 input B;
 output S;
 input clk;
 input en;
 input rst_n;

 wire \a_reg[0] ;
 wire \a_reg[1] ;
 wire \a_reg[2] ;
 wire \a_reg[3] ;
 wire \a_reg[4] ;
 wire \a_reg[5] ;
 wire \a_reg[6] ;
 wire \a_reg[7] ;
 wire \b_reg[0] ;
 wire \b_reg[1] ;
 wire \b_reg[2] ;
 wire \b_reg[3] ;
 wire \b_reg[4] ;
 wire \b_reg[5] ;
 wire \b_reg[6] ;
 wire \b_reg[7] ;
 wire \sum[0] ;
 wire \sum[1] ;
 wire \sum[2] ;
 wire \sum[3] ;
 wire \sum[4] ;
 wire \sum[5] ;
 wire \sum[6] ;
 wire \sum[7] ;
 wire \sum[8] ;
 wire \add0/_00_ ;
 wire \add0/_01_ ;
 wire \add0/_02_ ;
 wire \add0/_03_ ;
 wire \add0/_04_ ;
 wire \add0/_05_ ;
 wire \add0/_06_ ;
 wire \add0/_07_ ;
 wire \add0/_08_ ;
 wire \add0/_09_ ;
 wire \add0/_10_ ;
 wire \add0/_11_ ;
 wire \add0/_12_ ;
 wire \add0/_13_ ;
 wire \add0/_14_ ;
 wire \add0/_15_ ;
 wire \add0/_16_ ;
 wire \add0/_17_ ;
 wire \add0/_18_ ;
 wire \add0/_19_ ;
 wire \add0/_20_ ;
 wire \add0/_21_ ;
 wire \add0/_22_ ;
 wire \add0/_23_ ;
 wire \add0/_24_ ;
 wire \add0/_25_ ;
 wire \add0/_26_ ;
 wire \add0/_27_ ;
 wire \add0/_28_ ;
 wire \add0/_29_ ;
 wire \add0/_30_ ;
 wire \add0/_31_ ;
 wire \cmp0/_0_ ;
 wire \cmp0/_1_ ;
 wire \sr_a/_00_ ;
 wire \sr_a/_01_ ;
 wire \sr_a/_02_ ;
 wire \sr_a/_03_ ;
 wire \sr_a/_04_ ;
 wire \sr_a/_05_ ;
 wire \sr_a/_06_ ;
 wire \sr_a/_07_ ;
 wire \sr_b/_00_ ;
 wire \sr_b/_01_ ;
 wire \sr_b/_02_ ;
 wire \sr_b/_03_ ;
 wire \sr_b/_04_ ;
 wire \sr_b/_05_ ;
 wire \sr_b/_06_ ;
 wire \sr_b/_07_ ;
 wire clknet_0_clk;
 wire clknet_1_0__leaf_clk;
 wire clknet_1_1__leaf_clk;

 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_0_Left_29 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_0_Right_0 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_10_Left_39 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_10_Right_10 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_11_Left_40 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_11_Right_11 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_12_Left_41 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_12_Right_12 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_13_Left_42 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_13_Right_13 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_14_Left_43 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_14_Right_14 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_15_Left_44 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_15_Right_15 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_16_Left_45 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_16_Right_16 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_17_Left_46 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_17_Right_17 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_18_Left_47 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_18_Right_18 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_19_Left_48 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_19_Right_19 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_1_Left_30 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_1_Right_1 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_20_Left_49 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_20_Right_20 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_21_Left_50 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_21_Right_21 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_22_Left_51 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_22_Right_22 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_23_Left_52 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_23_Right_23 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_24_Left_53 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_24_Right_24 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_25_Left_54 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_25_Right_25 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_26_Left_55 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_26_Right_26 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_27_Left_56 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_27_Right_27 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_28_Left_57 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_28_Right_28 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_2_Left_31 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_2_Right_2 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_3_Left_32 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_3_Right_3 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_4_Left_33 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_4_Right_4 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_5_Left_34 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_5_Right_5 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_6_Left_35 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_6_Right_6 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_7_Left_36 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_7_Right_7 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_8_Left_37 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_8_Right_8 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_9_Left_38 ();
 sky130_fd_sc_hd__decap_3 PHY_EDGE_ROW_9_Right_9 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_0_58 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_0_59 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_0_60 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_0_61 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_0_62 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_0_63 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_10_91 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_10_92 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_10_93 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_11_94 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_11_95 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_11_96 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_12_97 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_12_98 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_12_99 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_13_100 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_13_101 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_13_102 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_14_103 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_14_104 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_14_105 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_15_106 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_15_107 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_15_108 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_16_109 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_16_110 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_16_111 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_17_112 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_17_113 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_17_114 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_18_115 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_18_116 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_18_117 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_19_118 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_19_119 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_19_120 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_1_64 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_1_65 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_1_66 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_20_121 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_20_122 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_20_123 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_21_124 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_21_125 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_21_126 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_22_127 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_22_128 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_22_129 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_23_130 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_23_131 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_23_132 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_24_133 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_24_134 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_24_135 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_25_136 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_25_137 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_25_138 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_26_139 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_26_140 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_26_141 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_27_142 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_27_143 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_27_144 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_28_145 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_28_146 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_28_147 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_28_148 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_28_149 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_28_150 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_2_67 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_2_68 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_2_69 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_3_70 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_3_71 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_3_72 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_4_73 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_4_74 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_4_75 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_5_76 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_5_77 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_5_78 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_6_79 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_6_80 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_6_81 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_7_82 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_7_83 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_7_84 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_8_85 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_8_86 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_8_87 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_9_88 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_9_89 ();
 sky130_fd_sc_hd__tapvpwrvgnd_1 TAP_TAPCELL_ROW_9_90 ();
 sky130_fd_sc_hd__nand2_2 \add0/_32_  (.A(\b_reg[0] ),
    .B(\a_reg[0] ),
    .Y(\add0/_00_ ));
 sky130_fd_sc_hd__and2_2 \add0/_33_  (.A(\b_reg[1] ),
    .B(\a_reg[1] ),
    .X(\add0/_01_ ));
 sky130_fd_sc_hd__xor2_2 \add0/_34_  (.A(\b_reg[1] ),
    .B(\a_reg[1] ),
    .X(\add0/_02_ ));
 sky130_fd_sc_hd__xnor2_2 \add0/_35_  (.A(\add0/_00_ ),
    .B(\add0/_02_ ),
    .Y(\sum[1] ));
 sky130_fd_sc_hd__a31o_2 \add0/_36_  (.A1(\b_reg[0] ),
    .A2(\a_reg[0] ),
    .A3(\add0/_02_ ),
    .B1(\add0/_01_ ),
    .X(\add0/_03_ ));
 sky130_fd_sc_hd__or2_2 \add0/_37_  (.A(\b_reg[2] ),
    .B(\a_reg[2] ),
    .X(\add0/_04_ ));
 sky130_fd_sc_hd__nand2_2 \add0/_38_  (.A(\b_reg[2] ),
    .B(\a_reg[2] ),
    .Y(\add0/_05_ ));
 sky130_fd_sc_hd__and2_2 \add0/_39_  (.A(\add0/_04_ ),
    .B(\add0/_05_ ),
    .X(\add0/_06_ ));
 sky130_fd_sc_hd__xor2_2 \add0/_40_  (.A(\add0/_03_ ),
    .B(\add0/_06_ ),
    .X(\sum[2] ));
 sky130_fd_sc_hd__nor2_2 \add0/_41_  (.A(\b_reg[3] ),
    .B(\a_reg[3] ),
    .Y(\add0/_07_ ));
 sky130_fd_sc_hd__or2_2 \add0/_42_  (.A(\b_reg[3] ),
    .B(\a_reg[3] ),
    .X(\add0/_08_ ));
 sky130_fd_sc_hd__and2_2 \add0/_43_  (.A(\b_reg[3] ),
    .B(\a_reg[3] ),
    .X(\add0/_09_ ));
 sky130_fd_sc_hd__nor2_2 \add0/_44_  (.A(\add0/_07_ ),
    .B(\add0/_09_ ),
    .Y(\add0/_10_ ));
 sky130_fd_sc_hd__a21bo_2 \add0/_45_  (.A1(\add0/_03_ ),
    .A2(\add0/_06_ ),
    .B1_N(\add0/_05_ ),
    .X(\add0/_11_ ));
 sky130_fd_sc_hd__xor2_2 \add0/_46_  (.A(\add0/_10_ ),
    .B(\add0/_11_ ),
    .X(\sum[3] ));
 sky130_fd_sc_hd__and2_2 \add0/_47_  (.A(\b_reg[4] ),
    .B(\a_reg[4] ),
    .X(\add0/_12_ ));
 sky130_fd_sc_hd__nor2_2 \add0/_48_  (.A(\b_reg[4] ),
    .B(\a_reg[4] ),
    .Y(\add0/_13_ ));
 sky130_fd_sc_hd__nor2_2 \add0/_49_  (.A(\add0/_12_ ),
    .B(\add0/_13_ ),
    .Y(\add0/_14_ ));
 sky130_fd_sc_hd__a31o_2 \add0/_50_  (.A1(\b_reg[2] ),
    .A2(\a_reg[2] ),
    .A3(\add0/_08_ ),
    .B1(\add0/_09_ ),
    .X(\add0/_15_ ));
 sky130_fd_sc_hd__a31o_2 \add0/_51_  (.A1(\add0/_03_ ),
    .A2(\add0/_06_ ),
    .A3(\add0/_10_ ),
    .B1(\add0/_15_ ),
    .X(\add0/_16_ ));
 sky130_fd_sc_hd__xor2_2 \add0/_52_  (.A(\add0/_14_ ),
    .B(\add0/_16_ ),
    .X(\sum[4] ));
 sky130_fd_sc_hd__nor2_2 \add0/_53_  (.A(\b_reg[5] ),
    .B(\a_reg[5] ),
    .Y(\add0/_17_ ));
 sky130_fd_sc_hd__or2_2 \add0/_54_  (.A(\b_reg[5] ),
    .B(\a_reg[5] ),
    .X(\add0/_18_ ));
 sky130_fd_sc_hd__and2_2 \add0/_55_  (.A(\b_reg[5] ),
    .B(\a_reg[5] ),
    .X(\add0/_19_ ));
 sky130_fd_sc_hd__nor2_2 \add0/_56_  (.A(\add0/_17_ ),
    .B(\add0/_19_ ),
    .Y(\add0/_20_ ));
 sky130_fd_sc_hd__a21o_2 \add0/_57_  (.A1(\add0/_14_ ),
    .A2(\add0/_16_ ),
    .B1(\add0/_12_ ),
    .X(\add0/_21_ ));
 sky130_fd_sc_hd__xor2_2 \add0/_58_  (.A(\add0/_20_ ),
    .B(\add0/_21_ ),
    .X(\sum[5] ));
 sky130_fd_sc_hd__nand2_2 \add0/_59_  (.A(\b_reg[6] ),
    .B(\a_reg[6] ),
    .Y(\add0/_22_ ));
 sky130_fd_sc_hd__or2_2 \add0/_60_  (.A(\b_reg[6] ),
    .B(\a_reg[6] ),
    .X(\add0/_23_ ));
 sky130_fd_sc_hd__nand2_2 \add0/_61_  (.A(\add0/_22_ ),
    .B(\add0/_23_ ),
    .Y(\add0/_24_ ));
 sky130_fd_sc_hd__a31o_2 \add0/_62_  (.A1(\b_reg[4] ),
    .A2(\a_reg[4] ),
    .A3(\add0/_18_ ),
    .B1(\add0/_19_ ),
    .X(\add0/_25_ ));
 sky130_fd_sc_hd__a31o_2 \add0/_63_  (.A1(\add0/_14_ ),
    .A2(\add0/_16_ ),
    .A3(\add0/_20_ ),
    .B1(\add0/_25_ ),
    .X(\add0/_26_ ));
 sky130_fd_sc_hd__xnor2_2 \add0/_64_  (.A(\add0/_24_ ),
    .B(\add0/_26_ ),
    .Y(\sum[6] ));
 sky130_fd_sc_hd__and2_2 \add0/_65_  (.A(\b_reg[7] ),
    .B(\a_reg[7] ),
    .X(\add0/_27_ ));
 sky130_fd_sc_hd__nor2_2 \add0/_66_  (.A(\b_reg[7] ),
    .B(\a_reg[7] ),
    .Y(\add0/_28_ ));
 sky130_fd_sc_hd__nor2_2 \add0/_67_  (.A(\add0/_27_ ),
    .B(\add0/_28_ ),
    .Y(\add0/_29_ ));
 sky130_fd_sc_hd__a21boi_2 \add0/_68_  (.A1(\add0/_23_ ),
    .A2(\add0/_26_ ),
    .B1_N(\add0/_22_ ),
    .Y(\add0/_30_ ));
 sky130_fd_sc_hd__xnor2_2 \add0/_69_  (.A(\add0/_29_ ),
    .B(\add0/_30_ ),
    .Y(\sum[7] ));
 sky130_fd_sc_hd__or2_2 \add0/_70_  (.A(\b_reg[0] ),
    .B(\a_reg[0] ),
    .X(\add0/_31_ ));
 sky130_fd_sc_hd__and2_2 \add0/_71_  (.A(\add0/_00_ ),
    .B(\add0/_31_ ),
    .X(\sum[0] ));
 sky130_fd_sc_hd__o21bai_2 \add0/_72_  (.A1(\add0/_28_ ),
    .A2(\add0/_30_ ),
    .B1_N(\add0/_27_ ),
    .Y(\sum[8] ));
 sky130_fd_sc_hd__clkbuf_16 clkbuf_0_clk (.A(clk),
    .X(clknet_0_clk));
 sky130_fd_sc_hd__clkbuf_16 clkbuf_1_0__f_clk (.A(clknet_0_clk),
    .X(clknet_1_0__leaf_clk));
 sky130_fd_sc_hd__clkbuf_16 clkbuf_1_1__f_clk (.A(clknet_0_clk),
    .X(clknet_1_1__leaf_clk));
 sky130_fd_sc_hd__and3_2 \cmp0/_2_  (.A(\sum[6] ),
    .B(\sum[7] ),
    .C(\sum[8] ),
    .X(\cmp0/_0_ ));
 sky130_fd_sc_hd__and4bb_2 \cmp0/_3_  (.A_N(\sum[3] ),
    .B_N(\sum[2] ),
    .C(\sum[4] ),
    .D(\sum[5] ),
    .X(\cmp0/_1_ ));
 sky130_fd_sc_hd__and4bb_2 \cmp0/_4_  (.A_N(\sum[1] ),
    .B_N(\sum[0] ),
    .C(\cmp0/_0_ ),
    .D(\cmp0/_1_ ),
    .X(S));
 sky130_fd_sc_hd__mux2_1 \sr_a/_08_  (.A0(\a_reg[0] ),
    .A1(A),
    .S(en),
    .X(\sr_a/_00_ ));
 sky130_fd_sc_hd__mux2_1 \sr_a/_09_  (.A0(\a_reg[1] ),
    .A1(\a_reg[0] ),
    .S(en),
    .X(\sr_a/_01_ ));
 sky130_fd_sc_hd__mux2_1 \sr_a/_10_  (.A0(\a_reg[2] ),
    .A1(\a_reg[1] ),
    .S(en),
    .X(\sr_a/_02_ ));
 sky130_fd_sc_hd__mux2_1 \sr_a/_11_  (.A0(\a_reg[3] ),
    .A1(\a_reg[2] ),
    .S(en),
    .X(\sr_a/_03_ ));
 sky130_fd_sc_hd__mux2_1 \sr_a/_12_  (.A0(\a_reg[4] ),
    .A1(\a_reg[3] ),
    .S(en),
    .X(\sr_a/_04_ ));
 sky130_fd_sc_hd__mux2_1 \sr_a/_13_  (.A0(\a_reg[5] ),
    .A1(\a_reg[4] ),
    .S(en),
    .X(\sr_a/_05_ ));
 sky130_fd_sc_hd__mux2_1 \sr_a/_14_  (.A0(\a_reg[6] ),
    .A1(\a_reg[5] ),
    .S(en),
    .X(\sr_a/_06_ ));
 sky130_fd_sc_hd__mux2_1 \sr_a/_15_  (.A0(\a_reg[7] ),
    .A1(\a_reg[6] ),
    .S(en),
    .X(\sr_a/_07_ ));
 sky130_fd_sc_hd__dfrtp_2 \sr_a/_16_  (.CLK(clknet_1_1__leaf_clk),
    .D(\sr_a/_00_ ),
    .RESET_B(rst_n),
    .Q(\a_reg[0] ));
 sky130_fd_sc_hd__dfrtp_2 \sr_a/_17_  (.CLK(clknet_1_1__leaf_clk),
    .D(\sr_a/_01_ ),
    .RESET_B(rst_n),
    .Q(\a_reg[1] ));
 sky130_fd_sc_hd__dfrtp_2 \sr_a/_18_  (.CLK(clknet_1_1__leaf_clk),
    .D(\sr_a/_02_ ),
    .RESET_B(rst_n),
    .Q(\a_reg[2] ));
 sky130_fd_sc_hd__dfrtp_2 \sr_a/_19_  (.CLK(clknet_1_1__leaf_clk),
    .D(\sr_a/_03_ ),
    .RESET_B(rst_n),
    .Q(\a_reg[3] ));
 sky130_fd_sc_hd__dfrtp_2 \sr_a/_20_  (.CLK(clknet_1_1__leaf_clk),
    .D(\sr_a/_04_ ),
    .RESET_B(rst_n),
    .Q(\a_reg[4] ));
 sky130_fd_sc_hd__dfrtp_2 \sr_a/_21_  (.CLK(clknet_1_1__leaf_clk),
    .D(\sr_a/_05_ ),
    .RESET_B(rst_n),
    .Q(\a_reg[5] ));
 sky130_fd_sc_hd__dfrtp_2 \sr_a/_22_  (.CLK(clknet_1_1__leaf_clk),
    .D(\sr_a/_06_ ),
    .RESET_B(rst_n),
    .Q(\a_reg[6] ));
 sky130_fd_sc_hd__dfrtp_2 \sr_a/_23_  (.CLK(clknet_1_1__leaf_clk),
    .D(\sr_a/_07_ ),
    .RESET_B(rst_n),
    .Q(\a_reg[7] ));
 sky130_fd_sc_hd__mux2_1 \sr_b/_08_  (.A0(\b_reg[0] ),
    .A1(B),
    .S(en),
    .X(\sr_b/_00_ ));
 sky130_fd_sc_hd__mux2_1 \sr_b/_09_  (.A0(\b_reg[1] ),
    .A1(\b_reg[0] ),
    .S(en),
    .X(\sr_b/_01_ ));
 sky130_fd_sc_hd__mux2_1 \sr_b/_10_  (.A0(\b_reg[2] ),
    .A1(\b_reg[1] ),
    .S(en),
    .X(\sr_b/_02_ ));
 sky130_fd_sc_hd__mux2_1 \sr_b/_11_  (.A0(\b_reg[3] ),
    .A1(\b_reg[2] ),
    .S(en),
    .X(\sr_b/_03_ ));
 sky130_fd_sc_hd__mux2_1 \sr_b/_12_  (.A0(\b_reg[4] ),
    .A1(\b_reg[3] ),
    .S(en),
    .X(\sr_b/_04_ ));
 sky130_fd_sc_hd__mux2_1 \sr_b/_13_  (.A0(\b_reg[5] ),
    .A1(\b_reg[4] ),
    .S(en),
    .X(\sr_b/_05_ ));
 sky130_fd_sc_hd__mux2_1 \sr_b/_14_  (.A0(\b_reg[6] ),
    .A1(\b_reg[5] ),
    .S(en),
    .X(\sr_b/_06_ ));
 sky130_fd_sc_hd__mux2_1 \sr_b/_15_  (.A0(\b_reg[7] ),
    .A1(\b_reg[6] ),
    .S(en),
    .X(\sr_b/_07_ ));
 sky130_fd_sc_hd__dfrtp_2 \sr_b/_16_  (.CLK(clknet_1_0__leaf_clk),
    .D(\sr_b/_00_ ),
    .RESET_B(rst_n),
    .Q(\b_reg[0] ));
 sky130_fd_sc_hd__dfrtp_2 \sr_b/_17_  (.CLK(clknet_1_0__leaf_clk),
    .D(\sr_b/_01_ ),
    .RESET_B(rst_n),
    .Q(\b_reg[1] ));
 sky130_fd_sc_hd__dfrtp_2 \sr_b/_18_  (.CLK(clknet_1_0__leaf_clk),
    .D(\sr_b/_02_ ),
    .RESET_B(rst_n),
    .Q(\b_reg[2] ));
 sky130_fd_sc_hd__dfrtp_2 \sr_b/_19_  (.CLK(clknet_1_0__leaf_clk),
    .D(\sr_b/_03_ ),
    .RESET_B(rst_n),
    .Q(\b_reg[3] ));
 sky130_fd_sc_hd__dfrtp_2 \sr_b/_20_  (.CLK(clknet_1_0__leaf_clk),
    .D(\sr_b/_04_ ),
    .RESET_B(rst_n),
    .Q(\b_reg[4] ));
 sky130_fd_sc_hd__dfrtp_2 \sr_b/_21_  (.CLK(clknet_1_0__leaf_clk),
    .D(\sr_b/_05_ ),
    .RESET_B(rst_n),
    .Q(\b_reg[5] ));
 sky130_fd_sc_hd__dfrtp_2 \sr_b/_22_  (.CLK(clknet_1_0__leaf_clk),
    .D(\sr_b/_06_ ),
    .RESET_B(rst_n),
    .Q(\b_reg[6] ));
 sky130_fd_sc_hd__dfrtp_2 \sr_b/_23_  (.CLK(clknet_1_0__leaf_clk),
    .D(\sr_b/_07_ ),
    .RESET_B(rst_n),
    .Q(\b_reg[7] ));
endmodule
