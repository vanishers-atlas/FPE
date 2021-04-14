grammar FPE_assembly;

/* Parser Rules */

	/* expr are a way to encode constants within a program,
		their as be as simple as a number literal,
		or a complex expression built from a range of operands and
		prevousally computed const.
		Const exprs are evaluated by the assembler, this means they
		can able be used to preform assembly time calculations not runtime ones
	*/
	expr 	: ORB expr CRB	/* bracket precedence */
				| expr multiplicative=('*'|'/'|'%') expr 	/* multiplicative precedence */
				| expr additive=('+'|'-') 					expr	/* additive precedence */
				| expr_operand
				;
		expr_operand 	:	DEC_NUM					/* decimal 			mumber literals */
									| BIN_NUM					/* binary  			number literals */
									|	OCT_NUM					/* octal       	number literals */
									| HEX_NUM					/* hexadecimal 	number literals */
									| IDENTIFER				/* an already defined constant 	*/
									;


	/* jump labels are used to mark location to which the program can jump
	*/
	jump_label : IDENTIFER ;

	/* scopes are used to group statements and operations together
		within FPE assembly that are used to determine the bodies for certain
		statements (eg to tell ZOL statements what instructions to repeat)
		They may also be used for a form of commenting (akin to indenting),
		as the assembler ignores unrequired scopes
		Nore that tool chain expection the whole program to be unclosed in a scope
	*/
	scope : '{' ( statement | operation )* '}' ;

	/* Memory accesses, used for fetching(storing) data from(to) memories
	*/
	access_fetch	: access_imm
								| access_get
								| access_reg
								| access_ram
								| access_rom_a
								| access_rom_b
								;
	access_store 	: access_put
								| access_reg
								| access_ram
								;

	access_imm : expr ;
	access_get : 'GET' '[' addr ']' ('<' access_get_mod (',' access_get_mod)* '>')? ;
		access_get_mod : 'ADV' | 'NO_ADV' ;
	access_put : 'PUT' '[' addr ']' ;
	access_reg : 'REG' '[' addr ']' ;
	access_ram : 'RAM' '[' addr ']' ;
	access_rom_a : 'ROMA' '[' addr ']' ;
	access_rom_b : 'ROMB' '[' addr ']' ;

	addr 	: addr_literal
	 			| addr_bam
				;

		addr_literal  : expr ;
		addr_bam : 	'BAM' '[' expr ']'
								('<' addr_bam_mod (',' addr_bam_mod)* '>')? ;
			addr_bam_mod 	: 'FORWARD'  /* seek forward  after read*/
										| 'BACKWARD' /* seek BACKWARD after read */
										;

	/* Statements are parts of an FPE program which don't map to program code
		And thus don't take up processor cycles
		However may affect the hardware generated (eg ZOLs
	*/
	statement : state_zol
						| state_jump_label
						| state_constant
						;

		state_zol : 'ZOL' '(' expr ')' scope ;

		state_jump_label : jump_label ':' ;

		state_constant : 'DEF' IDENTIFER expr ';' ;


	/* operations are parts of an FPE program which map to program code
		And thus take up processor cycles
	*/
	operation : op_void	';'
		| op_pc 	';'
		| op_bam 	';'
		| op_alu  ';'
		;

		op_void : op_void_nop ;
			op_void_nop : 'NOP' ;

		op_pc 	: op_pc_jump ;
			op_pc_jump	: mnemonic=( 'JMP' | 'JEQ' | 'JNE' | 'JLT'| 'JLE' | 'JGT' | 'JGE' )
										'(' jump_label ')' ;

		op_bam	:	op_bam_reset | op_bam_seek;
			op_bam_reset 	: 'RESET' 'BAM' '[' expr ']' ;
			op_bam_seek		: 'SEEK'  'BAM' '[' expr ']'
											'(' access_fetch ')'
											( '<' op_bam_seek_mod ( ',' op_bam_seek_mod )* '>')? ;
				op_bam_seek_mod	: 'FORWARD'		/* seek forward */
					| 'BACKWARD'	/* seek back */
					;

		op_alu 	: op_alu_1o_1r | op_alu_1o_1e_1r | op_alu_2o_0r | op_alu_2o_1r ;
			op_alu_1o_1r 		:  mnemonic=( 'MOV' | 'NOT' )
												'(' alu_operand ',' alu_result ')' ;
			op_alu_1o_1e_1r :  mnemonic=( 'LSH' | 'RSH' | 'LRL' | 'RRL' )
												'(' alu_operand ',' expr ',' alu_result ')' ;
			op_alu_2o_0r 		:  mnemonic=( 'UCMP' | 'SCMP' )
												'(' alu_operand ',' alu_operand ')' ;
			op_alu_2o_1r 		:  mnemonic=( 'ADD' | 'SUB' | 'AND' | 'OR' | 'XOR' | 'MUL' )
												'(' alu_operand ',' alu_operand ',' alu_result ')' ;
				alu_operand : access_fetch
										| internal=('ACC' | 'ACC') ;
				alu_result 	: access_store
										| internal=('ACC' | 'ACC') ;

/* lexer Rules */
	/* Symbol Tokens */
		ORB : '(' ;
		CRB : ')' ;


	/* Number Handling */
		DEC_NUM : [0-9]+ ;
		BIN_NUM : '0' [bB]	[0-1]+ ;
		OCT_NUM : '0' [oO] 	[0-7]+ ;
		HEX_NUM : '0' [xX]	[0-9A-Fa-f]+ ;

	/* General IDENTIFER Handling */
		IDENTIFER : [_a-zA-Z][_a-zA-Z0-9]* ;

	/* Whitespace and comment Skipping */
		MUTL_LINE_COMMENT : '//*' .*? '*//' -> skip ;
		SING_LINE_COMMENT : '//' .*? [\n\r]+ -> skip ;
		WHITESPACE : [ \t\n\r]+ -> skip ;
