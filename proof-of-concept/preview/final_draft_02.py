# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 14:00:40 2015

@author: timibennatan
"""
import os
from os.path import isfile, isdir, join, dirname, realpath
import flask
import pandas as pd
import requests
import unicodedata
from StringIO import StringIO
import pandas.io.json
import pdb

TEST_FILES_DIR = join(dirname(realpath(__file__)), 'test-files')

# Create the application.
app = flask.Flask(__name__)

@app.route('/')
def landpage():
    return "hello world"
    
@app.route('/list-files')
def list_files():

    # Does the directory exist?
    #
    if not isdir(TEST_FILES_DIR):
        # No
        d= {"ERR_FOUND": True,
            "ERR_MSG": 'Sorry, file directory not found: %s' % TEST_FILES_DIR
            }
        return flask.render_template("list_files.html", **d)
        
    # Retrieve list of file names from "TEST_FILES_DIR"
    #
    file_names = os.listdir(TEST_FILES_DIR)

    # Were any files found?
    #
    if len(file_names) == 0:
        d= {"ERR_FOUND": True,
            "ERR_MSG": 'Sorry, no files found in directory: %s' % TEST_FILES_DIR
            }
        return flask.render_template("list_files.html", **d)
     
    # Show the file names on the webpage 
    #   
    d= {"file_names": file_names,
        }
    
    return flask.render_template("list_files.html", **d)
    

@app.route('/preview-file/<filename>')
def read_file(filename):
    
    d = { 'filename' : filename }
    
    # Does the file exist in the test directory?
    #
    filepath = join(TEST_FILES_DIR, filename)
    if not isfile(filepath):
        d.update({"ERR_FOUND": True,
                "ERR_MSG": 'The file was not found: %s' % filepath
                })
        return flask.render_template("index.html", **d)
            

    df = pd.read_csv(filepath, sep='\t')
       
    #CREATING A LONG STRING TO ITERATE THROUGH THE VARIABLE NAMES AND 
    #CREATE THE BODY OF THE VARIABLE HTML TABLE'''
   
    variables = df.columns
    length = len(df.columns)
        
    df_preview = df[1:16]
    df_html = df_preview.to_html(index = False)
    
    '''start = variables_html.find("class=\"")
    stop = variables_html.find(">")
    new_html1 = variables_html[:start] + 'class = "table "' + variables_html[stop:]'''
    
    start = df_html.find('class="')
    stop = df_html.find(">")
    new_html2 = df_html[:start] + 'class = "table table-striped"' + df_html[stop:]
    
    d.update( { "variables" : variables, 
            'data' : new_html2 })
    


    return flask.render_template("index.html" , **d)
    #return filename


@app.route('/summary/<filename>/<variable>')
def summary_stats(filename, variable):
    
    d = { 'filename' : filename,
        'chosen_variable' : variable }
    
    # Does the file exist in the test directory?
    #
    filepath = join(TEST_FILES_DIR, filename)
    if not isfile(filepath):
        d.update({"ERR_FOUND": True,
                "ERR_MSG": 'The file was not found: %s' % filename
                })
        return flask.render_template("variable_metadata.html", **d)
            

    df = pd.read_csv(filepath, sep='\t')
    
    # does the variable exist
    if not variable in df.columns:
        d.update({"ERR_FOUND": True,
                "ERR_MSG": 'The variable %s was not found in file: %s' % (variable, filename)
                })
        return flask.render_template("variable_metadata.html", **d)
    
    s = df[variable]    # get a pandas series
    
    d.update({"variables" : df.columns,
        "summary_dict" : s.describe().to_dict()
        })
    
    return flask.render_template("variable_metadata.html", **d)
    
    

if __name__ == '__main__':
    app.debug = True
    app.static_folder = join(dirname(realpath(__file__)), 'static')
    app.run()









