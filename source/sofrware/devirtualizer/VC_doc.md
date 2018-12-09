**sequentialBlock**
  * **sequentialBlock** **sequentialBlock**
  * **varibleStatement**
  * **codeBlock**

**varibleStatement**
  * **varible** = **expression**;
  * **varible** _**binaryOperator**=_ **expression**;

**varible**
  * **dataType** **varableName**
  * **varableName**

**dataType**
  * _int_
  * _float_
  * _string_

**varableName**
  * [A-Za-z_][A-Za-z0-9_]\*

**expression**
  * ( **expression** )
  * **unaryOperator** **expression**
  * **expression** **binaryOperator** **expression**
  * **operand**

**unaryOperator**
  * **dataType** (data casting)
  * \-      (negation)
  * _lg_    (log base 2)
  * _abs_   (absolute value)
  * (next|last)_(pos|neg!out|in) (rounding functions)

**binaryOperator**
  * \+ (addition)
  * \- (subtraction)
  * \* (multiplication)
  * ^ (power)
  * / (devidion)
  * % (remember)
  * _log_ (A log base B)

**operand**
  * _param_ **dataType** **string** (parameter reading)
  * **varableName**
  * **literal**

**string**
* " ([^(\\|")]|(\\\\|\\"))\* "

**literal**
  * **integer**
  * **float**
  * **string**

**integer**
  * [\+\-]?[0-9]+

**float**
 * [\+\-]?[0-9]+(.[0-9]+)?([eE][\+\-]?[0-9]+(.[0-9]+))

**codeBlock**
  * _code_{**codeString**}

**codeString**
  * **codeString** **dropIn** **codeString**
  * ([^@}^]|(\^[\d\D]))*

  Note codeString uses char escaping for @ } ^, using the ^ character. If unknown char escape, "\^[@}^]", is encounted a warning will be issued and the char escape read as the second char, to include the 'char escapse' in the code string first escape the ^ char using ^^

**dropIn**
  * @**expression**
