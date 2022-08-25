import string

""" tokens string literals """
PROGRAM_LITERAL  = "program"
FUNCTION_LITERAL  = "function"
VAR_LITERAL      = "var"
IF_LITERAL       = "if"
WHILE_LITERAL    = "while"
EQUAL_LITERAL    = "equal"
NOTEQUAL_LITERAL = "notequal"
AND_LITERAL      = "and"
OR_LITERAL       = "or"
TRUE_LITERAL     = "true"
FALSE_LITERAL    = "false"
ADVANCE_LITERAL  = "advance"   # lib  
TURN_LITERAL     = "turn"      # lib  
COLOR_LITERAL    = "color"     # lib  

"""  token types  """
TT_PROGRAM    = "program"
TT_DEFINITION = "definition"
TT_KEYWORD    = "keyword"
TT_OPERATOR   = "operator"
TT_NUMBER     = "number"
TT_VAR        = "var"
TT_ID         = "id"
TT_ASSIGNMENT = "assignment"          # =  
TT_LIB        = "lib"                 # lib  
TT_BOOLEAN    = "boolean"

TT_COMMA          = "comma"          
TT_SEMICOLON      = "semicolon"       # ;  
TT_LEFT_PAREN     = "left_paren"      # (  
TT_RIGHT_PAREN    = "right_paren"     # )  
TT_LEFT_BRACKET   = "left_bracket"    # {  
TT_RIGHT_BRACKET  = "right_bracket"   # }  

LETTERS = string.ascii_letters
DIGITS = '0123456789'

class Error:
  def __init__(self, error_name, details) -> None:
    self.error_name = error_name
    self.details = details

  def __repr__(self) -> str:
    return f'Error: {self.error_name}: {self.details}'
  
  def to_string(self):
    return f'Error: {self.error_name}: {self.details}'

class Token:
  def __init__(self, type_, value=None):
    self.type = type_
    self.value = value
  
  def __repr__(self) -> str:
    if self.value:
      return f'{self.type} : {self.value}'
    return f'{self.type}'

class Lexer:
  def __init__(self, text_) -> None:
    self.pos = -1
    self.current_char = None
    self.text = ' ' + text_ + ' '
    self.advance()
  
  def advance(self):
    self.pos += 1
    self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
  
  def tokenizer(self):
    tokens = []
    while self.current_char != None:
      c = self.current_char
      # stopwords
      if c in ' \n\t':
        self.advance()
      
      # keywords and identifiers
      elif c in LETTERS:
        tokens.append(self.makeLexeme())
      # numbers
      elif c in DIGITS:
        tokens.append(self.makeDigit())
      # separators
      elif c in '();{,}':
        tokens.append(self.makeSeparator())
        self.advance()
      #operators
      elif c in '+-*/':
        tokens.append(self.makeOperator())
        self.advance()
      # assignment
      elif c in '=':
        tokens.append(Token(TT_ASSIGNMENT, c))
        self.advance()
      else:
        print(Error('invalid token', c))
        self.advance()
    return tokens

  def makeLexeme(self):
    lexeme = ''
    while self.current_char in LETTERS:
      lexeme += self.current_char
      self.advance()
    if lexeme == PROGRAM_LITERAL:
      return Token(TT_PROGRAM, lexeme)

    if lexeme == WHILE_LITERAL or lexeme == IF_LITERAL:
      return Token(TT_KEYWORD, lexeme)

    if lexeme == VAR_LITERAL:
      return Token(TT_VAR, lexeme)

    if lexeme == EQUAL_LITERAL or lexeme == NOTEQUAL_LITERAL or lexeme == AND_LITERAL or lexeme == OR_LITERAL:
      return Token(TT_OPERATOR, lexeme)

    if lexeme == TRUE_LITERAL or lexeme == FALSE_LITERAL:
      return Token(TT_BOOLEAN, lexeme)

    if lexeme == ADVANCE_LITERAL or lexeme == TURN_LITERAL or lexeme == COLOR_LITERAL:
      return Token(TT_LIB, lexeme)

    return Token(TT_ID, lexeme) #identifier

  def makeDigit(self):
    num_str = ''
    while self.current_char in DIGITS:
      num_str += self.current_char
      self.advance()
    return Token(TT_NUMBER, num_str)

  def makeSeparator(self):
    c = self.current_char
    if c=='(': return Token(TT_LEFT_PAREN, c)
    if c==')': return Token(TT_RIGHT_PAREN, c)
    if c=='{': return Token(TT_LEFT_BRACKET, c)
    if c=='}': return Token(TT_RIGHT_BRACKET, c)
    if c==',': return Token(TT_COMMA, c)
    if c==';': return Token(TT_SEMICOLON, c)
    return Token("","")

  def makeOperator(self):
    return Token(TT_OPERATOR, self.current_char)



























CONSOLE_LITERAL = "console.log"
