parser grammar templated_json_parser;

options { tokenVocab=templated_json_lexer; }

/* String Building */
  string : OSQ (escaped_chars | NEC)* CSQ ;
    escaped_chars : EQM | EBSL | EFSL | EBSP | EFF | ENL | EHC | EHT | EHC ;

/* JSON Sythax */
  obj : OCB entry (COMMA  entry)* CCB  ;

  entry :  key=string  COLON  value ;

  value : value_json
    | value_placehold	// Simple templlate
    | value_concat		// A set of values to be concatinated into a string
    | value_expr			// An expr to be calulated then the result used
  ;

  value_json :
    // Terminal json values
      NUM
      | BOOL
      | NULL
      | string
    // Nested objects
      | obj
  ;

  value_placehold : PLACEHOLDER ;

  /* expression_values are a group of numbers and templated_values formed into an expression with the basic math operations,
   that once TEMPLATED_ID are swapping is solved are fifilled into the oupt json as a num value
   note the expression is limited to integers and integer srithmetic */
    value_expr : ORB expr CRB ;
      expr 	:  ORB  expr  CRB 	/* bracket precedence */
        |  expr  multiplicative=(EXP|MUL|DIV)	 expr /* multiplicative precedence */
        |  expr  additive=(ADD|SUB) 		   expr /* additive precedence */
        |  expr_leaf
      ;
      expr_leaf : string | PLACEHOLDER | NUM ;


  /* Concated_values are a group of strings and templated_values
   that once TEMPLATED_ID are swapping are concated together in a single string */
    value_concat :  concat_leaf  (AMP  concat_leaf) + ;
      concat_leaf : string | expr | PLACEHOLDER ;
