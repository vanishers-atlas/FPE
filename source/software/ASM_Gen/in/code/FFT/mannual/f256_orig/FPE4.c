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
void FPE4PE0() {

  // **** Variable declaration **** //
	int T1024_i0;
	int T1024_i1;
	int T1024_o0;
	int T1024_o1;
	int T1024_W;

	int T1025_i0;
	int T1025_i1;
	int T1025_o0;
	int T1025_o1;
	int T1025_W;

	int T1026_i0;
	int T1026_i1;
	int T1026_o0;
	int T1026_o1;
	int T1026_W;

	int T1027_i0;
	int T1027_i1;
	int T1027_o0;
	int T1027_o1;
	int T1027_W;

	int T1028_i0;
	int T1028_i1;
	int T1028_o0;
	int T1028_o1;
	int T1028_W;

	int T1029_i0;
	int T1029_i1;
	int T1029_o0;
	int T1029_o1;
	int T1029_W;

	int T1030_i0;
	int T1030_i1;
	int T1030_o0;
	int T1030_o1;
	int T1030_W;

	int T1031_i0;
	int T1031_i1;
	int T1031_o0;
	int T1031_o1;
	int T1031_W;

	int T1032_i0;
	int T1032_i1;
	int T1032_o0;
	int T1032_o1;
	int T1032_W;

	int T1033_i0;
	int T1033_i1;
	int T1033_o0;
	int T1033_o1;
	int T1033_W;

	int T1034_i0;
	int T1034_i1;
	int T1034_o0;
	int T1034_o1;
	int T1034_W;

	int T1035_i0;
	int T1035_i1;
	int T1035_o0;
	int T1035_o1;
	int T1035_W;

	int T1036_i0;
	int T1036_i1;
	int T1036_o0;
	int T1036_o1;
	int T1036_W;

	int T1037_i0;
	int T1037_i1;
	int T1037_o0;
	int T1037_o1;
	int T1037_W;

	int T1038_i0;
	int T1038_i1;
	int T1038_o0;
	int T1038_o1;
	int T1038_W;

	int T1039_i0;
	int T1039_i1;
	int T1039_o0;
	int T1039_o1;
	int T1039_W;

	int T1040_i0;
	int T1040_i1;
	int T1040_o0;
	int T1040_o1;
	int T1040_W;

	int T1041_i0;
	int T1041_i1;
	int T1041_o0;
	int T1041_o1;
	int T1041_W;

	int T1042_i0;
	int T1042_i1;
	int T1042_o0;
	int T1042_o1;
	int T1042_W;

	int T1043_i0;
	int T1043_i1;
	int T1043_o0;
	int T1043_o1;
	int T1043_W;

	int T1044_i0;
	int T1044_i1;
	int T1044_o0;
	int T1044_o1;
	int T1044_W;

	int T1045_i0;
	int T1045_i1;
	int T1045_o0;
	int T1045_o1;
	int T1045_W;

	int T1046_i0;
	int T1046_i1;
	int T1046_o0;
	int T1046_o1;
	int T1046_W;

	int T1047_i0;
	int T1047_i1;
	int T1047_o0;
	int T1047_o1;
	int T1047_W;

	int T1048_i0;
	int T1048_i1;
	int T1048_o0;
	int T1048_o1;
	int T1048_W;

	int T1049_i0;
	int T1049_i1;
	int T1049_o0;
	int T1049_o1;
	int T1049_W;

	int T1050_i0;
	int T1050_i1;
	int T1050_o0;
	int T1050_o1;
	int T1050_W;

	int T1051_i0;
	int T1051_i1;
	int T1051_o0;
	int T1051_o1;
	int T1051_W;

	int T1052_i0;
	int T1052_i1;
	int T1052_o0;
	int T1052_o1;
	int T1052_W;

	int T1053_i0;
	int T1053_i1;
	int T1053_o0;
	int T1053_o1;
	int T1053_W;

	int T1054_i0;
	int T1054_i1;
	int T1054_o0;
	int T1054_o1;
	int T1054_W;

	int T1055_i0;
	int T1055_i1;
	int T1055_o0;
	int T1055_o1;
	int T1055_W;

	int T1056_i0;
	int T1056_i1;
	int T1056_o0;
	int T1056_o1;
	int T1056_W;

	int T1057_i0;
	int T1057_i1;
	int T1057_o0;
	int T1057_o1;
	int T1057_W;

	int T1058_i0;
	int T1058_i1;
	int T1058_o0;
	int T1058_o1;
	int T1058_W;

	int T1059_i0;
	int T1059_i1;
	int T1059_o0;
	int T1059_o1;
	int T1059_W;

	int T1060_i0;
	int T1060_i1;
	int T1060_o0;
	int T1060_o1;
	int T1060_W;

	int T1061_i0;
	int T1061_i1;
	int T1061_o0;
	int T1061_o1;
	int T1061_W;

	int T1062_i0;
	int T1062_i1;
	int T1062_o0;
	int T1062_o1;
	int T1062_W;

	int T1063_i0;
	int T1063_i1;
	int T1063_o0;
	int T1063_o1;
	int T1063_W;

	int T1064_i0;
	int T1064_i1;
	int T1064_o0;
	int T1064_o1;
	int T1064_W;

	int T1065_i0;
	int T1065_i1;
	int T1065_o0;
	int T1065_o1;
	int T1065_W;

	int T1066_i0;
	int T1066_i1;
	int T1066_o0;
	int T1066_o1;
	int T1066_W;

	int T1067_i0;
	int T1067_i1;
	int T1067_o0;
	int T1067_o1;
	int T1067_W;

	int T1068_i0;
	int T1068_i1;
	int T1068_o0;
	int T1068_o1;
	int T1068_W;

	int T1069_i0;
	int T1069_i1;
	int T1069_o0;
	int T1069_o1;
	int T1069_W;

	int T1070_i0;
	int T1070_i1;
	int T1070_o0;
	int T1070_o1;
	int T1070_W;

	int T1071_i0;
	int T1071_i1;
	int T1071_o0;
	int T1071_o1;
	int T1071_W;

	int T1072_i0;
	int T1072_i1;
	int T1072_o0;
	int T1072_o1;
	int T1072_W;

	int T1073_i0;
	int T1073_i1;
	int T1073_o0;
	int T1073_o1;
	int T1073_W;

	int T1074_i0;
	int T1074_i1;
	int T1074_o0;
	int T1074_o1;
	int T1074_W;

	int T1075_i0;
	int T1075_i1;
	int T1075_o0;
	int T1075_o1;
	int T1075_W;

	int T1076_i0;
	int T1076_i1;
	int T1076_o0;
	int T1076_o1;
	int T1076_W;

	int T1077_i0;
	int T1077_i1;
	int T1077_o0;
	int T1077_o1;
	int T1077_W;

	int T1078_i0;
	int T1078_i1;
	int T1078_o0;
	int T1078_o1;
	int T1078_W;

	int T1079_i0;
	int T1079_i1;
	int T1079_o0;
	int T1079_o1;
	int T1079_W;

	int T1080_i0;
	int T1080_i1;
	int T1080_o0;
	int T1080_o1;
	int T1080_W;

	int T1081_i0;
	int T1081_i1;
	int T1081_o0;
	int T1081_o1;
	int T1081_W;

	int T1082_i0;
	int T1082_i1;
	int T1082_o0;
	int T1082_o1;
	int T1082_W;

	int T1083_i0;
	int T1083_i1;
	int T1083_o0;
	int T1083_o1;
	int T1083_W;

	int T1084_i0;
	int T1084_i1;
	int T1084_o0;
	int T1084_o1;
	int T1084_W;

	int T1085_i0;
	int T1085_i1;
	int T1085_o0;
	int T1085_o1;
	int T1085_W;

	int T1086_i0;
	int T1086_i1;
	int T1086_o0;
	int T1086_o1;
	int T1086_W;

	int T1087_i0;
	int T1087_i1;
	int T1087_o0;
	int T1087_o1;
	int T1087_W;

	int T1088_i0;
	int T1088_i1;
	int T1088_o0;
	int T1088_o1;
	int T1088_W;

	int T1089_i0;
	int T1089_i1;
	int T1089_o0;
	int T1089_o1;
	int T1089_W;

	int T1090_i0;
	int T1090_i1;
	int T1090_o0;
	int T1090_o1;
	int T1090_W;

	int T1091_i0;
	int T1091_i1;
	int T1091_o0;
	int T1091_o1;
	int T1091_W;

	int T1092_i0;
	int T1092_i1;
	int T1092_o0;
	int T1092_o1;
	int T1092_W;

	int T1093_i0;
	int T1093_i1;
	int T1093_o0;
	int T1093_o1;
	int T1093_W;

	int T1094_i0;
	int T1094_i1;
	int T1094_o0;
	int T1094_o1;
	int T1094_W;

	int T1095_i0;
	int T1095_i1;
	int T1095_o0;
	int T1095_o1;
	int T1095_W;

	int T1096_i0;
	int T1096_i1;
	int T1096_o0;
	int T1096_o1;
	int T1096_W;

	int T1097_i0;
	int T1097_i1;
	int T1097_o0;
	int T1097_o1;
	int T1097_W;

	int T1098_i0;
	int T1098_i1;
	int T1098_o0;
	int T1098_o1;
	int T1098_W;

	int T1099_i0;
	int T1099_i1;
	int T1099_o0;
	int T1099_o1;
	int T1099_W;

	int T1100_i0;
	int T1100_i1;
	int T1100_o0;
	int T1100_o1;
	int T1100_W;

	int T1101_i0;
	int T1101_i1;
	int T1101_o0;
	int T1101_o1;
	int T1101_W;

	int T1102_i0;
	int T1102_i1;
	int T1102_o0;
	int T1102_o1;
	int T1102_W;

	int T1103_i0;
	int T1103_i1;
	int T1103_o0;
	int T1103_o1;
	int T1103_W;

	int T1104_i0;
	int T1104_i1;
	int T1104_o0;
	int T1104_o1;
	int T1104_W;

	int T1105_i0;
	int T1105_i1;
	int T1105_o0;
	int T1105_o1;
	int T1105_W;

	int T1106_i0;
	int T1106_i1;
	int T1106_o0;
	int T1106_o1;
	int T1106_W;

	int T1107_i0;
	int T1107_i1;
	int T1107_o0;
	int T1107_o1;
	int T1107_W;

	int T1108_i0;
	int T1108_i1;
	int T1108_o0;
	int T1108_o1;
	int T1108_W;

	int T1109_i0;
	int T1109_i1;
	int T1109_o0;
	int T1109_o1;
	int T1109_W;

	int T1110_i0;
	int T1110_i1;
	int T1110_o0;
	int T1110_o1;
	int T1110_W;

	int T1111_i0;
	int T1111_i1;
	int T1111_o0;
	int T1111_o1;
	int T1111_W;

	int T1112_i0;
	int T1112_i1;
	int T1112_o0;
	int T1112_o1;
	int T1112_W;

	int T1113_i0;
	int T1113_i1;
	int T1113_o0;
	int T1113_o1;
	int T1113_W;

	int T1114_i0;
	int T1114_i1;
	int T1114_o0;
	int T1114_o1;
	int T1114_W;

	int T1115_i0;
	int T1115_i1;
	int T1115_o0;
	int T1115_o1;
	int T1115_W;

	int T1116_i0;
	int T1116_i1;
	int T1116_o0;
	int T1116_o1;
	int T1116_W;

	int T1117_i0;
	int T1117_i1;
	int T1117_o0;
	int T1117_o1;
	int T1117_W;

	int T1118_i0;
	int T1118_i1;
	int T1118_o0;
	int T1118_o1;
	int T1118_W;

	int T1119_i0;
	int T1119_i1;
	int T1119_o0;
	int T1119_o1;
	int T1119_W;

	int T1120_i0;
	int T1120_i1;
	int T1120_o0;
	int T1120_o1;
	int T1120_W;

	int T1121_i0;
	int T1121_i1;
	int T1121_o0;
	int T1121_o1;
	int T1121_W;

	int T1122_i0;
	int T1122_i1;
	int T1122_o0;
	int T1122_o1;
	int T1122_W;

	int T1123_i0;
	int T1123_i1;
	int T1123_o0;
	int T1123_o1;
	int T1123_W;

	int T1124_i0;
	int T1124_i1;
	int T1124_o0;
	int T1124_o1;
	int T1124_W;

	int T1125_i0;
	int T1125_i1;
	int T1125_o0;
	int T1125_o1;
	int T1125_W;

	int T1126_i0;
	int T1126_i1;
	int T1126_o0;
	int T1126_o1;
	int T1126_W;

	int T1127_i0;
	int T1127_i1;
	int T1127_o0;
	int T1127_o1;
	int T1127_W;

	int T1128_i0;
	int T1128_i1;
	int T1128_o0;
	int T1128_o1;
	int T1128_W;

	int T1129_i0;
	int T1129_i1;
	int T1129_o0;
	int T1129_o1;
	int T1129_W;

	int T1130_i0;
	int T1130_i1;
	int T1130_o0;
	int T1130_o1;
	int T1130_W;

	int T1131_i0;
	int T1131_i1;
	int T1131_o0;
	int T1131_o1;
	int T1131_W;

	int T1132_i0;
	int T1132_i1;
	int T1132_o0;
	int T1132_o1;
	int T1132_W;

	int T1133_i0;
	int T1133_i1;
	int T1133_o0;
	int T1133_o1;
	int T1133_W;

	int T1134_i0;
	int T1134_i1;
	int T1134_o0;
	int T1134_o1;
	int T1134_W;

	int T1135_i0;
	int T1135_i1;
	int T1135_o0;
	int T1135_o1;
	int T1135_W;

	int T1136_i0;
	int T1136_i1;
	int T1136_o0;
	int T1136_o1;
	int T1136_W;

	int T1137_i0;
	int T1137_i1;
	int T1137_o0;
	int T1137_o1;
	int T1137_W;

	int T1138_i0;
	int T1138_i1;
	int T1138_o0;
	int T1138_o1;
	int T1138_W;

	int T1139_i0;
	int T1139_i1;
	int T1139_o0;
	int T1139_o1;
	int T1139_W;

	int T1140_i0;
	int T1140_i1;
	int T1140_o0;
	int T1140_o1;
	int T1140_W;

	int T1141_i0;
	int T1141_i1;
	int T1141_o0;
	int T1141_o1;
	int T1141_W;

	int T1142_i0;
	int T1142_i1;
	int T1142_o0;
	int T1142_o1;
	int T1142_W;

	int T1143_i0;
	int T1143_i1;
	int T1143_o0;
	int T1143_o1;
	int T1143_W;

	int T1144_i0;
	int T1144_i1;
	int T1144_o0;
	int T1144_o1;
	int T1144_W;

	int T1145_i0;
	int T1145_i1;
	int T1145_o0;
	int T1145_o1;
	int T1145_W;

	int T1146_i0;
	int T1146_i1;
	int T1146_o0;
	int T1146_o1;
	int T1146_W;

	int T1147_i0;
	int T1147_i1;
	int T1147_o0;
	int T1147_o1;
	int T1147_W;

	int T1148_i0;
	int T1148_i1;
	int T1148_o0;
	int T1148_o1;
	int T1148_W;

	int T1149_i0;
	int T1149_i1;
	int T1149_o0;
	int T1149_o1;
	int T1149_W;

	int T1150_i0;
	int T1150_i1;
	int T1150_o0;
	int T1150_o1;
	int T1150_W;

	int T1151_i0;
	int T1151_i1;
	int T1151_o0;
	int T1151_o1;
	int T1151_W;

	int T1152_i0;
	int T1152_i1;
	int T1152_o0;
	int T1152_o1;
	int T1152_W;

	int T1153_i0;
	int T1153_i1;
	int T1153_o0;
	int T1153_o1;
	int T1153_W;

	int T1154_i0;
	int T1154_i1;
	int T1154_o0;
	int T1154_o1;
	int T1154_W;

	int T1155_i0;
	int T1155_i1;
	int T1155_o0;
	int T1155_o1;
	int T1155_W;

	int T1156_i0;
	int T1156_i1;
	int T1156_o0;
	int T1156_o1;
	int T1156_W;

	int T1157_i0;
	int T1157_i1;
	int T1157_o0;
	int T1157_o1;
	int T1157_W;

	int T1158_i0;
	int T1158_i1;
	int T1158_o0;
	int T1158_o1;
	int T1158_W;

	int T1159_i0;
	int T1159_i1;
	int T1159_o0;
	int T1159_o1;
	int T1159_W;

	int T1160_i0;
	int T1160_i1;
	int T1160_o0;
	int T1160_o1;
	int T1160_W;

	int T1161_i0;
	int T1161_i1;
	int T1161_o0;
	int T1161_o1;
	int T1161_W;

	int T1162_i0;
	int T1162_i1;
	int T1162_o0;
	int T1162_o1;
	int T1162_W;

	int T1163_i0;
	int T1163_i1;
	int T1163_o0;
	int T1163_o1;
	int T1163_W;

	int T1164_i0;
	int T1164_i1;
	int T1164_o0;
	int T1164_o1;
	int T1164_W;

	int T1165_i0;
	int T1165_i1;
	int T1165_o0;
	int T1165_o1;
	int T1165_W;

	int T1166_i0;
	int T1166_i1;
	int T1166_o0;
	int T1166_o1;
	int T1166_W;

	int T1167_i0;
	int T1167_i1;
	int T1167_o0;
	int T1167_o1;
	int T1167_W;

	int T1168_i0;
	int T1168_i1;
	int T1168_o0;
	int T1168_o1;
	int T1168_W;

	int T1169_i0;
	int T1169_i1;
	int T1169_o0;
	int T1169_o1;
	int T1169_W;

	int T1170_i0;
	int T1170_i1;
	int T1170_o0;
	int T1170_o1;
	int T1170_W;

	int T1171_i0;
	int T1171_i1;
	int T1171_o0;
	int T1171_o1;
	int T1171_W;

	int T1172_i0;
	int T1172_i1;
	int T1172_o0;
	int T1172_o1;
	int T1172_W;

	int T1173_i0;
	int T1173_i1;
	int T1173_o0;
	int T1173_o1;
	int T1173_W;

	int T1174_i0;
	int T1174_i1;
	int T1174_o0;
	int T1174_o1;
	int T1174_W;

	int T1175_i0;
	int T1175_i1;
	int T1175_o0;
	int T1175_o1;
	int T1175_W;

	int T1176_i0;
	int T1176_i1;
	int T1176_o0;
	int T1176_o1;
	int T1176_W;

	int T1177_i0;
	int T1177_i1;
	int T1177_o0;
	int T1177_o1;
	int T1177_W;

	int T1178_i0;
	int T1178_i1;
	int T1178_o0;
	int T1178_o1;
	int T1178_W;

	int T1179_i0;
	int T1179_i1;
	int T1179_o0;
	int T1179_o1;
	int T1179_W;

	int T1180_i0;
	int T1180_i1;
	int T1180_o0;
	int T1180_o1;
	int T1180_W;

	int T1181_i0;
	int T1181_i1;
	int T1181_o0;
	int T1181_o1;
	int T1181_W;

	int T1182_i0;
	int T1182_i1;
	int T1182_o0;
	int T1182_o1;
	int T1182_W;

	int T1183_i0;
	int T1183_i1;
	int T1183_o0;
	int T1183_o1;
	int T1183_W;

	int T1184_i0;
	int T1184_i1;
	int T1184_o0;
	int T1184_o1;
	int T1184_W;

	int T1185_i0;
	int T1185_i1;
	int T1185_o0;
	int T1185_o1;
	int T1185_W;

	int T1186_i0;
	int T1186_i1;
	int T1186_o0;
	int T1186_o1;
	int T1186_W;

	int T1187_i0;
	int T1187_i1;
	int T1187_o0;
	int T1187_o1;
	int T1187_W;

	int T1188_i0;
	int T1188_i1;
	int T1188_o0;
	int T1188_o1;
	int T1188_W;

	int T1189_i0;
	int T1189_i1;
	int T1189_o0;
	int T1189_o1;
	int T1189_W;

	int T1190_i0;
	int T1190_i1;
	int T1190_o0;
	int T1190_o1;
	int T1190_W;

	int T1191_i0;
	int T1191_i1;
	int T1191_o0;
	int T1191_o1;
	int T1191_W;

	int T1192_i0;
	int T1192_i1;
	int T1192_o0;
	int T1192_o1;
	int T1192_W;

	int T1193_i0;
	int T1193_i1;
	int T1193_o0;
	int T1193_o1;
	int T1193_W;

	int T1194_i0;
	int T1194_i1;
	int T1194_o0;
	int T1194_o1;
	int T1194_W;

	int T1195_i0;
	int T1195_i1;
	int T1195_o0;
	int T1195_o1;
	int T1195_W;

	int T1196_i0;
	int T1196_i1;
	int T1196_o0;
	int T1196_o1;
	int T1196_W;

	int T1197_i0;
	int T1197_i1;
	int T1197_o0;
	int T1197_o1;
	int T1197_W;

	int T1198_i0;
	int T1198_i1;
	int T1198_o0;
	int T1198_o1;
	int T1198_W;

	int T1199_i0;
	int T1199_i1;
	int T1199_o0;
	int T1199_o1;
	int T1199_W;

	int T1200_i0;
	int T1200_i1;
	int T1200_o0;
	int T1200_o1;
	int T1200_W;

	int T1201_i0;
	int T1201_i1;
	int T1201_o0;
	int T1201_o1;
	int T1201_W;

	int T1202_i0;
	int T1202_i1;
	int T1202_o0;
	int T1202_o1;
	int T1202_W;

	int T1203_i0;
	int T1203_i1;
	int T1203_o0;
	int T1203_o1;
	int T1203_W;

	int T1204_i0;
	int T1204_i1;
	int T1204_o0;
	int T1204_o1;
	int T1204_W;

	int T1205_i0;
	int T1205_i1;
	int T1205_o0;
	int T1205_o1;
	int T1205_W;

	int T1206_i0;
	int T1206_i1;
	int T1206_o0;
	int T1206_o1;
	int T1206_W;

	int T1207_i0;
	int T1207_i1;
	int T1207_o0;
	int T1207_o1;
	int T1207_W;

	int T1208_i0;
	int T1208_i1;
	int T1208_o0;
	int T1208_o1;
	int T1208_W;

	int T1209_i0;
	int T1209_i1;
	int T1209_o0;
	int T1209_o1;
	int T1209_W;

	int T1210_i0;
	int T1210_i1;
	int T1210_o0;
	int T1210_o1;
	int T1210_W;

	int T1211_i0;
	int T1211_i1;
	int T1211_o0;
	int T1211_o1;
	int T1211_W;

	int T1212_i0;
	int T1212_i1;
	int T1212_o0;
	int T1212_o1;
	int T1212_W;

	int T1213_i0;
	int T1213_i1;
	int T1213_o0;
	int T1213_o1;
	int T1213_W;

	int T1214_i0;
	int T1214_i1;
	int T1214_o0;
	int T1214_o1;
	int T1214_W;

	int T1215_i0;
	int T1215_i1;
	int T1215_o0;
	int T1215_o1;
	int T1215_W;

	int T1216_i0;
	int T1216_i1;
	int T1216_o0;
	int T1216_o1;
	int T1216_W;

	int T1217_i0;
	int T1217_i1;
	int T1217_o0;
	int T1217_o1;
	int T1217_W;

	int T1218_i0;
	int T1218_i1;
	int T1218_o0;
	int T1218_o1;
	int T1218_W;

	int T1219_i0;
	int T1219_i1;
	int T1219_o0;
	int T1219_o1;
	int T1219_W;

	int T1220_i0;
	int T1220_i1;
	int T1220_o0;
	int T1220_o1;
	int T1220_W;

	int T1221_i0;
	int T1221_i1;
	int T1221_o0;
	int T1221_o1;
	int T1221_W;

	int T1222_i0;
	int T1222_i1;
	int T1222_o0;
	int T1222_o1;
	int T1222_W;

	int T1223_i0;
	int T1223_i1;
	int T1223_o0;
	int T1223_o1;
	int T1223_W;

	int T1224_i0;
	int T1224_i1;
	int T1224_o0;
	int T1224_o1;
	int T1224_W;

	int T1225_i0;
	int T1225_i1;
	int T1225_o0;
	int T1225_o1;
	int T1225_W;

	int T1226_i0;
	int T1226_i1;
	int T1226_o0;
	int T1226_o1;
	int T1226_W;

	int T1227_i0;
	int T1227_i1;
	int T1227_o0;
	int T1227_o1;
	int T1227_W;

	int T1228_i0;
	int T1228_i1;
	int T1228_o0;
	int T1228_o1;
	int T1228_W;

	int T1229_i0;
	int T1229_i1;
	int T1229_o0;
	int T1229_o1;
	int T1229_W;

	int T1230_i0;
	int T1230_i1;
	int T1230_o0;
	int T1230_o1;
	int T1230_W;

	int T1231_i0;
	int T1231_i1;
	int T1231_o0;
	int T1231_o1;
	int T1231_W;

	int T1232_i0;
	int T1232_i1;
	int T1232_o0;
	int T1232_o1;
	int T1232_W;

	int T1233_i0;
	int T1233_i1;
	int T1233_o0;
	int T1233_o1;
	int T1233_W;

	int T1234_i0;
	int T1234_i1;
	int T1234_o0;
	int T1234_o1;
	int T1234_W;

	int T1235_i0;
	int T1235_i1;
	int T1235_o0;
	int T1235_o1;
	int T1235_W;

	int T1236_i0;
	int T1236_i1;
	int T1236_o0;
	int T1236_o1;
	int T1236_W;

	int T1237_i0;
	int T1237_i1;
	int T1237_o0;
	int T1237_o1;
	int T1237_W;

	int T1238_i0;
	int T1238_i1;
	int T1238_o0;
	int T1238_o1;
	int T1238_W;

	int T1239_i0;
	int T1239_i1;
	int T1239_o0;
	int T1239_o1;
	int T1239_W;

	int T1240_i0;
	int T1240_i1;
	int T1240_o0;
	int T1240_o1;
	int T1240_W;

	int T1241_i0;
	int T1241_i1;
	int T1241_o0;
	int T1241_o1;
	int T1241_W;

	int T1242_i0;
	int T1242_i1;
	int T1242_o0;
	int T1242_o1;
	int T1242_W;

	int T1243_i0;
	int T1243_i1;
	int T1243_o0;
	int T1243_o1;
	int T1243_W;

	int T1244_i0;
	int T1244_i1;
	int T1244_o0;
	int T1244_o1;
	int T1244_W;

	int T1245_i0;
	int T1245_i1;
	int T1245_o0;
	int T1245_o1;
	int T1245_W;

	int T1246_i0;
	int T1246_i1;
	int T1246_o0;
	int T1246_o1;
	int T1246_W;

	int T1247_i0;
	int T1247_i1;
	int T1247_o0;
	int T1247_o1;
	int T1247_W;

	int T1248_i0;
	int T1248_i1;
	int T1248_o0;
	int T1248_o1;
	int T1248_W;

	int T1249_i0;
	int T1249_i1;
	int T1249_o0;
	int T1249_o1;
	int T1249_W;

	int T1250_i0;
	int T1250_i1;
	int T1250_o0;
	int T1250_o1;
	int T1250_W;

	int T1251_i0;
	int T1251_i1;
	int T1251_o0;
	int T1251_o1;
	int T1251_W;

	int T1252_i0;
	int T1252_i1;
	int T1252_o0;
	int T1252_o1;
	int T1252_W;

	int T1253_i0;
	int T1253_i1;
	int T1253_o0;
	int T1253_o1;
	int T1253_W;

	int T1254_i0;
	int T1254_i1;
	int T1254_o0;
	int T1254_o1;
	int T1254_W;

	int T1255_i0;
	int T1255_i1;
	int T1255_o0;
	int T1255_o1;
	int T1255_W;

	int T1256_i0;
	int T1256_i1;
	int T1256_o0;
	int T1256_o1;
	int T1256_W;

	int T1257_i0;
	int T1257_i1;
	int T1257_o0;
	int T1257_o1;
	int T1257_W;

	int T1258_i0;
	int T1258_i1;
	int T1258_o0;
	int T1258_o1;
	int T1258_W;

	int T1259_i0;
	int T1259_i1;
	int T1259_o0;
	int T1259_o1;
	int T1259_W;

	int T1260_i0;
	int T1260_i1;
	int T1260_o0;
	int T1260_o1;
	int T1260_W;

	int T1261_i0;
	int T1261_i1;
	int T1261_o0;
	int T1261_o1;
	int T1261_W;

	int T1262_i0;
	int T1262_i1;
	int T1262_o0;
	int T1262_o1;
	int T1262_W;

	int T1263_i0;
	int T1263_i1;
	int T1263_o0;
	int T1263_o1;
	int T1263_W;

	int T1264_i0;
	int T1264_i1;
	int T1264_o0;
	int T1264_o1;
	int T1264_W;

	int T1265_i0;
	int T1265_i1;
	int T1265_o0;
	int T1265_o1;
	int T1265_W;

	int T1266_i0;
	int T1266_i1;
	int T1266_o0;
	int T1266_o1;
	int T1266_W;

	int T1267_i0;
	int T1267_i1;
	int T1267_o0;
	int T1267_o1;
	int T1267_W;

	int T1268_i0;
	int T1268_i1;
	int T1268_o0;
	int T1268_o1;
	int T1268_W;

	int T1269_i0;
	int T1269_i1;
	int T1269_o0;
	int T1269_o1;
	int T1269_W;

	int T1270_i0;
	int T1270_i1;
	int T1270_o0;
	int T1270_o1;
	int T1270_W;

	int T1271_i0;
	int T1271_i1;
	int T1271_o0;
	int T1271_o1;
	int T1271_W;

	int T1272_i0;
	int T1272_i1;
	int T1272_o0;
	int T1272_o1;
	int T1272_W;

	int T1273_i0;
	int T1273_i1;
	int T1273_o0;
	int T1273_o1;
	int T1273_W;

	int T1274_i0;
	int T1274_i1;
	int T1274_o0;
	int T1274_o1;
	int T1274_W;

	int T1275_i0;
	int T1275_i1;
	int T1275_o0;
	int T1275_o1;
	int T1275_W;

	int T1276_i0;
	int T1276_i1;
	int T1276_o0;
	int T1276_o1;
	int T1276_W;

	int T1277_i0;
	int T1277_i1;
	int T1277_o0;
	int T1277_o1;
	int T1277_W;

	int T1278_i0;
	int T1278_i1;
	int T1278_o0;
	int T1278_o1;
	int T1278_W;

	int T1279_i0;
	int T1279_i1;
	int T1279_o0;
	int T1279_o1;
	int T1279_W;


  // **** Parameter initialisation **** //
T1024_W = 16384;
T1025_W = -209436987;
T1026_W = -410895583;
T1027_W = -596495049;
T1028_W = -759222975;
T1029_W = -892787826;
T1030_W = -992012162;
T1031_W = -1053094788;
T1032_W = -1073741824;
T1033_W = -1053101180;
T1034_W = -992024702;
T1035_W = -892806030;
T1036_W = -759246145;
T1037_W = -596522295;
T1038_W = -410925857;
T1039_W = -209469125;
T1040_W = 16384;
T1041_W = -209436987;
T1042_W = -410895583;
T1043_W = -596495049;
T1044_W = -759222975;
T1045_W = -892787826;
T1046_W = -992012162;
T1047_W = -1053094788;
T1048_W = -1073741824;
T1049_W = -1053101180;
T1050_W = -992024702;
T1051_W = -892806030;
T1052_W = -759246145;
T1053_W = -596522295;
T1054_W = -410925857;
T1055_W = -209469125;
T1056_W = 16384;
T1057_W = -209436987;
T1058_W = -410895583;
T1059_W = -596495049;
T1060_W = -759222975;
T1061_W = -892787826;
T1062_W = -992012162;
T1063_W = -1053094788;
T1064_W = -1073741824;
T1065_W = -1053101180;
T1066_W = -992024702;
T1067_W = -892806030;
T1068_W = -759246145;
T1069_W = -596522295;
T1070_W = -410925857;
T1071_W = -209469125;
T1072_W = 16384;
T1073_W = -209436987;
T1074_W = -410895583;
T1075_W = -596495049;
T1076_W = -759222975;
T1077_W = -892787826;
T1078_W = -992012162;
T1079_W = -1053094788;
T1080_W = -1073741824;
T1081_W = -1053101180;
T1082_W = -992024702;
T1083_W = -892806030;
T1084_W = -759246145;
T1085_W = -596522295;
T1086_W = -410925857;
T1087_W = -209469125;
T1088_W = 16384;
T1089_W = -209436987;
T1090_W = -410895583;
T1091_W = -596495049;
T1092_W = -759222975;
T1093_W = -892787826;
T1094_W = -992012162;
T1095_W = -1053094788;
T1096_W = -1073741824;
T1097_W = -1053101180;
T1098_W = -992024702;
T1099_W = -892806030;
T1100_W = -759246145;
T1101_W = -596522295;
T1102_W = -410925857;
T1103_W = -209469125;
T1104_W = 16384;
T1105_W = -209436987;
T1106_W = -410895583;
T1107_W = -596495049;
T1108_W = -759222975;
T1109_W = -892787826;
T1110_W = -992012162;
T1111_W = -1053094788;
T1112_W = -1073741824;
T1113_W = -1053101180;
T1114_W = -992024702;
T1115_W = -892806030;
T1116_W = -759246145;
T1117_W = -596522295;
T1118_W = -410925857;
T1119_W = -209469125;
T1120_W = 16384;
T1121_W = -209436987;
T1122_W = -410895583;
T1123_W = -596495049;
T1124_W = -759222975;
T1125_W = -892787826;
T1126_W = -992012162;
T1127_W = -1053094788;
T1128_W = -1073741824;
T1129_W = -1053101180;
T1130_W = -992024702;
T1131_W = -892806030;
T1132_W = -759246145;
T1133_W = -596522295;
T1134_W = -410925857;
T1135_W = -209469125;
T1136_W = 16384;
T1137_W = -209436987;
T1138_W = -410895583;
T1139_W = -596495049;
T1140_W = -759222975;
T1141_W = -892787826;
T1142_W = -992012162;
T1143_W = -1053094788;
T1144_W = -1073741824;
T1145_W = -1053101180;
T1146_W = -992024702;
T1147_W = -892806030;
T1148_W = -759246145;
T1149_W = -596522295;
T1150_W = -410925857;
T1151_W = -209469125;
T1152_W = 16384;
T1153_W = -209436987;
T1154_W = -410895583;
T1155_W = -596495049;
T1156_W = -759222975;
T1157_W = -892787826;
T1158_W = -992012162;
T1159_W = -1053094788;
T1160_W = -1073741824;
T1161_W = -1053101180;
T1162_W = -992024702;
T1163_W = -892806030;
T1164_W = -759246145;
T1165_W = -596522295;
T1166_W = -410925857;
T1167_W = -209469125;
T1168_W = 16384;
T1169_W = -209436987;
T1170_W = -410895583;
T1171_W = -596495049;
T1172_W = -759222975;
T1173_W = -892787826;
T1174_W = -992012162;
T1175_W = -1053094788;
T1176_W = -1073741824;
T1177_W = -1053101180;
T1178_W = -992024702;
T1179_W = -892806030;
T1180_W = -759246145;
T1181_W = -596522295;
T1182_W = -410925857;
T1183_W = -209469125;
T1184_W = 16384;
T1185_W = -209436987;
T1186_W = -410895583;
T1187_W = -596495049;
T1188_W = -759222975;
T1189_W = -892787826;
T1190_W = -992012162;
T1191_W = -1053094788;
T1192_W = -1073741824;
T1193_W = -1053101180;
T1194_W = -992024702;
T1195_W = -892806030;
T1196_W = -759246145;
T1197_W = -596522295;
T1198_W = -410925857;
T1199_W = -209469125;
T1200_W = 16384;
T1201_W = -209436987;
T1202_W = -410895583;
T1203_W = -596495049;
T1204_W = -759222975;
T1205_W = -892787826;
T1206_W = -992012162;
T1207_W = -1053094788;
T1208_W = -1073741824;
T1209_W = -1053101180;
T1210_W = -992024702;
T1211_W = -892806030;
T1212_W = -759246145;
T1213_W = -596522295;
T1214_W = -410925857;
T1215_W = -209469125;
T1216_W = 16384;
T1217_W = -209436987;
T1218_W = -410895583;
T1219_W = -596495049;
T1220_W = -759222975;
T1221_W = -892787826;
T1222_W = -992012162;
T1223_W = -1053094788;
T1224_W = -1073741824;
T1225_W = -1053101180;
T1226_W = -992024702;
T1227_W = -892806030;
T1228_W = -759246145;
T1229_W = -596522295;
T1230_W = -410925857;
T1231_W = -209469125;
T1232_W = 16384;
T1233_W = -209436987;
T1234_W = -410895583;
T1235_W = -596495049;
T1236_W = -759222975;
T1237_W = -892787826;
T1238_W = -992012162;
T1239_W = -1053094788;
T1240_W = -1073741824;
T1241_W = -1053101180;
T1242_W = -992024702;
T1243_W = -892806030;
T1244_W = -759246145;
T1245_W = -596522295;
T1246_W = -410925857;
T1247_W = -209469125;
T1248_W = 16384;
T1249_W = -209436987;
T1250_W = -410895583;
T1251_W = -596495049;
T1252_W = -759222975;
T1253_W = -892787826;
T1254_W = -992012162;
T1255_W = -1053094788;
T1256_W = -1073741824;
T1257_W = -1053101180;
T1258_W = -992024702;
T1259_W = -892806030;
T1260_W = -759246145;
T1261_W = -596522295;
T1262_W = -410925857;
T1263_W = -209469125;
T1264_W = 16384;
T1265_W = -209436987;
T1266_W = -410895583;
T1267_W = -596495049;
T1268_W = -759222975;
T1269_W = -892787826;
T1270_W = -992012162;
T1271_W = -1053094788;
T1272_W = -1073741824;
T1273_W = -1053101180;
T1274_W = -992024702;
T1275_W = -892806030;
T1276_W = -759246145;
T1277_W = -596522295;
T1278_W = -410925857;
T1279_W = -209469125;

  // **** Code body **** //

	GET_FIFO(T1024_i0, 0);
	GET_FIFO(T1024_i1, 2);
	Butterfly(T1024_i0, T1024_i1, &T1024_o0, &T1024_o1, T1024_W);
	PUT_FIFO(T1024_o0, 0);
	PUT_FIFO(T1024_o1, 1);

	GET_FIFO(T1025_i0, 0);
	GET_FIFO(T1025_i1, 2);
	Butterfly(T1025_i0, T1025_i1, &T1025_o0, &T1025_o1, T1025_W);
	PUT_FIFO(T1025_o0, 0);
	PUT_FIFO(T1025_o1, 1);

	GET_FIFO(T1026_i0, 0);
	GET_FIFO(T1026_i1, 2);
	Butterfly(T1026_i0, T1026_i1, &T1026_o0, &T1026_o1, T1026_W);
	PUT_FIFO(T1026_o0, 0);
	PUT_FIFO(T1026_o1, 1);

	GET_FIFO(T1027_i0, 0);
	GET_FIFO(T1027_i1, 2);
	Butterfly(T1027_i0, T1027_i1, &T1027_o0, &T1027_o1, T1027_W);
	PUT_FIFO(T1027_o0, 0);
	PUT_FIFO(T1027_o1, 1);

	GET_FIFO(T1028_i0, 0);
	GET_FIFO(T1028_i1, 2);
	Butterfly(T1028_i0, T1028_i1, &T1028_o0, &T1028_o1, T1028_W);
	PUT_FIFO(T1028_o0, 0);
	PUT_FIFO(T1028_o1, 1);

	GET_FIFO(T1029_i0, 0);
	GET_FIFO(T1029_i1, 2);
	Butterfly(T1029_i0, T1029_i1, &T1029_o0, &T1029_o1, T1029_W);
	PUT_FIFO(T1029_o0, 0);
	PUT_FIFO(T1029_o1, 1);

	GET_FIFO(T1030_i0, 0);
	GET_FIFO(T1030_i1, 2);
	Butterfly(T1030_i0, T1030_i1, &T1030_o0, &T1030_o1, T1030_W);
	PUT_FIFO(T1030_o0, 0);
	PUT_FIFO(T1030_o1, 1);

	GET_FIFO(T1031_i0, 0);
	GET_FIFO(T1031_i1, 2);
	Butterfly(T1031_i0, T1031_i1, &T1031_o0, &T1031_o1, T1031_W);
	PUT_FIFO(T1031_o0, 0);
	PUT_FIFO(T1031_o1, 1);

	GET_FIFO(T1032_i0, 1);
	GET_FIFO(T1032_i1, 3);
	Butterfly(T1032_i0, T1032_i1, &T1032_o0, &T1032_o1, T1032_W);
	PUT_FIFO(T1032_o0, 0);
	PUT_FIFO(T1032_o1, 1);

	GET_FIFO(T1033_i0, 1);
	GET_FIFO(T1033_i1, 3);
	Butterfly(T1033_i0, T1033_i1, &T1033_o0, &T1033_o1, T1033_W);
	PUT_FIFO(T1033_o0, 0);
	PUT_FIFO(T1033_o1, 1);

	GET_FIFO(T1034_i0, 1);
	GET_FIFO(T1034_i1, 3);
	Butterfly(T1034_i0, T1034_i1, &T1034_o0, &T1034_o1, T1034_W);
	PUT_FIFO(T1034_o0, 0);
	PUT_FIFO(T1034_o1, 1);

	GET_FIFO(T1035_i0, 1);
	GET_FIFO(T1035_i1, 3);
	Butterfly(T1035_i0, T1035_i1, &T1035_o0, &T1035_o1, T1035_W);
	PUT_FIFO(T1035_o0, 0);
	PUT_FIFO(T1035_o1, 1);

	GET_FIFO(T1036_i0, 1);
	GET_FIFO(T1036_i1, 3);
	Butterfly(T1036_i0, T1036_i1, &T1036_o0, &T1036_o1, T1036_W);
	PUT_FIFO(T1036_o0, 0);
	PUT_FIFO(T1036_o1, 1);

	GET_FIFO(T1037_i0, 1);
	GET_FIFO(T1037_i1, 3);
	Butterfly(T1037_i0, T1037_i1, &T1037_o0, &T1037_o1, T1037_W);
	PUT_FIFO(T1037_o0, 0);
	PUT_FIFO(T1037_o1, 1);

	GET_FIFO(T1038_i0, 1);
	GET_FIFO(T1038_i1, 3);
	Butterfly(T1038_i0, T1038_i1, &T1038_o0, &T1038_o1, T1038_W);
	PUT_FIFO(T1038_o0, 0);
	PUT_FIFO(T1038_o1, 1);

	GET_FIFO(T1039_i0, 1);
	GET_FIFO(T1039_i1, 3);
	Butterfly(T1039_i0, T1039_i1, &T1039_o0, &T1039_o1, T1039_W);
	PUT_FIFO(T1039_o0, 0);
	PUT_FIFO(T1039_o1, 1);

	GET_FIFO(T1040_i0, 0);
	GET_FIFO(T1040_i1, 2);
	Butterfly(T1040_i0, T1040_i1, &T1040_o0, &T1040_o1, T1040_W);
	PUT_FIFO(T1040_o0, 2);
	PUT_FIFO(T1040_o1, 3);

	GET_FIFO(T1041_i0, 0);
	GET_FIFO(T1041_i1, 2);
	Butterfly(T1041_i0, T1041_i1, &T1041_o0, &T1041_o1, T1041_W);
	PUT_FIFO(T1041_o0, 2);
	PUT_FIFO(T1041_o1, 3);

	GET_FIFO(T1042_i0, 0);
	GET_FIFO(T1042_i1, 2);
	Butterfly(T1042_i0, T1042_i1, &T1042_o0, &T1042_o1, T1042_W);
	PUT_FIFO(T1042_o0, 2);
	PUT_FIFO(T1042_o1, 3);

	GET_FIFO(T1043_i0, 0);
	GET_FIFO(T1043_i1, 2);
	Butterfly(T1043_i0, T1043_i1, &T1043_o0, &T1043_o1, T1043_W);
	PUT_FIFO(T1043_o0, 2);
	PUT_FIFO(T1043_o1, 3);

	GET_FIFO(T1044_i0, 0);
	GET_FIFO(T1044_i1, 2);
	Butterfly(T1044_i0, T1044_i1, &T1044_o0, &T1044_o1, T1044_W);
	PUT_FIFO(T1044_o0, 2);
	PUT_FIFO(T1044_o1, 3);

	GET_FIFO(T1045_i0, 0);
	GET_FIFO(T1045_i1, 2);
	Butterfly(T1045_i0, T1045_i1, &T1045_o0, &T1045_o1, T1045_W);
	PUT_FIFO(T1045_o0, 2);
	PUT_FIFO(T1045_o1, 3);

	GET_FIFO(T1046_i0, 0);
	GET_FIFO(T1046_i1, 2);
	Butterfly(T1046_i0, T1046_i1, &T1046_o0, &T1046_o1, T1046_W);
	PUT_FIFO(T1046_o0, 2);
	PUT_FIFO(T1046_o1, 3);

	GET_FIFO(T1047_i0, 0);
	GET_FIFO(T1047_i1, 2);
	Butterfly(T1047_i0, T1047_i1, &T1047_o0, &T1047_o1, T1047_W);
	PUT_FIFO(T1047_o0, 2);
	PUT_FIFO(T1047_o1, 3);

	GET_FIFO(T1048_i0, 1);
	GET_FIFO(T1048_i1, 3);
	Butterfly(T1048_i0, T1048_i1, &T1048_o0, &T1048_o1, T1048_W);
	PUT_FIFO(T1048_o0, 2);
	PUT_FIFO(T1048_o1, 3);

	GET_FIFO(T1049_i0, 1);
	GET_FIFO(T1049_i1, 3);
	Butterfly(T1049_i0, T1049_i1, &T1049_o0, &T1049_o1, T1049_W);
	PUT_FIFO(T1049_o0, 2);
	PUT_FIFO(T1049_o1, 3);

	GET_FIFO(T1050_i0, 1);
	GET_FIFO(T1050_i1, 3);
	Butterfly(T1050_i0, T1050_i1, &T1050_o0, &T1050_o1, T1050_W);
	PUT_FIFO(T1050_o0, 2);
	PUT_FIFO(T1050_o1, 3);

	GET_FIFO(T1051_i0, 1);
	GET_FIFO(T1051_i1, 3);
	Butterfly(T1051_i0, T1051_i1, &T1051_o0, &T1051_o1, T1051_W);
	PUT_FIFO(T1051_o0, 2);
	PUT_FIFO(T1051_o1, 3);

	GET_FIFO(T1052_i0, 1);
	GET_FIFO(T1052_i1, 3);
	Butterfly(T1052_i0, T1052_i1, &T1052_o0, &T1052_o1, T1052_W);
	PUT_FIFO(T1052_o0, 2);
	PUT_FIFO(T1052_o1, 3);

	GET_FIFO(T1053_i0, 1);
	GET_FIFO(T1053_i1, 3);
	Butterfly(T1053_i0, T1053_i1, &T1053_o0, &T1053_o1, T1053_W);
	PUT_FIFO(T1053_o0, 2);
	PUT_FIFO(T1053_o1, 3);

	GET_FIFO(T1054_i0, 1);
	GET_FIFO(T1054_i1, 3);
	Butterfly(T1054_i0, T1054_i1, &T1054_o0, &T1054_o1, T1054_W);
	PUT_FIFO(T1054_o0, 2);
	PUT_FIFO(T1054_o1, 3);

	GET_FIFO(T1055_i0, 1);
	GET_FIFO(T1055_i1, 3);
	Butterfly(T1055_i0, T1055_i1, &T1055_o0, &T1055_o1, T1055_W);
	PUT_FIFO(T1055_o0, 2);
	PUT_FIFO(T1055_o1, 3);

	GET_FIFO(T1056_i0, 0);
	GET_FIFO(T1056_i1, 2);
	Butterfly(T1056_i0, T1056_i1, &T1056_o0, &T1056_o1, T1056_W);
	PUT_FIFO(T1056_o0, 0);
	PUT_FIFO(T1056_o1, 1);

	GET_FIFO(T1057_i0, 0);
	GET_FIFO(T1057_i1, 2);
	Butterfly(T1057_i0, T1057_i1, &T1057_o0, &T1057_o1, T1057_W);
	PUT_FIFO(T1057_o0, 0);
	PUT_FIFO(T1057_o1, 1);

	GET_FIFO(T1058_i0, 0);
	GET_FIFO(T1058_i1, 2);
	Butterfly(T1058_i0, T1058_i1, &T1058_o0, &T1058_o1, T1058_W);
	PUT_FIFO(T1058_o0, 0);
	PUT_FIFO(T1058_o1, 1);

	GET_FIFO(T1059_i0, 0);
	GET_FIFO(T1059_i1, 2);
	Butterfly(T1059_i0, T1059_i1, &T1059_o0, &T1059_o1, T1059_W);
	PUT_FIFO(T1059_o0, 0);
	PUT_FIFO(T1059_o1, 1);

	GET_FIFO(T1060_i0, 0);
	GET_FIFO(T1060_i1, 2);
	Butterfly(T1060_i0, T1060_i1, &T1060_o0, &T1060_o1, T1060_W);
	PUT_FIFO(T1060_o0, 0);
	PUT_FIFO(T1060_o1, 1);

	GET_FIFO(T1061_i0, 0);
	GET_FIFO(T1061_i1, 2);
	Butterfly(T1061_i0, T1061_i1, &T1061_o0, &T1061_o1, T1061_W);
	PUT_FIFO(T1061_o0, 0);
	PUT_FIFO(T1061_o1, 1);

	GET_FIFO(T1062_i0, 0);
	GET_FIFO(T1062_i1, 2);
	Butterfly(T1062_i0, T1062_i1, &T1062_o0, &T1062_o1, T1062_W);
	PUT_FIFO(T1062_o0, 0);
	PUT_FIFO(T1062_o1, 1);

	GET_FIFO(T1063_i0, 0);
	GET_FIFO(T1063_i1, 2);
	Butterfly(T1063_i0, T1063_i1, &T1063_o0, &T1063_o1, T1063_W);
	PUT_FIFO(T1063_o0, 0);
	PUT_FIFO(T1063_o1, 1);

	GET_FIFO(T1064_i0, 1);
	GET_FIFO(T1064_i1, 3);
	Butterfly(T1064_i0, T1064_i1, &T1064_o0, &T1064_o1, T1064_W);
	PUT_FIFO(T1064_o0, 0);
	PUT_FIFO(T1064_o1, 1);

	GET_FIFO(T1065_i0, 1);
	GET_FIFO(T1065_i1, 3);
	Butterfly(T1065_i0, T1065_i1, &T1065_o0, &T1065_o1, T1065_W);
	PUT_FIFO(T1065_o0, 0);
	PUT_FIFO(T1065_o1, 1);

	GET_FIFO(T1066_i0, 1);
	GET_FIFO(T1066_i1, 3);
	Butterfly(T1066_i0, T1066_i1, &T1066_o0, &T1066_o1, T1066_W);
	PUT_FIFO(T1066_o0, 0);
	PUT_FIFO(T1066_o1, 1);

	GET_FIFO(T1067_i0, 1);
	GET_FIFO(T1067_i1, 3);
	Butterfly(T1067_i0, T1067_i1, &T1067_o0, &T1067_o1, T1067_W);
	PUT_FIFO(T1067_o0, 0);
	PUT_FIFO(T1067_o1, 1);

	GET_FIFO(T1068_i0, 1);
	GET_FIFO(T1068_i1, 3);
	Butterfly(T1068_i0, T1068_i1, &T1068_o0, &T1068_o1, T1068_W);
	PUT_FIFO(T1068_o0, 0);
	PUT_FIFO(T1068_o1, 1);

	GET_FIFO(T1069_i0, 1);
	GET_FIFO(T1069_i1, 3);
	Butterfly(T1069_i0, T1069_i1, &T1069_o0, &T1069_o1, T1069_W);
	PUT_FIFO(T1069_o0, 0);
	PUT_FIFO(T1069_o1, 1);

	GET_FIFO(T1070_i0, 1);
	GET_FIFO(T1070_i1, 3);
	Butterfly(T1070_i0, T1070_i1, &T1070_o0, &T1070_o1, T1070_W);
	PUT_FIFO(T1070_o0, 0);
	PUT_FIFO(T1070_o1, 1);

	GET_FIFO(T1071_i0, 1);
	GET_FIFO(T1071_i1, 3);
	Butterfly(T1071_i0, T1071_i1, &T1071_o0, &T1071_o1, T1071_W);
	PUT_FIFO(T1071_o0, 0);
	PUT_FIFO(T1071_o1, 1);

	GET_FIFO(T1072_i0, 0);
	GET_FIFO(T1072_i1, 2);
	Butterfly(T1072_i0, T1072_i1, &T1072_o0, &T1072_o1, T1072_W);
	PUT_FIFO(T1072_o0, 2);
	PUT_FIFO(T1072_o1, 3);

	GET_FIFO(T1073_i0, 0);
	GET_FIFO(T1073_i1, 2);
	Butterfly(T1073_i0, T1073_i1, &T1073_o0, &T1073_o1, T1073_W);
	PUT_FIFO(T1073_o0, 2);
	PUT_FIFO(T1073_o1, 3);

	GET_FIFO(T1074_i0, 0);
	GET_FIFO(T1074_i1, 2);
	Butterfly(T1074_i0, T1074_i1, &T1074_o0, &T1074_o1, T1074_W);
	PUT_FIFO(T1074_o0, 2);
	PUT_FIFO(T1074_o1, 3);

	GET_FIFO(T1075_i0, 0);
	GET_FIFO(T1075_i1, 2);
	Butterfly(T1075_i0, T1075_i1, &T1075_o0, &T1075_o1, T1075_W);
	PUT_FIFO(T1075_o0, 2);
	PUT_FIFO(T1075_o1, 3);

	GET_FIFO(T1076_i0, 0);
	GET_FIFO(T1076_i1, 2);
	Butterfly(T1076_i0, T1076_i1, &T1076_o0, &T1076_o1, T1076_W);
	PUT_FIFO(T1076_o0, 2);
	PUT_FIFO(T1076_o1, 3);

	GET_FIFO(T1077_i0, 0);
	GET_FIFO(T1077_i1, 2);
	Butterfly(T1077_i0, T1077_i1, &T1077_o0, &T1077_o1, T1077_W);
	PUT_FIFO(T1077_o0, 2);
	PUT_FIFO(T1077_o1, 3);

	GET_FIFO(T1078_i0, 0);
	GET_FIFO(T1078_i1, 2);
	Butterfly(T1078_i0, T1078_i1, &T1078_o0, &T1078_o1, T1078_W);
	PUT_FIFO(T1078_o0, 2);
	PUT_FIFO(T1078_o1, 3);

	GET_FIFO(T1079_i0, 0);
	GET_FIFO(T1079_i1, 2);
	Butterfly(T1079_i0, T1079_i1, &T1079_o0, &T1079_o1, T1079_W);
	PUT_FIFO(T1079_o0, 2);
	PUT_FIFO(T1079_o1, 3);

	GET_FIFO(T1080_i0, 1);
	GET_FIFO(T1080_i1, 3);
	Butterfly(T1080_i0, T1080_i1, &T1080_o0, &T1080_o1, T1080_W);
	PUT_FIFO(T1080_o0, 2);
	PUT_FIFO(T1080_o1, 3);

	GET_FIFO(T1081_i0, 1);
	GET_FIFO(T1081_i1, 3);
	Butterfly(T1081_i0, T1081_i1, &T1081_o0, &T1081_o1, T1081_W);
	PUT_FIFO(T1081_o0, 2);
	PUT_FIFO(T1081_o1, 3);

	GET_FIFO(T1082_i0, 1);
	GET_FIFO(T1082_i1, 3);
	Butterfly(T1082_i0, T1082_i1, &T1082_o0, &T1082_o1, T1082_W);
	PUT_FIFO(T1082_o0, 2);
	PUT_FIFO(T1082_o1, 3);

	GET_FIFO(T1083_i0, 1);
	GET_FIFO(T1083_i1, 3);
	Butterfly(T1083_i0, T1083_i1, &T1083_o0, &T1083_o1, T1083_W);
	PUT_FIFO(T1083_o0, 2);
	PUT_FIFO(T1083_o1, 3);

	GET_FIFO(T1084_i0, 1);
	GET_FIFO(T1084_i1, 3);
	Butterfly(T1084_i0, T1084_i1, &T1084_o0, &T1084_o1, T1084_W);
	PUT_FIFO(T1084_o0, 2);
	PUT_FIFO(T1084_o1, 3);

	GET_FIFO(T1085_i0, 1);
	GET_FIFO(T1085_i1, 3);
	Butterfly(T1085_i0, T1085_i1, &T1085_o0, &T1085_o1, T1085_W);
	PUT_FIFO(T1085_o0, 2);
	PUT_FIFO(T1085_o1, 3);

	GET_FIFO(T1086_i0, 1);
	GET_FIFO(T1086_i1, 3);
	Butterfly(T1086_i0, T1086_i1, &T1086_o0, &T1086_o1, T1086_W);
	PUT_FIFO(T1086_o0, 2);
	PUT_FIFO(T1086_o1, 3);

	GET_FIFO(T1087_i0, 1);
	GET_FIFO(T1087_i1, 3);
	Butterfly(T1087_i0, T1087_i1, &T1087_o0, &T1087_o1, T1087_W);
	PUT_FIFO(T1087_o0, 2);
	PUT_FIFO(T1087_o1, 3);

	GET_FIFO(T1088_i0, 0);
	GET_FIFO(T1088_i1, 2);
	Butterfly(T1088_i0, T1088_i1, &T1088_o0, &T1088_o1, T1088_W);
	PUT_FIFO(T1088_o0, 0);
	PUT_FIFO(T1088_o1, 1);

	GET_FIFO(T1089_i0, 0);
	GET_FIFO(T1089_i1, 2);
	Butterfly(T1089_i0, T1089_i1, &T1089_o0, &T1089_o1, T1089_W);
	PUT_FIFO(T1089_o0, 0);
	PUT_FIFO(T1089_o1, 1);

	GET_FIFO(T1090_i0, 0);
	GET_FIFO(T1090_i1, 2);
	Butterfly(T1090_i0, T1090_i1, &T1090_o0, &T1090_o1, T1090_W);
	PUT_FIFO(T1090_o0, 0);
	PUT_FIFO(T1090_o1, 1);

	GET_FIFO(T1091_i0, 0);
	GET_FIFO(T1091_i1, 2);
	Butterfly(T1091_i0, T1091_i1, &T1091_o0, &T1091_o1, T1091_W);
	PUT_FIFO(T1091_o0, 0);
	PUT_FIFO(T1091_o1, 1);

	GET_FIFO(T1092_i0, 0);
	GET_FIFO(T1092_i1, 2);
	Butterfly(T1092_i0, T1092_i1, &T1092_o0, &T1092_o1, T1092_W);
	PUT_FIFO(T1092_o0, 0);
	PUT_FIFO(T1092_o1, 1);

	GET_FIFO(T1093_i0, 0);
	GET_FIFO(T1093_i1, 2);
	Butterfly(T1093_i0, T1093_i1, &T1093_o0, &T1093_o1, T1093_W);
	PUT_FIFO(T1093_o0, 0);
	PUT_FIFO(T1093_o1, 1);

	GET_FIFO(T1094_i0, 0);
	GET_FIFO(T1094_i1, 2);
	Butterfly(T1094_i0, T1094_i1, &T1094_o0, &T1094_o1, T1094_W);
	PUT_FIFO(T1094_o0, 0);
	PUT_FIFO(T1094_o1, 1);

	GET_FIFO(T1095_i0, 0);
	GET_FIFO(T1095_i1, 2);
	Butterfly(T1095_i0, T1095_i1, &T1095_o0, &T1095_o1, T1095_W);
	PUT_FIFO(T1095_o0, 0);
	PUT_FIFO(T1095_o1, 1);

	GET_FIFO(T1096_i0, 1);
	GET_FIFO(T1096_i1, 3);
	Butterfly(T1096_i0, T1096_i1, &T1096_o0, &T1096_o1, T1096_W);
	PUT_FIFO(T1096_o0, 0);
	PUT_FIFO(T1096_o1, 1);

	GET_FIFO(T1097_i0, 1);
	GET_FIFO(T1097_i1, 3);
	Butterfly(T1097_i0, T1097_i1, &T1097_o0, &T1097_o1, T1097_W);
	PUT_FIFO(T1097_o0, 0);
	PUT_FIFO(T1097_o1, 1);

	GET_FIFO(T1098_i0, 1);
	GET_FIFO(T1098_i1, 3);
	Butterfly(T1098_i0, T1098_i1, &T1098_o0, &T1098_o1, T1098_W);
	PUT_FIFO(T1098_o0, 0);
	PUT_FIFO(T1098_o1, 1);

	GET_FIFO(T1099_i0, 1);
	GET_FIFO(T1099_i1, 3);
	Butterfly(T1099_i0, T1099_i1, &T1099_o0, &T1099_o1, T1099_W);
	PUT_FIFO(T1099_o0, 0);
	PUT_FIFO(T1099_o1, 1);

	GET_FIFO(T1100_i0, 1);
	GET_FIFO(T1100_i1, 3);
	Butterfly(T1100_i0, T1100_i1, &T1100_o0, &T1100_o1, T1100_W);
	PUT_FIFO(T1100_o0, 0);
	PUT_FIFO(T1100_o1, 1);

	GET_FIFO(T1101_i0, 1);
	GET_FIFO(T1101_i1, 3);
	Butterfly(T1101_i0, T1101_i1, &T1101_o0, &T1101_o1, T1101_W);
	PUT_FIFO(T1101_o0, 0);
	PUT_FIFO(T1101_o1, 1);

	GET_FIFO(T1102_i0, 1);
	GET_FIFO(T1102_i1, 3);
	Butterfly(T1102_i0, T1102_i1, &T1102_o0, &T1102_o1, T1102_W);
	PUT_FIFO(T1102_o0, 0);
	PUT_FIFO(T1102_o1, 1);

	GET_FIFO(T1103_i0, 1);
	GET_FIFO(T1103_i1, 3);
	Butterfly(T1103_i0, T1103_i1, &T1103_o0, &T1103_o1, T1103_W);
	PUT_FIFO(T1103_o0, 0);
	PUT_FIFO(T1103_o1, 1);

	GET_FIFO(T1104_i0, 0);
	GET_FIFO(T1104_i1, 2);
	Butterfly(T1104_i0, T1104_i1, &T1104_o0, &T1104_o1, T1104_W);
	PUT_FIFO(T1104_o0, 2);
	PUT_FIFO(T1104_o1, 3);

	GET_FIFO(T1105_i0, 0);
	GET_FIFO(T1105_i1, 2);
	Butterfly(T1105_i0, T1105_i1, &T1105_o0, &T1105_o1, T1105_W);
	PUT_FIFO(T1105_o0, 2);
	PUT_FIFO(T1105_o1, 3);

	GET_FIFO(T1106_i0, 0);
	GET_FIFO(T1106_i1, 2);
	Butterfly(T1106_i0, T1106_i1, &T1106_o0, &T1106_o1, T1106_W);
	PUT_FIFO(T1106_o0, 2);
	PUT_FIFO(T1106_o1, 3);

	GET_FIFO(T1107_i0, 0);
	GET_FIFO(T1107_i1, 2);
	Butterfly(T1107_i0, T1107_i1, &T1107_o0, &T1107_o1, T1107_W);
	PUT_FIFO(T1107_o0, 2);
	PUT_FIFO(T1107_o1, 3);

	GET_FIFO(T1108_i0, 0);
	GET_FIFO(T1108_i1, 2);
	Butterfly(T1108_i0, T1108_i1, &T1108_o0, &T1108_o1, T1108_W);
	PUT_FIFO(T1108_o0, 2);
	PUT_FIFO(T1108_o1, 3);

	GET_FIFO(T1109_i0, 0);
	GET_FIFO(T1109_i1, 2);
	Butterfly(T1109_i0, T1109_i1, &T1109_o0, &T1109_o1, T1109_W);
	PUT_FIFO(T1109_o0, 2);
	PUT_FIFO(T1109_o1, 3);

	GET_FIFO(T1110_i0, 0);
	GET_FIFO(T1110_i1, 2);
	Butterfly(T1110_i0, T1110_i1, &T1110_o0, &T1110_o1, T1110_W);
	PUT_FIFO(T1110_o0, 2);
	PUT_FIFO(T1110_o1, 3);

	GET_FIFO(T1111_i0, 0);
	GET_FIFO(T1111_i1, 2);
	Butterfly(T1111_i0, T1111_i1, &T1111_o0, &T1111_o1, T1111_W);
	PUT_FIFO(T1111_o0, 2);
	PUT_FIFO(T1111_o1, 3);

	GET_FIFO(T1112_i0, 1);
	GET_FIFO(T1112_i1, 3);
	Butterfly(T1112_i0, T1112_i1, &T1112_o0, &T1112_o1, T1112_W);
	PUT_FIFO(T1112_o0, 2);
	PUT_FIFO(T1112_o1, 3);

	GET_FIFO(T1113_i0, 1);
	GET_FIFO(T1113_i1, 3);
	Butterfly(T1113_i0, T1113_i1, &T1113_o0, &T1113_o1, T1113_W);
	PUT_FIFO(T1113_o0, 2);
	PUT_FIFO(T1113_o1, 3);

	GET_FIFO(T1114_i0, 1);
	GET_FIFO(T1114_i1, 3);
	Butterfly(T1114_i0, T1114_i1, &T1114_o0, &T1114_o1, T1114_W);
	PUT_FIFO(T1114_o0, 2);
	PUT_FIFO(T1114_o1, 3);

	GET_FIFO(T1115_i0, 1);
	GET_FIFO(T1115_i1, 3);
	Butterfly(T1115_i0, T1115_i1, &T1115_o0, &T1115_o1, T1115_W);
	PUT_FIFO(T1115_o0, 2);
	PUT_FIFO(T1115_o1, 3);

	GET_FIFO(T1116_i0, 1);
	GET_FIFO(T1116_i1, 3);
	Butterfly(T1116_i0, T1116_i1, &T1116_o0, &T1116_o1, T1116_W);
	PUT_FIFO(T1116_o0, 2);
	PUT_FIFO(T1116_o1, 3);

	GET_FIFO(T1117_i0, 1);
	GET_FIFO(T1117_i1, 3);
	Butterfly(T1117_i0, T1117_i1, &T1117_o0, &T1117_o1, T1117_W);
	PUT_FIFO(T1117_o0, 2);
	PUT_FIFO(T1117_o1, 3);

	GET_FIFO(T1118_i0, 1);
	GET_FIFO(T1118_i1, 3);
	Butterfly(T1118_i0, T1118_i1, &T1118_o0, &T1118_o1, T1118_W);
	PUT_FIFO(T1118_o0, 2);
	PUT_FIFO(T1118_o1, 3);

	GET_FIFO(T1119_i0, 1);
	GET_FIFO(T1119_i1, 3);
	Butterfly(T1119_i0, T1119_i1, &T1119_o0, &T1119_o1, T1119_W);
	PUT_FIFO(T1119_o0, 2);
	PUT_FIFO(T1119_o1, 3);

	GET_FIFO(T1120_i0, 0);
	GET_FIFO(T1120_i1, 2);
	Butterfly(T1120_i0, T1120_i1, &T1120_o0, &T1120_o1, T1120_W);
	PUT_FIFO(T1120_o0, 0);
	PUT_FIFO(T1120_o1, 1);

	GET_FIFO(T1121_i0, 0);
	GET_FIFO(T1121_i1, 2);
	Butterfly(T1121_i0, T1121_i1, &T1121_o0, &T1121_o1, T1121_W);
	PUT_FIFO(T1121_o0, 0);
	PUT_FIFO(T1121_o1, 1);

	GET_FIFO(T1122_i0, 0);
	GET_FIFO(T1122_i1, 2);
	Butterfly(T1122_i0, T1122_i1, &T1122_o0, &T1122_o1, T1122_W);
	PUT_FIFO(T1122_o0, 0);
	PUT_FIFO(T1122_o1, 1);

	GET_FIFO(T1123_i0, 0);
	GET_FIFO(T1123_i1, 2);
	Butterfly(T1123_i0, T1123_i1, &T1123_o0, &T1123_o1, T1123_W);
	PUT_FIFO(T1123_o0, 0);
	PUT_FIFO(T1123_o1, 1);

	GET_FIFO(T1124_i0, 0);
	GET_FIFO(T1124_i1, 2);
	Butterfly(T1124_i0, T1124_i1, &T1124_o0, &T1124_o1, T1124_W);
	PUT_FIFO(T1124_o0, 0);
	PUT_FIFO(T1124_o1, 1);

	GET_FIFO(T1125_i0, 0);
	GET_FIFO(T1125_i1, 2);
	Butterfly(T1125_i0, T1125_i1, &T1125_o0, &T1125_o1, T1125_W);
	PUT_FIFO(T1125_o0, 0);
	PUT_FIFO(T1125_o1, 1);

	GET_FIFO(T1126_i0, 0);
	GET_FIFO(T1126_i1, 2);
	Butterfly(T1126_i0, T1126_i1, &T1126_o0, &T1126_o1, T1126_W);
	PUT_FIFO(T1126_o0, 0);
	PUT_FIFO(T1126_o1, 1);

	GET_FIFO(T1127_i0, 0);
	GET_FIFO(T1127_i1, 2);
	Butterfly(T1127_i0, T1127_i1, &T1127_o0, &T1127_o1, T1127_W);
	PUT_FIFO(T1127_o0, 0);
	PUT_FIFO(T1127_o1, 1);

	GET_FIFO(T1128_i0, 1);
	GET_FIFO(T1128_i1, 3);
	Butterfly(T1128_i0, T1128_i1, &T1128_o0, &T1128_o1, T1128_W);
	PUT_FIFO(T1128_o0, 0);
	PUT_FIFO(T1128_o1, 1);

	GET_FIFO(T1129_i0, 1);
	GET_FIFO(T1129_i1, 3);
	Butterfly(T1129_i0, T1129_i1, &T1129_o0, &T1129_o1, T1129_W);
	PUT_FIFO(T1129_o0, 0);
	PUT_FIFO(T1129_o1, 1);

	GET_FIFO(T1130_i0, 1);
	GET_FIFO(T1130_i1, 3);
	Butterfly(T1130_i0, T1130_i1, &T1130_o0, &T1130_o1, T1130_W);
	PUT_FIFO(T1130_o0, 0);
	PUT_FIFO(T1130_o1, 1);

	GET_FIFO(T1131_i0, 1);
	GET_FIFO(T1131_i1, 3);
	Butterfly(T1131_i0, T1131_i1, &T1131_o0, &T1131_o1, T1131_W);
	PUT_FIFO(T1131_o0, 0);
	PUT_FIFO(T1131_o1, 1);

	GET_FIFO(T1132_i0, 1);
	GET_FIFO(T1132_i1, 3);
	Butterfly(T1132_i0, T1132_i1, &T1132_o0, &T1132_o1, T1132_W);
	PUT_FIFO(T1132_o0, 0);
	PUT_FIFO(T1132_o1, 1);

	GET_FIFO(T1133_i0, 1);
	GET_FIFO(T1133_i1, 3);
	Butterfly(T1133_i0, T1133_i1, &T1133_o0, &T1133_o1, T1133_W);
	PUT_FIFO(T1133_o0, 0);
	PUT_FIFO(T1133_o1, 1);

	GET_FIFO(T1134_i0, 1);
	GET_FIFO(T1134_i1, 3);
	Butterfly(T1134_i0, T1134_i1, &T1134_o0, &T1134_o1, T1134_W);
	PUT_FIFO(T1134_o0, 0);
	PUT_FIFO(T1134_o1, 1);

	GET_FIFO(T1135_i0, 1);
	GET_FIFO(T1135_i1, 3);
	Butterfly(T1135_i0, T1135_i1, &T1135_o0, &T1135_o1, T1135_W);
	PUT_FIFO(T1135_o0, 0);
	PUT_FIFO(T1135_o1, 1);

	GET_FIFO(T1136_i0, 0);
	GET_FIFO(T1136_i1, 2);
	Butterfly(T1136_i0, T1136_i1, &T1136_o0, &T1136_o1, T1136_W);
	PUT_FIFO(T1136_o0, 2);
	PUT_FIFO(T1136_o1, 3);

	GET_FIFO(T1137_i0, 0);
	GET_FIFO(T1137_i1, 2);
	Butterfly(T1137_i0, T1137_i1, &T1137_o0, &T1137_o1, T1137_W);
	PUT_FIFO(T1137_o0, 2);
	PUT_FIFO(T1137_o1, 3);

	GET_FIFO(T1138_i0, 0);
	GET_FIFO(T1138_i1, 2);
	Butterfly(T1138_i0, T1138_i1, &T1138_o0, &T1138_o1, T1138_W);
	PUT_FIFO(T1138_o0, 2);
	PUT_FIFO(T1138_o1, 3);

	GET_FIFO(T1139_i0, 0);
	GET_FIFO(T1139_i1, 2);
	Butterfly(T1139_i0, T1139_i1, &T1139_o0, &T1139_o1, T1139_W);
	PUT_FIFO(T1139_o0, 2);
	PUT_FIFO(T1139_o1, 3);

	GET_FIFO(T1140_i0, 0);
	GET_FIFO(T1140_i1, 2);
	Butterfly(T1140_i0, T1140_i1, &T1140_o0, &T1140_o1, T1140_W);
	PUT_FIFO(T1140_o0, 2);
	PUT_FIFO(T1140_o1, 3);

	GET_FIFO(T1141_i0, 0);
	GET_FIFO(T1141_i1, 2);
	Butterfly(T1141_i0, T1141_i1, &T1141_o0, &T1141_o1, T1141_W);
	PUT_FIFO(T1141_o0, 2);
	PUT_FIFO(T1141_o1, 3);

	GET_FIFO(T1142_i0, 0);
	GET_FIFO(T1142_i1, 2);
	Butterfly(T1142_i0, T1142_i1, &T1142_o0, &T1142_o1, T1142_W);
	PUT_FIFO(T1142_o0, 2);
	PUT_FIFO(T1142_o1, 3);

	GET_FIFO(T1143_i0, 0);
	GET_FIFO(T1143_i1, 2);
	Butterfly(T1143_i0, T1143_i1, &T1143_o0, &T1143_o1, T1143_W);
	PUT_FIFO(T1143_o0, 2);
	PUT_FIFO(T1143_o1, 3);

	GET_FIFO(T1144_i0, 1);
	GET_FIFO(T1144_i1, 3);
	Butterfly(T1144_i0, T1144_i1, &T1144_o0, &T1144_o1, T1144_W);
	PUT_FIFO(T1144_o0, 2);
	PUT_FIFO(T1144_o1, 3);

	GET_FIFO(T1145_i0, 1);
	GET_FIFO(T1145_i1, 3);
	Butterfly(T1145_i0, T1145_i1, &T1145_o0, &T1145_o1, T1145_W);
	PUT_FIFO(T1145_o0, 2);
	PUT_FIFO(T1145_o1, 3);

	GET_FIFO(T1146_i0, 1);
	GET_FIFO(T1146_i1, 3);
	Butterfly(T1146_i0, T1146_i1, &T1146_o0, &T1146_o1, T1146_W);
	PUT_FIFO(T1146_o0, 2);
	PUT_FIFO(T1146_o1, 3);

	GET_FIFO(T1147_i0, 1);
	GET_FIFO(T1147_i1, 3);
	Butterfly(T1147_i0, T1147_i1, &T1147_o0, &T1147_o1, T1147_W);
	PUT_FIFO(T1147_o0, 2);
	PUT_FIFO(T1147_o1, 3);

	GET_FIFO(T1148_i0, 1);
	GET_FIFO(T1148_i1, 3);
	Butterfly(T1148_i0, T1148_i1, &T1148_o0, &T1148_o1, T1148_W);
	PUT_FIFO(T1148_o0, 2);
	PUT_FIFO(T1148_o1, 3);

	GET_FIFO(T1149_i0, 1);
	GET_FIFO(T1149_i1, 3);
	Butterfly(T1149_i0, T1149_i1, &T1149_o0, &T1149_o1, T1149_W);
	PUT_FIFO(T1149_o0, 2);
	PUT_FIFO(T1149_o1, 3);

	GET_FIFO(T1150_i0, 1);
	GET_FIFO(T1150_i1, 3);
	Butterfly(T1150_i0, T1150_i1, &T1150_o0, &T1150_o1, T1150_W);
	PUT_FIFO(T1150_o0, 2);
	PUT_FIFO(T1150_o1, 3);

	GET_FIFO(T1151_i0, 1);
	GET_FIFO(T1151_i1, 3);
	Butterfly(T1151_i0, T1151_i1, &T1151_o0, &T1151_o1, T1151_W);
	PUT_FIFO(T1151_o0, 2);
	PUT_FIFO(T1151_o1, 3);

	GET_FIFO(T1152_i0, 0);
	GET_FIFO(T1152_i1, 2);
	Butterfly(T1152_i0, T1152_i1, &T1152_o0, &T1152_o1, T1152_W);
	PUT_FIFO(T1152_o0, 0);
	PUT_FIFO(T1152_o1, 1);

	GET_FIFO(T1153_i0, 0);
	GET_FIFO(T1153_i1, 2);
	Butterfly(T1153_i0, T1153_i1, &T1153_o0, &T1153_o1, T1153_W);
	PUT_FIFO(T1153_o0, 0);
	PUT_FIFO(T1153_o1, 1);

	GET_FIFO(T1154_i0, 0);
	GET_FIFO(T1154_i1, 2);
	Butterfly(T1154_i0, T1154_i1, &T1154_o0, &T1154_o1, T1154_W);
	PUT_FIFO(T1154_o0, 0);
	PUT_FIFO(T1154_o1, 1);

	GET_FIFO(T1155_i0, 0);
	GET_FIFO(T1155_i1, 2);
	Butterfly(T1155_i0, T1155_i1, &T1155_o0, &T1155_o1, T1155_W);
	PUT_FIFO(T1155_o0, 0);
	PUT_FIFO(T1155_o1, 1);

	GET_FIFO(T1156_i0, 0);
	GET_FIFO(T1156_i1, 2);
	Butterfly(T1156_i0, T1156_i1, &T1156_o0, &T1156_o1, T1156_W);
	PUT_FIFO(T1156_o0, 0);
	PUT_FIFO(T1156_o1, 1);

	GET_FIFO(T1157_i0, 0);
	GET_FIFO(T1157_i1, 2);
	Butterfly(T1157_i0, T1157_i1, &T1157_o0, &T1157_o1, T1157_W);
	PUT_FIFO(T1157_o0, 0);
	PUT_FIFO(T1157_o1, 1);

	GET_FIFO(T1158_i0, 0);
	GET_FIFO(T1158_i1, 2);
	Butterfly(T1158_i0, T1158_i1, &T1158_o0, &T1158_o1, T1158_W);
	PUT_FIFO(T1158_o0, 0);
	PUT_FIFO(T1158_o1, 1);

	GET_FIFO(T1159_i0, 0);
	GET_FIFO(T1159_i1, 2);
	Butterfly(T1159_i0, T1159_i1, &T1159_o0, &T1159_o1, T1159_W);
	PUT_FIFO(T1159_o0, 0);
	PUT_FIFO(T1159_o1, 1);

	GET_FIFO(T1160_i0, 1);
	GET_FIFO(T1160_i1, 3);
	Butterfly(T1160_i0, T1160_i1, &T1160_o0, &T1160_o1, T1160_W);
	PUT_FIFO(T1160_o0, 0);
	PUT_FIFO(T1160_o1, 1);

	GET_FIFO(T1161_i0, 1);
	GET_FIFO(T1161_i1, 3);
	Butterfly(T1161_i0, T1161_i1, &T1161_o0, &T1161_o1, T1161_W);
	PUT_FIFO(T1161_o0, 0);
	PUT_FIFO(T1161_o1, 1);

	GET_FIFO(T1162_i0, 1);
	GET_FIFO(T1162_i1, 3);
	Butterfly(T1162_i0, T1162_i1, &T1162_o0, &T1162_o1, T1162_W);
	PUT_FIFO(T1162_o0, 0);
	PUT_FIFO(T1162_o1, 1);

	GET_FIFO(T1163_i0, 1);
	GET_FIFO(T1163_i1, 3);
	Butterfly(T1163_i0, T1163_i1, &T1163_o0, &T1163_o1, T1163_W);
	PUT_FIFO(T1163_o0, 0);
	PUT_FIFO(T1163_o1, 1);

	GET_FIFO(T1164_i0, 1);
	GET_FIFO(T1164_i1, 3);
	Butterfly(T1164_i0, T1164_i1, &T1164_o0, &T1164_o1, T1164_W);
	PUT_FIFO(T1164_o0, 0);
	PUT_FIFO(T1164_o1, 1);

	GET_FIFO(T1165_i0, 1);
	GET_FIFO(T1165_i1, 3);
	Butterfly(T1165_i0, T1165_i1, &T1165_o0, &T1165_o1, T1165_W);
	PUT_FIFO(T1165_o0, 0);
	PUT_FIFO(T1165_o1, 1);

	GET_FIFO(T1166_i0, 1);
	GET_FIFO(T1166_i1, 3);
	Butterfly(T1166_i0, T1166_i1, &T1166_o0, &T1166_o1, T1166_W);
	PUT_FIFO(T1166_o0, 0);
	PUT_FIFO(T1166_o1, 1);

	GET_FIFO(T1167_i0, 1);
	GET_FIFO(T1167_i1, 3);
	Butterfly(T1167_i0, T1167_i1, &T1167_o0, &T1167_o1, T1167_W);
	PUT_FIFO(T1167_o0, 0);
	PUT_FIFO(T1167_o1, 1);

	GET_FIFO(T1168_i0, 0);
	GET_FIFO(T1168_i1, 2);
	Butterfly(T1168_i0, T1168_i1, &T1168_o0, &T1168_o1, T1168_W);
	PUT_FIFO(T1168_o0, 2);
	PUT_FIFO(T1168_o1, 3);

	GET_FIFO(T1169_i0, 0);
	GET_FIFO(T1169_i1, 2);
	Butterfly(T1169_i0, T1169_i1, &T1169_o0, &T1169_o1, T1169_W);
	PUT_FIFO(T1169_o0, 2);
	PUT_FIFO(T1169_o1, 3);

	GET_FIFO(T1170_i0, 0);
	GET_FIFO(T1170_i1, 2);
	Butterfly(T1170_i0, T1170_i1, &T1170_o0, &T1170_o1, T1170_W);
	PUT_FIFO(T1170_o0, 2);
	PUT_FIFO(T1170_o1, 3);

	GET_FIFO(T1171_i0, 0);
	GET_FIFO(T1171_i1, 2);
	Butterfly(T1171_i0, T1171_i1, &T1171_o0, &T1171_o1, T1171_W);
	PUT_FIFO(T1171_o0, 2);
	PUT_FIFO(T1171_o1, 3);

	GET_FIFO(T1172_i0, 0);
	GET_FIFO(T1172_i1, 2);
	Butterfly(T1172_i0, T1172_i1, &T1172_o0, &T1172_o1, T1172_W);
	PUT_FIFO(T1172_o0, 2);
	PUT_FIFO(T1172_o1, 3);

	GET_FIFO(T1173_i0, 0);
	GET_FIFO(T1173_i1, 2);
	Butterfly(T1173_i0, T1173_i1, &T1173_o0, &T1173_o1, T1173_W);
	PUT_FIFO(T1173_o0, 2);
	PUT_FIFO(T1173_o1, 3);

	GET_FIFO(T1174_i0, 0);
	GET_FIFO(T1174_i1, 2);
	Butterfly(T1174_i0, T1174_i1, &T1174_o0, &T1174_o1, T1174_W);
	PUT_FIFO(T1174_o0, 2);
	PUT_FIFO(T1174_o1, 3);

	GET_FIFO(T1175_i0, 0);
	GET_FIFO(T1175_i1, 2);
	Butterfly(T1175_i0, T1175_i1, &T1175_o0, &T1175_o1, T1175_W);
	PUT_FIFO(T1175_o0, 2);
	PUT_FIFO(T1175_o1, 3);

	GET_FIFO(T1176_i0, 1);
	GET_FIFO(T1176_i1, 3);
	Butterfly(T1176_i0, T1176_i1, &T1176_o0, &T1176_o1, T1176_W);
	PUT_FIFO(T1176_o0, 2);
	PUT_FIFO(T1176_o1, 3);

	GET_FIFO(T1177_i0, 1);
	GET_FIFO(T1177_i1, 3);
	Butterfly(T1177_i0, T1177_i1, &T1177_o0, &T1177_o1, T1177_W);
	PUT_FIFO(T1177_o0, 2);
	PUT_FIFO(T1177_o1, 3);

	GET_FIFO(T1178_i0, 1);
	GET_FIFO(T1178_i1, 3);
	Butterfly(T1178_i0, T1178_i1, &T1178_o0, &T1178_o1, T1178_W);
	PUT_FIFO(T1178_o0, 2);
	PUT_FIFO(T1178_o1, 3);

	GET_FIFO(T1179_i0, 1);
	GET_FIFO(T1179_i1, 3);
	Butterfly(T1179_i0, T1179_i1, &T1179_o0, &T1179_o1, T1179_W);
	PUT_FIFO(T1179_o0, 2);
	PUT_FIFO(T1179_o1, 3);

	GET_FIFO(T1180_i0, 1);
	GET_FIFO(T1180_i1, 3);
	Butterfly(T1180_i0, T1180_i1, &T1180_o0, &T1180_o1, T1180_W);
	PUT_FIFO(T1180_o0, 2);
	PUT_FIFO(T1180_o1, 3);

	GET_FIFO(T1181_i0, 1);
	GET_FIFO(T1181_i1, 3);
	Butterfly(T1181_i0, T1181_i1, &T1181_o0, &T1181_o1, T1181_W);
	PUT_FIFO(T1181_o0, 2);
	PUT_FIFO(T1181_o1, 3);

	GET_FIFO(T1182_i0, 1);
	GET_FIFO(T1182_i1, 3);
	Butterfly(T1182_i0, T1182_i1, &T1182_o0, &T1182_o1, T1182_W);
	PUT_FIFO(T1182_o0, 2);
	PUT_FIFO(T1182_o1, 3);

	GET_FIFO(T1183_i0, 1);
	GET_FIFO(T1183_i1, 3);
	Butterfly(T1183_i0, T1183_i1, &T1183_o0, &T1183_o1, T1183_W);
	PUT_FIFO(T1183_o0, 2);
	PUT_FIFO(T1183_o1, 3);

	GET_FIFO(T1184_i0, 0);
	GET_FIFO(T1184_i1, 2);
	Butterfly(T1184_i0, T1184_i1, &T1184_o0, &T1184_o1, T1184_W);
	PUT_FIFO(T1184_o0, 0);
	PUT_FIFO(T1184_o1, 1);

	GET_FIFO(T1185_i0, 0);
	GET_FIFO(T1185_i1, 2);
	Butterfly(T1185_i0, T1185_i1, &T1185_o0, &T1185_o1, T1185_W);
	PUT_FIFO(T1185_o0, 0);
	PUT_FIFO(T1185_o1, 1);

	GET_FIFO(T1186_i0, 0);
	GET_FIFO(T1186_i1, 2);
	Butterfly(T1186_i0, T1186_i1, &T1186_o0, &T1186_o1, T1186_W);
	PUT_FIFO(T1186_o0, 0);
	PUT_FIFO(T1186_o1, 1);

	GET_FIFO(T1187_i0, 0);
	GET_FIFO(T1187_i1, 2);
	Butterfly(T1187_i0, T1187_i1, &T1187_o0, &T1187_o1, T1187_W);
	PUT_FIFO(T1187_o0, 0);
	PUT_FIFO(T1187_o1, 1);

	GET_FIFO(T1188_i0, 0);
	GET_FIFO(T1188_i1, 2);
	Butterfly(T1188_i0, T1188_i1, &T1188_o0, &T1188_o1, T1188_W);
	PUT_FIFO(T1188_o0, 0);
	PUT_FIFO(T1188_o1, 1);

	GET_FIFO(T1189_i0, 0);
	GET_FIFO(T1189_i1, 2);
	Butterfly(T1189_i0, T1189_i1, &T1189_o0, &T1189_o1, T1189_W);
	PUT_FIFO(T1189_o0, 0);
	PUT_FIFO(T1189_o1, 1);

	GET_FIFO(T1190_i0, 0);
	GET_FIFO(T1190_i1, 2);
	Butterfly(T1190_i0, T1190_i1, &T1190_o0, &T1190_o1, T1190_W);
	PUT_FIFO(T1190_o0, 0);
	PUT_FIFO(T1190_o1, 1);

	GET_FIFO(T1191_i0, 0);
	GET_FIFO(T1191_i1, 2);
	Butterfly(T1191_i0, T1191_i1, &T1191_o0, &T1191_o1, T1191_W);
	PUT_FIFO(T1191_o0, 0);
	PUT_FIFO(T1191_o1, 1);

	GET_FIFO(T1192_i0, 1);
	GET_FIFO(T1192_i1, 3);
	Butterfly(T1192_i0, T1192_i1, &T1192_o0, &T1192_o1, T1192_W);
	PUT_FIFO(T1192_o0, 0);
	PUT_FIFO(T1192_o1, 1);

	GET_FIFO(T1193_i0, 1);
	GET_FIFO(T1193_i1, 3);
	Butterfly(T1193_i0, T1193_i1, &T1193_o0, &T1193_o1, T1193_W);
	PUT_FIFO(T1193_o0, 0);
	PUT_FIFO(T1193_o1, 1);

	GET_FIFO(T1194_i0, 1);
	GET_FIFO(T1194_i1, 3);
	Butterfly(T1194_i0, T1194_i1, &T1194_o0, &T1194_o1, T1194_W);
	PUT_FIFO(T1194_o0, 0);
	PUT_FIFO(T1194_o1, 1);

	GET_FIFO(T1195_i0, 1);
	GET_FIFO(T1195_i1, 3);
	Butterfly(T1195_i0, T1195_i1, &T1195_o0, &T1195_o1, T1195_W);
	PUT_FIFO(T1195_o0, 0);
	PUT_FIFO(T1195_o1, 1);

	GET_FIFO(T1196_i0, 1);
	GET_FIFO(T1196_i1, 3);
	Butterfly(T1196_i0, T1196_i1, &T1196_o0, &T1196_o1, T1196_W);
	PUT_FIFO(T1196_o0, 0);
	PUT_FIFO(T1196_o1, 1);

	GET_FIFO(T1197_i0, 1);
	GET_FIFO(T1197_i1, 3);
	Butterfly(T1197_i0, T1197_i1, &T1197_o0, &T1197_o1, T1197_W);
	PUT_FIFO(T1197_o0, 0);
	PUT_FIFO(T1197_o1, 1);

	GET_FIFO(T1198_i0, 1);
	GET_FIFO(T1198_i1, 3);
	Butterfly(T1198_i0, T1198_i1, &T1198_o0, &T1198_o1, T1198_W);
	PUT_FIFO(T1198_o0, 0);
	PUT_FIFO(T1198_o1, 1);

	GET_FIFO(T1199_i0, 1);
	GET_FIFO(T1199_i1, 3);
	Butterfly(T1199_i0, T1199_i1, &T1199_o0, &T1199_o1, T1199_W);
	PUT_FIFO(T1199_o0, 0);
	PUT_FIFO(T1199_o1, 1);

	GET_FIFO(T1200_i0, 0);
	GET_FIFO(T1200_i1, 2);
	Butterfly(T1200_i0, T1200_i1, &T1200_o0, &T1200_o1, T1200_W);
	PUT_FIFO(T1200_o0, 2);
	PUT_FIFO(T1200_o1, 3);

	GET_FIFO(T1201_i0, 0);
	GET_FIFO(T1201_i1, 2);
	Butterfly(T1201_i0, T1201_i1, &T1201_o0, &T1201_o1, T1201_W);
	PUT_FIFO(T1201_o0, 2);
	PUT_FIFO(T1201_o1, 3);

	GET_FIFO(T1202_i0, 0);
	GET_FIFO(T1202_i1, 2);
	Butterfly(T1202_i0, T1202_i1, &T1202_o0, &T1202_o1, T1202_W);
	PUT_FIFO(T1202_o0, 2);
	PUT_FIFO(T1202_o1, 3);

	GET_FIFO(T1203_i0, 0);
	GET_FIFO(T1203_i1, 2);
	Butterfly(T1203_i0, T1203_i1, &T1203_o0, &T1203_o1, T1203_W);
	PUT_FIFO(T1203_o0, 2);
	PUT_FIFO(T1203_o1, 3);

	GET_FIFO(T1204_i0, 0);
	GET_FIFO(T1204_i1, 2);
	Butterfly(T1204_i0, T1204_i1, &T1204_o0, &T1204_o1, T1204_W);
	PUT_FIFO(T1204_o0, 2);
	PUT_FIFO(T1204_o1, 3);

	GET_FIFO(T1205_i0, 0);
	GET_FIFO(T1205_i1, 2);
	Butterfly(T1205_i0, T1205_i1, &T1205_o0, &T1205_o1, T1205_W);
	PUT_FIFO(T1205_o0, 2);
	PUT_FIFO(T1205_o1, 3);

	GET_FIFO(T1206_i0, 0);
	GET_FIFO(T1206_i1, 2);
	Butterfly(T1206_i0, T1206_i1, &T1206_o0, &T1206_o1, T1206_W);
	PUT_FIFO(T1206_o0, 2);
	PUT_FIFO(T1206_o1, 3);

	GET_FIFO(T1207_i0, 0);
	GET_FIFO(T1207_i1, 2);
	Butterfly(T1207_i0, T1207_i1, &T1207_o0, &T1207_o1, T1207_W);
	PUT_FIFO(T1207_o0, 2);
	PUT_FIFO(T1207_o1, 3);

	GET_FIFO(T1208_i0, 1);
	GET_FIFO(T1208_i1, 3);
	Butterfly(T1208_i0, T1208_i1, &T1208_o0, &T1208_o1, T1208_W);
	PUT_FIFO(T1208_o0, 2);
	PUT_FIFO(T1208_o1, 3);

	GET_FIFO(T1209_i0, 1);
	GET_FIFO(T1209_i1, 3);
	Butterfly(T1209_i0, T1209_i1, &T1209_o0, &T1209_o1, T1209_W);
	PUT_FIFO(T1209_o0, 2);
	PUT_FIFO(T1209_o1, 3);

	GET_FIFO(T1210_i0, 1);
	GET_FIFO(T1210_i1, 3);
	Butterfly(T1210_i0, T1210_i1, &T1210_o0, &T1210_o1, T1210_W);
	PUT_FIFO(T1210_o0, 2);
	PUT_FIFO(T1210_o1, 3);

	GET_FIFO(T1211_i0, 1);
	GET_FIFO(T1211_i1, 3);
	Butterfly(T1211_i0, T1211_i1, &T1211_o0, &T1211_o1, T1211_W);
	PUT_FIFO(T1211_o0, 2);
	PUT_FIFO(T1211_o1, 3);

	GET_FIFO(T1212_i0, 1);
	GET_FIFO(T1212_i1, 3);
	Butterfly(T1212_i0, T1212_i1, &T1212_o0, &T1212_o1, T1212_W);
	PUT_FIFO(T1212_o0, 2);
	PUT_FIFO(T1212_o1, 3);

	GET_FIFO(T1213_i0, 1);
	GET_FIFO(T1213_i1, 3);
	Butterfly(T1213_i0, T1213_i1, &T1213_o0, &T1213_o1, T1213_W);
	PUT_FIFO(T1213_o0, 2);
	PUT_FIFO(T1213_o1, 3);

	GET_FIFO(T1214_i0, 1);
	GET_FIFO(T1214_i1, 3);
	Butterfly(T1214_i0, T1214_i1, &T1214_o0, &T1214_o1, T1214_W);
	PUT_FIFO(T1214_o0, 2);
	PUT_FIFO(T1214_o1, 3);

	GET_FIFO(T1215_i0, 1);
	GET_FIFO(T1215_i1, 3);
	Butterfly(T1215_i0, T1215_i1, &T1215_o0, &T1215_o1, T1215_W);
	PUT_FIFO(T1215_o0, 2);
	PUT_FIFO(T1215_o1, 3);

	GET_FIFO(T1216_i0, 0);
	GET_FIFO(T1216_i1, 2);
	Butterfly(T1216_i0, T1216_i1, &T1216_o0, &T1216_o1, T1216_W);
	PUT_FIFO(T1216_o0, 0);
	PUT_FIFO(T1216_o1, 1);

	GET_FIFO(T1217_i0, 0);
	GET_FIFO(T1217_i1, 2);
	Butterfly(T1217_i0, T1217_i1, &T1217_o0, &T1217_o1, T1217_W);
	PUT_FIFO(T1217_o0, 0);
	PUT_FIFO(T1217_o1, 1);

	GET_FIFO(T1218_i0, 0);
	GET_FIFO(T1218_i1, 2);
	Butterfly(T1218_i0, T1218_i1, &T1218_o0, &T1218_o1, T1218_W);
	PUT_FIFO(T1218_o0, 0);
	PUT_FIFO(T1218_o1, 1);

	GET_FIFO(T1219_i0, 0);
	GET_FIFO(T1219_i1, 2);
	Butterfly(T1219_i0, T1219_i1, &T1219_o0, &T1219_o1, T1219_W);
	PUT_FIFO(T1219_o0, 0);
	PUT_FIFO(T1219_o1, 1);

	GET_FIFO(T1220_i0, 0);
	GET_FIFO(T1220_i1, 2);
	Butterfly(T1220_i0, T1220_i1, &T1220_o0, &T1220_o1, T1220_W);
	PUT_FIFO(T1220_o0, 0);
	PUT_FIFO(T1220_o1, 1);

	GET_FIFO(T1221_i0, 0);
	GET_FIFO(T1221_i1, 2);
	Butterfly(T1221_i0, T1221_i1, &T1221_o0, &T1221_o1, T1221_W);
	PUT_FIFO(T1221_o0, 0);
	PUT_FIFO(T1221_o1, 1);

	GET_FIFO(T1222_i0, 0);
	GET_FIFO(T1222_i1, 2);
	Butterfly(T1222_i0, T1222_i1, &T1222_o0, &T1222_o1, T1222_W);
	PUT_FIFO(T1222_o0, 0);
	PUT_FIFO(T1222_o1, 1);

	GET_FIFO(T1223_i0, 0);
	GET_FIFO(T1223_i1, 2);
	Butterfly(T1223_i0, T1223_i1, &T1223_o0, &T1223_o1, T1223_W);
	PUT_FIFO(T1223_o0, 0);
	PUT_FIFO(T1223_o1, 1);

	GET_FIFO(T1224_i0, 1);
	GET_FIFO(T1224_i1, 3);
	Butterfly(T1224_i0, T1224_i1, &T1224_o0, &T1224_o1, T1224_W);
	PUT_FIFO(T1224_o0, 0);
	PUT_FIFO(T1224_o1, 1);

	GET_FIFO(T1225_i0, 1);
	GET_FIFO(T1225_i1, 3);
	Butterfly(T1225_i0, T1225_i1, &T1225_o0, &T1225_o1, T1225_W);
	PUT_FIFO(T1225_o0, 0);
	PUT_FIFO(T1225_o1, 1);

	GET_FIFO(T1226_i0, 1);
	GET_FIFO(T1226_i1, 3);
	Butterfly(T1226_i0, T1226_i1, &T1226_o0, &T1226_o1, T1226_W);
	PUT_FIFO(T1226_o0, 0);
	PUT_FIFO(T1226_o1, 1);

	GET_FIFO(T1227_i0, 1);
	GET_FIFO(T1227_i1, 3);
	Butterfly(T1227_i0, T1227_i1, &T1227_o0, &T1227_o1, T1227_W);
	PUT_FIFO(T1227_o0, 0);
	PUT_FIFO(T1227_o1, 1);

	GET_FIFO(T1228_i0, 1);
	GET_FIFO(T1228_i1, 3);
	Butterfly(T1228_i0, T1228_i1, &T1228_o0, &T1228_o1, T1228_W);
	PUT_FIFO(T1228_o0, 0);
	PUT_FIFO(T1228_o1, 1);

	GET_FIFO(T1229_i0, 1);
	GET_FIFO(T1229_i1, 3);
	Butterfly(T1229_i0, T1229_i1, &T1229_o0, &T1229_o1, T1229_W);
	PUT_FIFO(T1229_o0, 0);
	PUT_FIFO(T1229_o1, 1);

	GET_FIFO(T1230_i0, 1);
	GET_FIFO(T1230_i1, 3);
	Butterfly(T1230_i0, T1230_i1, &T1230_o0, &T1230_o1, T1230_W);
	PUT_FIFO(T1230_o0, 0);
	PUT_FIFO(T1230_o1, 1);

	GET_FIFO(T1231_i0, 1);
	GET_FIFO(T1231_i1, 3);
	Butterfly(T1231_i0, T1231_i1, &T1231_o0, &T1231_o1, T1231_W);
	PUT_FIFO(T1231_o0, 0);
	PUT_FIFO(T1231_o1, 1);

	GET_FIFO(T1232_i0, 0);
	GET_FIFO(T1232_i1, 2);
	Butterfly(T1232_i0, T1232_i1, &T1232_o0, &T1232_o1, T1232_W);
	PUT_FIFO(T1232_o0, 2);
	PUT_FIFO(T1232_o1, 3);

	GET_FIFO(T1233_i0, 0);
	GET_FIFO(T1233_i1, 2);
	Butterfly(T1233_i0, T1233_i1, &T1233_o0, &T1233_o1, T1233_W);
	PUT_FIFO(T1233_o0, 2);
	PUT_FIFO(T1233_o1, 3);

	GET_FIFO(T1234_i0, 0);
	GET_FIFO(T1234_i1, 2);
	Butterfly(T1234_i0, T1234_i1, &T1234_o0, &T1234_o1, T1234_W);
	PUT_FIFO(T1234_o0, 2);
	PUT_FIFO(T1234_o1, 3);

	GET_FIFO(T1235_i0, 0);
	GET_FIFO(T1235_i1, 2);
	Butterfly(T1235_i0, T1235_i1, &T1235_o0, &T1235_o1, T1235_W);
	PUT_FIFO(T1235_o0, 2);
	PUT_FIFO(T1235_o1, 3);

	GET_FIFO(T1236_i0, 0);
	GET_FIFO(T1236_i1, 2);
	Butterfly(T1236_i0, T1236_i1, &T1236_o0, &T1236_o1, T1236_W);
	PUT_FIFO(T1236_o0, 2);
	PUT_FIFO(T1236_o1, 3);

	GET_FIFO(T1237_i0, 0);
	GET_FIFO(T1237_i1, 2);
	Butterfly(T1237_i0, T1237_i1, &T1237_o0, &T1237_o1, T1237_W);
	PUT_FIFO(T1237_o0, 2);
	PUT_FIFO(T1237_o1, 3);

	GET_FIFO(T1238_i0, 0);
	GET_FIFO(T1238_i1, 2);
	Butterfly(T1238_i0, T1238_i1, &T1238_o0, &T1238_o1, T1238_W);
	PUT_FIFO(T1238_o0, 2);
	PUT_FIFO(T1238_o1, 3);

	GET_FIFO(T1239_i0, 0);
	GET_FIFO(T1239_i1, 2);
	Butterfly(T1239_i0, T1239_i1, &T1239_o0, &T1239_o1, T1239_W);
	PUT_FIFO(T1239_o0, 2);
	PUT_FIFO(T1239_o1, 3);

	GET_FIFO(T1240_i0, 1);
	GET_FIFO(T1240_i1, 3);
	Butterfly(T1240_i0, T1240_i1, &T1240_o0, &T1240_o1, T1240_W);
	PUT_FIFO(T1240_o0, 2);
	PUT_FIFO(T1240_o1, 3);

	GET_FIFO(T1241_i0, 1);
	GET_FIFO(T1241_i1, 3);
	Butterfly(T1241_i0, T1241_i1, &T1241_o0, &T1241_o1, T1241_W);
	PUT_FIFO(T1241_o0, 2);
	PUT_FIFO(T1241_o1, 3);

	GET_FIFO(T1242_i0, 1);
	GET_FIFO(T1242_i1, 3);
	Butterfly(T1242_i0, T1242_i1, &T1242_o0, &T1242_o1, T1242_W);
	PUT_FIFO(T1242_o0, 2);
	PUT_FIFO(T1242_o1, 3);

	GET_FIFO(T1243_i0, 1);
	GET_FIFO(T1243_i1, 3);
	Butterfly(T1243_i0, T1243_i1, &T1243_o0, &T1243_o1, T1243_W);
	PUT_FIFO(T1243_o0, 2);
	PUT_FIFO(T1243_o1, 3);

	GET_FIFO(T1244_i0, 1);
	GET_FIFO(T1244_i1, 3);
	Butterfly(T1244_i0, T1244_i1, &T1244_o0, &T1244_o1, T1244_W);
	PUT_FIFO(T1244_o0, 2);
	PUT_FIFO(T1244_o1, 3);

	GET_FIFO(T1245_i0, 1);
	GET_FIFO(T1245_i1, 3);
	Butterfly(T1245_i0, T1245_i1, &T1245_o0, &T1245_o1, T1245_W);
	PUT_FIFO(T1245_o0, 2);
	PUT_FIFO(T1245_o1, 3);

	GET_FIFO(T1246_i0, 1);
	GET_FIFO(T1246_i1, 3);
	Butterfly(T1246_i0, T1246_i1, &T1246_o0, &T1246_o1, T1246_W);
	PUT_FIFO(T1246_o0, 2);
	PUT_FIFO(T1246_o1, 3);

	GET_FIFO(T1247_i0, 1);
	GET_FIFO(T1247_i1, 3);
	Butterfly(T1247_i0, T1247_i1, &T1247_o0, &T1247_o1, T1247_W);
	PUT_FIFO(T1247_o0, 2);
	PUT_FIFO(T1247_o1, 3);

	GET_FIFO(T1248_i0, 0);
	GET_FIFO(T1248_i1, 2);
	Butterfly(T1248_i0, T1248_i1, &T1248_o0, &T1248_o1, T1248_W);
	PUT_FIFO(T1248_o0, 0);
	PUT_FIFO(T1248_o1, 1);

	GET_FIFO(T1249_i0, 0);
	GET_FIFO(T1249_i1, 2);
	Butterfly(T1249_i0, T1249_i1, &T1249_o0, &T1249_o1, T1249_W);
	PUT_FIFO(T1249_o0, 0);
	PUT_FIFO(T1249_o1, 1);

	GET_FIFO(T1250_i0, 0);
	GET_FIFO(T1250_i1, 2);
	Butterfly(T1250_i0, T1250_i1, &T1250_o0, &T1250_o1, T1250_W);
	PUT_FIFO(T1250_o0, 0);
	PUT_FIFO(T1250_o1, 1);

	GET_FIFO(T1251_i0, 0);
	GET_FIFO(T1251_i1, 2);
	Butterfly(T1251_i0, T1251_i1, &T1251_o0, &T1251_o1, T1251_W);
	PUT_FIFO(T1251_o0, 0);
	PUT_FIFO(T1251_o1, 1);

	GET_FIFO(T1252_i0, 0);
	GET_FIFO(T1252_i1, 2);
	Butterfly(T1252_i0, T1252_i1, &T1252_o0, &T1252_o1, T1252_W);
	PUT_FIFO(T1252_o0, 0);
	PUT_FIFO(T1252_o1, 1);

	GET_FIFO(T1253_i0, 0);
	GET_FIFO(T1253_i1, 2);
	Butterfly(T1253_i0, T1253_i1, &T1253_o0, &T1253_o1, T1253_W);
	PUT_FIFO(T1253_o0, 0);
	PUT_FIFO(T1253_o1, 1);

	GET_FIFO(T1254_i0, 0);
	GET_FIFO(T1254_i1, 2);
	Butterfly(T1254_i0, T1254_i1, &T1254_o0, &T1254_o1, T1254_W);
	PUT_FIFO(T1254_o0, 0);
	PUT_FIFO(T1254_o1, 1);

	GET_FIFO(T1255_i0, 0);
	GET_FIFO(T1255_i1, 2);
	Butterfly(T1255_i0, T1255_i1, &T1255_o0, &T1255_o1, T1255_W);
	PUT_FIFO(T1255_o0, 0);
	PUT_FIFO(T1255_o1, 1);

	GET_FIFO(T1256_i0, 1);
	GET_FIFO(T1256_i1, 3);
	Butterfly(T1256_i0, T1256_i1, &T1256_o0, &T1256_o1, T1256_W);
	PUT_FIFO(T1256_o0, 0);
	PUT_FIFO(T1256_o1, 1);

	GET_FIFO(T1257_i0, 1);
	GET_FIFO(T1257_i1, 3);
	Butterfly(T1257_i0, T1257_i1, &T1257_o0, &T1257_o1, T1257_W);
	PUT_FIFO(T1257_o0, 0);
	PUT_FIFO(T1257_o1, 1);

	GET_FIFO(T1258_i0, 1);
	GET_FIFO(T1258_i1, 3);
	Butterfly(T1258_i0, T1258_i1, &T1258_o0, &T1258_o1, T1258_W);
	PUT_FIFO(T1258_o0, 0);
	PUT_FIFO(T1258_o1, 1);

	GET_FIFO(T1259_i0, 1);
	GET_FIFO(T1259_i1, 3);
	Butterfly(T1259_i0, T1259_i1, &T1259_o0, &T1259_o1, T1259_W);
	PUT_FIFO(T1259_o0, 0);
	PUT_FIFO(T1259_o1, 1);

	GET_FIFO(T1260_i0, 1);
	GET_FIFO(T1260_i1, 3);
	Butterfly(T1260_i0, T1260_i1, &T1260_o0, &T1260_o1, T1260_W);
	PUT_FIFO(T1260_o0, 0);
	PUT_FIFO(T1260_o1, 1);

	GET_FIFO(T1261_i0, 1);
	GET_FIFO(T1261_i1, 3);
	Butterfly(T1261_i0, T1261_i1, &T1261_o0, &T1261_o1, T1261_W);
	PUT_FIFO(T1261_o0, 0);
	PUT_FIFO(T1261_o1, 1);

	GET_FIFO(T1262_i0, 1);
	GET_FIFO(T1262_i1, 3);
	Butterfly(T1262_i0, T1262_i1, &T1262_o0, &T1262_o1, T1262_W);
	PUT_FIFO(T1262_o0, 0);
	PUT_FIFO(T1262_o1, 1);

	GET_FIFO(T1263_i0, 1);
	GET_FIFO(T1263_i1, 3);
	Butterfly(T1263_i0, T1263_i1, &T1263_o0, &T1263_o1, T1263_W);
	PUT_FIFO(T1263_o0, 0);
	PUT_FIFO(T1263_o1, 1);

	GET_FIFO(T1264_i0, 0);
	GET_FIFO(T1264_i1, 2);
	Butterfly(T1264_i0, T1264_i1, &T1264_o0, &T1264_o1, T1264_W);
	PUT_FIFO(T1264_o0, 2);
	PUT_FIFO(T1264_o1, 3);

	GET_FIFO(T1265_i0, 0);
	GET_FIFO(T1265_i1, 2);
	Butterfly(T1265_i0, T1265_i1, &T1265_o0, &T1265_o1, T1265_W);
	PUT_FIFO(T1265_o0, 2);
	PUT_FIFO(T1265_o1, 3);

	GET_FIFO(T1266_i0, 0);
	GET_FIFO(T1266_i1, 2);
	Butterfly(T1266_i0, T1266_i1, &T1266_o0, &T1266_o1, T1266_W);
	PUT_FIFO(T1266_o0, 2);
	PUT_FIFO(T1266_o1, 3);

	GET_FIFO(T1267_i0, 0);
	GET_FIFO(T1267_i1, 2);
	Butterfly(T1267_i0, T1267_i1, &T1267_o0, &T1267_o1, T1267_W);
	PUT_FIFO(T1267_o0, 2);
	PUT_FIFO(T1267_o1, 3);

	GET_FIFO(T1268_i0, 0);
	GET_FIFO(T1268_i1, 2);
	Butterfly(T1268_i0, T1268_i1, &T1268_o0, &T1268_o1, T1268_W);
	PUT_FIFO(T1268_o0, 2);
	PUT_FIFO(T1268_o1, 3);

	GET_FIFO(T1269_i0, 0);
	GET_FIFO(T1269_i1, 2);
	Butterfly(T1269_i0, T1269_i1, &T1269_o0, &T1269_o1, T1269_W);
	PUT_FIFO(T1269_o0, 2);
	PUT_FIFO(T1269_o1, 3);

	GET_FIFO(T1270_i0, 0);
	GET_FIFO(T1270_i1, 2);
	Butterfly(T1270_i0, T1270_i1, &T1270_o0, &T1270_o1, T1270_W);
	PUT_FIFO(T1270_o0, 2);
	PUT_FIFO(T1270_o1, 3);

	GET_FIFO(T1271_i0, 0);
	GET_FIFO(T1271_i1, 2);
	Butterfly(T1271_i0, T1271_i1, &T1271_o0, &T1271_o1, T1271_W);
	PUT_FIFO(T1271_o0, 2);
	PUT_FIFO(T1271_o1, 3);

	GET_FIFO(T1272_i0, 1);
	GET_FIFO(T1272_i1, 3);
	Butterfly(T1272_i0, T1272_i1, &T1272_o0, &T1272_o1, T1272_W);
	PUT_FIFO(T1272_o0, 2);
	PUT_FIFO(T1272_o1, 3);

	GET_FIFO(T1273_i0, 1);
	GET_FIFO(T1273_i1, 3);
	Butterfly(T1273_i0, T1273_i1, &T1273_o0, &T1273_o1, T1273_W);
	PUT_FIFO(T1273_o0, 2);
	PUT_FIFO(T1273_o1, 3);

	GET_FIFO(T1274_i0, 1);
	GET_FIFO(T1274_i1, 3);
	Butterfly(T1274_i0, T1274_i1, &T1274_o0, &T1274_o1, T1274_W);
	PUT_FIFO(T1274_o0, 2);
	PUT_FIFO(T1274_o1, 3);

	GET_FIFO(T1275_i0, 1);
	GET_FIFO(T1275_i1, 3);
	Butterfly(T1275_i0, T1275_i1, &T1275_o0, &T1275_o1, T1275_W);
	PUT_FIFO(T1275_o0, 2);
	PUT_FIFO(T1275_o1, 3);

	GET_FIFO(T1276_i0, 1);
	GET_FIFO(T1276_i1, 3);
	Butterfly(T1276_i0, T1276_i1, &T1276_o0, &T1276_o1, T1276_W);
	PUT_FIFO(T1276_o0, 2);
	PUT_FIFO(T1276_o1, 3);

	GET_FIFO(T1277_i0, 1);
	GET_FIFO(T1277_i1, 3);
	Butterfly(T1277_i0, T1277_i1, &T1277_o0, &T1277_o1, T1277_W);
	PUT_FIFO(T1277_o0, 2);
	PUT_FIFO(T1277_o1, 3);

	GET_FIFO(T1278_i0, 1);
	GET_FIFO(T1278_i1, 3);
	Butterfly(T1278_i0, T1278_i1, &T1278_o0, &T1278_o1, T1278_W);
	PUT_FIFO(T1278_o0, 2);
	PUT_FIFO(T1278_o1, 3);

	GET_FIFO(T1279_i0, 1);
	GET_FIFO(T1279_i1, 3);
	Butterfly(T1279_i0, T1279_i1, &T1279_o0, &T1279_o1, T1279_W);
	PUT_FIFO(T1279_o0, 2);
	PUT_FIFO(T1279_o1, 3);
}
