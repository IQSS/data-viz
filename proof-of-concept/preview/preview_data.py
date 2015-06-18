import flask
import pandas as pd
import os
import requests
import unicodedata
import sys


# Create the application.
app = flask.Flask(__name__)


@app.route('/preview/<fileid>/')
def read_file(fileid):

#GET DATA FROM API---------------------------

	download_url = 'http://dataverse.harvard.edu/api/access/datafile/' + fileid
	request = requests.get(download_url)

	d =  request.text
	d_string = unicodedata.normalize("NFKD", d).encode("ascii",'ignore')
	
	if sys.version_info[0] < 3:
		from StringIO import StringIO
	else:
	    	from io import StringIO
    

# CREATE PANDAS DATAFRAME FROM DATA--------------------

	from pandas import DataFrame

	
	TESTDATA=StringIO(d_string)
	df = DataFrame.from_csv(TESTDATA, sep="\t", parse_dates=False, header = True)


# 


	f = open("./Templates/index.html", "w")

	f.write("<!DOCTYPE html><html><head></head><body><table border = '1'><tr>")

	total_rows = df.shape[0]
	total_cols = df.shape[1]

	df_index = pd.Series(range(0,total_rows))
	pd.DataFrame.set_index(df, df_index)

	for i in df.columns.values:
		f.write ("<th>")
		f.write(i)
		f.write('</th>')




	for row in range(0,16):
		f.write('<tr>')
		for each in range(0,total_cols):
			f.write("<td>")
			f.write(str(df.loc[row][each]))
			f.write('</td>')
		f.write('</tr>')

	f.close()

	return flask.render_Template("index.html")

if __name__ == '__main__':
    app.debug=True
    app.run()










