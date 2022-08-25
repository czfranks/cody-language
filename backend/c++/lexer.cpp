#include <bits/stdc++.h>
using namespace std;

/* 

echo "4+3 equal 7 and 4*4 notequal 16" > hola.txt & ./out < hola.txt */
/* 
python:
result = os.system('echo "4+3 equal 7 and 4*4 notequal16 16" > hola.txt & ./out < hola.txt')
 */

  /* tokens string literals */
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
  #define  ADVANCE_LITERAL  "advance" /* lib */
  #define  TURN_LITERAL     "turn"    /* lib */
  #define  COLOR_LITERAL    "color"   /* lib */

  /* token types  */
  #define TT_PROGRAM    "program"
  #define TT_DEFINITION "definition"
  #define TT_KEYWORD    "keyword"
  #define TT_OPERATOR   "operator"
  #define TT_NUMBER     "number"
  #define TT_VAR        "var"
  #define TT_ID         "id"
  #define TT_ASSIGNMENT "assignment" /* = */
  #define TT_LIB        "lib"
  #define TT_BOOLEAN    "boolean"

  #define TT_COMMA          "comma"         /* , */
  #define TT_SEMICOLON      "semicolon"     /* ; */
  #define TT_LEFT_PAREN     "left_paren"    /* ( */
  #define TT_RIGHT_PAREN    "right_paren"   /* ) */
  #define TT_LEFT_BRACKET   "left_bracket"  /* { */
  #define TT_RIGHT_BRACKET  "right_bracket" /* } */


struct Token
{
  string type;
  string value;
};

typedef vector<Token> Tokens;

struct Lexer 
{
  int pos;
  char current_char;
  string text;

  Lexer(string _text)
  {
    text = _text;
    text = " " + text + " ";
    pos = -1;
    advance();
  }
  Tokens tokenizer()
  {
    Tokens tokens;
    char c;
    while(pos < text.size())
    {
      c = current_char;
      if(c == '\n' || c == '\t' || c == ' ')
        advance();
      
      /* keywords and identifiers */
      else if(isalpha(c))
      {
        tokens.push_back(makeLexeme());
      }
      /* numbers */
      else if(isdigit(c))
      {
        tokens.push_back(makeDigit());
      }
      /* separators */
      else if(c=='(' || c==')' || c==';' || c==',' || c=='{' || c=='}'){
        tokens.push_back(makeSeparator());
        advance();
      }
      /* operators */
      else if(c=='+' || c=='-' || c=='*' || c=='/'){
        tokens.push_back(makeOperator());
        advance();
      }
      /* ASSIGNMENT */
      else if(c=='='){
        tokens.push_back({TT_ASSIGNMENT, string(1,c)});
        advance();
      }

      else {
        cerr << "Error: invalid token[" << c << "]" << endl;
        advance();
      }
    }

    return tokens;
  }

  Token makeLexeme()
  {
    string lexeme = "";
    while(isalpha(current_char)){
      lexeme += string(1, current_char);
      advance();
    }
    if(lexeme == PROGRAM_LITERAL)
      return {TT_PROGRAM, lexeme};
    if( lexeme == WHILE_LITERAL || lexeme == IF_LITERAL || lexeme == VAR_LITERAL)
      return {TT_KEYWORD, lexeme};
    if( lexeme == EQUAL_LITERAL || lexeme == NOTEQUAL_LITERAL || lexeme == AND_LITERAL || lexeme == OR_LITERAL)
      return {TT_OPERATOR, lexeme};
    
    if( lexeme == ADVANCE_LITERAL || lexeme == TURN_LITERAL || lexeme == COLOR_LITERAL)
      return {TT_LIB, lexeme};
    return {TT_ID, lexeme}; //identifier
  }

  Token makeDigit()
  {
    string number = "";
    while(isdigit(current_char)){
      number += string(1, current_char);
      advance();
    }
    return {TT_NUMBER, number};
  }

  Token makeSeparator()
  {
    char c = current_char;
    if(c=='(') return {TT_LEFT_PAREN, string(1, c)};
    if(c==')') return {TT_RIGHT_PAREN, string(1, c)};
    if(c=='{') return {TT_LEFT_BRACKET, string(1, c)};
    if(c=='}') return {TT_RIGHT_BRACKET, string(1, c)};
    if(c==',') return {TT_COMMA, string(1, c)};
    if(c==';') return {TT_SEMICOLON, string(1, c)};
    return {"",""};
  }

  Token makeOperator()
  {
    return {TT_OPERATOR, string(1, current_char)};
  }

  void advance()
  {
    if(pos + 1 >= text.size())
       pos = text.size();
    else {
      pos = pos + 1;
      current_char = text[pos];
    }
  }
}; //END LEXER

struct parser
{

};

/* reading file */
string readFile(string filename)
{
  ifstream in(filename, ios_base::in);
  string s = "";
  char c;
  while(!in.eof())
  {
    c = in.get();
    if(c>0)
      s += string(1, c);
  }
  return s;
}

int main(int argc, char *argv[])
{
  
  string text = readFile(argv[1]);
  Lexer l(text);
  Tokens tokens = l.tokenizer();
  cout << string(30,'.') << endl;
  for (int i = 0; i < tokens.size(); i++)
  {
    cout << tokens[i].type << ": " << tokens[i].value << endl;
  }
  

}
