package sspc.util;

import sspc.softgen.SWGenUtils;

public class HelpHand {
	public static void main(String[] args) {
//		int a[] = {14, 15, 16, 17, 33};
//		int a[] = {18, 19, 20, 21, 28, 29, 30, 31, 32};
//		int a[] = {22, 23, 27};
//		int a[] = {24, 25, 26};
//		int width = getRPTEndWidth(a);
//		System.out.println("RPT width is: " + width);
		
		printPipeline("test.txt", "id_sm_wen");
		
	}
	
	
	public static int getRPTEndWidth(int a[]) {
		int difIdx = 0;
		
		String endIBits = SWGenUtils.intToBinary(a[a.length-1], 10);
		
		for (int ai : a) {
			if (ai == a[a.length-1]) break;
			
			String bits = SWGenUtils.intToBinary(ai, 10);
			for (int i = 0; i < bits.length(); i++) {
				if (bits.charAt(9 - i) != endIBits.charAt(9 - i)) {
					difIdx = Math.max(difIdx, i);
					break;
				}
			}
		}
		return difIdx+1;
	}
	
	public static void printPipeline(String filename, String signame) {
		String code = new String("");
		
		code += "u_buf_"+signame+"_Pb2:m_word_generic_reg1 generic map(REG_NUM=>PB2_DEPTH) \r\n"
			  + "  port map(clk=>clk, rst=>open, i_d=>"+signame+"_Pb1, o_d=>"+signame+"_Pb2);"
			  + "\r\n"			  
			  + "u_buf_"+signame+"_Pa0:m_word_generic_reg1 generic map(REG_NUM=>PA0_DEPTH) \r\n"
			  + "  port map(clk=>clk, rst=>open, i_d=>"+signame+"_Pb2, o_d=>"+signame+"_Pa0);"
			  + "\r\n"			  
			  + "u_buf_"+signame+"_Pa1:m_word_generic_reg1 generic map(REG_NUM=>PA1_DEPTH) \r\n"
			  + "  port map(clk=>clk, rst=>open, i_d=>"+signame+"_Pa0, o_d=>"+signame+"_Pa1);"
			  + "\r\n"				  
			  + "u_buf_"+signame+"_Pa1x:m_word_generic_reg1 generic map(REG_NUM=>PA1X_DEPTH) \r\n"
			  + "  port map(clk=>clk, rst=>open, i_d=>"+signame+"_Pa1, o_d=>"+signame+"_Pa1x);"
			  + "\r\n"			  
			  + "u_buf_"+signame+"_Pa2:m_word_generic_reg1 generic map(REG_NUM=>1) \r\n"
			  + "  port map(clk=>clk, rst=>open, i_d=>"+signame+"_Pa1x, o_d=>"+signame+"_Pa2);"
			  + "\r\n"			  
			  + "u_buf_"+signame+"_Pa3:m_word_generic_reg1 generic map(REG_NUM=>1) \r\n"
			  + "  port map(clk=>clk, rst=>open, i_d=>"+signame+"_Pa2, o_d=>"+signame+"_Pa3);"
			  + "\r\n";
		
		SWGenUtils.writeToFile(filename, code);
	}
}
