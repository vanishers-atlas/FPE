static inline void APED1(Complex zf[4],Complex s_16QAM,Complex initR44,Complex initR33,Complex initR34,
              Complex initR22,Complex initR23,Complex initR24,Complex initR11,Complex initR12,
              Complex initR13,Complex initR14,Complex *aped1zf_tmp1,Complex *aped1zf_tmp2,
              float *aped1APED,Complex *aped1s4,Complex *aped1s3,Complex *aped1zf2,
              Complex *aped1zf1,Complex *aped1R33,Complex *aped1R22,Complex *aped1R11,Complex *aped1R23,
              Complex *aped1R24,Complex *aped1R12,Complex *aped1R13,Complex *aped1R14){
	// s4-zf4
	Complex_Sub(s_16QAM,zf[Mt-1],aped1zf_tmp1);
	// abs(R44*(s4-zf4))^2
	Complex mul1;
	Complex_Mult(initR44,*aped1zf_tmp1,&mul1);
	Complex_Abs2(mul1,aped1APED);// Output Port
	// s3 = slice(zf3-R34*(s4-zf4))	
	Complex sub1;
	Complex_Sub(s_16QAM,zf[Mt-1],&sub1);
	Complex mul2;
	Complex_Mult(initR34,sub1,&mul2);
	Complex sub2;
	Complex_Sub(zf[Mt-2],mul2,&sub2);
	SLICE(aped1s3->real,sub2.real);// Output Port
	SLICE(aped1s3->imag,sub2.imag);// Output Port
	// s3-zf3
	Complex_Sub(*aped1s3,zf[Mt-2],aped1zf_tmp2);// Output Port
	
	*aped1zf2 = zf[Mt-3];
	*aped1zf1 = zf[Mt-4];
	*aped1s4 = s_16QAM;
	*aped1R33 = initR33;
	*aped1R22 = initR22;
	*aped1R11 = initR11;
	*aped1R23 = initR23;
	*aped1R24 = initR24;
	*aped1R12 = initR12;
	*aped1R13 = initR13;
	*aped1R14 = initR14;
}
