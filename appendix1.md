### 附录1 词法生成规则

#### lex_rule.txt

NFA	S	ε	A	REAL+
NFA	S	.	C	
NFA	S	char	IDENTIFIER	
NFA	S	e/E	IDENTIFIER	
NFA	S	i	IDENTIFIER	
NFA	S	'	K
NFA	K	i	K	
NFA	K	d+	K
NFA	K	e/E	K
NFA	K	char	K
NFA	K	0	K
NFA	K	ε	K
NFA	K	'	STRING
NFA	IDENTIFIER	char	IDENTIFIER	
NFA	IDENTIFIER	i	IDENTIFIER	
NFA	IDENTIFIER	e/E	IDENTIFIER	
NFA	IDENTIFIER	d+	IDENTIFIER	
NFA	IDENTIFIER	0	IDENTIFIER	
NFA	A	0	INT	
NFA	A	d+	B	
NFA	B	d+	B	
NFA	B	0	B	
NFA	B	ε	INT	
NFA	C	0	DOUBLE	
NFA	C	d+	DOUBLE	
NFA	INT	.	DOUBLE	
NFA	DOUBLE	d+	DOUBLE	
NFA	DOUBLE	0	DOUBLE	
NFA	INT	e/E	D	
NFA	DOUBLE	e/E	D	
NFA	D	+/-	F	
NFA	D	ε	F
NFA	F	d+	DOUBLE	
NFA	F	0	DOUBLE	
NFA	INT	+/-	REAL+	
NFA	DOUBLE	+/-	REAL+	
NFA	REAL+	0	I_INT	
NFA	REAL+	d+	H	
NFA	REAL+	.	G	
NFA	REAL+	i	COMPLEX	
NFA	H	0	H	
NFA	H	d+	H	
NFA	H	ε	I_INT	
NFA	I_INT	.	I_DOUBLE	
NFA	G	d+	I_DOUBLE	
NFA	G	0	I_DOUBLE	
NFA	I_DOUBLE	d+	I_DOUBLE	
NFA	I_DOUBLE	0	I_DOUBLE	
NFA	I_INT	e/E	I	
NFA	I_DOUBLE	e/E	I	
NFA	I	+/-	J	
NFA	I	ε	J		
NFA	J	d+	I_DOUBLE	
NFA	J	0	I_DOUBLE	
NFA	I_INT	i	COMPLEX	
NFA	I_DOUBLE	i	COMPLEX	
Keyword	for			
Keyword	while						
Keyword	if			
Keyword	else			
Keyword	return			
Keyword	break			
Keyword	continue			
Keyword	def			
Keyword	class			
Keyword	int
Keyword	double
Keyword	dict
Keyword	list
Keyword	tuple
AssignmentOperator	+=			
AssignmentOperator	-=			
AssignmentOperator	*=			
AssignmentOperator	/=
AssignmentOperator	//=
AssignmentOperator	%=			
AssignmentOperator	=
BinaryOperator	and
BinaryOperator	or
BinaryOperator	xor
BinaryOperator	==			
BinaryOperator	**			
BinaryOperator	+			
BinaryOperator	-			
BinaryOperator	*
BinaryOperator	/
BinaryOperator	//
BinaryOperator	%
BinaryOperator	in
BinaryOperator	<
BinaryOperator	>
BinaryOperator	<=
BinaryOperator	>=
UnaryOperator	!
UnaryOperator	not
Delimiter	.						
Delimiter	:
Delimiter	(
Delimiter	)
Delimiter	{
Delimiter	}
Delimiter	[
Delimiter	]			
Delimiter	,
DFAType	INT			
DFAType	DOUBLE			
DFAType	COMPLEX			
DFAType	IDENTIFIER	
DFAType	STRING		
Expressionrule	S	identifier	A
Expressionrule	S	keyword	A
Expressionrule	S	assignment_operator	Expr1	
Expressionrule	S	binary_operator	Expr1	
Expressionrule	S	unary_operator	Expr1	
Expressionrule	S	delimiter	Expr1	
Expressionrule	S	ε	Expr1	
Expressionrule	A	assignment_operator	Expr1
Expressionrule	A	binary_operator	Expr1
Expressionrule	A	unary_operator	Expr1
Expressionrule	A	delimiter	Expr1	
Expressionrule	Expr1	datatype	Expr2	
Expressionrule	Expr1	assignment_operator	Expr1
Expressionrule	Expr1	binary_operator	Expr1
Expressionrule	Expr1	unary_operator	Expr1
Expressionrule	Expr1	delimiter	Expr1
Expressionrule	Expr1	identifier	Expr2	
Expressionrule	Expr2	ε	A	