### 附录2 LR1生成规则

#### grammar_rule.txt

G	S'	S
G	S	Assignment	S	
G	S	Assignment	
G	S	Funcdef	S	
G	S	Funcdef
G	S	Func	S	
G	S	Func
G	S	Loop	S	
G	S	Loop
G	S	Branch	S	
G	S	Branch	
G   S   Funcall S
G   S   Funcall
G	Expr	Expr	BinaryOp	Expr
G	Expr	UnaryOp	Expr	
G	Expr	(	Expr	)
G	Expr	const		
G	Expr	ids	
G	Expr	Funcall	
G	Expr	id  [ Expr ]
G	Assignment	ids	AssignmentOp	Expr
G   ids     id  .    ids
G   ids     id
G   Funcall ids ( )
G   Funcall ids ( Consts )	
G   Consts const
G   Consts const , Consts
G   Paras id , Paras
G   Paras id
G   Funcdef def id ( ) { S }
G   Funcdef def id ( Paras ) { S }
G   Funcdef def id ( Paras ) { }
G   Funcdef def id (  ) { }
G   Loop while ( Expr ) { S }
G   Loop while ( Expr ) { }
G   Branch if ( Expr ) { S }
G   Branch if ( Expr ) { }
isVN	S'		
isVN	S		
isVN	Expr			
isVN	Assignment	
isVN	Funcdef	
isVN	Loop	
isVN	Branch	
isVN	Paras	
isVN	Consts	
isVN	Funcall	
isVN	ids							
filter	DOUBLE	const		
filter	INT	const		
filter	COMPLEX	const	
filter	STRING	const	
filter	IDENTIFIER	id		
filter	BINARY_OPERATOR	BinaryOp		
filter	UNARY_OPERATOR	UnaryOp		
filter	ASSIGNMENT_OPERATOR	AssignmentOp		