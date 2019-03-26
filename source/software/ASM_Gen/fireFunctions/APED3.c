static inline void APED3(Complex aped2zf_tmp1,Complex aped2zf_tmp2,Complex aped2zf_tmp3,float aped2APED,
	Complex aped2s4,Complex aped2s3,Complex aped2s2,Complex aped2zf1,Complex R22,Complex R14,
	Complex R13,Complex R12,Complex R11,Complex *s1,Complex *s2,Complex *s3,Complex *s4,float *aped3APED){
	// abs(R22*(s2-zf2))^2
	Complex mul1;
	Complex_Mult(R22,aped2zf_tmp3,&mul1);
	float aped;
	Complex_Abs2(mul1,&aped);
	*aped3APED = aped2APED + aped;
	// s1 = slice(zf1-R12*(s2-zf2)-R23*(s3-zf3)-R24*(s4-zf4))
	Complex mul2;
	Complex_Mult(R12,aped2zf_tmp3,&mul2);
	Complex sub1;
	Complex_Sub(aped2zf1,mul2,&sub1);
	Complex mul3;
	Complex_Mult(R14,aped2zf_tmp1,&mul3);
	Complex mul4;
	Complex_Mult(R13,aped2zf_tmp2,&mul4);
	Complex sub2;
	Complex_Sub(sub1,mul4,&sub2);
	Complex sub3;
	Complex_Sub(sub2,mul3,&sub3);
	SLICE(s1->real,sub3.real);// Output Port
	SLICE(s1->imag,sub3.imag);// Output Port
	// s1-zf1
	Complex zf_tmp4;
	Complex_Sub(*s1,aped2zf1,&zf_tmp4);// Output Port
	// abs(R11*(s1-zf1))^2
	Complex mul5;
	Complex_Mult(R11,zf_tmp4,&mul5);
	Complex_Abs2(mul5,&aped);
	*aped3APED = *aped3APED + aped;// Output Port
	*s2 = aped2s2;
	*s3 = aped2s3;
	*s4 = aped2s4;
}