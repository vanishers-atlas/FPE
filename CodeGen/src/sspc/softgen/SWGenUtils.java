package sspc.softgen;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;

public class SWGenUtils {
	public static void main(String[] args) {
		
		int test = getSafeWidth(512);
//		String test = intToBinary(-5, 4);
		System.out.println("Result is " + test);
		return;
	}
	
	private SWGenUtils() {
		// Do nothing. Instances of this class cannot be created. 
	}

	public static int getIntOfString(String str) {
		return Integer.parseInt(str.replaceAll("[\\D]", ""));
	}
	
	public static int getNearestPowerOf2(int data) {
		double t = Math.log10(data)/Math.log10(2);
		double cl = Math.ceil(t);
		return (int) Math.pow(2, cl);
	}
	
	public static int getAddressWidth(int num) {		
		int t = (int) Math.ceil(Math.log(num)/Math.log(2));
		if (t == 0)
			t++;
		return t;
	}
	
	/**
	 * Get the width of integer which is possibly negative. 'Safe' means
	 * it keeps the sign bit.
	 * 
	 * Note it is different from getAddressWidth() above. E.g. 512 needs
	 * 11 bits to express (01 000 000 000), but -512 only needs 10 bits 
	 * (1 000 000 000).
	 * @param num
	 * @return
	 */
	public static int getSafeWidth(int num) {
		if (num > 0)
			return (int) Math.ceil(Math.log(num+0.5)/Math.log(2)) + 1;
		else if (num == 0)
			return 0;
		else {
			int num_abs = Math.abs(num);
			return (int) Math.ceil(Math.log(num_abs)/Math.log(2)) + 1;
		}		
	}
	
	/**
	 * Get certain bit of an integer.
	 * @param din The input integer
	 * @param j The wanted bit (index from 0)
	 * @return
	 */
	public static int getCertainBit(long din, int j) {
		// NOTE the last &1 is used to guarantee the case when j = 31.
		// Java has no unsigned arithmetic. When j is 31, the arithmetic shift 
		// right is will result an -1. 
		return (int) (((din & 1<<j) >> j) & 1); 
	}
	
	/**
	 * Get the digits part of a string
	 * @param str
	 * @return
	 */
	public static int getDigits(String str) {
		return Integer.parseInt(str.replaceAll("[\\D]", ""));
	}
	
	/**
	 * Write content to a file.
	 * @param fname Name of the file
	 * @param content The string to be written
	 * @throws IOException When file operation fails
	 */
	public static void writeToFile(String fname, String content) {
		Writer writer = null;
		File file = new File(fname);
		try {
			writer = new BufferedWriter(new FileWriter(file));
			writer.write(content);
			writer.close();
		} catch (IOException e) {
			throw new RuntimeException(e);
		}
	}
	
	/** Empty a directory
	 * 
	 */
	public static void emptyDirectory(String dirName) {
		File dir = new File(dirName);	    
		if (!dir.exists()) {
			System.out.println(dirName + " does not exist");
			return;
		}

		String[] info = dir.list();
		for (int i = 0; i < info.length; i++) {
			File n = new File(dirName + File.separator + info[i]);
			if (!n.isFile()) // skip ., .., other directories too
				continue;

			if (!n.delete())
				System.err.println("Couldn't remove " + n.getPath());

		}
	}
	
	/**
	 * Convert float to fixed-point
	 * @param re The float to convert
	 * @param totalBits The total bits of fixed-point
	 * @param fracBits The number of fraction bits of the fixed-point
	 * @return The converted fixed-point
	 */
	public static int float2fix(double re, int totalBits, int fracBits) {
		int fix = (int) Math.round(re* Math.pow(2, fracBits));
		if (fix == Math.pow(2, totalBits-1)) 
			fix -= 1;
		return fix;
	}
	
	/**
	 * Convert int to binary string.
	 * @param d
	 * @param width The width of binary
	 * @return
	 */
	public static String intToBinary(int d, int width) {
		if (d >= Math.pow(2, width)) {
//			d = (int) (Math.pow(2, width)-1);
			throw new RuntimeException("Error input to convert! The data is " + d + 
					"; the width is " + width);
		} else if (d < 0) {
			return Integer.toBinaryString(d).substring(32-width);
			
		} else			
			return String.format("%" + width + "s", Integer.toBinaryString(d))
					.replace(" ", "0");
	}
	
	/**
	 * Split the specified name at the first period and return the two parts as
	 * a two-element array. If there is no period, the second element is null.
	 * 
	 * @param name The name to split.
	 * @return The name before and after the first period as a two-element
	 *         array.
	 */
	public static String[] splitName(String name) {
		String[] result = new String[2];
		int period = name.indexOf(".");

		if (period < 0) {
			result[0] = name;
		} else {
			result[0] = name.substring(0, period);
			result[1] = name.substring(period + 1);
		}

		return result;
	}
}
