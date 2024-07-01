grammar templated_json;

/* Parser Rules */

	/* String Building */
		string : '"' ( WS | US | DIGITS | LETTERS )+ '"' ;
		placeholder : '$' ( US | DIGITS | LETTERS )+ ;

	/* JSON Sythax */
		obj : WS* '{' entry ( WS* ','  entry)* '}' WS* ;

		entry : WS* key=string WS* ':' WS* value ;

		value : value_json
			  value_placehold	// Simple templlate
			| value_concat		// A set of values to be concatinated into a string
			| value_expr			// An expr to be calulated then the result used
			| value_json
		;

		value_json :
			// Terminal json values
				DIGITS
				| BOOL
				| NULL
				| string
			// Nested objects
				| obj
		;

		value_placehold : placeholder ;

		/* expression_values are a group of numbers and templated_values formed into an expression with the basic math operations,
		 that once TEMPLATED_ID are swapping is solved are fifilled into the oupt json as a num value
		 note the expression is limited to integers and integer srithmetic */
			value_expr : '(' expr ')' ;
				expr 	: WS* '(' WS* expr WS* ')' 	/* bracket precedence */
					| WS* expr WS* multiplicative=('*'|'/')	WS* expr /* multiplicative precedence */
					| WS* expr WS* additive=('+'|'-') 		  WS* expr /* additive precedence */
					| WS* expr_leaf
				;
				expr_leaf : string | placeholder | placeholder ;


		/* Concated_values are a group of strings and templated_values
		 that once TEMPLATED_ID are swapping are concated together in a single string */
			value_concat : WS* value_concat WS* '&' WS* concat_leaf
				| WS* concat_leaf WS* '&' WS* concat_leaf
			;
				concat_leaf : string | value_expr;

/* lexer Rules */
	/* JSON Token Handling */
		BOOL : 'true' | 'false';
		NULL : 'null' ;

	/* String fragments */
		US : '_' ;
		WS : [ \t\n\r]+ ;
		DIGITS : [0-9]+ ;
		LETTERS : [a-zA-Z]+ ;
