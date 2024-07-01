lexer grammar templated_json_lexer;

/* JSON Token Handling */
  NUM   : [0-9]+ ;
  BOOL  : 'true' | 'false';
  NULL  : 'null' ;

/* Symbol tokens */
  COMMA : ',' ;
  COLON : ':' ;

  OCB : '{' ;
  CCB : '}' ;

  ORB : '(' ;
  CRB : ')' ;

  EXP : '^' ;
  MUL : '*' ;
  DIV : '/' ;
  ADD : '+' ;
  SUB : '-' ;

  AMP : '&' ;

/* Whitespace and comment discarding */
  SING_LINE_COMMENT : '//' .*? [\n\r]+ -> skip ;
  WHITESPACE : [ \t\n\r]+ -> skip ;

 // String handling
 PLACEHOLDER : '$'[_0-9a-zA-Z]+ ;
 OSQ : '"' -> pushMode(STRING) ;

mode STRING;
  EQM : '\\"' ;
  EBSL : '\\\\' ;
  EFSL : '\\/' ;
  EBSP : '\\b' ;
  EFF : '\\f' ;
  ENL : '\\n' ;
  ECR : '\\r' ;
  EHT : '\\t' ;
  EHC : '\\u'[0-9a-fA-F][0-9a-fA-F][0-9a-fA-F][0-9a-fA-F] ;
  CSQ : '"' -> popMode ;

  NEC : [0-9a-zA-Z_.]+ ;
