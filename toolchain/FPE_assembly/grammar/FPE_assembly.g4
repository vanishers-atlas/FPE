grammar FPE_assembly;

/* Parser Rules */

	/* Rules for the 2 ways IDENTIFERs are used
	*/
	ident_dec : IDENTIFER ;
	ident_ref : IDENTIFER ;

	/* expr are a way to encode constants within a program,
		their as be as simple as a number literal,
		or a complex expression built from a range of operands and
		prevousally computed const.
		Const exprs are evaluated by the assembler, this means they
		can able be used to preform assembly time calculations not runtime ones
	*/
	expr 	: '(' expr ')'	/* bracket precedence */
				| expr multiplicative=('*'|'/'|'%') expr 	/* multiplicative precedence */
				| expr additive=('+'|'-') 					expr	/* additive precedence */
				| expr_operand
				;
		expr_operand 	:	DEC_NUM					/* decimal 			mumber literals */
									| BIN_NUM					/* binary  			number literals */
									|	OCT_NUM					/* octal       	number literals */
									| HEX_NUM					/* hexadecimal 	number literals */
									| ident_ref				/* an already defined constant 	*/
									;

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

	/* Boundary/Binary Allign Parallel (BAP) Memory accesses,
		used for fetching(storing) blocks of data from(to) memories
	*/
	bap_fetch	: access_reg
						| access_ram
						| access_rom_a
						| access_rom_b
						;
	bap_store : access_reg
						| access_ram
							;

	access_imm : expr ;
	access_get : 'GET' '[' addr ']' ('<' advance_mod=('ADV' | 'NO_ADV') '>')? ;
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
								('<' step_mod=('FORWARD' | 'BACKWARD') '>')? ;

	/* Statements are parts of an FPE program which don't map to program code
		And thus don't take up processor cycles
		However may affect the hardware generated (eg ZOLs
	*/
	statement : state_zol
						| state_jump_label
						| state_loop_label
						| state_constant
						| state_component
						;

		state_zol : 'ZOL' '(' expr ')' scope ;

		state_jump_label : ident_dec ':' ;

		state_loop_label : 'LOOP' ident_dec ':' scope ;

		state_constant : 'DEF' ident_dec expr ';' ;

		state_component : 'COM' com_name=ident_dec ':'
				com_type=IDENTIFER '('
			 	(
					state_component_parameter
					(',' state_component_parameter)*
				)?
				')' ';'
			;
			state_component_parameter : para_name=IDENTIFER ':' (IDENTIFER|expr) ;


	/* operations are parts of an FPE program which map to program code
		And thus take up processor cycles
	*/
	operation : op_void	';'
		| op_pc 	';'
		| op_bam 	';'
		| op_alu  ';'
		| op_palu ';'
		| op_ZOL  ';'
		;

		op_void : op_void_nop ;
			op_void_nop : 'NOP' ;

		op_pc 	: op_pc_only_jump | op_pc_alu_jump;
			op_pc_only_jump : 'JMP' '(' ident_ref ')' ;
			op_pc_alu_jump	: mnemonic=( 'JEQ' | 'JNE' | 'JLT'| 'JLE' | 'JGT' | 'JGE' ) '(' ident_ref ')' ;

		op_bam	:	op_bam_reset | op_bam_seek;
			op_bam_reset 	: 'RESET' 'BAM' '[' expr ']' ;
			op_bam_seek		: 'SEEK'  'BAM' '[' expr ']'
											'(' access_fetch ')'
											( '<' step_mod=('FORWARD' | 'BACKWARD') '>')? ;

		op_ZOL : op_ZOL_seek | op_ZOL_set ;
			op_ZOL_seek : exe_com=ident_ref '.' 'SEEK' '(' loop_label=ident_ref ')' ;
			op_ZOL_set  : exe_com=ident_ref '.' 'SET' '(' iterations=access_fetch ')' ;

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
										| internal='ACC' ;
				alu_result 	: access_store
										| internal='ACC' ;

		op_palu 	: op_palu_1o_1r | op_palu_1o_1e_1r | op_palu_2o_1r ;
			op_palu_1o_1r 	:  mnemonic=( 'PMOV' | 'PNOT' )
							'('expr ',' palu_operand ',' palu_result ')' ;

			op_palu_1o_1e_1r :  mnemonic=( 'PLSH' | 'PRSH' | 'PLRL' | 'PRRL' )
							'(' expr ',' palu_operand ',' expr ',' palu_result ')' ;

			op_palu_2o_1r 	:  mnemonic=( 'PAND' | 'POR' | 'PXOR' | 'PADD' | 'PSUB'  )
							'('expr ',' palu_operand ',' palu_operand ',' palu_result ')' ;

				palu_operand : bap_fetch
											| internal='ACC' ;
				palu_result 	: bap_store
											| internal='ACC' ;


/* lexer Rules */
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
