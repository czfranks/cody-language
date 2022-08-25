import os
import sys
import subprocess

from lexer import *
from parser import *

ROUTE_YACC_ANALIZER = 'yacc/analizer/'
ROUTE_YACC_CONDEXPR = 'yacc/condexpr/'
ROUTE_TMP_FILES = 'tmp/'

def yaccAnalizer(text):
  cmd = f'echo "{text}" > {ROUTE_TMP_FILES}ana.txt & ./{ROUTE_YACC_ANALIZER}out < {ROUTE_TMP_FILES}ana.txt'
  result = subprocess.check_output(cmd, shell=True) #,  text=True, encoding='unicode'

  if 'syntax error' in str(result):
    return 'Syntax error', True
  elif 'Lexical' in str(result):
    return str(result), True
  else:
    return 'Success', False



#result = yaccAnalizer('program{.}')
#print("result: ", result)

#result = yaccCondexpr('3-23')
#print("result: ", result)


def gen(text):
  #filename = sys.argv[1]
  #f = open(filename, 'r')
  #text = f.read()

  res, err = yaccAnalizer(text)
  if err: #fail yacc analizer
    return Error("yacc analizer: ", res)

  #generating tokens
  lx = Lexer(text)
  tokens = lx.tokenizer()
  for tok in tokens:
    print(tok)
  
  #generating AST and Code generation
  parser = Parser()
  code, err = parser.parse(tokens)
  if err != None:
    return err
  else:
    parser.genCode()
    return None

  
