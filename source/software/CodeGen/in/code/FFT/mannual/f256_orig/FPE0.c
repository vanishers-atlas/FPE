#include "header.h"


// **** Fire function declaration **** //
static inline void butterfly_sharecoe(int i0, int i1, int *o0, int *o1, int W) {
asm ("ADDMULSRA1 %[A0], %[b0], %[w0], %[a0]\n\t"
     "SUBMULSRA1 %[B0], %[b0], %[w0], %[a0]\n\t"
     : [A0]"=&r"(*o0), [B0]"=&r"(*o1)
     : [b0]"r"(i1), [w0]"i"(W), [a0]"r"(i0)
      );
}

// **** Main function **** //
void FPE0PE0() {

  // **** Variable declaration **** //
	int T0_i0;
	int T0_i1;
	int T0_o0;
	int T0_o1;
	int T0_W;

	int T1_i0;
	int T1_i1;
	int T1_o0;
	int T1_o1;
	int T1_W;

	int T2_i0;
	int T2_i1;
	int T2_o0;
	int T2_o1;
	int T2_W;

	int T3_i0;
	int T3_i1;
	int T3_o0;
	int T3_o1;
	int T3_W;

	int T4_i0;
	int T4_i1;
	int T4_o0;
	int T4_o1;
	int T4_W;

	int T5_i0;
	int T5_i1;
	int T5_o0;
	int T5_o1;
	int T5_W;

	int T6_i0;
	int T6_i1;
	int T6_o0;
	int T6_o1;
	int T6_W;

	int T7_i0;
	int T7_i1;
	int T7_o0;
	int T7_o1;
	int T7_W;

	int T8_i0;
	int T8_i1;
	int T8_o0;
	int T8_o1;
	int T8_W;

	int T9_i0;
	int T9_i1;
	int T9_o0;
	int T9_o1;
	int T9_W;

	int T10_i0;
	int T10_i1;
	int T10_o0;
	int T10_o1;
	int T10_W;

	int T11_i0;
	int T11_i1;
	int T11_o0;
	int T11_o1;
	int T11_W;

	int T12_i0;
	int T12_i1;
	int T12_o0;
	int T12_o1;
	int T12_W;

	int T13_i0;
	int T13_i1;
	int T13_o0;
	int T13_o1;
	int T13_W;

	int T14_i0;
	int T14_i1;
	int T14_o0;
	int T14_o1;
	int T14_W;

	int T15_i0;
	int T15_i1;
	int T15_o0;
	int T15_o1;
	int T15_W;

	int T16_i0;
	int T16_i1;
	int T16_o0;
	int T16_o1;
	int T16_W;

	int T17_i0;
	int T17_i1;
	int T17_o0;
	int T17_o1;
	int T17_W;

	int T18_i0;
	int T18_i1;
	int T18_o0;
	int T18_o1;
	int T18_W;

	int T19_i0;
	int T19_i1;
	int T19_o0;
	int T19_o1;
	int T19_W;

	int T20_i0;
	int T20_i1;
	int T20_o0;
	int T20_o1;
	int T20_W;

	int T21_i0;
	int T21_i1;
	int T21_o0;
	int T21_o1;
	int T21_W;

	int T22_i0;
	int T22_i1;
	int T22_o0;
	int T22_o1;
	int T22_W;

	int T23_i0;
	int T23_i1;
	int T23_o0;
	int T23_o1;
	int T23_W;

	int T24_i0;
	int T24_i1;
	int T24_o0;
	int T24_o1;
	int T24_W;

	int T25_i0;
	int T25_i1;
	int T25_o0;
	int T25_o1;
	int T25_W;

	int T26_i0;
	int T26_i1;
	int T26_o0;
	int T26_o1;
	int T26_W;

	int T27_i0;
	int T27_i1;
	int T27_o0;
	int T27_o1;
	int T27_W;

	int T28_i0;
	int T28_i1;
	int T28_o0;
	int T28_o1;
	int T28_W;

	int T29_i0;
	int T29_i1;
	int T29_o0;
	int T29_o1;
	int T29_W;

	int T30_i0;
	int T30_i1;
	int T30_o0;
	int T30_o1;
	int T30_W;

	int T31_i0;
	int T31_i1;
	int T31_o0;
	int T31_o1;
	int T31_W;

	int T32_i0;
	int T32_i1;
	int T32_o0;
	int T32_o1;
	int T32_W;

	int T33_i0;
	int T33_i1;
	int T33_o0;
	int T33_o1;
	int T33_W;

	int T34_i0;
	int T34_i1;
	int T34_o0;
	int T34_o1;
	int T34_W;

	int T35_i0;
	int T35_i1;
	int T35_o0;
	int T35_o1;
	int T35_W;

	int T36_i0;
	int T36_i1;
	int T36_o0;
	int T36_o1;
	int T36_W;

	int T37_i0;
	int T37_i1;
	int T37_o0;
	int T37_o1;
	int T37_W;

	int T38_i0;
	int T38_i1;
	int T38_o0;
	int T38_o1;
	int T38_W;

	int T39_i0;
	int T39_i1;
	int T39_o0;
	int T39_o1;
	int T39_W;

	int T40_i0;
	int T40_i1;
	int T40_o0;
	int T40_o1;
	int T40_W;

	int T41_i0;
	int T41_i1;
	int T41_o0;
	int T41_o1;
	int T41_W;

	int T42_i0;
	int T42_i1;
	int T42_o0;
	int T42_o1;
	int T42_W;

	int T43_i0;
	int T43_i1;
	int T43_o0;
	int T43_o1;
	int T43_W;

	int T44_i0;
	int T44_i1;
	int T44_o0;
	int T44_o1;
	int T44_W;

	int T45_i0;
	int T45_i1;
	int T45_o0;
	int T45_o1;
	int T45_W;

	int T46_i0;
	int T46_i1;
	int T46_o0;
	int T46_o1;
	int T46_W;

	int T47_i0;
	int T47_i1;
	int T47_o0;
	int T47_o1;
	int T47_W;

	int T48_i0;
	int T48_i1;
	int T48_o0;
	int T48_o1;
	int T48_W;

	int T49_i0;
	int T49_i1;
	int T49_o0;
	int T49_o1;
	int T49_W;

	int T50_i0;
	int T50_i1;
	int T50_o0;
	int T50_o1;
	int T50_W;

	int T51_i0;
	int T51_i1;
	int T51_o0;
	int T51_o1;
	int T51_W;

	int T52_i0;
	int T52_i1;
	int T52_o0;
	int T52_o1;
	int T52_W;

	int T53_i0;
	int T53_i1;
	int T53_o0;
	int T53_o1;
	int T53_W;

	int T54_i0;
	int T54_i1;
	int T54_o0;
	int T54_o1;
	int T54_W;

	int T55_i0;
	int T55_i1;
	int T55_o0;
	int T55_o1;
	int T55_W;

	int T56_i0;
	int T56_i1;
	int T56_o0;
	int T56_o1;
	int T56_W;

	int T57_i0;
	int T57_i1;
	int T57_o0;
	int T57_o1;
	int T57_W;

	int T58_i0;
	int T58_i1;
	int T58_o0;
	int T58_o1;
	int T58_W;

	int T59_i0;
	int T59_i1;
	int T59_o0;
	int T59_o1;
	int T59_W;

	int T60_i0;
	int T60_i1;
	int T60_o0;
	int T60_o1;
	int T60_W;

	int T61_i0;
	int T61_i1;
	int T61_o0;
	int T61_o1;
	int T61_W;

	int T62_i0;
	int T62_i1;
	int T62_o0;
	int T62_o1;
	int T62_W;

	int T63_i0;
	int T63_i1;
	int T63_o0;
	int T63_o1;
	int T63_W;

	int T64_i0;
	int T64_i1;
	int T64_o0;
	int T64_o1;
	int T64_W;

	int T65_i0;
	int T65_i1;
	int T65_o0;
	int T65_o1;
	int T65_W;

	int T66_i0;
	int T66_i1;
	int T66_o0;
	int T66_o1;
	int T66_W;

	int T67_i0;
	int T67_i1;
	int T67_o0;
	int T67_o1;
	int T67_W;

	int T68_i0;
	int T68_i1;
	int T68_o0;
	int T68_o1;
	int T68_W;

	int T69_i0;
	int T69_i1;
	int T69_o0;
	int T69_o1;
	int T69_W;

	int T70_i0;
	int T70_i1;
	int T70_o0;
	int T70_o1;
	int T70_W;

	int T71_i0;
	int T71_i1;
	int T71_o0;
	int T71_o1;
	int T71_W;

	int T72_i0;
	int T72_i1;
	int T72_o0;
	int T72_o1;
	int T72_W;

	int T73_i0;
	int T73_i1;
	int T73_o0;
	int T73_o1;
	int T73_W;

	int T74_i0;
	int T74_i1;
	int T74_o0;
	int T74_o1;
	int T74_W;

	int T75_i0;
	int T75_i1;
	int T75_o0;
	int T75_o1;
	int T75_W;

	int T76_i0;
	int T76_i1;
	int T76_o0;
	int T76_o1;
	int T76_W;

	int T77_i0;
	int T77_i1;
	int T77_o0;
	int T77_o1;
	int T77_W;

	int T78_i0;
	int T78_i1;
	int T78_o0;
	int T78_o1;
	int T78_W;

	int T79_i0;
	int T79_i1;
	int T79_o0;
	int T79_o1;
	int T79_W;

	int T80_i0;
	int T80_i1;
	int T80_o0;
	int T80_o1;
	int T80_W;

	int T81_i0;
	int T81_i1;
	int T81_o0;
	int T81_o1;
	int T81_W;

	int T82_i0;
	int T82_i1;
	int T82_o0;
	int T82_o1;
	int T82_W;

	int T83_i0;
	int T83_i1;
	int T83_o0;
	int T83_o1;
	int T83_W;

	int T84_i0;
	int T84_i1;
	int T84_o0;
	int T84_o1;
	int T84_W;

	int T85_i0;
	int T85_i1;
	int T85_o0;
	int T85_o1;
	int T85_W;

	int T86_i0;
	int T86_i1;
	int T86_o0;
	int T86_o1;
	int T86_W;

	int T87_i0;
	int T87_i1;
	int T87_o0;
	int T87_o1;
	int T87_W;

	int T88_i0;
	int T88_i1;
	int T88_o0;
	int T88_o1;
	int T88_W;

	int T89_i0;
	int T89_i1;
	int T89_o0;
	int T89_o1;
	int T89_W;

	int T90_i0;
	int T90_i1;
	int T90_o0;
	int T90_o1;
	int T90_W;

	int T91_i0;
	int T91_i1;
	int T91_o0;
	int T91_o1;
	int T91_W;

	int T92_i0;
	int T92_i1;
	int T92_o0;
	int T92_o1;
	int T92_W;

	int T93_i0;
	int T93_i1;
	int T93_o0;
	int T93_o1;
	int T93_W;

	int T94_i0;
	int T94_i1;
	int T94_o0;
	int T94_o1;
	int T94_W;

	int T95_i0;
	int T95_i1;
	int T95_o0;
	int T95_o1;
	int T95_W;

	int T96_i0;
	int T96_i1;
	int T96_o0;
	int T96_o1;
	int T96_W;

	int T97_i0;
	int T97_i1;
	int T97_o0;
	int T97_o1;
	int T97_W;

	int T98_i0;
	int T98_i1;
	int T98_o0;
	int T98_o1;
	int T98_W;

	int T99_i0;
	int T99_i1;
	int T99_o0;
	int T99_o1;
	int T99_W;

	int T100_i0;
	int T100_i1;
	int T100_o0;
	int T100_o1;
	int T100_W;

	int T101_i0;
	int T101_i1;
	int T101_o0;
	int T101_o1;
	int T101_W;

	int T102_i0;
	int T102_i1;
	int T102_o0;
	int T102_o1;
	int T102_W;

	int T103_i0;
	int T103_i1;
	int T103_o0;
	int T103_o1;
	int T103_W;

	int T104_i0;
	int T104_i1;
	int T104_o0;
	int T104_o1;
	int T104_W;

	int T105_i0;
	int T105_i1;
	int T105_o0;
	int T105_o1;
	int T105_W;

	int T106_i0;
	int T106_i1;
	int T106_o0;
	int T106_o1;
	int T106_W;

	int T107_i0;
	int T107_i1;
	int T107_o0;
	int T107_o1;
	int T107_W;

	int T108_i0;
	int T108_i1;
	int T108_o0;
	int T108_o1;
	int T108_W;

	int T109_i0;
	int T109_i1;
	int T109_o0;
	int T109_o1;
	int T109_W;

	int T110_i0;
	int T110_i1;
	int T110_o0;
	int T110_o1;
	int T110_W;

	int T111_i0;
	int T111_i1;
	int T111_o0;
	int T111_o1;
	int T111_W;

	int T112_i0;
	int T112_i1;
	int T112_o0;
	int T112_o1;
	int T112_W;

	int T113_i0;
	int T113_i1;
	int T113_o0;
	int T113_o1;
	int T113_W;

	int T114_i0;
	int T114_i1;
	int T114_o0;
	int T114_o1;
	int T114_W;

	int T115_i0;
	int T115_i1;
	int T115_o0;
	int T115_o1;
	int T115_W;

	int T116_i0;
	int T116_i1;
	int T116_o0;
	int T116_o1;
	int T116_W;

	int T117_i0;
	int T117_i1;
	int T117_o0;
	int T117_o1;
	int T117_W;

	int T118_i0;
	int T118_i1;
	int T118_o0;
	int T118_o1;
	int T118_W;

	int T119_i0;
	int T119_i1;
	int T119_o0;
	int T119_o1;
	int T119_W;

	int T120_i0;
	int T120_i1;
	int T120_o0;
	int T120_o1;
	int T120_W;

	int T121_i0;
	int T121_i1;
	int T121_o0;
	int T121_o1;
	int T121_W;

	int T122_i0;
	int T122_i1;
	int T122_o0;
	int T122_o1;
	int T122_W;

	int T123_i0;
	int T123_i1;
	int T123_o0;
	int T123_o1;
	int T123_W;

	int T124_i0;
	int T124_i1;
	int T124_o0;
	int T124_o1;
	int T124_W;

	int T125_i0;
	int T125_i1;
	int T125_o0;
	int T125_o1;
	int T125_W;

	int T126_i0;
	int T126_i1;
	int T126_o0;
	int T126_o1;
	int T126_W;

	int T127_i0;
	int T127_i1;
	int T127_o0;
	int T127_o1;
	int T127_W;

	int T128_i0;
	int T128_i1;
	int T128_o0;
	int T128_o1;
	int T128_W;

	int T129_i0;
	int T129_i1;
	int T129_o0;
	int T129_o1;
	int T129_W;

	int T130_i0;
	int T130_i1;
	int T130_o0;
	int T130_o1;
	int T130_W;

	int T131_i0;
	int T131_i1;
	int T131_o0;
	int T131_o1;
	int T131_W;

	int T132_i0;
	int T132_i1;
	int T132_o0;
	int T132_o1;
	int T132_W;

	int T133_i0;
	int T133_i1;
	int T133_o0;
	int T133_o1;
	int T133_W;

	int T134_i0;
	int T134_i1;
	int T134_o0;
	int T134_o1;
	int T134_W;

	int T135_i0;
	int T135_i1;
	int T135_o0;
	int T135_o1;
	int T135_W;

	int T136_i0;
	int T136_i1;
	int T136_o0;
	int T136_o1;
	int T136_W;

	int T137_i0;
	int T137_i1;
	int T137_o0;
	int T137_o1;
	int T137_W;

	int T138_i0;
	int T138_i1;
	int T138_o0;
	int T138_o1;
	int T138_W;

	int T139_i0;
	int T139_i1;
	int T139_o0;
	int T139_o1;
	int T139_W;

	int T140_i0;
	int T140_i1;
	int T140_o0;
	int T140_o1;
	int T140_W;

	int T141_i0;
	int T141_i1;
	int T141_o0;
	int T141_o1;
	int T141_W;

	int T142_i0;
	int T142_i1;
	int T142_o0;
	int T142_o1;
	int T142_W;

	int T143_i0;
	int T143_i1;
	int T143_o0;
	int T143_o1;
	int T143_W;

	int T144_i0;
	int T144_i1;
	int T144_o0;
	int T144_o1;
	int T144_W;

	int T145_i0;
	int T145_i1;
	int T145_o0;
	int T145_o1;
	int T145_W;

	int T146_i0;
	int T146_i1;
	int T146_o0;
	int T146_o1;
	int T146_W;

	int T147_i0;
	int T147_i1;
	int T147_o0;
	int T147_o1;
	int T147_W;

	int T148_i0;
	int T148_i1;
	int T148_o0;
	int T148_o1;
	int T148_W;

	int T149_i0;
	int T149_i1;
	int T149_o0;
	int T149_o1;
	int T149_W;

	int T150_i0;
	int T150_i1;
	int T150_o0;
	int T150_o1;
	int T150_W;

	int T151_i0;
	int T151_i1;
	int T151_o0;
	int T151_o1;
	int T151_W;

	int T152_i0;
	int T152_i1;
	int T152_o0;
	int T152_o1;
	int T152_W;

	int T153_i0;
	int T153_i1;
	int T153_o0;
	int T153_o1;
	int T153_W;

	int T154_i0;
	int T154_i1;
	int T154_o0;
	int T154_o1;
	int T154_W;

	int T155_i0;
	int T155_i1;
	int T155_o0;
	int T155_o1;
	int T155_W;

	int T156_i0;
	int T156_i1;
	int T156_o0;
	int T156_o1;
	int T156_W;

	int T157_i0;
	int T157_i1;
	int T157_o0;
	int T157_o1;
	int T157_W;

	int T158_i0;
	int T158_i1;
	int T158_o0;
	int T158_o1;
	int T158_W;

	int T159_i0;
	int T159_i1;
	int T159_o0;
	int T159_o1;
	int T159_W;

	int T160_i0;
	int T160_i1;
	int T160_o0;
	int T160_o1;
	int T160_W;

	int T161_i0;
	int T161_i1;
	int T161_o0;
	int T161_o1;
	int T161_W;

	int T162_i0;
	int T162_i1;
	int T162_o0;
	int T162_o1;
	int T162_W;

	int T163_i0;
	int T163_i1;
	int T163_o0;
	int T163_o1;
	int T163_W;

	int T164_i0;
	int T164_i1;
	int T164_o0;
	int T164_o1;
	int T164_W;

	int T165_i0;
	int T165_i1;
	int T165_o0;
	int T165_o1;
	int T165_W;

	int T166_i0;
	int T166_i1;
	int T166_o0;
	int T166_o1;
	int T166_W;

	int T167_i0;
	int T167_i1;
	int T167_o0;
	int T167_o1;
	int T167_W;

	int T168_i0;
	int T168_i1;
	int T168_o0;
	int T168_o1;
	int T168_W;

	int T169_i0;
	int T169_i1;
	int T169_o0;
	int T169_o1;
	int T169_W;

	int T170_i0;
	int T170_i1;
	int T170_o0;
	int T170_o1;
	int T170_W;

	int T171_i0;
	int T171_i1;
	int T171_o0;
	int T171_o1;
	int T171_W;

	int T172_i0;
	int T172_i1;
	int T172_o0;
	int T172_o1;
	int T172_W;

	int T173_i0;
	int T173_i1;
	int T173_o0;
	int T173_o1;
	int T173_W;

	int T174_i0;
	int T174_i1;
	int T174_o0;
	int T174_o1;
	int T174_W;

	int T175_i0;
	int T175_i1;
	int T175_o0;
	int T175_o1;
	int T175_W;

	int T176_i0;
	int T176_i1;
	int T176_o0;
	int T176_o1;
	int T176_W;

	int T177_i0;
	int T177_i1;
	int T177_o0;
	int T177_o1;
	int T177_W;

	int T178_i0;
	int T178_i1;
	int T178_o0;
	int T178_o1;
	int T178_W;

	int T179_i0;
	int T179_i1;
	int T179_o0;
	int T179_o1;
	int T179_W;

	int T180_i0;
	int T180_i1;
	int T180_o0;
	int T180_o1;
	int T180_W;

	int T181_i0;
	int T181_i1;
	int T181_o0;
	int T181_o1;
	int T181_W;

	int T182_i0;
	int T182_i1;
	int T182_o0;
	int T182_o1;
	int T182_W;

	int T183_i0;
	int T183_i1;
	int T183_o0;
	int T183_o1;
	int T183_W;

	int T184_i0;
	int T184_i1;
	int T184_o0;
	int T184_o1;
	int T184_W;

	int T185_i0;
	int T185_i1;
	int T185_o0;
	int T185_o1;
	int T185_W;

	int T186_i0;
	int T186_i1;
	int T186_o0;
	int T186_o1;
	int T186_W;

	int T187_i0;
	int T187_i1;
	int T187_o0;
	int T187_o1;
	int T187_W;

	int T188_i0;
	int T188_i1;
	int T188_o0;
	int T188_o1;
	int T188_W;

	int T189_i0;
	int T189_i1;
	int T189_o0;
	int T189_o1;
	int T189_W;

	int T190_i0;
	int T190_i1;
	int T190_o0;
	int T190_o1;
	int T190_W;

	int T191_i0;
	int T191_i1;
	int T191_o0;
	int T191_o1;
	int T191_W;

	int T192_i0;
	int T192_i1;
	int T192_o0;
	int T192_o1;
	int T192_W;

	int T193_i0;
	int T193_i1;
	int T193_o0;
	int T193_o1;
	int T193_W;

	int T194_i0;
	int T194_i1;
	int T194_o0;
	int T194_o1;
	int T194_W;

	int T195_i0;
	int T195_i1;
	int T195_o0;
	int T195_o1;
	int T195_W;

	int T196_i0;
	int T196_i1;
	int T196_o0;
	int T196_o1;
	int T196_W;

	int T197_i0;
	int T197_i1;
	int T197_o0;
	int T197_o1;
	int T197_W;

	int T198_i0;
	int T198_i1;
	int T198_o0;
	int T198_o1;
	int T198_W;

	int T199_i0;
	int T199_i1;
	int T199_o0;
	int T199_o1;
	int T199_W;

	int T200_i0;
	int T200_i1;
	int T200_o0;
	int T200_o1;
	int T200_W;

	int T201_i0;
	int T201_i1;
	int T201_o0;
	int T201_o1;
	int T201_W;

	int T202_i0;
	int T202_i1;
	int T202_o0;
	int T202_o1;
	int T202_W;

	int T203_i0;
	int T203_i1;
	int T203_o0;
	int T203_o1;
	int T203_W;

	int T204_i0;
	int T204_i1;
	int T204_o0;
	int T204_o1;
	int T204_W;

	int T205_i0;
	int T205_i1;
	int T205_o0;
	int T205_o1;
	int T205_W;

	int T206_i0;
	int T206_i1;
	int T206_o0;
	int T206_o1;
	int T206_W;

	int T207_i0;
	int T207_i1;
	int T207_o0;
	int T207_o1;
	int T207_W;

	int T208_i0;
	int T208_i1;
	int T208_o0;
	int T208_o1;
	int T208_W;

	int T209_i0;
	int T209_i1;
	int T209_o0;
	int T209_o1;
	int T209_W;

	int T210_i0;
	int T210_i1;
	int T210_o0;
	int T210_o1;
	int T210_W;

	int T211_i0;
	int T211_i1;
	int T211_o0;
	int T211_o1;
	int T211_W;

	int T212_i0;
	int T212_i1;
	int T212_o0;
	int T212_o1;
	int T212_W;

	int T213_i0;
	int T213_i1;
	int T213_o0;
	int T213_o1;
	int T213_W;

	int T214_i0;
	int T214_i1;
	int T214_o0;
	int T214_o1;
	int T214_W;

	int T215_i0;
	int T215_i1;
	int T215_o0;
	int T215_o1;
	int T215_W;

	int T216_i0;
	int T216_i1;
	int T216_o0;
	int T216_o1;
	int T216_W;

	int T217_i0;
	int T217_i1;
	int T217_o0;
	int T217_o1;
	int T217_W;

	int T218_i0;
	int T218_i1;
	int T218_o0;
	int T218_o1;
	int T218_W;

	int T219_i0;
	int T219_i1;
	int T219_o0;
	int T219_o1;
	int T219_W;

	int T220_i0;
	int T220_i1;
	int T220_o0;
	int T220_o1;
	int T220_W;

	int T221_i0;
	int T221_i1;
	int T221_o0;
	int T221_o1;
	int T221_W;

	int T222_i0;
	int T222_i1;
	int T222_o0;
	int T222_o1;
	int T222_W;

	int T223_i0;
	int T223_i1;
	int T223_o0;
	int T223_o1;
	int T223_W;

	int T224_i0;
	int T224_i1;
	int T224_o0;
	int T224_o1;
	int T224_W;

	int T225_i0;
	int T225_i1;
	int T225_o0;
	int T225_o1;
	int T225_W;

	int T226_i0;
	int T226_i1;
	int T226_o0;
	int T226_o1;
	int T226_W;

	int T227_i0;
	int T227_i1;
	int T227_o0;
	int T227_o1;
	int T227_W;

	int T228_i0;
	int T228_i1;
	int T228_o0;
	int T228_o1;
	int T228_W;

	int T229_i0;
	int T229_i1;
	int T229_o0;
	int T229_o1;
	int T229_W;

	int T230_i0;
	int T230_i1;
	int T230_o0;
	int T230_o1;
	int T230_W;

	int T231_i0;
	int T231_i1;
	int T231_o0;
	int T231_o1;
	int T231_W;

	int T232_i0;
	int T232_i1;
	int T232_o0;
	int T232_o1;
	int T232_W;

	int T233_i0;
	int T233_i1;
	int T233_o0;
	int T233_o1;
	int T233_W;

	int T234_i0;
	int T234_i1;
	int T234_o0;
	int T234_o1;
	int T234_W;

	int T235_i0;
	int T235_i1;
	int T235_o0;
	int T235_o1;
	int T235_W;

	int T236_i0;
	int T236_i1;
	int T236_o0;
	int T236_o1;
	int T236_W;

	int T237_i0;
	int T237_i1;
	int T237_o0;
	int T237_o1;
	int T237_W;

	int T238_i0;
	int T238_i1;
	int T238_o0;
	int T238_o1;
	int T238_W;

	int T239_i0;
	int T239_i1;
	int T239_o0;
	int T239_o1;
	int T239_W;

	int T240_i0;
	int T240_i1;
	int T240_o0;
	int T240_o1;
	int T240_W;

	int T241_i0;
	int T241_i1;
	int T241_o0;
	int T241_o1;
	int T241_W;

	int T242_i0;
	int T242_i1;
	int T242_o0;
	int T242_o1;
	int T242_W;

	int T243_i0;
	int T243_i1;
	int T243_o0;
	int T243_o1;
	int T243_W;

	int T244_i0;
	int T244_i1;
	int T244_o0;
	int T244_o1;
	int T244_W;

	int T245_i0;
	int T245_i1;
	int T245_o0;
	int T245_o1;
	int T245_W;

	int T246_i0;
	int T246_i1;
	int T246_o0;
	int T246_o1;
	int T246_W;

	int T247_i0;
	int T247_i1;
	int T247_o0;
	int T247_o1;
	int T247_W;

	int T248_i0;
	int T248_i1;
	int T248_o0;
	int T248_o1;
	int T248_W;

	int T249_i0;
	int T249_i1;
	int T249_o0;
	int T249_o1;
	int T249_W;

	int T250_i0;
	int T250_i1;
	int T250_o0;
	int T250_o1;
	int T250_W;

	int T251_i0;
	int T251_i1;
	int T251_o0;
	int T251_o1;
	int T251_W;

	int T252_i0;
	int T252_i1;
	int T252_o0;
	int T252_o1;
	int T252_W;

	int T253_i0;
	int T253_i1;
	int T253_o0;
	int T253_o1;
	int T253_W;

	int T254_i0;
	int T254_i1;
	int T254_o0;
	int T254_o1;
	int T254_W;

	int T255_i0;
	int T255_i1;
	int T255_o0;
	int T255_o1;
	int T255_W;


  // **** Parameter initialisation **** //
T0_W = 16384;
T1_W = 16384;
T2_W = 16384;
T3_W = 16384;
T4_W = 16384;
T5_W = 16384;
T6_W = 16384;
T7_W = 16384;
T8_W = 16384;
T9_W = 16384;
T10_W = 16384;
T11_W = 16384;
T12_W = 16384;
T13_W = 16384;
T14_W = 16384;
T15_W = 16384;
T16_W = 16384;
T17_W = 16384;
T18_W = 16384;
T19_W = 16384;
T20_W = 16384;
T21_W = 16384;
T22_W = 16384;
T23_W = 16384;
T24_W = 16384;
T25_W = 16384;
T26_W = 16384;
T27_W = 16384;
T28_W = 16384;
T29_W = 16384;
T30_W = 16384;
T31_W = 16384;
T32_W = 16384;
T33_W = 16384;
T34_W = 16384;
T35_W = 16384;
T36_W = 16384;
T37_W = 16384;
T38_W = 16384;
T39_W = 16384;
T40_W = 16384;
T41_W = 16384;
T42_W = 16384;
T43_W = 16384;
T44_W = 16384;
T45_W = 16384;
T46_W = 16384;
T47_W = 16384;
T48_W = 16384;
T49_W = 16384;
T50_W = 16384;
T51_W = 16384;
T52_W = 16384;
T53_W = 16384;
T54_W = 16384;
T55_W = 16384;
T56_W = 16384;
T57_W = 16384;
T58_W = 16384;
T59_W = 16384;
T60_W = 16384;
T61_W = 16384;
T62_W = 16384;
T63_W = 16384;
T64_W = 16384;
T65_W = 16384;
T66_W = 16384;
T67_W = 16384;
T68_W = 16384;
T69_W = 16384;
T70_W = 16384;
T71_W = 16384;
T72_W = 16384;
T73_W = 16384;
T74_W = 16384;
T75_W = 16384;
T76_W = 16384;
T77_W = 16384;
T78_W = 16384;
T79_W = 16384;
T80_W = 16384;
T81_W = 16384;
T82_W = 16384;
T83_W = 16384;
T84_W = 16384;
T85_W = 16384;
T86_W = 16384;
T87_W = 16384;
T88_W = 16384;
T89_W = 16384;
T90_W = 16384;
T91_W = 16384;
T92_W = 16384;
T93_W = 16384;
T94_W = 16384;
T95_W = 16384;
T96_W = 16384;
T97_W = 16384;
T98_W = 16384;
T99_W = 16384;
T100_W = 16384;
T101_W = 16384;
T102_W = 16384;
T103_W = 16384;
T104_W = 16384;
T105_W = 16384;
T106_W = 16384;
T107_W = 16384;
T108_W = 16384;
T109_W = 16384;
T110_W = 16384;
T111_W = 16384;
T112_W = 16384;
T113_W = 16384;
T114_W = 16384;
T115_W = 16384;
T116_W = 16384;
T117_W = 16384;
T118_W = 16384;
T119_W = 16384;
T120_W = 16384;
T121_W = 16384;
T122_W = 16384;
T123_W = 16384;
T124_W = 16384;
T125_W = 16384;
T126_W = 16384;
T127_W = 16384;
T128_W = 16384;
T129_W = 16384;
T130_W = 16384;
T131_W = 16384;
T132_W = 16384;
T133_W = 16384;
T134_W = 16384;
T135_W = 16384;
T136_W = 16384;
T137_W = 16384;
T138_W = 16384;
T139_W = 16384;
T140_W = 16384;
T141_W = 16384;
T142_W = 16384;
T143_W = 16384;
T144_W = 16384;
T145_W = 16384;
T146_W = 16384;
T147_W = 16384;
T148_W = 16384;
T149_W = 16384;
T150_W = 16384;
T151_W = 16384;
T152_W = 16384;
T153_W = 16384;
T154_W = 16384;
T155_W = 16384;
T156_W = 16384;
T157_W = 16384;
T158_W = 16384;
T159_W = 16384;
T160_W = 16384;
T161_W = 16384;
T162_W = 16384;
T163_W = 16384;
T164_W = 16384;
T165_W = 16384;
T166_W = 16384;
T167_W = 16384;
T168_W = 16384;
T169_W = 16384;
T170_W = 16384;
T171_W = 16384;
T172_W = 16384;
T173_W = 16384;
T174_W = 16384;
T175_W = 16384;
T176_W = 16384;
T177_W = 16384;
T178_W = 16384;
T179_W = 16384;
T180_W = 16384;
T181_W = 16384;
T182_W = 16384;
T183_W = 16384;
T184_W = 16384;
T185_W = 16384;
T186_W = 16384;
T187_W = 16384;
T188_W = 16384;
T189_W = 16384;
T190_W = 16384;
T191_W = 16384;
T192_W = 16384;
T193_W = 16384;
T194_W = 16384;
T195_W = 16384;
T196_W = 16384;
T197_W = 16384;
T198_W = 16384;
T199_W = 16384;
T200_W = 16384;
T201_W = 16384;
T202_W = 16384;
T203_W = 16384;
T204_W = 16384;
T205_W = 16384;
T206_W = 16384;
T207_W = 16384;
T208_W = 16384;
T209_W = 16384;
T210_W = 16384;
T211_W = 16384;
T212_W = 16384;
T213_W = 16384;
T214_W = 16384;
T215_W = 16384;
T216_W = 16384;
T217_W = 16384;
T218_W = 16384;
T219_W = 16384;
T220_W = 16384;
T221_W = 16384;
T222_W = 16384;
T223_W = 16384;
T224_W = 16384;
T225_W = 16384;
T226_W = 16384;
T227_W = 16384;
T228_W = 16384;
T229_W = 16384;
T230_W = 16384;
T231_W = 16384;
T232_W = 16384;
T233_W = 16384;
T234_W = 16384;
T235_W = 16384;
T236_W = 16384;
T237_W = 16384;
T238_W = 16384;
T239_W = 16384;
T240_W = 16384;
T241_W = 16384;
T242_W = 16384;
T243_W = 16384;
T244_W = 16384;
T245_W = 16384;
T246_W = 16384;
T247_W = 16384;
T248_W = 16384;
T249_W = 16384;
T250_W = 16384;
T251_W = 16384;
T252_W = 16384;
T253_W = 16384;
T254_W = 16384;
T255_W = 16384;

  // **** Code body **** //

	GET_FIFO(T0_i0, 0);
	GET_FIFO(T0_i1, 0);
	Butterfly(T0_i0, T0_i1, &T0_o0, &T0_o1, T0_W);
	PUT_FIFO(T0_o0, 0);
	PUT_FIFO(T0_o1, 0);

	GET_FIFO(T1_i0, 0);
	GET_FIFO(T1_i1, 0);
	Butterfly(T1_i0, T1_i1, &T1_o0, &T1_o1, T1_W);
	PUT_FIFO(T1_o0, 1);
	PUT_FIFO(T1_o1, 1);

	GET_FIFO(T2_i0, 0);
	GET_FIFO(T2_i1, 0);
	Butterfly(T2_i0, T2_i1, &T2_o0, &T2_o1, T2_W);
	PUT_FIFO(T2_o0, 0);
	PUT_FIFO(T2_o1, 0);

	GET_FIFO(T3_i0, 0);
	GET_FIFO(T3_i1, 0);
	Butterfly(T3_i0, T3_i1, &T3_o0, &T3_o1, T3_W);
	PUT_FIFO(T3_o0, 1);
	PUT_FIFO(T3_o1, 1);

	GET_FIFO(T4_i0, 0);
	GET_FIFO(T4_i1, 0);
	Butterfly(T4_i0, T4_i1, &T4_o0, &T4_o1, T4_W);
	PUT_FIFO(T4_o0, 0);
	PUT_FIFO(T4_o1, 0);

	GET_FIFO(T5_i0, 0);
	GET_FIFO(T5_i1, 0);
	Butterfly(T5_i0, T5_i1, &T5_o0, &T5_o1, T5_W);
	PUT_FIFO(T5_o0, 1);
	PUT_FIFO(T5_o1, 1);

	GET_FIFO(T6_i0, 0);
	GET_FIFO(T6_i1, 0);
	Butterfly(T6_i0, T6_i1, &T6_o0, &T6_o1, T6_W);
	PUT_FIFO(T6_o0, 0);
	PUT_FIFO(T6_o1, 0);

	GET_FIFO(T7_i0, 0);
	GET_FIFO(T7_i1, 0);
	Butterfly(T7_i0, T7_i1, &T7_o0, &T7_o1, T7_W);
	PUT_FIFO(T7_o0, 1);
	PUT_FIFO(T7_o1, 1);

	GET_FIFO(T8_i0, 0);
	GET_FIFO(T8_i1, 0);
	Butterfly(T8_i0, T8_i1, &T8_o0, &T8_o1, T8_W);
	PUT_FIFO(T8_o0, 0);
	PUT_FIFO(T8_o1, 0);

	GET_FIFO(T9_i0, 0);
	GET_FIFO(T9_i1, 0);
	Butterfly(T9_i0, T9_i1, &T9_o0, &T9_o1, T9_W);
	PUT_FIFO(T9_o0, 1);
	PUT_FIFO(T9_o1, 1);

	GET_FIFO(T10_i0, 0);
	GET_FIFO(T10_i1, 0);
	Butterfly(T10_i0, T10_i1, &T10_o0, &T10_o1, T10_W);
	PUT_FIFO(T10_o0, 0);
	PUT_FIFO(T10_o1, 0);

	GET_FIFO(T11_i0, 0);
	GET_FIFO(T11_i1, 0);
	Butterfly(T11_i0, T11_i1, &T11_o0, &T11_o1, T11_W);
	PUT_FIFO(T11_o0, 1);
	PUT_FIFO(T11_o1, 1);

	GET_FIFO(T12_i0, 0);
	GET_FIFO(T12_i1, 0);
	Butterfly(T12_i0, T12_i1, &T12_o0, &T12_o1, T12_W);
	PUT_FIFO(T12_o0, 0);
	PUT_FIFO(T12_o1, 0);

	GET_FIFO(T13_i0, 0);
	GET_FIFO(T13_i1, 0);
	Butterfly(T13_i0, T13_i1, &T13_o0, &T13_o1, T13_W);
	PUT_FIFO(T13_o0, 1);
	PUT_FIFO(T13_o1, 1);

	GET_FIFO(T14_i0, 0);
	GET_FIFO(T14_i1, 0);
	Butterfly(T14_i0, T14_i1, &T14_o0, &T14_o1, T14_W);
	PUT_FIFO(T14_o0, 0);
	PUT_FIFO(T14_o1, 0);

	GET_FIFO(T15_i0, 0);
	GET_FIFO(T15_i1, 0);
	Butterfly(T15_i0, T15_i1, &T15_o0, &T15_o1, T15_W);
	PUT_FIFO(T15_o0, 1);
	PUT_FIFO(T15_o1, 1);

	GET_FIFO(T16_i0, 0);
	GET_FIFO(T16_i1, 0);
	Butterfly(T16_i0, T16_i1, &T16_o0, &T16_o1, T16_W);
	PUT_FIFO(T16_o0, 0);
	PUT_FIFO(T16_o1, 0);

	GET_FIFO(T17_i0, 0);
	GET_FIFO(T17_i1, 0);
	Butterfly(T17_i0, T17_i1, &T17_o0, &T17_o1, T17_W);
	PUT_FIFO(T17_o0, 1);
	PUT_FIFO(T17_o1, 1);

	GET_FIFO(T18_i0, 0);
	GET_FIFO(T18_i1, 0);
	Butterfly(T18_i0, T18_i1, &T18_o0, &T18_o1, T18_W);
	PUT_FIFO(T18_o0, 0);
	PUT_FIFO(T18_o1, 0);

	GET_FIFO(T19_i0, 0);
	GET_FIFO(T19_i1, 0);
	Butterfly(T19_i0, T19_i1, &T19_o0, &T19_o1, T19_W);
	PUT_FIFO(T19_o0, 1);
	PUT_FIFO(T19_o1, 1);

	GET_FIFO(T20_i0, 0);
	GET_FIFO(T20_i1, 0);
	Butterfly(T20_i0, T20_i1, &T20_o0, &T20_o1, T20_W);
	PUT_FIFO(T20_o0, 0);
	PUT_FIFO(T20_o1, 0);

	GET_FIFO(T21_i0, 0);
	GET_FIFO(T21_i1, 0);
	Butterfly(T21_i0, T21_i1, &T21_o0, &T21_o1, T21_W);
	PUT_FIFO(T21_o0, 1);
	PUT_FIFO(T21_o1, 1);

	GET_FIFO(T22_i0, 0);
	GET_FIFO(T22_i1, 0);
	Butterfly(T22_i0, T22_i1, &T22_o0, &T22_o1, T22_W);
	PUT_FIFO(T22_o0, 0);
	PUT_FIFO(T22_o1, 0);

	GET_FIFO(T23_i0, 0);
	GET_FIFO(T23_i1, 0);
	Butterfly(T23_i0, T23_i1, &T23_o0, &T23_o1, T23_W);
	PUT_FIFO(T23_o0, 1);
	PUT_FIFO(T23_o1, 1);

	GET_FIFO(T24_i0, 0);
	GET_FIFO(T24_i1, 0);
	Butterfly(T24_i0, T24_i1, &T24_o0, &T24_o1, T24_W);
	PUT_FIFO(T24_o0, 0);
	PUT_FIFO(T24_o1, 0);

	GET_FIFO(T25_i0, 0);
	GET_FIFO(T25_i1, 0);
	Butterfly(T25_i0, T25_i1, &T25_o0, &T25_o1, T25_W);
	PUT_FIFO(T25_o0, 1);
	PUT_FIFO(T25_o1, 1);

	GET_FIFO(T26_i0, 0);
	GET_FIFO(T26_i1, 0);
	Butterfly(T26_i0, T26_i1, &T26_o0, &T26_o1, T26_W);
	PUT_FIFO(T26_o0, 0);
	PUT_FIFO(T26_o1, 0);

	GET_FIFO(T27_i0, 0);
	GET_FIFO(T27_i1, 0);
	Butterfly(T27_i0, T27_i1, &T27_o0, &T27_o1, T27_W);
	PUT_FIFO(T27_o0, 1);
	PUT_FIFO(T27_o1, 1);

	GET_FIFO(T28_i0, 0);
	GET_FIFO(T28_i1, 0);
	Butterfly(T28_i0, T28_i1, &T28_o0, &T28_o1, T28_W);
	PUT_FIFO(T28_o0, 0);
	PUT_FIFO(T28_o1, 0);

	GET_FIFO(T29_i0, 0);
	GET_FIFO(T29_i1, 0);
	Butterfly(T29_i0, T29_i1, &T29_o0, &T29_o1, T29_W);
	PUT_FIFO(T29_o0, 1);
	PUT_FIFO(T29_o1, 1);

	GET_FIFO(T30_i0, 0);
	GET_FIFO(T30_i1, 0);
	Butterfly(T30_i0, T30_i1, &T30_o0, &T30_o1, T30_W);
	PUT_FIFO(T30_o0, 0);
	PUT_FIFO(T30_o1, 0);

	GET_FIFO(T31_i0, 0);
	GET_FIFO(T31_i1, 0);
	Butterfly(T31_i0, T31_i1, &T31_o0, &T31_o1, T31_W);
	PUT_FIFO(T31_o0, 1);
	PUT_FIFO(T31_o1, 1);

	GET_FIFO(T32_i0, 0);
	GET_FIFO(T32_i1, 0);
	Butterfly(T32_i0, T32_i1, &T32_o0, &T32_o1, T32_W);
	PUT_FIFO(T32_o0, 0);
	PUT_FIFO(T32_o1, 0);

	GET_FIFO(T33_i0, 0);
	GET_FIFO(T33_i1, 0);
	Butterfly(T33_i0, T33_i1, &T33_o0, &T33_o1, T33_W);
	PUT_FIFO(T33_o0, 1);
	PUT_FIFO(T33_o1, 1);

	GET_FIFO(T34_i0, 0);
	GET_FIFO(T34_i1, 0);
	Butterfly(T34_i0, T34_i1, &T34_o0, &T34_o1, T34_W);
	PUT_FIFO(T34_o0, 0);
	PUT_FIFO(T34_o1, 0);

	GET_FIFO(T35_i0, 0);
	GET_FIFO(T35_i1, 0);
	Butterfly(T35_i0, T35_i1, &T35_o0, &T35_o1, T35_W);
	PUT_FIFO(T35_o0, 1);
	PUT_FIFO(T35_o1, 1);

	GET_FIFO(T36_i0, 0);
	GET_FIFO(T36_i1, 0);
	Butterfly(T36_i0, T36_i1, &T36_o0, &T36_o1, T36_W);
	PUT_FIFO(T36_o0, 0);
	PUT_FIFO(T36_o1, 0);

	GET_FIFO(T37_i0, 0);
	GET_FIFO(T37_i1, 0);
	Butterfly(T37_i0, T37_i1, &T37_o0, &T37_o1, T37_W);
	PUT_FIFO(T37_o0, 1);
	PUT_FIFO(T37_o1, 1);

	GET_FIFO(T38_i0, 0);
	GET_FIFO(T38_i1, 0);
	Butterfly(T38_i0, T38_i1, &T38_o0, &T38_o1, T38_W);
	PUT_FIFO(T38_o0, 0);
	PUT_FIFO(T38_o1, 0);

	GET_FIFO(T39_i0, 0);
	GET_FIFO(T39_i1, 0);
	Butterfly(T39_i0, T39_i1, &T39_o0, &T39_o1, T39_W);
	PUT_FIFO(T39_o0, 1);
	PUT_FIFO(T39_o1, 1);

	GET_FIFO(T40_i0, 0);
	GET_FIFO(T40_i1, 0);
	Butterfly(T40_i0, T40_i1, &T40_o0, &T40_o1, T40_W);
	PUT_FIFO(T40_o0, 0);
	PUT_FIFO(T40_o1, 0);

	GET_FIFO(T41_i0, 0);
	GET_FIFO(T41_i1, 0);
	Butterfly(T41_i0, T41_i1, &T41_o0, &T41_o1, T41_W);
	PUT_FIFO(T41_o0, 1);
	PUT_FIFO(T41_o1, 1);

	GET_FIFO(T42_i0, 0);
	GET_FIFO(T42_i1, 0);
	Butterfly(T42_i0, T42_i1, &T42_o0, &T42_o1, T42_W);
	PUT_FIFO(T42_o0, 0);
	PUT_FIFO(T42_o1, 0);

	GET_FIFO(T43_i0, 0);
	GET_FIFO(T43_i1, 0);
	Butterfly(T43_i0, T43_i1, &T43_o0, &T43_o1, T43_W);
	PUT_FIFO(T43_o0, 1);
	PUT_FIFO(T43_o1, 1);

	GET_FIFO(T44_i0, 0);
	GET_FIFO(T44_i1, 0);
	Butterfly(T44_i0, T44_i1, &T44_o0, &T44_o1, T44_W);
	PUT_FIFO(T44_o0, 0);
	PUT_FIFO(T44_o1, 0);

	GET_FIFO(T45_i0, 0);
	GET_FIFO(T45_i1, 0);
	Butterfly(T45_i0, T45_i1, &T45_o0, &T45_o1, T45_W);
	PUT_FIFO(T45_o0, 1);
	PUT_FIFO(T45_o1, 1);

	GET_FIFO(T46_i0, 0);
	GET_FIFO(T46_i1, 0);
	Butterfly(T46_i0, T46_i1, &T46_o0, &T46_o1, T46_W);
	PUT_FIFO(T46_o0, 0);
	PUT_FIFO(T46_o1, 0);

	GET_FIFO(T47_i0, 0);
	GET_FIFO(T47_i1, 0);
	Butterfly(T47_i0, T47_i1, &T47_o0, &T47_o1, T47_W);
	PUT_FIFO(T47_o0, 1);
	PUT_FIFO(T47_o1, 1);

	GET_FIFO(T48_i0, 0);
	GET_FIFO(T48_i1, 0);
	Butterfly(T48_i0, T48_i1, &T48_o0, &T48_o1, T48_W);
	PUT_FIFO(T48_o0, 0);
	PUT_FIFO(T48_o1, 0);

	GET_FIFO(T49_i0, 0);
	GET_FIFO(T49_i1, 0);
	Butterfly(T49_i0, T49_i1, &T49_o0, &T49_o1, T49_W);
	PUT_FIFO(T49_o0, 1);
	PUT_FIFO(T49_o1, 1);

	GET_FIFO(T50_i0, 0);
	GET_FIFO(T50_i1, 0);
	Butterfly(T50_i0, T50_i1, &T50_o0, &T50_o1, T50_W);
	PUT_FIFO(T50_o0, 0);
	PUT_FIFO(T50_o1, 0);

	GET_FIFO(T51_i0, 0);
	GET_FIFO(T51_i1, 0);
	Butterfly(T51_i0, T51_i1, &T51_o0, &T51_o1, T51_W);
	PUT_FIFO(T51_o0, 1);
	PUT_FIFO(T51_o1, 1);

	GET_FIFO(T52_i0, 0);
	GET_FIFO(T52_i1, 0);
	Butterfly(T52_i0, T52_i1, &T52_o0, &T52_o1, T52_W);
	PUT_FIFO(T52_o0, 0);
	PUT_FIFO(T52_o1, 0);

	GET_FIFO(T53_i0, 0);
	GET_FIFO(T53_i1, 0);
	Butterfly(T53_i0, T53_i1, &T53_o0, &T53_o1, T53_W);
	PUT_FIFO(T53_o0, 1);
	PUT_FIFO(T53_o1, 1);

	GET_FIFO(T54_i0, 0);
	GET_FIFO(T54_i1, 0);
	Butterfly(T54_i0, T54_i1, &T54_o0, &T54_o1, T54_W);
	PUT_FIFO(T54_o0, 0);
	PUT_FIFO(T54_o1, 0);

	GET_FIFO(T55_i0, 0);
	GET_FIFO(T55_i1, 0);
	Butterfly(T55_i0, T55_i1, &T55_o0, &T55_o1, T55_W);
	PUT_FIFO(T55_o0, 1);
	PUT_FIFO(T55_o1, 1);

	GET_FIFO(T56_i0, 0);
	GET_FIFO(T56_i1, 0);
	Butterfly(T56_i0, T56_i1, &T56_o0, &T56_o1, T56_W);
	PUT_FIFO(T56_o0, 0);
	PUT_FIFO(T56_o1, 0);

	GET_FIFO(T57_i0, 0);
	GET_FIFO(T57_i1, 0);
	Butterfly(T57_i0, T57_i1, &T57_o0, &T57_o1, T57_W);
	PUT_FIFO(T57_o0, 1);
	PUT_FIFO(T57_o1, 1);

	GET_FIFO(T58_i0, 0);
	GET_FIFO(T58_i1, 0);
	Butterfly(T58_i0, T58_i1, &T58_o0, &T58_o1, T58_W);
	PUT_FIFO(T58_o0, 0);
	PUT_FIFO(T58_o1, 0);

	GET_FIFO(T59_i0, 0);
	GET_FIFO(T59_i1, 0);
	Butterfly(T59_i0, T59_i1, &T59_o0, &T59_o1, T59_W);
	PUT_FIFO(T59_o0, 1);
	PUT_FIFO(T59_o1, 1);

	GET_FIFO(T60_i0, 0);
	GET_FIFO(T60_i1, 0);
	Butterfly(T60_i0, T60_i1, &T60_o0, &T60_o1, T60_W);
	PUT_FIFO(T60_o0, 0);
	PUT_FIFO(T60_o1, 0);

	GET_FIFO(T61_i0, 0);
	GET_FIFO(T61_i1, 0);
	Butterfly(T61_i0, T61_i1, &T61_o0, &T61_o1, T61_W);
	PUT_FIFO(T61_o0, 1);
	PUT_FIFO(T61_o1, 1);

	GET_FIFO(T62_i0, 0);
	GET_FIFO(T62_i1, 0);
	Butterfly(T62_i0, T62_i1, &T62_o0, &T62_o1, T62_W);
	PUT_FIFO(T62_o0, 0);
	PUT_FIFO(T62_o1, 0);

	GET_FIFO(T63_i0, 0);
	GET_FIFO(T63_i1, 0);
	Butterfly(T63_i0, T63_i1, &T63_o0, &T63_o1, T63_W);
	PUT_FIFO(T63_o0, 1);
	PUT_FIFO(T63_o1, 1);

	GET_FIFO(T64_i0, 0);
	GET_FIFO(T64_i1, 0);
	Butterfly(T64_i0, T64_i1, &T64_o0, &T64_o1, T64_W);
	PUT_FIFO(T64_o0, 0);
	PUT_FIFO(T64_o1, 0);

	GET_FIFO(T65_i0, 0);
	GET_FIFO(T65_i1, 0);
	Butterfly(T65_i0, T65_i1, &T65_o0, &T65_o1, T65_W);
	PUT_FIFO(T65_o0, 1);
	PUT_FIFO(T65_o1, 1);

	GET_FIFO(T66_i0, 0);
	GET_FIFO(T66_i1, 0);
	Butterfly(T66_i0, T66_i1, &T66_o0, &T66_o1, T66_W);
	PUT_FIFO(T66_o0, 0);
	PUT_FIFO(T66_o1, 0);

	GET_FIFO(T67_i0, 0);
	GET_FIFO(T67_i1, 0);
	Butterfly(T67_i0, T67_i1, &T67_o0, &T67_o1, T67_W);
	PUT_FIFO(T67_o0, 1);
	PUT_FIFO(T67_o1, 1);

	GET_FIFO(T68_i0, 0);
	GET_FIFO(T68_i1, 0);
	Butterfly(T68_i0, T68_i1, &T68_o0, &T68_o1, T68_W);
	PUT_FIFO(T68_o0, 0);
	PUT_FIFO(T68_o1, 0);

	GET_FIFO(T69_i0, 0);
	GET_FIFO(T69_i1, 0);
	Butterfly(T69_i0, T69_i1, &T69_o0, &T69_o1, T69_W);
	PUT_FIFO(T69_o0, 1);
	PUT_FIFO(T69_o1, 1);

	GET_FIFO(T70_i0, 0);
	GET_FIFO(T70_i1, 0);
	Butterfly(T70_i0, T70_i1, &T70_o0, &T70_o1, T70_W);
	PUT_FIFO(T70_o0, 0);
	PUT_FIFO(T70_o1, 0);

	GET_FIFO(T71_i0, 0);
	GET_FIFO(T71_i1, 0);
	Butterfly(T71_i0, T71_i1, &T71_o0, &T71_o1, T71_W);
	PUT_FIFO(T71_o0, 1);
	PUT_FIFO(T71_o1, 1);

	GET_FIFO(T72_i0, 0);
	GET_FIFO(T72_i1, 0);
	Butterfly(T72_i0, T72_i1, &T72_o0, &T72_o1, T72_W);
	PUT_FIFO(T72_o0, 0);
	PUT_FIFO(T72_o1, 0);

	GET_FIFO(T73_i0, 0);
	GET_FIFO(T73_i1, 0);
	Butterfly(T73_i0, T73_i1, &T73_o0, &T73_o1, T73_W);
	PUT_FIFO(T73_o0, 1);
	PUT_FIFO(T73_o1, 1);

	GET_FIFO(T74_i0, 0);
	GET_FIFO(T74_i1, 0);
	Butterfly(T74_i0, T74_i1, &T74_o0, &T74_o1, T74_W);
	PUT_FIFO(T74_o0, 0);
	PUT_FIFO(T74_o1, 0);

	GET_FIFO(T75_i0, 0);
	GET_FIFO(T75_i1, 0);
	Butterfly(T75_i0, T75_i1, &T75_o0, &T75_o1, T75_W);
	PUT_FIFO(T75_o0, 1);
	PUT_FIFO(T75_o1, 1);

	GET_FIFO(T76_i0, 0);
	GET_FIFO(T76_i1, 0);
	Butterfly(T76_i0, T76_i1, &T76_o0, &T76_o1, T76_W);
	PUT_FIFO(T76_o0, 0);
	PUT_FIFO(T76_o1, 0);

	GET_FIFO(T77_i0, 0);
	GET_FIFO(T77_i1, 0);
	Butterfly(T77_i0, T77_i1, &T77_o0, &T77_o1, T77_W);
	PUT_FIFO(T77_o0, 1);
	PUT_FIFO(T77_o1, 1);

	GET_FIFO(T78_i0, 0);
	GET_FIFO(T78_i1, 0);
	Butterfly(T78_i0, T78_i1, &T78_o0, &T78_o1, T78_W);
	PUT_FIFO(T78_o0, 0);
	PUT_FIFO(T78_o1, 0);

	GET_FIFO(T79_i0, 0);
	GET_FIFO(T79_i1, 0);
	Butterfly(T79_i0, T79_i1, &T79_o0, &T79_o1, T79_W);
	PUT_FIFO(T79_o0, 1);
	PUT_FIFO(T79_o1, 1);

	GET_FIFO(T80_i0, 0);
	GET_FIFO(T80_i1, 0);
	Butterfly(T80_i0, T80_i1, &T80_o0, &T80_o1, T80_W);
	PUT_FIFO(T80_o0, 0);
	PUT_FIFO(T80_o1, 0);

	GET_FIFO(T81_i0, 0);
	GET_FIFO(T81_i1, 0);
	Butterfly(T81_i0, T81_i1, &T81_o0, &T81_o1, T81_W);
	PUT_FIFO(T81_o0, 1);
	PUT_FIFO(T81_o1, 1);

	GET_FIFO(T82_i0, 0);
	GET_FIFO(T82_i1, 0);
	Butterfly(T82_i0, T82_i1, &T82_o0, &T82_o1, T82_W);
	PUT_FIFO(T82_o0, 0);
	PUT_FIFO(T82_o1, 0);

	GET_FIFO(T83_i0, 0);
	GET_FIFO(T83_i1, 0);
	Butterfly(T83_i0, T83_i1, &T83_o0, &T83_o1, T83_W);
	PUT_FIFO(T83_o0, 1);
	PUT_FIFO(T83_o1, 1);

	GET_FIFO(T84_i0, 0);
	GET_FIFO(T84_i1, 0);
	Butterfly(T84_i0, T84_i1, &T84_o0, &T84_o1, T84_W);
	PUT_FIFO(T84_o0, 0);
	PUT_FIFO(T84_o1, 0);

	GET_FIFO(T85_i0, 0);
	GET_FIFO(T85_i1, 0);
	Butterfly(T85_i0, T85_i1, &T85_o0, &T85_o1, T85_W);
	PUT_FIFO(T85_o0, 1);
	PUT_FIFO(T85_o1, 1);

	GET_FIFO(T86_i0, 0);
	GET_FIFO(T86_i1, 0);
	Butterfly(T86_i0, T86_i1, &T86_o0, &T86_o1, T86_W);
	PUT_FIFO(T86_o0, 0);
	PUT_FIFO(T86_o1, 0);

	GET_FIFO(T87_i0, 0);
	GET_FIFO(T87_i1, 0);
	Butterfly(T87_i0, T87_i1, &T87_o0, &T87_o1, T87_W);
	PUT_FIFO(T87_o0, 1);
	PUT_FIFO(T87_o1, 1);

	GET_FIFO(T88_i0, 0);
	GET_FIFO(T88_i1, 0);
	Butterfly(T88_i0, T88_i1, &T88_o0, &T88_o1, T88_W);
	PUT_FIFO(T88_o0, 0);
	PUT_FIFO(T88_o1, 0);

	GET_FIFO(T89_i0, 0);
	GET_FIFO(T89_i1, 0);
	Butterfly(T89_i0, T89_i1, &T89_o0, &T89_o1, T89_W);
	PUT_FIFO(T89_o0, 1);
	PUT_FIFO(T89_o1, 1);

	GET_FIFO(T90_i0, 0);
	GET_FIFO(T90_i1, 0);
	Butterfly(T90_i0, T90_i1, &T90_o0, &T90_o1, T90_W);
	PUT_FIFO(T90_o0, 0);
	PUT_FIFO(T90_o1, 0);

	GET_FIFO(T91_i0, 0);
	GET_FIFO(T91_i1, 0);
	Butterfly(T91_i0, T91_i1, &T91_o0, &T91_o1, T91_W);
	PUT_FIFO(T91_o0, 1);
	PUT_FIFO(T91_o1, 1);

	GET_FIFO(T92_i0, 0);
	GET_FIFO(T92_i1, 0);
	Butterfly(T92_i0, T92_i1, &T92_o0, &T92_o1, T92_W);
	PUT_FIFO(T92_o0, 0);
	PUT_FIFO(T92_o1, 0);

	GET_FIFO(T93_i0, 0);
	GET_FIFO(T93_i1, 0);
	Butterfly(T93_i0, T93_i1, &T93_o0, &T93_o1, T93_W);
	PUT_FIFO(T93_o0, 1);
	PUT_FIFO(T93_o1, 1);

	GET_FIFO(T94_i0, 0);
	GET_FIFO(T94_i1, 0);
	Butterfly(T94_i0, T94_i1, &T94_o0, &T94_o1, T94_W);
	PUT_FIFO(T94_o0, 0);
	PUT_FIFO(T94_o1, 0);

	GET_FIFO(T95_i0, 0);
	GET_FIFO(T95_i1, 0);
	Butterfly(T95_i0, T95_i1, &T95_o0, &T95_o1, T95_W);
	PUT_FIFO(T95_o0, 1);
	PUT_FIFO(T95_o1, 1);

	GET_FIFO(T96_i0, 0);
	GET_FIFO(T96_i1, 0);
	Butterfly(T96_i0, T96_i1, &T96_o0, &T96_o1, T96_W);
	PUT_FIFO(T96_o0, 0);
	PUT_FIFO(T96_o1, 0);

	GET_FIFO(T97_i0, 0);
	GET_FIFO(T97_i1, 0);
	Butterfly(T97_i0, T97_i1, &T97_o0, &T97_o1, T97_W);
	PUT_FIFO(T97_o0, 1);
	PUT_FIFO(T97_o1, 1);

	GET_FIFO(T98_i0, 0);
	GET_FIFO(T98_i1, 0);
	Butterfly(T98_i0, T98_i1, &T98_o0, &T98_o1, T98_W);
	PUT_FIFO(T98_o0, 0);
	PUT_FIFO(T98_o1, 0);

	GET_FIFO(T99_i0, 0);
	GET_FIFO(T99_i1, 0);
	Butterfly(T99_i0, T99_i1, &T99_o0, &T99_o1, T99_W);
	PUT_FIFO(T99_o0, 1);
	PUT_FIFO(T99_o1, 1);

	GET_FIFO(T100_i0, 0);
	GET_FIFO(T100_i1, 0);
	Butterfly(T100_i0, T100_i1, &T100_o0, &T100_o1, T100_W);
	PUT_FIFO(T100_o0, 0);
	PUT_FIFO(T100_o1, 0);

	GET_FIFO(T101_i0, 0);
	GET_FIFO(T101_i1, 0);
	Butterfly(T101_i0, T101_i1, &T101_o0, &T101_o1, T101_W);
	PUT_FIFO(T101_o0, 1);
	PUT_FIFO(T101_o1, 1);

	GET_FIFO(T102_i0, 0);
	GET_FIFO(T102_i1, 0);
	Butterfly(T102_i0, T102_i1, &T102_o0, &T102_o1, T102_W);
	PUT_FIFO(T102_o0, 0);
	PUT_FIFO(T102_o1, 0);

	GET_FIFO(T103_i0, 0);
	GET_FIFO(T103_i1, 0);
	Butterfly(T103_i0, T103_i1, &T103_o0, &T103_o1, T103_W);
	PUT_FIFO(T103_o0, 1);
	PUT_FIFO(T103_o1, 1);

	GET_FIFO(T104_i0, 0);
	GET_FIFO(T104_i1, 0);
	Butterfly(T104_i0, T104_i1, &T104_o0, &T104_o1, T104_W);
	PUT_FIFO(T104_o0, 0);
	PUT_FIFO(T104_o1, 0);

	GET_FIFO(T105_i0, 0);
	GET_FIFO(T105_i1, 0);
	Butterfly(T105_i0, T105_i1, &T105_o0, &T105_o1, T105_W);
	PUT_FIFO(T105_o0, 1);
	PUT_FIFO(T105_o1, 1);

	GET_FIFO(T106_i0, 0);
	GET_FIFO(T106_i1, 0);
	Butterfly(T106_i0, T106_i1, &T106_o0, &T106_o1, T106_W);
	PUT_FIFO(T106_o0, 0);
	PUT_FIFO(T106_o1, 0);

	GET_FIFO(T107_i0, 0);
	GET_FIFO(T107_i1, 0);
	Butterfly(T107_i0, T107_i1, &T107_o0, &T107_o1, T107_W);
	PUT_FIFO(T107_o0, 1);
	PUT_FIFO(T107_o1, 1);

	GET_FIFO(T108_i0, 0);
	GET_FIFO(T108_i1, 0);
	Butterfly(T108_i0, T108_i1, &T108_o0, &T108_o1, T108_W);
	PUT_FIFO(T108_o0, 0);
	PUT_FIFO(T108_o1, 0);

	GET_FIFO(T109_i0, 0);
	GET_FIFO(T109_i1, 0);
	Butterfly(T109_i0, T109_i1, &T109_o0, &T109_o1, T109_W);
	PUT_FIFO(T109_o0, 1);
	PUT_FIFO(T109_o1, 1);

	GET_FIFO(T110_i0, 0);
	GET_FIFO(T110_i1, 0);
	Butterfly(T110_i0, T110_i1, &T110_o0, &T110_o1, T110_W);
	PUT_FIFO(T110_o0, 0);
	PUT_FIFO(T110_o1, 0);

	GET_FIFO(T111_i0, 0);
	GET_FIFO(T111_i1, 0);
	Butterfly(T111_i0, T111_i1, &T111_o0, &T111_o1, T111_W);
	PUT_FIFO(T111_o0, 1);
	PUT_FIFO(T111_o1, 1);

	GET_FIFO(T112_i0, 0);
	GET_FIFO(T112_i1, 0);
	Butterfly(T112_i0, T112_i1, &T112_o0, &T112_o1, T112_W);
	PUT_FIFO(T112_o0, 0);
	PUT_FIFO(T112_o1, 0);

	GET_FIFO(T113_i0, 0);
	GET_FIFO(T113_i1, 0);
	Butterfly(T113_i0, T113_i1, &T113_o0, &T113_o1, T113_W);
	PUT_FIFO(T113_o0, 1);
	PUT_FIFO(T113_o1, 1);

	GET_FIFO(T114_i0, 0);
	GET_FIFO(T114_i1, 0);
	Butterfly(T114_i0, T114_i1, &T114_o0, &T114_o1, T114_W);
	PUT_FIFO(T114_o0, 0);
	PUT_FIFO(T114_o1, 0);

	GET_FIFO(T115_i0, 0);
	GET_FIFO(T115_i1, 0);
	Butterfly(T115_i0, T115_i1, &T115_o0, &T115_o1, T115_W);
	PUT_FIFO(T115_o0, 1);
	PUT_FIFO(T115_o1, 1);

	GET_FIFO(T116_i0, 0);
	GET_FIFO(T116_i1, 0);
	Butterfly(T116_i0, T116_i1, &T116_o0, &T116_o1, T116_W);
	PUT_FIFO(T116_o0, 0);
	PUT_FIFO(T116_o1, 0);

	GET_FIFO(T117_i0, 0);
	GET_FIFO(T117_i1, 0);
	Butterfly(T117_i0, T117_i1, &T117_o0, &T117_o1, T117_W);
	PUT_FIFO(T117_o0, 1);
	PUT_FIFO(T117_o1, 1);

	GET_FIFO(T118_i0, 0);
	GET_FIFO(T118_i1, 0);
	Butterfly(T118_i0, T118_i1, &T118_o0, &T118_o1, T118_W);
	PUT_FIFO(T118_o0, 0);
	PUT_FIFO(T118_o1, 0);

	GET_FIFO(T119_i0, 0);
	GET_FIFO(T119_i1, 0);
	Butterfly(T119_i0, T119_i1, &T119_o0, &T119_o1, T119_W);
	PUT_FIFO(T119_o0, 1);
	PUT_FIFO(T119_o1, 1);

	GET_FIFO(T120_i0, 0);
	GET_FIFO(T120_i1, 0);
	Butterfly(T120_i0, T120_i1, &T120_o0, &T120_o1, T120_W);
	PUT_FIFO(T120_o0, 0);
	PUT_FIFO(T120_o1, 0);

	GET_FIFO(T121_i0, 0);
	GET_FIFO(T121_i1, 0);
	Butterfly(T121_i0, T121_i1, &T121_o0, &T121_o1, T121_W);
	PUT_FIFO(T121_o0, 1);
	PUT_FIFO(T121_o1, 1);

	GET_FIFO(T122_i0, 0);
	GET_FIFO(T122_i1, 0);
	Butterfly(T122_i0, T122_i1, &T122_o0, &T122_o1, T122_W);
	PUT_FIFO(T122_o0, 0);
	PUT_FIFO(T122_o1, 0);

	GET_FIFO(T123_i0, 0);
	GET_FIFO(T123_i1, 0);
	Butterfly(T123_i0, T123_i1, &T123_o0, &T123_o1, T123_W);
	PUT_FIFO(T123_o0, 1);
	PUT_FIFO(T123_o1, 1);

	GET_FIFO(T124_i0, 0);
	GET_FIFO(T124_i1, 0);
	Butterfly(T124_i0, T124_i1, &T124_o0, &T124_o1, T124_W);
	PUT_FIFO(T124_o0, 0);
	PUT_FIFO(T124_o1, 0);

	GET_FIFO(T125_i0, 0);
	GET_FIFO(T125_i1, 0);
	Butterfly(T125_i0, T125_i1, &T125_o0, &T125_o1, T125_W);
	PUT_FIFO(T125_o0, 1);
	PUT_FIFO(T125_o1, 1);

	GET_FIFO(T126_i0, 0);
	GET_FIFO(T126_i1, 0);
	Butterfly(T126_i0, T126_i1, &T126_o0, &T126_o1, T126_W);
	PUT_FIFO(T126_o0, 0);
	PUT_FIFO(T126_o1, 0);

	GET_FIFO(T127_i0, 0);
	GET_FIFO(T127_i1, 0);
	Butterfly(T127_i0, T127_i1, &T127_o0, &T127_o1, T127_W);
	PUT_FIFO(T127_o0, 1);
	PUT_FIFO(T127_o1, 1);

	GET_FIFO(T128_i0, 0);
	GET_FIFO(T128_i1, 0);
	Butterfly(T128_i0, T128_i1, &T128_o0, &T128_o1, T128_W);
	PUT_FIFO(T128_o0, 0);
	PUT_FIFO(T128_o1, 0);

	GET_FIFO(T129_i0, 0);
	GET_FIFO(T129_i1, 0);
	Butterfly(T129_i0, T129_i1, &T129_o0, &T129_o1, T129_W);
	PUT_FIFO(T129_o0, 1);
	PUT_FIFO(T129_o1, 1);

	GET_FIFO(T130_i0, 0);
	GET_FIFO(T130_i1, 0);
	Butterfly(T130_i0, T130_i1, &T130_o0, &T130_o1, T130_W);
	PUT_FIFO(T130_o0, 0);
	PUT_FIFO(T130_o1, 0);

	GET_FIFO(T131_i0, 0);
	GET_FIFO(T131_i1, 0);
	Butterfly(T131_i0, T131_i1, &T131_o0, &T131_o1, T131_W);
	PUT_FIFO(T131_o0, 1);
	PUT_FIFO(T131_o1, 1);

	GET_FIFO(T132_i0, 0);
	GET_FIFO(T132_i1, 0);
	Butterfly(T132_i0, T132_i1, &T132_o0, &T132_o1, T132_W);
	PUT_FIFO(T132_o0, 0);
	PUT_FIFO(T132_o1, 0);

	GET_FIFO(T133_i0, 0);
	GET_FIFO(T133_i1, 0);
	Butterfly(T133_i0, T133_i1, &T133_o0, &T133_o1, T133_W);
	PUT_FIFO(T133_o0, 1);
	PUT_FIFO(T133_o1, 1);

	GET_FIFO(T134_i0, 0);
	GET_FIFO(T134_i1, 0);
	Butterfly(T134_i0, T134_i1, &T134_o0, &T134_o1, T134_W);
	PUT_FIFO(T134_o0, 0);
	PUT_FIFO(T134_o1, 0);

	GET_FIFO(T135_i0, 0);
	GET_FIFO(T135_i1, 0);
	Butterfly(T135_i0, T135_i1, &T135_o0, &T135_o1, T135_W);
	PUT_FIFO(T135_o0, 1);
	PUT_FIFO(T135_o1, 1);

	GET_FIFO(T136_i0, 0);
	GET_FIFO(T136_i1, 0);
	Butterfly(T136_i0, T136_i1, &T136_o0, &T136_o1, T136_W);
	PUT_FIFO(T136_o0, 0);
	PUT_FIFO(T136_o1, 0);

	GET_FIFO(T137_i0, 0);
	GET_FIFO(T137_i1, 0);
	Butterfly(T137_i0, T137_i1, &T137_o0, &T137_o1, T137_W);
	PUT_FIFO(T137_o0, 1);
	PUT_FIFO(T137_o1, 1);

	GET_FIFO(T138_i0, 0);
	GET_FIFO(T138_i1, 0);
	Butterfly(T138_i0, T138_i1, &T138_o0, &T138_o1, T138_W);
	PUT_FIFO(T138_o0, 0);
	PUT_FIFO(T138_o1, 0);

	GET_FIFO(T139_i0, 0);
	GET_FIFO(T139_i1, 0);
	Butterfly(T139_i0, T139_i1, &T139_o0, &T139_o1, T139_W);
	PUT_FIFO(T139_o0, 1);
	PUT_FIFO(T139_o1, 1);

	GET_FIFO(T140_i0, 0);
	GET_FIFO(T140_i1, 0);
	Butterfly(T140_i0, T140_i1, &T140_o0, &T140_o1, T140_W);
	PUT_FIFO(T140_o0, 0);
	PUT_FIFO(T140_o1, 0);

	GET_FIFO(T141_i0, 0);
	GET_FIFO(T141_i1, 0);
	Butterfly(T141_i0, T141_i1, &T141_o0, &T141_o1, T141_W);
	PUT_FIFO(T141_o0, 1);
	PUT_FIFO(T141_o1, 1);

	GET_FIFO(T142_i0, 0);
	GET_FIFO(T142_i1, 0);
	Butterfly(T142_i0, T142_i1, &T142_o0, &T142_o1, T142_W);
	PUT_FIFO(T142_o0, 0);
	PUT_FIFO(T142_o1, 0);

	GET_FIFO(T143_i0, 0);
	GET_FIFO(T143_i1, 0);
	Butterfly(T143_i0, T143_i1, &T143_o0, &T143_o1, T143_W);
	PUT_FIFO(T143_o0, 1);
	PUT_FIFO(T143_o1, 1);

	GET_FIFO(T144_i0, 0);
	GET_FIFO(T144_i1, 0);
	Butterfly(T144_i0, T144_i1, &T144_o0, &T144_o1, T144_W);
	PUT_FIFO(T144_o0, 0);
	PUT_FIFO(T144_o1, 0);

	GET_FIFO(T145_i0, 0);
	GET_FIFO(T145_i1, 0);
	Butterfly(T145_i0, T145_i1, &T145_o0, &T145_o1, T145_W);
	PUT_FIFO(T145_o0, 1);
	PUT_FIFO(T145_o1, 1);

	GET_FIFO(T146_i0, 0);
	GET_FIFO(T146_i1, 0);
	Butterfly(T146_i0, T146_i1, &T146_o0, &T146_o1, T146_W);
	PUT_FIFO(T146_o0, 0);
	PUT_FIFO(T146_o1, 0);

	GET_FIFO(T147_i0, 0);
	GET_FIFO(T147_i1, 0);
	Butterfly(T147_i0, T147_i1, &T147_o0, &T147_o1, T147_W);
	PUT_FIFO(T147_o0, 1);
	PUT_FIFO(T147_o1, 1);

	GET_FIFO(T148_i0, 0);
	GET_FIFO(T148_i1, 0);
	Butterfly(T148_i0, T148_i1, &T148_o0, &T148_o1, T148_W);
	PUT_FIFO(T148_o0, 0);
	PUT_FIFO(T148_o1, 0);

	GET_FIFO(T149_i0, 0);
	GET_FIFO(T149_i1, 0);
	Butterfly(T149_i0, T149_i1, &T149_o0, &T149_o1, T149_W);
	PUT_FIFO(T149_o0, 1);
	PUT_FIFO(T149_o1, 1);

	GET_FIFO(T150_i0, 0);
	GET_FIFO(T150_i1, 0);
	Butterfly(T150_i0, T150_i1, &T150_o0, &T150_o1, T150_W);
	PUT_FIFO(T150_o0, 0);
	PUT_FIFO(T150_o1, 0);

	GET_FIFO(T151_i0, 0);
	GET_FIFO(T151_i1, 0);
	Butterfly(T151_i0, T151_i1, &T151_o0, &T151_o1, T151_W);
	PUT_FIFO(T151_o0, 1);
	PUT_FIFO(T151_o1, 1);

	GET_FIFO(T152_i0, 0);
	GET_FIFO(T152_i1, 0);
	Butterfly(T152_i0, T152_i1, &T152_o0, &T152_o1, T152_W);
	PUT_FIFO(T152_o0, 0);
	PUT_FIFO(T152_o1, 0);

	GET_FIFO(T153_i0, 0);
	GET_FIFO(T153_i1, 0);
	Butterfly(T153_i0, T153_i1, &T153_o0, &T153_o1, T153_W);
	PUT_FIFO(T153_o0, 1);
	PUT_FIFO(T153_o1, 1);

	GET_FIFO(T154_i0, 0);
	GET_FIFO(T154_i1, 0);
	Butterfly(T154_i0, T154_i1, &T154_o0, &T154_o1, T154_W);
	PUT_FIFO(T154_o0, 0);
	PUT_FIFO(T154_o1, 0);

	GET_FIFO(T155_i0, 0);
	GET_FIFO(T155_i1, 0);
	Butterfly(T155_i0, T155_i1, &T155_o0, &T155_o1, T155_W);
	PUT_FIFO(T155_o0, 1);
	PUT_FIFO(T155_o1, 1);

	GET_FIFO(T156_i0, 0);
	GET_FIFO(T156_i1, 0);
	Butterfly(T156_i0, T156_i1, &T156_o0, &T156_o1, T156_W);
	PUT_FIFO(T156_o0, 0);
	PUT_FIFO(T156_o1, 0);

	GET_FIFO(T157_i0, 0);
	GET_FIFO(T157_i1, 0);
	Butterfly(T157_i0, T157_i1, &T157_o0, &T157_o1, T157_W);
	PUT_FIFO(T157_o0, 1);
	PUT_FIFO(T157_o1, 1);

	GET_FIFO(T158_i0, 0);
	GET_FIFO(T158_i1, 0);
	Butterfly(T158_i0, T158_i1, &T158_o0, &T158_o1, T158_W);
	PUT_FIFO(T158_o0, 0);
	PUT_FIFO(T158_o1, 0);

	GET_FIFO(T159_i0, 0);
	GET_FIFO(T159_i1, 0);
	Butterfly(T159_i0, T159_i1, &T159_o0, &T159_o1, T159_W);
	PUT_FIFO(T159_o0, 1);
	PUT_FIFO(T159_o1, 1);

	GET_FIFO(T160_i0, 0);
	GET_FIFO(T160_i1, 0);
	Butterfly(T160_i0, T160_i1, &T160_o0, &T160_o1, T160_W);
	PUT_FIFO(T160_o0, 0);
	PUT_FIFO(T160_o1, 0);

	GET_FIFO(T161_i0, 0);
	GET_FIFO(T161_i1, 0);
	Butterfly(T161_i0, T161_i1, &T161_o0, &T161_o1, T161_W);
	PUT_FIFO(T161_o0, 1);
	PUT_FIFO(T161_o1, 1);

	GET_FIFO(T162_i0, 0);
	GET_FIFO(T162_i1, 0);
	Butterfly(T162_i0, T162_i1, &T162_o0, &T162_o1, T162_W);
	PUT_FIFO(T162_o0, 0);
	PUT_FIFO(T162_o1, 0);

	GET_FIFO(T163_i0, 0);
	GET_FIFO(T163_i1, 0);
	Butterfly(T163_i0, T163_i1, &T163_o0, &T163_o1, T163_W);
	PUT_FIFO(T163_o0, 1);
	PUT_FIFO(T163_o1, 1);

	GET_FIFO(T164_i0, 0);
	GET_FIFO(T164_i1, 0);
	Butterfly(T164_i0, T164_i1, &T164_o0, &T164_o1, T164_W);
	PUT_FIFO(T164_o0, 0);
	PUT_FIFO(T164_o1, 0);

	GET_FIFO(T165_i0, 0);
	GET_FIFO(T165_i1, 0);
	Butterfly(T165_i0, T165_i1, &T165_o0, &T165_o1, T165_W);
	PUT_FIFO(T165_o0, 1);
	PUT_FIFO(T165_o1, 1);

	GET_FIFO(T166_i0, 0);
	GET_FIFO(T166_i1, 0);
	Butterfly(T166_i0, T166_i1, &T166_o0, &T166_o1, T166_W);
	PUT_FIFO(T166_o0, 0);
	PUT_FIFO(T166_o1, 0);

	GET_FIFO(T167_i0, 0);
	GET_FIFO(T167_i1, 0);
	Butterfly(T167_i0, T167_i1, &T167_o0, &T167_o1, T167_W);
	PUT_FIFO(T167_o0, 1);
	PUT_FIFO(T167_o1, 1);

	GET_FIFO(T168_i0, 0);
	GET_FIFO(T168_i1, 0);
	Butterfly(T168_i0, T168_i1, &T168_o0, &T168_o1, T168_W);
	PUT_FIFO(T168_o0, 0);
	PUT_FIFO(T168_o1, 0);

	GET_FIFO(T169_i0, 0);
	GET_FIFO(T169_i1, 0);
	Butterfly(T169_i0, T169_i1, &T169_o0, &T169_o1, T169_W);
	PUT_FIFO(T169_o0, 1);
	PUT_FIFO(T169_o1, 1);

	GET_FIFO(T170_i0, 0);
	GET_FIFO(T170_i1, 0);
	Butterfly(T170_i0, T170_i1, &T170_o0, &T170_o1, T170_W);
	PUT_FIFO(T170_o0, 0);
	PUT_FIFO(T170_o1, 0);

	GET_FIFO(T171_i0, 0);
	GET_FIFO(T171_i1, 0);
	Butterfly(T171_i0, T171_i1, &T171_o0, &T171_o1, T171_W);
	PUT_FIFO(T171_o0, 1);
	PUT_FIFO(T171_o1, 1);

	GET_FIFO(T172_i0, 0);
	GET_FIFO(T172_i1, 0);
	Butterfly(T172_i0, T172_i1, &T172_o0, &T172_o1, T172_W);
	PUT_FIFO(T172_o0, 0);
	PUT_FIFO(T172_o1, 0);

	GET_FIFO(T173_i0, 0);
	GET_FIFO(T173_i1, 0);
	Butterfly(T173_i0, T173_i1, &T173_o0, &T173_o1, T173_W);
	PUT_FIFO(T173_o0, 1);
	PUT_FIFO(T173_o1, 1);

	GET_FIFO(T174_i0, 0);
	GET_FIFO(T174_i1, 0);
	Butterfly(T174_i0, T174_i1, &T174_o0, &T174_o1, T174_W);
	PUT_FIFO(T174_o0, 0);
	PUT_FIFO(T174_o1, 0);

	GET_FIFO(T175_i0, 0);
	GET_FIFO(T175_i1, 0);
	Butterfly(T175_i0, T175_i1, &T175_o0, &T175_o1, T175_W);
	PUT_FIFO(T175_o0, 1);
	PUT_FIFO(T175_o1, 1);

	GET_FIFO(T176_i0, 0);
	GET_FIFO(T176_i1, 0);
	Butterfly(T176_i0, T176_i1, &T176_o0, &T176_o1, T176_W);
	PUT_FIFO(T176_o0, 0);
	PUT_FIFO(T176_o1, 0);

	GET_FIFO(T177_i0, 0);
	GET_FIFO(T177_i1, 0);
	Butterfly(T177_i0, T177_i1, &T177_o0, &T177_o1, T177_W);
	PUT_FIFO(T177_o0, 1);
	PUT_FIFO(T177_o1, 1);

	GET_FIFO(T178_i0, 0);
	GET_FIFO(T178_i1, 0);
	Butterfly(T178_i0, T178_i1, &T178_o0, &T178_o1, T178_W);
	PUT_FIFO(T178_o0, 0);
	PUT_FIFO(T178_o1, 0);

	GET_FIFO(T179_i0, 0);
	GET_FIFO(T179_i1, 0);
	Butterfly(T179_i0, T179_i1, &T179_o0, &T179_o1, T179_W);
	PUT_FIFO(T179_o0, 1);
	PUT_FIFO(T179_o1, 1);

	GET_FIFO(T180_i0, 0);
	GET_FIFO(T180_i1, 0);
	Butterfly(T180_i0, T180_i1, &T180_o0, &T180_o1, T180_W);
	PUT_FIFO(T180_o0, 0);
	PUT_FIFO(T180_o1, 0);

	GET_FIFO(T181_i0, 0);
	GET_FIFO(T181_i1, 0);
	Butterfly(T181_i0, T181_i1, &T181_o0, &T181_o1, T181_W);
	PUT_FIFO(T181_o0, 1);
	PUT_FIFO(T181_o1, 1);

	GET_FIFO(T182_i0, 0);
	GET_FIFO(T182_i1, 0);
	Butterfly(T182_i0, T182_i1, &T182_o0, &T182_o1, T182_W);
	PUT_FIFO(T182_o0, 0);
	PUT_FIFO(T182_o1, 0);

	GET_FIFO(T183_i0, 0);
	GET_FIFO(T183_i1, 0);
	Butterfly(T183_i0, T183_i1, &T183_o0, &T183_o1, T183_W);
	PUT_FIFO(T183_o0, 1);
	PUT_FIFO(T183_o1, 1);

	GET_FIFO(T184_i0, 0);
	GET_FIFO(T184_i1, 0);
	Butterfly(T184_i0, T184_i1, &T184_o0, &T184_o1, T184_W);
	PUT_FIFO(T184_o0, 0);
	PUT_FIFO(T184_o1, 0);

	GET_FIFO(T185_i0, 0);
	GET_FIFO(T185_i1, 0);
	Butterfly(T185_i0, T185_i1, &T185_o0, &T185_o1, T185_W);
	PUT_FIFO(T185_o0, 1);
	PUT_FIFO(T185_o1, 1);

	GET_FIFO(T186_i0, 0);
	GET_FIFO(T186_i1, 0);
	Butterfly(T186_i0, T186_i1, &T186_o0, &T186_o1, T186_W);
	PUT_FIFO(T186_o0, 0);
	PUT_FIFO(T186_o1, 0);

	GET_FIFO(T187_i0, 0);
	GET_FIFO(T187_i1, 0);
	Butterfly(T187_i0, T187_i1, &T187_o0, &T187_o1, T187_W);
	PUT_FIFO(T187_o0, 1);
	PUT_FIFO(T187_o1, 1);

	GET_FIFO(T188_i0, 0);
	GET_FIFO(T188_i1, 0);
	Butterfly(T188_i0, T188_i1, &T188_o0, &T188_o1, T188_W);
	PUT_FIFO(T188_o0, 0);
	PUT_FIFO(T188_o1, 0);

	GET_FIFO(T189_i0, 0);
	GET_FIFO(T189_i1, 0);
	Butterfly(T189_i0, T189_i1, &T189_o0, &T189_o1, T189_W);
	PUT_FIFO(T189_o0, 1);
	PUT_FIFO(T189_o1, 1);

	GET_FIFO(T190_i0, 0);
	GET_FIFO(T190_i1, 0);
	Butterfly(T190_i0, T190_i1, &T190_o0, &T190_o1, T190_W);
	PUT_FIFO(T190_o0, 0);
	PUT_FIFO(T190_o1, 0);

	GET_FIFO(T191_i0, 0);
	GET_FIFO(T191_i1, 0);
	Butterfly(T191_i0, T191_i1, &T191_o0, &T191_o1, T191_W);
	PUT_FIFO(T191_o0, 1);
	PUT_FIFO(T191_o1, 1);

	GET_FIFO(T192_i0, 0);
	GET_FIFO(T192_i1, 0);
	Butterfly(T192_i0, T192_i1, &T192_o0, &T192_o1, T192_W);
	PUT_FIFO(T192_o0, 0);
	PUT_FIFO(T192_o1, 0);

	GET_FIFO(T193_i0, 0);
	GET_FIFO(T193_i1, 0);
	Butterfly(T193_i0, T193_i1, &T193_o0, &T193_o1, T193_W);
	PUT_FIFO(T193_o0, 1);
	PUT_FIFO(T193_o1, 1);

	GET_FIFO(T194_i0, 0);
	GET_FIFO(T194_i1, 0);
	Butterfly(T194_i0, T194_i1, &T194_o0, &T194_o1, T194_W);
	PUT_FIFO(T194_o0, 0);
	PUT_FIFO(T194_o1, 0);

	GET_FIFO(T195_i0, 0);
	GET_FIFO(T195_i1, 0);
	Butterfly(T195_i0, T195_i1, &T195_o0, &T195_o1, T195_W);
	PUT_FIFO(T195_o0, 1);
	PUT_FIFO(T195_o1, 1);

	GET_FIFO(T196_i0, 0);
	GET_FIFO(T196_i1, 0);
	Butterfly(T196_i0, T196_i1, &T196_o0, &T196_o1, T196_W);
	PUT_FIFO(T196_o0, 0);
	PUT_FIFO(T196_o1, 0);

	GET_FIFO(T197_i0, 0);
	GET_FIFO(T197_i1, 0);
	Butterfly(T197_i0, T197_i1, &T197_o0, &T197_o1, T197_W);
	PUT_FIFO(T197_o0, 1);
	PUT_FIFO(T197_o1, 1);

	GET_FIFO(T198_i0, 0);
	GET_FIFO(T198_i1, 0);
	Butterfly(T198_i0, T198_i1, &T198_o0, &T198_o1, T198_W);
	PUT_FIFO(T198_o0, 0);
	PUT_FIFO(T198_o1, 0);

	GET_FIFO(T199_i0, 0);
	GET_FIFO(T199_i1, 0);
	Butterfly(T199_i0, T199_i1, &T199_o0, &T199_o1, T199_W);
	PUT_FIFO(T199_o0, 1);
	PUT_FIFO(T199_o1, 1);

	GET_FIFO(T200_i0, 0);
	GET_FIFO(T200_i1, 0);
	Butterfly(T200_i0, T200_i1, &T200_o0, &T200_o1, T200_W);
	PUT_FIFO(T200_o0, 0);
	PUT_FIFO(T200_o1, 0);

	GET_FIFO(T201_i0, 0);
	GET_FIFO(T201_i1, 0);
	Butterfly(T201_i0, T201_i1, &T201_o0, &T201_o1, T201_W);
	PUT_FIFO(T201_o0, 1);
	PUT_FIFO(T201_o1, 1);

	GET_FIFO(T202_i0, 0);
	GET_FIFO(T202_i1, 0);
	Butterfly(T202_i0, T202_i1, &T202_o0, &T202_o1, T202_W);
	PUT_FIFO(T202_o0, 0);
	PUT_FIFO(T202_o1, 0);

	GET_FIFO(T203_i0, 0);
	GET_FIFO(T203_i1, 0);
	Butterfly(T203_i0, T203_i1, &T203_o0, &T203_o1, T203_W);
	PUT_FIFO(T203_o0, 1);
	PUT_FIFO(T203_o1, 1);

	GET_FIFO(T204_i0, 0);
	GET_FIFO(T204_i1, 0);
	Butterfly(T204_i0, T204_i1, &T204_o0, &T204_o1, T204_W);
	PUT_FIFO(T204_o0, 0);
	PUT_FIFO(T204_o1, 0);

	GET_FIFO(T205_i0, 0);
	GET_FIFO(T205_i1, 0);
	Butterfly(T205_i0, T205_i1, &T205_o0, &T205_o1, T205_W);
	PUT_FIFO(T205_o0, 1);
	PUT_FIFO(T205_o1, 1);

	GET_FIFO(T206_i0, 0);
	GET_FIFO(T206_i1, 0);
	Butterfly(T206_i0, T206_i1, &T206_o0, &T206_o1, T206_W);
	PUT_FIFO(T206_o0, 0);
	PUT_FIFO(T206_o1, 0);

	GET_FIFO(T207_i0, 0);
	GET_FIFO(T207_i1, 0);
	Butterfly(T207_i0, T207_i1, &T207_o0, &T207_o1, T207_W);
	PUT_FIFO(T207_o0, 1);
	PUT_FIFO(T207_o1, 1);

	GET_FIFO(T208_i0, 0);
	GET_FIFO(T208_i1, 0);
	Butterfly(T208_i0, T208_i1, &T208_o0, &T208_o1, T208_W);
	PUT_FIFO(T208_o0, 0);
	PUT_FIFO(T208_o1, 0);

	GET_FIFO(T209_i0, 0);
	GET_FIFO(T209_i1, 0);
	Butterfly(T209_i0, T209_i1, &T209_o0, &T209_o1, T209_W);
	PUT_FIFO(T209_o0, 1);
	PUT_FIFO(T209_o1, 1);

	GET_FIFO(T210_i0, 0);
	GET_FIFO(T210_i1, 0);
	Butterfly(T210_i0, T210_i1, &T210_o0, &T210_o1, T210_W);
	PUT_FIFO(T210_o0, 0);
	PUT_FIFO(T210_o1, 0);

	GET_FIFO(T211_i0, 0);
	GET_FIFO(T211_i1, 0);
	Butterfly(T211_i0, T211_i1, &T211_o0, &T211_o1, T211_W);
	PUT_FIFO(T211_o0, 1);
	PUT_FIFO(T211_o1, 1);

	GET_FIFO(T212_i0, 0);
	GET_FIFO(T212_i1, 0);
	Butterfly(T212_i0, T212_i1, &T212_o0, &T212_o1, T212_W);
	PUT_FIFO(T212_o0, 0);
	PUT_FIFO(T212_o1, 0);

	GET_FIFO(T213_i0, 0);
	GET_FIFO(T213_i1, 0);
	Butterfly(T213_i0, T213_i1, &T213_o0, &T213_o1, T213_W);
	PUT_FIFO(T213_o0, 1);
	PUT_FIFO(T213_o1, 1);

	GET_FIFO(T214_i0, 0);
	GET_FIFO(T214_i1, 0);
	Butterfly(T214_i0, T214_i1, &T214_o0, &T214_o1, T214_W);
	PUT_FIFO(T214_o0, 0);
	PUT_FIFO(T214_o1, 0);

	GET_FIFO(T215_i0, 0);
	GET_FIFO(T215_i1, 0);
	Butterfly(T215_i0, T215_i1, &T215_o0, &T215_o1, T215_W);
	PUT_FIFO(T215_o0, 1);
	PUT_FIFO(T215_o1, 1);

	GET_FIFO(T216_i0, 0);
	GET_FIFO(T216_i1, 0);
	Butterfly(T216_i0, T216_i1, &T216_o0, &T216_o1, T216_W);
	PUT_FIFO(T216_o0, 0);
	PUT_FIFO(T216_o1, 0);

	GET_FIFO(T217_i0, 0);
	GET_FIFO(T217_i1, 0);
	Butterfly(T217_i0, T217_i1, &T217_o0, &T217_o1, T217_W);
	PUT_FIFO(T217_o0, 1);
	PUT_FIFO(T217_o1, 1);

	GET_FIFO(T218_i0, 0);
	GET_FIFO(T218_i1, 0);
	Butterfly(T218_i0, T218_i1, &T218_o0, &T218_o1, T218_W);
	PUT_FIFO(T218_o0, 0);
	PUT_FIFO(T218_o1, 0);

	GET_FIFO(T219_i0, 0);
	GET_FIFO(T219_i1, 0);
	Butterfly(T219_i0, T219_i1, &T219_o0, &T219_o1, T219_W);
	PUT_FIFO(T219_o0, 1);
	PUT_FIFO(T219_o1, 1);

	GET_FIFO(T220_i0, 0);
	GET_FIFO(T220_i1, 0);
	Butterfly(T220_i0, T220_i1, &T220_o0, &T220_o1, T220_W);
	PUT_FIFO(T220_o0, 0);
	PUT_FIFO(T220_o1, 0);

	GET_FIFO(T221_i0, 0);
	GET_FIFO(T221_i1, 0);
	Butterfly(T221_i0, T221_i1, &T221_o0, &T221_o1, T221_W);
	PUT_FIFO(T221_o0, 1);
	PUT_FIFO(T221_o1, 1);

	GET_FIFO(T222_i0, 0);
	GET_FIFO(T222_i1, 0);
	Butterfly(T222_i0, T222_i1, &T222_o0, &T222_o1, T222_W);
	PUT_FIFO(T222_o0, 0);
	PUT_FIFO(T222_o1, 0);

	GET_FIFO(T223_i0, 0);
	GET_FIFO(T223_i1, 0);
	Butterfly(T223_i0, T223_i1, &T223_o0, &T223_o1, T223_W);
	PUT_FIFO(T223_o0, 1);
	PUT_FIFO(T223_o1, 1);

	GET_FIFO(T224_i0, 0);
	GET_FIFO(T224_i1, 0);
	Butterfly(T224_i0, T224_i1, &T224_o0, &T224_o1, T224_W);
	PUT_FIFO(T224_o0, 0);
	PUT_FIFO(T224_o1, 0);

	GET_FIFO(T225_i0, 0);
	GET_FIFO(T225_i1, 0);
	Butterfly(T225_i0, T225_i1, &T225_o0, &T225_o1, T225_W);
	PUT_FIFO(T225_o0, 1);
	PUT_FIFO(T225_o1, 1);

	GET_FIFO(T226_i0, 0);
	GET_FIFO(T226_i1, 0);
	Butterfly(T226_i0, T226_i1, &T226_o0, &T226_o1, T226_W);
	PUT_FIFO(T226_o0, 0);
	PUT_FIFO(T226_o1, 0);

	GET_FIFO(T227_i0, 0);
	GET_FIFO(T227_i1, 0);
	Butterfly(T227_i0, T227_i1, &T227_o0, &T227_o1, T227_W);
	PUT_FIFO(T227_o0, 1);
	PUT_FIFO(T227_o1, 1);

	GET_FIFO(T228_i0, 0);
	GET_FIFO(T228_i1, 0);
	Butterfly(T228_i0, T228_i1, &T228_o0, &T228_o1, T228_W);
	PUT_FIFO(T228_o0, 0);
	PUT_FIFO(T228_o1, 0);

	GET_FIFO(T229_i0, 0);
	GET_FIFO(T229_i1, 0);
	Butterfly(T229_i0, T229_i1, &T229_o0, &T229_o1, T229_W);
	PUT_FIFO(T229_o0, 1);
	PUT_FIFO(T229_o1, 1);

	GET_FIFO(T230_i0, 0);
	GET_FIFO(T230_i1, 0);
	Butterfly(T230_i0, T230_i1, &T230_o0, &T230_o1, T230_W);
	PUT_FIFO(T230_o0, 0);
	PUT_FIFO(T230_o1, 0);

	GET_FIFO(T231_i0, 0);
	GET_FIFO(T231_i1, 0);
	Butterfly(T231_i0, T231_i1, &T231_o0, &T231_o1, T231_W);
	PUT_FIFO(T231_o0, 1);
	PUT_FIFO(T231_o1, 1);

	GET_FIFO(T232_i0, 0);
	GET_FIFO(T232_i1, 0);
	Butterfly(T232_i0, T232_i1, &T232_o0, &T232_o1, T232_W);
	PUT_FIFO(T232_o0, 0);
	PUT_FIFO(T232_o1, 0);

	GET_FIFO(T233_i0, 0);
	GET_FIFO(T233_i1, 0);
	Butterfly(T233_i0, T233_i1, &T233_o0, &T233_o1, T233_W);
	PUT_FIFO(T233_o0, 1);
	PUT_FIFO(T233_o1, 1);

	GET_FIFO(T234_i0, 0);
	GET_FIFO(T234_i1, 0);
	Butterfly(T234_i0, T234_i1, &T234_o0, &T234_o1, T234_W);
	PUT_FIFO(T234_o0, 0);
	PUT_FIFO(T234_o1, 0);

	GET_FIFO(T235_i0, 0);
	GET_FIFO(T235_i1, 0);
	Butterfly(T235_i0, T235_i1, &T235_o0, &T235_o1, T235_W);
	PUT_FIFO(T235_o0, 1);
	PUT_FIFO(T235_o1, 1);

	GET_FIFO(T236_i0, 0);
	GET_FIFO(T236_i1, 0);
	Butterfly(T236_i0, T236_i1, &T236_o0, &T236_o1, T236_W);
	PUT_FIFO(T236_o0, 0);
	PUT_FIFO(T236_o1, 0);

	GET_FIFO(T237_i0, 0);
	GET_FIFO(T237_i1, 0);
	Butterfly(T237_i0, T237_i1, &T237_o0, &T237_o1, T237_W);
	PUT_FIFO(T237_o0, 1);
	PUT_FIFO(T237_o1, 1);

	GET_FIFO(T238_i0, 0);
	GET_FIFO(T238_i1, 0);
	Butterfly(T238_i0, T238_i1, &T238_o0, &T238_o1, T238_W);
	PUT_FIFO(T238_o0, 0);
	PUT_FIFO(T238_o1, 0);

	GET_FIFO(T239_i0, 0);
	GET_FIFO(T239_i1, 0);
	Butterfly(T239_i0, T239_i1, &T239_o0, &T239_o1, T239_W);
	PUT_FIFO(T239_o0, 1);
	PUT_FIFO(T239_o1, 1);

	GET_FIFO(T240_i0, 0);
	GET_FIFO(T240_i1, 0);
	Butterfly(T240_i0, T240_i1, &T240_o0, &T240_o1, T240_W);
	PUT_FIFO(T240_o0, 0);
	PUT_FIFO(T240_o1, 0);

	GET_FIFO(T241_i0, 0);
	GET_FIFO(T241_i1, 0);
	Butterfly(T241_i0, T241_i1, &T241_o0, &T241_o1, T241_W);
	PUT_FIFO(T241_o0, 1);
	PUT_FIFO(T241_o1, 1);

	GET_FIFO(T242_i0, 0);
	GET_FIFO(T242_i1, 0);
	Butterfly(T242_i0, T242_i1, &T242_o0, &T242_o1, T242_W);
	PUT_FIFO(T242_o0, 0);
	PUT_FIFO(T242_o1, 0);

	GET_FIFO(T243_i0, 0);
	GET_FIFO(T243_i1, 0);
	Butterfly(T243_i0, T243_i1, &T243_o0, &T243_o1, T243_W);
	PUT_FIFO(T243_o0, 1);
	PUT_FIFO(T243_o1, 1);

	GET_FIFO(T244_i0, 0);
	GET_FIFO(T244_i1, 0);
	Butterfly(T244_i0, T244_i1, &T244_o0, &T244_o1, T244_W);
	PUT_FIFO(T244_o0, 0);
	PUT_FIFO(T244_o1, 0);

	GET_FIFO(T245_i0, 0);
	GET_FIFO(T245_i1, 0);
	Butterfly(T245_i0, T245_i1, &T245_o0, &T245_o1, T245_W);
	PUT_FIFO(T245_o0, 1);
	PUT_FIFO(T245_o1, 1);

	GET_FIFO(T246_i0, 0);
	GET_FIFO(T246_i1, 0);
	Butterfly(T246_i0, T246_i1, &T246_o0, &T246_o1, T246_W);
	PUT_FIFO(T246_o0, 0);
	PUT_FIFO(T246_o1, 0);

	GET_FIFO(T247_i0, 0);
	GET_FIFO(T247_i1, 0);
	Butterfly(T247_i0, T247_i1, &T247_o0, &T247_o1, T247_W);
	PUT_FIFO(T247_o0, 1);
	PUT_FIFO(T247_o1, 1);

	GET_FIFO(T248_i0, 0);
	GET_FIFO(T248_i1, 0);
	Butterfly(T248_i0, T248_i1, &T248_o0, &T248_o1, T248_W);
	PUT_FIFO(T248_o0, 0);
	PUT_FIFO(T248_o1, 0);

	GET_FIFO(T249_i0, 0);
	GET_FIFO(T249_i1, 0);
	Butterfly(T249_i0, T249_i1, &T249_o0, &T249_o1, T249_W);
	PUT_FIFO(T249_o0, 1);
	PUT_FIFO(T249_o1, 1);

	GET_FIFO(T250_i0, 0);
	GET_FIFO(T250_i1, 0);
	Butterfly(T250_i0, T250_i1, &T250_o0, &T250_o1, T250_W);
	PUT_FIFO(T250_o0, 0);
	PUT_FIFO(T250_o1, 0);

	GET_FIFO(T251_i0, 0);
	GET_FIFO(T251_i1, 0);
	Butterfly(T251_i0, T251_i1, &T251_o0, &T251_o1, T251_W);
	PUT_FIFO(T251_o0, 1);
	PUT_FIFO(T251_o1, 1);

	GET_FIFO(T252_i0, 0);
	GET_FIFO(T252_i1, 0);
	Butterfly(T252_i0, T252_i1, &T252_o0, &T252_o1, T252_W);
	PUT_FIFO(T252_o0, 0);
	PUT_FIFO(T252_o1, 0);

	GET_FIFO(T253_i0, 0);
	GET_FIFO(T253_i1, 0);
	Butterfly(T253_i0, T253_i1, &T253_o0, &T253_o1, T253_W);
	PUT_FIFO(T253_o0, 1);
	PUT_FIFO(T253_o1, 1);

	GET_FIFO(T254_i0, 0);
	GET_FIFO(T254_i1, 0);
	Butterfly(T254_i0, T254_i1, &T254_o0, &T254_o1, T254_W);
	PUT_FIFO(T254_o0, 0);
	PUT_FIFO(T254_o1, 0);

	GET_FIFO(T255_i0, 0);
	GET_FIFO(T255_i1, 0);
	Butterfly(T255_i0, T255_i1, &T255_o0, &T255_o1, T255_W);
	PUT_FIFO(T255_o0, 1);
	PUT_FIFO(T255_o1, 1);
}
