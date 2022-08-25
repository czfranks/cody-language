%{
  #include <stdio.h>
  #include <ctype.h>
  #include <string.h>

  #define  PROGRAM_LITERAL  "program"
  #define  VAR_LITERAL      "var"
  #define  IF_LITERAL       "if"
  #define  WHILE_LITERAL    "while"

  #define  EQUAL_LITERAL    "equal"
  #define  NOTEQUAL_LITERAL "notequal"
  #define  AND_LITERAL      "and"
  #define  OR_LITERAL       "or"
  #define  TRUE_LITERAL     "true"
  #define  FALSE_LITERAL    "false"

      /* lib */
  #define  ADVANCE_LITERAL  "advance"
  #define  TURN_LITERAL     "turn"
  #define  COLOR_LITERAL    "color"

%}

%token VAR ID IF NUM BOOLEAN WHILE   /* statements */
%token AND OR EQUAL NOTEQUAL /* conditionals */
%token PROGRAM               /* begin program */
%token ADVANCE TURN COLOR    /* lib functions */
%left '+' '-'
%left '*' '/'
%left AND OR
%left EQUAL NOTEQUAL
%right '='
%%
  program:      PROGRAM block ;
  block:        '{' listStmt '}' ;
  listStmt:     stmt listStmt
               | listVarDef listStmt
               | listLib listStmt
               | ;
  listVarDef:   VAR listVar ';' listVarDef 
               | ;
  listVar:      ID ',' listVar 
               | ID ;
  listLib:      lib ';' listLib
               | ;

  stmt:         ';'
               | IF '(' cond ')' stmt
               | WHILE '(' cond ')' stmt
               | ID '=' expr ';';
               | block ;

  lib:          ADVANCE '(' expr ')'
               | TURN '(' expr ')'
               | COLOR '(' expr ',' expr ',' expr ')' ;

  cond:         eq AND eq
               | eq OR  eq
               | eq ; 

  eq:           expr EQUAL expr
               | expr NOTEQUAL expr
               | BOOLEAN ;

  expr:         expr '+' term
               | expr '-' term
               | term ;

  term:         term '*' factor
               | term '/' factor
               | factor ;

  factor:       '(' expr ')'
               | NUM
               | ID ;

%%
int yylex()
{
  int c;
  char lexema[30];
  char *p;
  do c=getchar(); while (isspace(c));
  if(c==27) return EOF;
  if (isalpha(c))
  {
    p=lexema;
    do { *p++=c; c=getchar(); } while (isalpha(c));
    ungetc(c,stdin);
    *p=0;
    if (strcmp(lexema,PROGRAM_LITERAL)==0) return PROGRAM;
    if (strcmp(lexema,VAR_LITERAL)==0) return VAR;
    if (strcmp(lexema,IF_LITERAL)==0) return IF;
    if (strcmp(lexema,WHILE_LITERAL)==0) return WHILE;

    if (strcmp(lexema,EQUAL_LITERAL)==0) return EQUAL;
    if (strcmp(lexema,NOTEQUAL_LITERAL)==0) return NOTEQUAL;
    if (strcmp(lexema,AND_LITERAL)==0) return AND;
    if (strcmp(lexema,OR_LITERAL)==0) return OR;
    if (strcmp(lexema,TRUE_LITERAL)==0) return BOOLEAN;
    if (strcmp(lexema,FALSE_LITERAL)==0) return BOOLEAN;

    /* lib */
    if (strcmp(lexema,ADVANCE_LITERAL)==0) return ADVANCE;
    if (strcmp(lexema,TURN_LITERAL)==0) return TURN;
    if (strcmp(lexema,COLOR_LITERAL)==0) return COLOR;
    
    return ID;
  }
  if(c=='(' || c==')' || c==';' || c==',' || c=='{' || c=='}') return c;
  if(c=='+' || c=='-' || c=='*' || c=='/') return c;
  if(c=='=') return c;
  if(isdigit(c))
  {
    ungetc(c,stdin);
    scanf("%d",&c);
    return NUM;
  }
  if(c>0 && c<256)
    yyerror("Lexical error: ", c);
}

yyerror(char *m, int chr)
{
  fprintf(stdout, "%s char: %c , ascii: %d", m, chr, chr);
  exit(0);
}
void main()
{
  yyparse();
}
