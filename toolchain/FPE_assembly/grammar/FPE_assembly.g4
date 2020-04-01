grammar FPE_assembly;

/* Parser Rules */

	/* Statements are parts of an FPE program which don't map to program code
		And thus don't take up processor cycles
		eg labels to jump to or scopes
	*/
	statement : scope | label | zol ;

		scope : OCB ( statement | operation )* CCB ;

		label : STRING COLON ;

		zol : ZOL ORB NUMBER CRB scope ;

	/* operations are parts of an FPE program which map to program code
		And thus take up processor cycles
		eg ADD or jumps
	*/
	operation : (void_operation | pc_operation | bam_operation | alu_operation) SEMICOLON;

		void_operation : void_0f_0s;
			void_0f_0s : void_0f_0s_mnemonic ;
				void_0f_0s_mnemonic	:  NOP ;

		pc_operation : pc_0f_0s;
			pc_0f_0s	: pc_0f_0s_mnemonic ORB STRING CRB ;
				pc_0f_0s_mnemonic	: JMP | JLT ;

		bam_operation : bam_0f_0s | bam_1f_0s ;
			bam_0f_0s	: bam_0f_0s_mnemonic OSB NUMBER CSB ;
				bam_0f_0s_mnemonic	: BAM_RST ;
			bam_1f_0s	: bam_1f_0s_mnemonic OSB NUMBER CSB ORB mem_fetch CRB ;
				bam_1f_0s_mnemonic	: BAM_ADV ;

		alu_operation : alu_1f_1s | alu_2f_0s | alu_2f_1s ;
			alu_1f_1s 	: alu_1f_1s_mnemonic ORB alu_fetch COMMA alu_store CRB ;
				alu_1f_1s_mnemonic : MOV ;
			alu_2f_0s	: alu_2f_0s_mnemonic ORB alu_fetch COMMA alu_fetch CRB ;
				alu_2f_0s_mnemonic : CMP ;
			alu_2f_1s	: alu_2f_1s_mnemonic ORB alu_fetch COMMA alu_fetch COMMA alu_store CRB ;
				alu_2f_1s_mnemonic : AND | ADD ;

	alu_fetch : mem_fetch | ACC ;
	alu_store : mem_store | ACC ;

	mem_fetch	: imm_access | get_access | reg_access | ram_access | rom_access ;
	mem_store : put_access | reg_access | ram_access ;
		imm_access : NUMBER ;
		get_access : (GET | GET_ADV) OSB mem_addr CSB ;
		put_access : PUT OSB mem_addr CSB ;
		reg_access : REG OSB mem_addr CSB ;
		ram_access : RAM OSB mem_addr CSB ;
		rom_access : ROM OSB mem_addr CSB ;

	mem_addr : encoded_addr | bam_addr ;
		encoded_addr : NUMBER ;
		bam_addr : (BAM | BAM_ADV) OSB NUMBER CSB ;

/* lexer Rules */

	/* Bracket Tokens */
		OAB : '<' ;
		CAB : '>' ;
		OCB : '{' ;
		CCB : '}' ;
		ORB : '(' ;
		CRB : ')' ;
		OSB : '[' ;
		CSB : ']' ;

	/* Special character Tokens */
		SEMICOLON 	: ';' ;
		COLON 			: ':' ;
		COMMA 			: ',' ;

	/* Caseless Fragments */
		fragment UNDERSCORE : '_' ;
		fragment A : ('a'|'A') ;
		fragment B : ('b'|'B') ;
		fragment C : ('c'|'C') ;
		fragment D : ('d'|'D') ;
		fragment E : ('e'|'E') ;
		fragment F : ('f'|'F') ;
		fragment G : ('g'|'G') ;
		fragment H : ('h'|'H') ;
		fragment I : ('i'|'I') ;
		fragment J : ('j'|'J') ;
		fragment K : ('k'|'K') ;
		fragment L : ('l'|'L') ;
		fragment M : ('m'|'M') ;
		fragment N : ('n'|'N') ;
		fragment O : ('o'|'O') ;
		fragment P : ('p'|'P') ;
		fragment Q : ('q'|'Q') ;
		fragment R : ('r'|'R') ;
		fragment S : ('s'|'S') ;
		fragment T : ('t'|'T') ;
		fragment U : ('u'|'U') ;
		fragment V : ('v'|'V') ;
		fragment W : ('w'|'W') ;
		fragment X : ('x'|'X') ;
		fragment Y : ('y'|'Y') ;
		fragment Z : ('z'|'Z') ;

	/* Number Handling */
		fragment BIN : '0' B [0-1]+ ;
		fragment OCT : '0' O [0-7]+ ;
		fragment HEX : '0' X [0-9A-Fa-f]+ ;
		fragment DEC : [+-]? [0-9]+ ;

		NUMBER : (BIN | OCT | HEX | DEC) ;

	/* Keyword tokens */
		ACC				: A C C ;
		ADD				: A D D ;
		AND 			: A N D ;
		BAM 			: B A M ;
		BAM_ADV		: B A M UNDERSCORE A D V ;
		BAM_RST		:	B A M UNDERSCORE R S T ;
		CMP				: C M P ;
		GET 			: G E T ;
		GET_ADV		: G E T UNDERSCORE A D V ;
		JMP 			: J M P ;
		JLT	 			: J L T ;
		MOV 			: M O V ;
		NOP 			: N O P ;
		PUT 			: P U T ;
		RAM 			: R A M ;
		REG 			: R E G ;
		ROM 			: R O M ;
		ZOL 			: Z O L ;

	/* General String Handling */
		STRING : [_a-zA-Z][_a-zA-Z0-9]* ;

	/* Whitespace and comment Skipping */
		MUTL_LINE_COMMENT : '//*' .*? '*//' -> skip ;
		SING_LINE_COMMENT : '//' .*? [\n\r]+ -> skip ;
		WHITESPACE : [ \t\n\r]+ -> skip ;
