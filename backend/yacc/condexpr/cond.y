/**************************************************/
/* Ejemplo en YACC de una calculadora simple */
/* */
/* prg -> exp */
/* exp -> exp + term | exp - term | term */
/* term -> term * factor | factor */
/* factor -> ( exp ) | num */
/* */
/* Pruebe con la entradas: */
/* w = 1+12+(4-21-(5+(3)))-8 */
/* w = 2+8*(2-6) */
/**************************************************/

%{
  #include <stdio.h>
  #include <ctype.h>
  #include <math.h>
  #include <stdlib.h>


  #define  EQUAL_LITERAL    "equal"
  #define  NOTEQUAL_LITERAL "notequal"
  #define  AND_LITERAL      "and"
  #define  OR_LITERAL       "or"
  #define  TRUE_LITERAL     "true"
  #define  FALSE_LITERAL    "false"
%}


%token ID AND OR EQUAL NOTEQUAL BOOLEAN NUM
%left '+' '-' /* + es asociativo por la izquierda */
%left '*' '/'
%left EQUAL NOTEQUAL AND OR

%%
  prg:          cond                 {printf("%d\n", $1);};
               | expr                {printf("%d\n", $1);};

  cond:         eq AND eq           {$$=$1 && $3;};
               | eq OR  eq          {$$=$1 || $3;};
               | eq                 {$$=$1;};

  eq:           expr EQUAL expr     {$$=$1 == $3;};
               | expr NOTEQUAL expr {$$=$1 != $3;};
               | BOOLEAN            {$$=$1;};

  expr:         expr '+' term       {$$=$1 + $3;};
               | expr '-' term      {$$=$1 - $3;};
               | term               {$$=$1;};

  term:         term '*' factor     {$$=$1 * $3;};
               | term '/' factor    {$$=$1 / $3;};
               | factor             {$$=$1;};

  factor:       '(' expr ')'        {$$=$2;};
               | NUM                {$$=$1;};

%%

yylex() /* analizador lexico */
{
  int c;
  char lexema[30];
  char *p;
  do c=getchar(); while(c == ' ' || c == '\t');
  if(c=='\n') return EOF;
  if (isalpha(c))
  {
    p=lexema;
    do { *p++=c; c=getchar(); } while (isalpha(c));
    ungetc(c,stdin);
    *p=0;

    if (strcmp(lexema,EQUAL_LITERAL)==0) return EQUAL;
    if (strcmp(lexema,NOTEQUAL_LITERAL)==0) return NOTEQUAL;
    if (strcmp(lexema,AND_LITERAL)==0) return AND;
    if (strcmp(lexema,OR_LITERAL)==0) return OR;
    if (strcmp(lexema,TRUE_LITERAL)==0){
      yylval = 1;
      return BOOLEAN;
    } 
    if (strcmp(lexema,FALSE_LITERAL)==0){
      yylval = 0;
      return BOOLEAN;
    } 
    
  }
  if(c=='(' || c==')') return yylval = c;
  if(c=='+' || c=='-' || c=='*' || c=='/') return yylval = c;
  if(isdigit(c))
  {
    ungetc(c,stdin);
    scanf("%d",&yylval);
    return NUM;
  }
  
  if(c>0 && c<256)
    yyerror("Lexical error: ", c);
  return c;
}

yyerror(char *m, int chr)
{
  fprintf(stdout, "%s char: %c , ascii: %d", m, chr, chr);
  exit(0);
}

int main()
{
  //while(1)
  //{
    yyparse(); /* analizador sintactico */
  //  printf("\n");
  //}

  return 0;
}
 
