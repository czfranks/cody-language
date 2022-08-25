from flask import Blueprint, current_app, json, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from werkzeug.wrappers import response
from flask_cors import CORS
import numpy as np
import logging
import cv2
import os
import sys

from solver import *


api_code = Blueprint('api_code', __name__, url_prefix='/api')
CORS(api_code)

@api_code.route('/')
def hello():
    return 'generador de codigo Compiladores Final'

@api_code.route('/gen', methods=['GET', 'POST'])
def generator():
    if request.method == 'POST':
        #text_code = request.form['code']
        #text_code = request.json['code'];
        text_code = request.data;
        text_code = text_code.decode('utf-8')

        print(':>>>>>>: ', type(text_code), ", ", text_code)
        res = gen(text_code)
        if res != None:
          return jsonify({'code':'.', 'error':res.to_string()})
        filename = f'{ROUTE_TMP_FILES}gen.txt'
        text_file = open(filename, 'r')
        text_gen = text_file.read()
        text_file.close()
        return jsonify({'code':text_gen, 'error':None})
    return 'other'



# reques.data recive un Text/plain mediante el metodo post
#request.data = {
"""     program {
  var x, y, z;
  x = 4;
  y = 5;
  z = 10;
  if(z equal 10)
  {
    advance(z);
  }
  while(x + 2*3 notequal (y + 10) )
  {
    turn(45);
    advance(x*10 + z*z);
    x = x + 1;
  }
  var w, r;
  w = 3; r = 4;
  if(w notequal 3 or r equal 3){
    turn(135);
    color(x*3, (y-1)*100, z*3);
  }
} """
#}
