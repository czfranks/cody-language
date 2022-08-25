from distutils.errors import PreprocessError
from re import I

from matplotlib.animation import FuncAnimation
from lexer import *
import subprocess

ROUTE_YACC_CONDEXPR = 'yacc/condexpr/'
ROUTE_TMP_FILES = 'tmp/'

def yaccCondexpr(text):
  cmd = f'echo "{text}" > {ROUTE_TMP_FILES}cond.txt & ./{ROUTE_YACC_CONDEXPR}out < {ROUTE_TMP_FILES}cond.txt'
  result = subprocess.check_output(cmd, shell=True) #,  text=True, encoding='unicode'

  if 'syntax error' in str(result):
    return 'Syntax error', True
  elif 'Lexical' in str(result):
    return str(result), True
  else:
    return str(int(result)), False


TT_EXPR = 'expr'

class Parser:
  def __init__(self):
    self.tokens = []
    self.code = ''
    self.symbol_table = {}

  def parse(self, tokens):
    #declaracion de varibles
    err = self.preprocessVar(tokens)
    if err != None:
      return '', err
    
    #verificacion de ambiguedades con variables
    err = self.verifyAssignment()
    if err != None:
      return '', err

    #generacion de codigo
    self.code = self.traduction()

    return self.code, None


  def preprocessVar(self, tokens):
    pos = 0
    while(pos < len(tokens)):
      t = tokens[pos]
      
      #reducing with variable declarations
      if t.type == TT_VAR:
        print("total")
        while pos < len(tokens): # while True:
          pos += 1
          t = tokens[pos]
          if(t.type == TT_ID and t.value not in self.symbol_table):
            self.symbol_table[t.value] = None
          else:
            return Error('Semantic: ', f'La variable [{t.value}] ya fue declara previamente.')
          pos += 1
          t = tokens[pos]
          if t.type == TT_SEMICOLON:
            break
          if(t.type == TT_COMMA):
            continue
      else:
        self.tokens.append(t)
      pos += 1
    return None

  def verifyAssignment(self):
    pos = 0
    init = []
    while(pos < len(self.tokens)):
      t = self.tokens[pos]
      if t.type == TT_ASSIGNMENT:
        prev_t = self.tokens[pos-1]
        init.append(prev_t.value)

      if t.type == TT_ID:
        if t.value not in self.symbol_table:
          return Error('Semantic: ', f'La variable [ {t.value} ] No fue declarada.')
        next_t = self.tokens[pos+1]
        if next_t.type != TT_ASSIGNMENT:
          if t.value not in init:
            return Error('Semantic: ', f'La variable [ {t.value} ] esta siendo usada sin inicializar.')

      pos += 1
      
    return None

  def traduction(self):
    text = ''
    for key, value in self.symbol_table.items():
      text += 'var ' + key + ' ;\n'
    for t in self.tokens:
      if t.type == TT_PROGRAM:
        text += IF_LITERAL + '('+TRUE_LITERAL+')\n'
      elif t.type == TT_OPERATOR:
        if t.value == EQUAL_LITERAL:
          text += ' === ';
        elif t.value == NOTEQUAL_LITERAL:
          text += ' !== ';
        elif t.value == OR_LITERAL:
          text += ' || ';
        elif t.value == AND_LITERAL:
          text += ' && ';
        else:
          text += t.value
      elif t.type == TT_BOOLEAN:
        if t.value == TRUE_LITERAL:
          text += ' true '
        else:
          text += ' false '
      elif t.type == TT_LIB:
        if t.value == ADVANCE_LITERAL:
          text += ADVANCE_LITERAL
        elif t.value == TURN_LITERAL:
          text += TURN_LITERAL
        else:
          text += COLOR_LITERAL
      elif t.type == TT_SEMICOLON:
        text += ';\n';
      elif t.type == TT_LEFT_BRACKET:
        text += '{\n';
      elif t.type == TT_RIGHT_BRACKET:
        text += '}\n';
      else:
        text += ' ' + t.value + ' '

    text += FUNCTION_LITERAL + ' ' + ADVANCE_LITERAL + '(e){'+CONSOLE_LITERAL+'("'+ADVANCE_LITERAL+'",e);}\n';
    text += FUNCTION_LITERAL + ' ' + TURN_LITERAL + '(e){'+CONSOLE_LITERAL+'("'+TURN_LITERAL+'",e);}\n';
    text += FUNCTION_LITERAL + ' ' + COLOR_LITERAL + '(a,b,c){'+CONSOLE_LITERAL+'("'+COLOR_LITERAL+'",a,b,c);}\n';
    return text
    

  def genCode(self):
    filename = f'{ROUTE_TMP_FILES}gen.js'
    text_file = open(filename, 'w');
    text_file.write(self.code)
    text_file.close()

    cmd = f'node {filename} > {ROUTE_TMP_FILES}gen.txt'
    result = subprocess.check_output(cmd, shell=True) #,  text=True, encoding='unicode'

    print("gencode result: ", result)


#""" 
#>>> d.get('hola') == None
#True
#>>> d['dota2'] = None
#>>> d
#{'gaa': 'aea', 'dota2': None}
#{'keywan': 'camote', 'o': None}
#>>> ('o',None) in d
#False
#>>> 'o' in d
#True
#>>> 'franls' in d
#False
# """


