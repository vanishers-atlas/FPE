#define GET_FIFO(DATA, CHANNEL) asm volatile ("GET %0, ^" #CHANNEL "\n\t":"=f"(DATA)::);
#define PUT_FIFO(DATA, CHANNEL) asm volatile ("PUT %0, ^" #CHANNEL "\n\t"::"f"(DATA):);
#define SLICE(OUT, IN) asm ("DECONST %0, %1\n\t":"=f"(OUT):"f"(IN):);
#define LDSORT1(IN0) asm volatile ("LDSORT %0 \n\t"::"f"(IN0):);
#define UNLDSORT1(DATA) asm volatile ("UNLDSORT %0\n\t":"=f"(DATA)::);
#define SORT() asm volatile ("SORT \n\t":::);

typedef struct
{
	float real;// real part of a complex value
	float imag;// imag part of a complex value
} Complexfloat;


typedef struct
{
	double real;// real part of a complex value
	double imag;// imag part of a complex value
} Complexdouble;

static inline Complexfloat Complexfloat_Sub (Complexfloat a, Complexfloat b){
	Complexfloat c;
	
	c.real=a.real-b.real;
	c.imag=a.imag-b.imag;
	
	return c;
}

static inline Complexfloat Complexfloat_Mult (Complexfloat a, Complexfloat b){
	Complexfloat c;
	
	c.real=a.real * b.real - a.imag * b.imag ;
	c.imag=a.real * b.imag + b.real *a.imag ;
	
	return c;
}

static inline Complexfloat Complexfloatbyfloat_Mult (float a, Complexfloat b){
	Complexfloat c;
	
	c.real=a * b.real;
	c.imag=a * b.imag;
	
	return c;
}

static inline float Complexfloat_Abs2 (Complexfloat a){
	
    return  a.real*a.real+a.imag*a.imag;
	
}

static inline Complexdouble Complexdouble_Sub (Complexdouble a, Complexdouble b){
	Complexdouble c;
	
	c.real=a.real-b.real;
	c.imag=a.imag-b.imag;
	
	return c;
}

static inline Complexdouble Complexdouble_Mult (Complexdouble a, Complexdouble b){
	Complexdouble c;
	
	c.real=a.real * b.real - a.imag * b.imag ;
	c.imag=a.real * b.imag + b.real *a.imag ;
	
	return c;
}

static inline double Complexdouble_Abs2 (Complexdouble a){
    return a.real*a.real+a.imag*a.imag;
}
