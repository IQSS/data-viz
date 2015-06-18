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
    
    # Does the file exist in the test directory?
    #
    filepath = join(TEST_FILES_DIR, filename)
    if not isfile(filepath):
        d= {"ERR_FOUND": True,
                "ERR_MSG": 'The file was not found: %s' % filepath
                }
        return flask.render_template("list_files.html", **d)
            

    df = pd.read_csv(filepath, sep='\t')
       
    #CREATING A LONG STRING TO ITERATE THROUGH THE VARIABLE NAMES AND 
    #CREATE THE BODY OF THE VARIABLE HTML TABLE'''
   
    variables = df.columns
    length = len(df.columns)
    long_string = str()
    
    for i in range(0,length):
        long_string +="<tr> "
        long_string += "<td> " 
        long_string += variables[i] 
        long_string += "</td> " 
        long_string += "</tr>"
    
    
    
    df_preview = df[1:16]
    df_html = df_preview.to_html(index = False)
    
    '''start = variables_html.find("class=\"")
    stop = variables_html.find(">")
    new_html1 = variables_html[:start] + 'class = "table "' + variables_html[stop:]'''
    
    start = df_html.find('class="')
    stop = df_html.find(">")
    new_html2 = df_html[:start] + 'class = "table table-striped"' + df_html[stop:]
    
    d = { "variables" : variables, 'data' : new_html2, "filename" : filename}
    


    return flask.render_template("index.html" , **d)
    #return filename


@app.route('/summary/<variable>/')
def summary_stats(variable):
    #pdb.set_trace()
    json_data = pandas.io.json.read_json(open("/Users/timibennatan/Desktop/PracticeMetadata/metadata.json"))
    
    df = pd.DataFrame(json_data)
    variables = df.columns




    json_variable = json_data[variable]
    df_variable = pd.DataFrame(json_variable)

    length_variables = len(variables)
    length_df = df.shape[0]
    
    #iterate through the varibles to create a table of variables
    variables_table = str()
    for i in range(0,length_variables):
        variables_table +="<tr> "
        variables_table += "<td> " 
        variables_table += variables[i] 
        variables_table += "</td> " 
        variables_table += "</tr>"
    
    summary_table = str()
    for i in range(1, length_df):
        summary_table += "<tr>"
        summary_table += "<td>"
        summary_table += df_variable.index[i]
        summary_table += "</td>"
        summary_table += "<td>"
        summary_table += str(df_variable.ix[i,0])
        summary_table += "</td>"
        summary_table += "</tr>"



     
    #df_variable.index[0] = "Summary Metric"
    #df_variable.columns = "Variable Value"
    
    metadata_html = df_variable.to_html()
    
    d= {"variables": variables_table,"summary": summary_table}
    
    return flask.render_template("metadata_preview.html", **d)
    
    

if __name__ == '__main__':
    app.debug = True
    app.static_folder = join(dirname(realpath(__file__)), 'static')
    app.run()









