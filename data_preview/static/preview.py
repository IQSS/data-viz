# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 14:00:40 2015

@author: timibennatan
"""
from os.path import join, dirname, realpath
import flask
import pandas as pd
import requests
import unicodedata
from StringIO import StringIO
import pandas.io.json
import pdb
import json
from flask import Flask, jsonify, render_template, request, make_response

# Create the application.
app = flask.Flask(__name__)

@app.route('/summary_stats/')
def summary_stats():
	#pdb.set_trace()

	#these variables  will get redefined later:
	data_multibar = None
	data_stackedarea = None
	data_pie = None
	data_barline = None
	data_scatter = None
	all_plot_types = None


	new_variable = request.args.get("new_variable", default = None, type=str)
	variable_list_string = request.args.get("variable_list_string", default = None, type = str)

	variable_list = variable_list_string.split('||')
	number_of_variables = len(variable_list)


	#here we will use the actual metadata json file in the future,
	# which is already loaded in TwoRavens
	metadata_all = pandas.io.json.read_json("/Users/timibennatan/Desktop/law_metadata.json")
	#

	#create a list of all the different plot types in the current selected variables
	#from the metadata:
	plottype_list = list()

	for var in variable_list:


		metadata_variable_series = metadata_all[var]
		metadata_variable = pandas.DataFrame(metadata_variable_series)
	
		is_plottype = metadata_variable.index == "plottype"
		plottype_df = metadata_variable[is_plottype]
		plottype = str(plottype_df.ix[0,0])

		#adding each plottype to the 'plottype' list:
		plottype_list.append(plottype)

	#create a list with all the UNIQUE plottypes:
	unique_plottypes = list(set(plottype_list))




		#below I format the data to fit in with the chart in mind, then name it something like:
		#data_(a graph type)_json. 
		#NOTE TO FUTURE SELF!!! if this does not work for every data set, convert to a 
		#'try/except' configuration, with a default at NONE.

#any type, any number of varaibles: _____________~~_____________~~_____________~~____ any type/number
	#pdb.set_trace()



#NOTE: THE SCATTER DATA IS INCORRECT, AND THE .JS IS NOT YET FORMATTED. 
	# data_scatter = list()
	# for var in variable_list:
	# 	data_scatter.append({'key':var})
	# 	data_scatter.append({'values': list()}) #add data itself to this list in the form
	# 	#										# of key-value pairs



		
	# 	metadata_variable_series = metadata_all[var]
	# 	metadata_variable = pandas.DataFrame(metadata_variable_series)
	
	# 	is_plottype = metadata_variable.index == "plottype"
	# 	plottype_df = metadata_variable[is_plottype]
	# 	scatter_plottype = str(plottype_df.ix[0,0])

	# 	if scatter_plottype == "bar" : #if variable is 'bar'

	# 		is_plotvalues = metadata_variable.index == "plotvalues"
	# 		plotvalues_df = metadata_variable[is_plotvalues]
	# 		plotvalues_unicode = plotvalues_df.ix[0,0]
	# 		plotvalues_dict = dict(plotvalues_unicode)

	# 		for each in plotvalues_dict:
	# 			sub_dict = dict()
	# 			sub_dict['y'] = plotvalues_dict[each]
	# 			sub_dict['x'] = each
	# 			data_scatter[1]['values'].append(sub_dict)

	# 	else: #if variable is 'continuous'
	# 		scatter_plotx_list = metadata_variable.ix['plotx',0]
	# 		scatter_ploty_list = metadata_variable.ix['ploty',0]
	# 		length = len(scatter_plotx_list)

	# 		for each in range(0, length):
	# 			sub_dict = dict()
	# 			sub_dict['x'] = scatter_plotx_list[each]
	# 			sub_dict['y'] = scatter_ploty_list[each]
	# 			data_scatter['values'].append(sub_dict)


	#pdb.set_trace()






#_____________~~_____________~~_____________~~_____________~~_____________~~_________any type/number




		#check what types we have in the selected variables. 
	if len(unique_plottypes) == 1 and 'bar' in unique_plottypes:
		#if yes: construct the data in the appropriate format;
		
		all_plot_types = "bars_only" #will use this in the javascript later
		#to indicate which type of graph to build



#_______________________________________________________________________________________bar only

#creating data for multibar ––   ––   ––––   ––   ––––   ––   ––––   ––   ––––   ––  multibar
		data_multibar = list()
		for var in variable_list:
			sub_data = dict()

			sub_data['values'] = list()

			metadata_variable_series = metadata_all[var]
			metadata_variable = pandas.DataFrame(metadata_variable_series)
			is_plotvalues = metadata_variable.index == "plotvalues"
			plotvalues_df = metadata_variable[is_plotvalues]
			plotvalues_unicode = plotvalues_df.ix[0,0]
			plotvalues_dict = dict(plotvalues_unicode)

			for each in plotvalues_dict:
				sub_dict = {'y':plotvalues_dict[each],'x':each,}
				sub_data['values'].append(sub_dict)

			data_multibar.append(sub_data)



			sub_data['key']=var
#––   ––   ––––   ––   ––––   ––   ––––   ––   ––––   ––   ––––   ––   ––––   ––  multibar

#creating data for pie chart~~~   ~~~ ~~~   ~~~ ~~~   ~~~ ~~~   ~~~ ~~~   ~~~ ~~ pie 

		if (number_of_variables == 1):

			data_pie = list()
			for var in variable_list:
				

				metadata_variable_series = metadata_all[var]
				metadata_variable = pandas.DataFrame(metadata_variable_series)
				is_plotvalues = metadata_variable.index == "plotvalues"
				plotvalues_df = metadata_variable[is_plotvalues]
				plotvalues_unicode = plotvalues_df.ix[0,0]
				plotvalues_dict = dict(plotvalues_unicode)

				for each in plotvalues_dict:
					sub_data = {'value':plotvalues_dict[each], 'label':each}

					data_pie.append(sub_data)





#~~~   ~~~ ~~~   ~~~ ~~~   ~~~ ~~~   ~~~ ~~~   ~~~ ~~~   ~~~ ~~~   ~~~ ~~~    pie   
			
#_______________________________________________________________________________________ bar only
	

	#see if the selected variable are all type 'continuous'
	elif len(unique_plottypes) == 1 and 'continuous' in unique_plottypes:
		#if yes, construct data appropriately:

		all_plot_types = "continuous_only"

#_____________________________________________________________________________continuous only

#stackedarea --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --   stackedarea
		#pdb.set_trace()

		all_xvalues = list()

		for var in variable_list:
			metadata_variable_series = metadata_all[var]
			metadata_variable = pandas.DataFrame(metadata_variable_series)
			plotx_list = metadata_variable.ix['plotx',0]
			for each in plotx_list:
				all_xvalues.append(each)

		all_xvalues = list(set(all_xvalues))




		data_stackedarea = list()

		for var in variable_list:
			sub_data = dict()

			sub_data['key'] = var

			metadata_variable_series = metadata_all[var]
			metadata_variable = pandas.DataFrame(metadata_variable_series)
			#save the 'plotx' and 'ploty' values individually as lists

			plotx_list = metadata_variable.ix['plotx',0]
			ploty_list = metadata_variable.ix['ploty',0]
			length = len(plotx_list)

			missing_xvalues = list(set(all_xvalues) - set(plotx_list))

			for each_x in missing_xvalues:
				plotx_list.append(each_x)
				ploty_list.append(0)
			#start adding values
			sub_data['values'] = list()

			
			for each in range(0, length):
				sub_list = list()
				

				sub_list.append(plotx_list[each])


				sub_list.append(ploty_list[each])
				sub_data['values'].append(sub_list)

			

			
			data_stackedarea.append(sub_data)


		

#stackedarea --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --   stackedarea


#––   ––   ––––   ––   ––––   ––   ––––   ––   ––––   ––   ––––   ––   ––––   ––  multibar

		data_multibar = list()



		for var in variable_list:
		

			metadata_variable_series = metadata_all[var]
			metadata_variable = pandas.DataFrame(metadata_variable_series)
			#save the 'plotx' and 'ploty' values individually as lists
			plotx_list = metadata_variable.ix['plotx',0]
			ploty_list = metadata_variable.ix['ploty',0]
			length = len(plotx_list)

			sub_data = dict()
			sub_data['key'] = var
			sub_data['values'] = list()

			xval_list = list()
			for each in range(0, length):
				sub_dict = dict()

				sub_dict['x'] = plotx_list[each]
				sub_dict['y'] = ploty_list[each]
				#xval_list.append(plotx_list[each])

				sub_data['values'].append(sub_dict)

			data_multibar.append(sub_data)




#––   ––   ––––   ––   ––––   ––   ––––   ––   ––––   ––   ––––   ––   ––––   ––  multibar



#_________________________________________________________________________________ continuous only

#the following code are for graphs with variables of "mixed type"
#-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- mixed

	else:
		all_plot_types = "mixed"

#creating data for the list/bar chart
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ bar/line
		

		data_barline = list()

		for var in variable_list:
			sub_data = dict()
			metadata_variable_series = metadata_all[var]
			metadata_variable = pandas.DataFrame(metadata_variable_series)
		
			is_plottype = metadata_variable.index == "plottype"
			plottype_df = metadata_variable[is_plottype]
			barline_plottype = str(plottype_df.ix[0,0])

			

			if barline_plottype == "bar" : #if variable is 'bar'

				is_plotvalues = metadata_variable.index == "plotvalues"
				plotvalues_df = metadata_variable[is_plotvalues]
				plotvalues_unicode = plotvalues_df.ix[0,0]
				plotvalues_dict = dict(plotvalues_unicode)

				sub_data = dict()
				sub_data['key'] = var
				sub_data['bar'] = 'true'
				sub_data['values'] = list()
				

				for each in plotvalues_dict:
					sub_list = list()
					sub_list.append(plotvalues_dict[each])
					sub_list.append(each)

					sub_data['values'].append(sub_list)

				data_barline.append(sub_data)

			else: #if variable is continuous
				sub_data = dict()
				sub_data['key'] = var
				sub_data['values'] = list()

				barline_plotx_list = metadata_variable.ix['plotx',0]
				barline_ploty_list = metadata_variable.ix['ploty',0]
				length = len(barline_plotx_list)

				for each in range(0, length):
					sub_list = list()
					sub_list.append(barline_plotx_list[each])
					sub_list.append(barline_ploty_list[each])
					sub_data['values'].append(sub_list)

				data_barline.append(sub_data)










#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ bar/line

		

#-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- mixed


	
	metadata_html = metadata_variable.to_html(header = False)

	#add the bootsrap table classes
	start = metadata_html.find('class="')
	stop = metadata_html.find(">")
	metadata_html= metadata_html[:start] + 'class = "table-condensed table-striped>"' + '<thead><tr class = "metadata_header"><th>Summary Metric</th><th>Value</th></tr></thead>'+ metadata_html[stop+1:] 
	



#here we will construct the data json objects, compatible with specific graph types. 
#___________________________________________________________________________________________
	data_json_multibar = json.dumps(data_multibar)
	data_json_stackedarea= json.dumps(data_stackedarea)
	data_json_pie = json.dumps(data_pie)
	data_json_barline = json.dumps(data_barline)
	data_json_scatter = json.dumps(data_scatter)
#___________________________________________________________________________________________
	#pdb.set_trace()

	example_modal = '<button type="button" class="btn btn-primary" data-toggle="modal" data-target=".bs-example-modal-sm">Small modal</button><div class="modal fade bs-example-modal-sm" tabindex="-1" role="dialog"><div class="modal-dialog modal-sm"><div class="modal-content">content</div></div></div>'

	d = {'number_of_variables': number_of_variables,
		'new_variable': new_variable,
		'plottype_list': plottype_list,	#each plottype for each variable
		'all_plot_types':all_plot_types, #expresses the unique plot types
		'plottype': plottype,
		'variable_list': variable_list,
	    'metadata_html' : metadata_html,
	    'data_json_multibar': data_json_multibar,
	    'data_json_stackedarea': data_json_stackedarea,
	    'data_json_pie': data_json_pie,
	    'data_json_barline' : data_json_barline}

	return jsonify(**d)

	

#___________________________________________________________________________________________


@app.route('/')
def landpage():
	return 'start with a file id in the url: e.g. "http://...fileid")'
#___________________________________________________________________________________________
#use fileid to create initial preview
@app.route('/<fileid>/')
def preview(fileid):
	#pdb.set_trace()
	



	download_url = 'http://dataverse.harvard.edu/api/access/datafile/' + str(fileid)
	request = requests.get(download_url)
	d =  request.text
	data_unicode = unicodedata.normalize("NFKD", d).encode("ascii",'ignore')

	data_string = StringIO(data_unicode)
	df = pd.read_table(data_string)
	df_preview = df[1:16]


    #create variable names for varaible table
	variables = df.columns   


   #Create HTML of pandas dataframe 
	df_html_unclassed = df_preview.to_html(index = False)
	start = df_html_unclassed.find('class="')
	stop = df_html_unclassed.find(">")
	df_html= df_html_unclassed[:start] + 'class = "table table-striped"' + df_html_unclassed[stop:]



	d = {"data": df_html, 'variables' : variables, 'fileid':fileid}

	return render_template('index_recover.html', **d)
#___________________________________________________________________________________________

 # @app.route('/sumstats_modals/')
 # def modals():
 # 	variable_list_string = request.args.get("variable_list_string", default = None, type = str)
 # 	variable_list = variable_list_string.split('||')
	# number_of_variables = len(variable_list)

	# example = '<button type="button" class="btn btn-primary" data-toggle="modal" data-target=".bs-example-modal-sm">Small modal</button><div class="modal fade bs-example-modal-sm" tabindex="-1" role="dialog" aria-labelledby="mySmallModalLabel"><div class="modal-dialog modal-sm"><div class="modal-content">content</div></div></div>'

	# d = {'example_modal': example}

	# return jsonify(**d)









 
if __name__ == '__main__':
	app.debug = True
	app.run()








