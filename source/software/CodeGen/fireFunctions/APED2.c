static inline void APED2(Complex aped1zf_tmp1,Complex aped1zf_tmp2,float aped1APED,Complex aped1s4,
			Complex aped1s3,Complex aped1zf2,Complex aped1zf1,Complex aped1R33,Complex aped1R22,Complex aped1R11,Complex aped1R23,
              Complex aped1R24,Complex aped1R12,Complex aped1R13,Complex aped1R14,
			Complex *aped2zf_tmp1,Complex *aped2zf_tmp2,Complex *aped2zf_tmp3,float *aped2APED,
			Complex *aped2s4,Complex *aped2s3,Complex *aped2s2,Complex *aped2zf1,Complex *aped2R22,
            Complex *aped2R11,Complex *aped2R12,Complex *aped2R13,Complex *aped2R14){
	// abs(R33*(s3-zf3))^2
	Complex mul1;
	Complex_Mult(aped1R33,aped1zf_tmp2,&mul1);
	float aped;
	Complex_Abs2(mul1,&aped);
	*aped2APED = aped1APED + aped;// Output Port
	// s2 = slice(zf2-R23*(s3-zf3)-R24*(s4-zf4))
	Complex mul2;
	Complex_Mult(aped1R23,aped1zf_tmp2,&mul2);
	Complex sub1;
	Complex_Sub(aped1zf2,mul2,&sub1);
	Complex mul3;
	Complex_Mult(aped1R24,aped1zf_tmp1,&mul3);
	Complex sub2;
	Complex_Sub(sub1,mul3,&sub2);
	SLICE(aped2s2->real,sub2.real);// Output Port
	SLICE(aped2s2->imag,sub2.imag);// Output Port
	// s2-zf2
	Complex_Sub(*aped2s2,aped1zf2,aped2zf_tmp3);// Output Port
	
	*aped2zf_tmp1 = aped1zf_tmp1;
	*aped2zf_tmp2 = aped1zf_tmp2;
	*aped2s4 = aped1s4;
	*aped2s3 = aped1s3;
	*aped2zf1 = aped1zf1;
	*aped2R22 = aped1R22;
	*aped2R11 = aped1R11;
	*aped2R12 = aped1R12;
	*aped2R13 = aped1R13;
	*aped2R14 = aped1R14;
}
