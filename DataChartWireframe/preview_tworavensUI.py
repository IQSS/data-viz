# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 14:00:40 2015

@author: timibennatan
"""
from os.path import join, dirname, realpath
import flask
import math
import pandas as pd
import requests
import unicodedata
from StringIO import StringIO
import pandas.io.json
import pdb
import json
import math
from flask import Flask, jsonify, render_template, request, make_response
import rpy2.robjects as robjects
from rpy2.robjects.packages import STAP
import pandas.rpy.common as com




# Create the application.
app = flask.Flask(__name__)

@app.route('/summary_stats/')
def summary_stats():
	#pdb.set_trace()

	#these variables  will get redefined later:
	data_multibar = None
	data_stackedarea = None
	data_pie = None
	data_scatter_continuous = None
	all_plot_types = None
	difference_domains_multibar = None
	warning_multibar = None
	warning_stackedarea = None
	line_data = None



	new_variable = request.args.get("new_variable", default = None, type=str)
	variable_list_string = request.args.get("variable_list_string", default = None, type = str)

	variable_list = variable_list_string.split('||')
	number_of_variables = len(variable_list)


	#here we will use the actual metadata json file in the future,
	# which is already loaded in TwoRavens
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




#_____________~~_____________~~_____________~~_____________~~_____________~~_________any type/number




		#check what types we have in the selected variables. 
	if len(unique_plottypes) == 1 and 'bar' in unique_plottypes:
		#if yes: construct the data in the appropriate format;
		
		all_plot_types = "bars_only" #will use this in the javascript later
		#to indicate which type of graph to build



#_______________________________________________________________________________________bar only

#creating data for multibar ––   ––   ––––   ––   ––––   ––   ––––   ––   ––––   ––  multibar

		all_xvalues = list()
		all_yvalues = list()
		list_of_domains_multibar = list()
		for var in variable_list:
			metadata_variable_series = metadata_all[var]
			metadata_variable = pandas.DataFrame(metadata_variable_series)
			is_plotvalues = metadata_variable.index == "plotvalues"
			plotvalues_df = metadata_variable[is_plotvalues]
			plotvalues_unicode = plotvalues_df.ix[0,0]
			plotvalues_dict = dict(plotvalues_unicode)

			individual_variable_domains= list() #used for the warning message
			for each in plotvalues_dict:
				all_xvalues.append(each)
				individual_variable_domains.append(each)
				all_yvalues.append(plotvalues_dict[each])

			list_of_domains_multibar.append(individual_variable_domains)

		
		union_multibar = list()
		intersection_multibar = list_of_domains_multibar[0]
		for each in list_of_domains_multibar:
			union_multibar = list(set(union_multibar) | set(each))
			intersection_multibar = list(set(intersection_multibar) & set(each))

		

		difference_domains_multibar = 100.0-(100.0* len(intersection_multibar)/len(union_multibar))

				
		#pdb.set_trace()
		all_xvalues = list(set(all_xvalues))



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

			xvalues_list = list()
			yvalues_list = list()
			for each in plotvalues_dict:
				xvalues_list.append(each)
				yvalues_list.append(plotvalues_dict[each])
				

			for each_x in all_xvalues:
				if each_x not in xvalues_list:
					xvalues_list.append(each_x)
					yvalues_list.append(None)

			xy = zip(xvalues_list, yvalues_list)
			xy.sort()
			length_xy = len(xy)





			for each in range(0,length_xy):
				sub_dict = {'x':xy[each][0],'y':xy[each][1],}
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
	elif (len(unique_plottypes) == 1 and 'continuous' in unique_plottypes):
		#if yes, construct data appropriately:

		all_plot_types = "continuous_only"

#_____________________________________________________________________________continuous only

#stackedarea --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --   stackedarea
		#calculating domain differences for stackedarea

		if number_of_variables == 1:




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


				#start adding values
				sub_data['values'] = list()

				xval_list = list()
				for each in range(0,length):
					xval_list.append(plotx_list[each])

				for each_x in all_xvalues:
					if each_x not in xval_list:
						plotx_list.append(each_x)
						ploty_list.append(None)

				xy = zip(plotx_list, ploty_list)
				xy.sort()

				length_xy = len(xy)




				for each in range(0, length_xy):
					sub_list = list()
					

					sub_list.append(xy[each][0])
					

					sub_list.append(xy[each][1])
					sub_data['values'].append(sub_list)

				
				
				
				data_stackedarea.append(sub_data)

			

			






	

#stackedarea --  --  --  --  --  --  --  --  --  --  --  --  --  --  --  --   stackedarea


#scatter continuous ~~~–––~~~–––~~~–––~~~–––~~~–––~~~–~~~~~–––~~~–––~~ scatter continuous

		data_scatter_continuous = list()

		

		for var in variable_list:

			sub_data = dict()

			sub_data['key']= var
			sub_data['values'] = list()

			
			metadata_variable_series = metadata_all[var]
			metadata_variable = pandas.DataFrame(metadata_variable_series)
		

			scatter_plotx_list = metadata_variable.ix['plotx',0]
			scatter_ploty_list = metadata_variable.ix['ploty',0]
			
					# scatter_plotx_list.append(each)
					# scatter_ploty_list.append(None)

			for each in range(0, len(scatter_plotx_list)):
				sub_dict = dict()
				sub_dict['x'] = scatter_plotx_list[each]
				sub_dict['y'] = scatter_ploty_list[each]
				sub_data['values'].append(sub_dict)

			data_scatter_continuous.append(sub_data)





#scatter continuous ~~~–––~~~–––~~~–––~~~–––~~~–––~~~–~~~~~–––~~~–––~~ scatter continuous


#line _______________    _______________    _______________    _______________   line

		line_data = list()

		for var in variable_list:

			metadata_variable_series = metadata_all[var]
			metadata_variable = pandas.DataFrame(metadata_variable_series)
		
			is_plottype = metadata_variable.index == "plottype"
			plottype_df = metadata_variable[is_plottype]
			line_plottype = str(plottype_df.ix[0,0])

			all_xvalues = list()
			all_yvalues = list()


			

			
			line_plotx_list = metadata_variable.ix['plotx',0]
			line_ploty_list = metadata_variable.ix['ploty',0]
			length = len(line_plotx_list)

			for each in range(0, length):

				all_xvalues.append(line_plotx_list[each])
				all_yvalues.append(line_ploty_list[each])

			xy = zip(all_xvalues,all_yvalues)
			xy.sort()

			sub_data = dict()
			sub_data['key']= var
			sub_data['values'] = list()

			for each in range(0, len(xy)):
				sub_dict = dict()
				sub_dict['x'] = xy[each][0]
				sub_dict['y']= xy[each][1]
				sub_data['values'].append(sub_dict)

			line_data.append(sub_data)



#line _______________    _______________    _______________    _______________   line



#––   ––   ––––   ––   ––––   ––   ––––   ––   ––––   ––   ––––   ––   ––––   ––  multibar
		# pdb.set_trace()
		data_multibar = list()

		all_xvalues = list()
		for var in variable_list:
			metadata_variable_series = metadata_all[var]
			metadata_variable = pandas.DataFrame(metadata_variable_series)

			plotx_list = metadata_variable.ix['plotx',0]
			for each in plotx_list:
				all_xvalues.append(each)

		all_xvalues = list(set(all_xvalues))



		for var in variable_list:
		

			metadata_variable_series = metadata_all[var]
			metadata_variable = pandas.DataFrame(metadata_variable_series)
			#save the 'plotx' and 'ploty' values individually as lists
			plotx_list = metadata_variable.ix['plotx',0]
			ploty_list = metadata_variable.ix['ploty',0]

			for each in all_xvalues:
				if each not in plotx_list:
					plotx_list.append(each)
					ploty_list.append(None)

			xy = zip(plotx_list, ploty_list)
			xy.sort()
			length_xy = len(xy)


			sub_data = dict()
			sub_data['key'] = var
			sub_data['values'] = list()

			xval_list = list()
			for each in range(0, length_xy):
				sub_dict = dict()

				sub_dict['x'] = xy[each][0]
				sub_dict['y'] = xy[each][1]
				#xval_list.append(plotx_list[each])

				sub_data['values'].append(sub_dict)

			data_multibar.append(sub_data)




#––   ––   ––––   ––   ––––   ––   ––––   ––   ––––   ––   ––––   ––   ––––   ––  multibar



#_________________________________________________________________________________ continuous only

#the following code are for graphs with variables of "mixed type"
#-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- mixed

	else:
		all_plot_types = "mixed"


		
#-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- mixed

	#pdb.set_trace()
	
	metadata_html = metadata_variable.to_html(header = False)

	header = '<h3>' + new_variable + ' summary stats</h3>'
	#add the bootsrap table classes
	start = metadata_html.find('class="')
	stop = metadata_html.find(">")
	metadata_html= header + metadata_html[:start] + 'class = "table-condensed table-striped>"' + '<thead><tr class = "metadata_header"><th>Summary Metric</th><th>Value</th></tr></thead>'+ metadata_html[stop+1:] 
	
#___________________________________________________________________________________________

	metadata_modals_buttons = '<h4> Selected Variables Metadata</h4>'
	metadata_modals_content=""

	for var in variable_list:
		metadata_variable_series = metadata_all[var]
		metadata_variable = pandas.DataFrame(metadata_variable_series)
		var_html = metadata_variable.to_html(header = False)

		#pdb.set_trace()
		metadata_modals_buttons += '<button type="button" class="btn btn-default sumstats_modals" data-toggle="modal" data-target=".' + var + '_sumstats' +'"><strong>' +var + '</strong> metadata' + '</button>'
		metadata_modals_content += '<div class="modal fade ' +var + '_sumstats' + '" tabindex="-1" role="dialog"><div class="modal-dialog modal-sm"><div class="modal-content">'+ var_html+'</div></div></div>'

#___________________________________________________________________________________________

#___________________________________________________________________________________________
# warning messages 
	if difference_domains_multibar != None and difference_domains_multibar > 30.:
		warning_multibar = '<div class="alert alert-warning alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button><strong>Warning:</strong> chart created but may be misleading. <strong>'+ str(difference_domains_multibar) + "%</strong> of the selected variables's domains to do not intersect. Please be cautious before inferring any relationship between these variables.</div>"


#___________________________________________________________________________________________



#here we will construct the data json objects, compatible with specific graph types. 
#___________________________________________________________________________________________
	data_json_multibar = json.dumps(data_multibar)
	data_json_stackedarea= json.dumps(data_stackedarea)
	data_json_pie = json.dumps(data_pie)
	data_json_scatter_continuous = json.dumps(data_scatter_continuous)
	data_json_line = json.dumps(line_data)
#___________________________________________________________________________________________
	#pdb.set_trace()


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
	    'data_json_scatter_continuous': data_json_scatter_continuous,
	    'data_json_line': data_json_line,
	    'metadata_modals_buttons': metadata_modals_buttons,
	    'metadata_modals_content':metadata_modals_content,
	    'warning_multibar':warning_multibar}

	return jsonify(**d)

	

#___________________________________________________________________________________________


@app.route('/')
def landpage():
	d = {}

	return render_template ('landpage.html', **d)
#___________________________________________________________________________________________
#___________________________________________________________________________________________


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

	global df_global
	df_global = df
	df_preview = df[1:16]


    #create variable names for varaible table
	variables = df.columns   

	total_rows = df.shape[0]
	total_cols = df.shape[1]
   #Create HTML of pandas dataframe 
	df_html_unclassed = df_preview.to_html(index = False)
	start = df_html_unclassed.find('class="')
	stop = df_html_unclassed.find(">")
	df_html= df_html_unclassed[:start] + 'class = "table table-striped"' + df_html_unclassed[stop:]

	
	r_dataframe = com.convert_to_r_dataframe(df_global)
	
	robjects.r('''
       source('preprocess.R')
	''')
	r_preprocess =  robjects.globalenv['preprocess']
	meta = str(r_preprocess(testdata =r_dataframe))
	meta= meta.replace('\\', '')
	meta=meta.replace('"\n', '')
	meta = meta.replace('[1] "', '')
	global metadata_all 
	metadata_all = pandas.io.json.read_json(meta)


	# metadata_all = pandas.io.json.read_json("/Users/timibennatan/Desktop/cl2014.json")
	
	metadata_subset = [0,3,4,9,12,13,14,16,17,20,24,25] #the summary metrics I want for the summary stats
	variable_info_dict = dict()
	for var in variables:
		metadata_variable_series = metadata_all[var]
		metadata_variable = pandas.DataFrame(metadata_variable_series)
		sumstats_variable = metadata_variable.ix[metadata_subset]
		sumstats_variable_html = str(sumstats_variable.to_html(header = False))
		start = sumstats_variable_html.find('class="')
		stop =sumstats_variable_html.find(">")
		sumstats_variable_html= sumstats_variable_html[:start] + 'class = "table-condensed table-striped>"' + sumstats_variable_html[stop+1:]
		sumstats_variable_html = sumstats_variable_html.replace('<','&lt;')
		sumstats_variable_html = sumstats_variable_html.replace('<','&gt;')
		variable_info_dict[var] = sumstats_variable_html


	#pdb.set_trace()





	d = {"data": df_html, 'variables' : variables, 'fileid':str(fileid), 'variable_info_dict':variable_info_dict, 'total_rows':total_rows, 'total_cols':total_cols}

	return render_template('gui.html', **d)

#___________________________________________________________________________________________

@app.route('/bivariate_scatter/')
def bivariate_scatter():

	x_value = request.args.get("x_value", default = None, type=str)
	y_value = request.args.get('y_value', default = None, type=str)
	z_value = request.args.get('z_value', default = None, type=str)

	x_or_y_missing = False
	repeated_variables = False
	z_empty = True
	inputs_valid = True
	all_data_numeric = True
	bivariate_data = None
	trivariant_data = None
	max_x_3d=None
	min_x_3d = None
	max_y_3d = None
	min_y_3d = None
	max_z_3d = None
	min_z_3d = None




	if x_value == '' or y_value == '':
		x_or_y_missing = True

	else: #both x and y are not missing

		if x_value == y_value or x_value == z_value or y_value ==z_value:
			repeated_variables = True

		else:#no repeated variables

			if z_value == '':

				if x_value not in df_global.columns or y_value not in df_global.columns:
					inputs_valid = False

				else: #all inputs valid
					
					col_list = [x_value, y_value]
					df= df_global[col_list]
					df_full = df.dropna()


					col_type_list = list()
					col_type_list.append(df_full[x_value].dtype)
					col_type_list.append(df_full[y_value].dtype)

					if(col_type_list[0] != 'int64' and col_type_list[0] != 'float64') or (col_type_list[1] != 'int64' and col_type_list[1] != 'float64'):

						all_data_numeric = False

					else: # all data numeric
						
						points_list = list()
						size_list = list()
						n_rows = df_full.shape[0]

						for row in range(0,n_rows):

							point = [df_full.iloc[row][x_value], df_full.iloc[row][y_value]]

							if point not in points_list: 
								points_list.append(point)
								size_list.append(1)

							else:
								point_index = points_list.index(point)
								size_list[point_index] += 1

						n_points = len(points_list)
						for i in range(0,n_points):
							points_list[i].append(size_list[i])

						bivariate_data= dict()
						bivariate_data['data'] = points_list




			else: #zvalue is specified
				z_empty= False

				if x_value not in df_global.columns or y_value not in df_global.columns or z_value not in df_global.columns:
					inputs_valid = False

				else: #all inputs valid
					col_list = [x_value, y_value, z_value]
					df= df_global[col_list]
					df_full = df.dropna()

					col_type_list = list()
					col_type_list.append(df_full[x_value].dtype)
					col_type_list.append(df_full[y_value].dtype)
					col_type_list.append(df_full[z_value].dtype)

					if(col_type_list[0] != 'int64' and col_type_list[0] != 'float64') or (col_type_list[1] != 'int64' and col_type_list[1] != 'float64') or (col_type_list[2] != 'int64' and col_type_list[2] != 'float64'):

						all_data_numeric = False

					else: #all data numeric
						points_list = list()
						n_rows = df_full.shape[0]

						x_value_list=list()
						y_value_list=list()
						z_value_list=list()

						for row in range(0,n_rows):

							x_value_list.append(df_full.iloc[row][x_value])
							y_value_list.append(df_full.iloc[row][y_value])
							z_value_list.append(df_full.iloc[row][z_value])

						xyz = zip(x_value_list,y_value_list,z_value_list)
						xyz.sort()

						for i in xyz:
							points_list.append(list(i))


						trivariant_data = dict()
						trivariant_data['ColorByPoint']= True
						trivariant_data['data'] = points_list

						max_x_3d = int(math.ceil(max(x_value_list)))
						min_x_3d = int(min(x_value_list))

						max_y_3d = int(math.ceil(max(y_value_list)))
						min_y_3d = int(min((y_value_list)))

						max_z_3d = int(math.ceil(max(z_value_list)))
						min_z_3d = int(min(z_value_list))

						#pdb.set_trace();




	

	d= {'x_or_y_missing':x_or_y_missing,
	 'z_empty': z_empty,
	  'inputs_valid': inputs_valid,
	  'repeated_variables': repeated_variables,
	   'all_data_numeric':all_data_numeric,
	   'bivariate_data': bivariate_data,
	   'trivariant_data':trivariant_data,
	   'max_x_3d':max_x_3d,
	   'max_y_3d':max_y_3d,
	   'max_z_3d': max_z_3d,
	   'min_x_3d': min_x_3d,
	   'min_y_3d': min_y_3d,
	   'min_z_3d': min_z_3d}
	return jsonify(**d)
#-----------------------------------------------------------------------------

@app.route('/bivariate_range_area/')
def range_area():

	x_value = request.args.get("x_value", default = None, type=str)
	y_value = request.args.get('y_value', default = None, type=str)

	x_or_y_missing = False
	repeated_variables = False
	inputs_valid = True
	y_axis_numeric = True
	data_range_area = None

	if x_value == '' or y_value == '':
		x_or_y_missing = True

	else: #both are not empty

		if x_value == y_value:
			repeated_variables = True

		else:#no repeated variables

			if x_value not in df_global.columns or y_value not in df_global.columns:
				inputs_valid = False

			else: #all inputs valid
				col_list = [x_value, y_value]
				df= df_global[col_list]
				df_full = df.dropna()


				col_type_list = list()
				col_type_list.append(df_full[y_value].dtype)

				if(col_type_list[0] != 'int64' and col_type_list[0] != 'float64') :
					y_axis_numeric = False

				else: #y_axis data is numeric
					
					n_rows= df_full.shape[0]
					data_dict = dict()

					for row in range(0,n_rows):

						if df_full.iloc[row][x_value] in data_dict.keys():

							data_dict[df_full.iloc[row][x_value]].append(df_full.iloc[row][y_value])

						else:
							data_dict[df_full.iloc[row][x_value]]= list()
							data_dict[df_full.iloc[row][x_value]].append(df_full.iloc[row][y_value])

					data_range_area = list()

					for each in data_dict:
						sub_list= list()
						sub_list.append(each)
						sub_list.append(min(data_dict[each]))
						sub_list.append(max(data_dict[each]))

						data_range_area.append(sub_list)


					if df_full[x_value].dtype == 'int64' or df_full[x_value].dtype == 'float64':
						data_range_area.sort(key=lambda x: x[0])

					#pdb.set_trace()




	#pdb.set_trace();
	d= {'x_or_y_missing':x_or_y_missing,
	'repeated_variables':repeated_variables,
	'inputs_valid':inputs_valid,
	'y_axis_numeric':y_axis_numeric,
	'data_range_area': data_range_area}
	return jsonify (**d)

#_________________________________________________________________________________________

@app.route('/bivariate_simple_heat_map/')
def simple_heat_map():

	x_value = request.args.get("x_value", default = None, type=str)
	y_value = request.args.get('y_value', default = None, type=str)

	x_or_y_missing = False
	repeated_variables = False
	inputs_valid = True
	simple_heat_map_data = None
	x_categories = None
	y_categories = None
	x_too_large = False
	y_too_large = False


	if x_value == '' or y_value == '':
		x_or_y_missing = True

	else: #both are not empty

		if x_value == y_value:
			repeated_variables = True

		else:#no repeated variables

			if x_value not in df_global.columns or y_value not in df_global.columns:
				inputs_valid = False

			else: #all inputs valid

				col_list = [x_value, y_value]
				df= df_global[col_list]
				df_full = df.dropna()


				x_categories = list(set(list(df_full[x_value])))
				y_categories = list(set(list(df_full[y_value])))

				#pdb.set_trace()
				if len (x_categories) > 51:
					x_too_large = True

				else:
					if len (y_categories) > 51:
						y_too_large = True

					else: #neither x nor y is too large
						#if x_categories.dtype == 'int64' or x_categories.dtype == 'float64':
						
						if pandas.Series(x_categories).dtype == 'float64' or pandas.Series(x_categories).dtype == 'int64':
							x_categories.sort()
						if pandas.Series(y_categories).dtype == 'float64' or pandas.Series(y_categories).dtype == 'int64':
							y_categories.sort()

						n_rows = df_full.shape[0]
						init_data_dict = dict()

						for row in range(0, n_rows):

							x_val = df_full.iloc[row][x_value]
							x_index = x_categories.index(x_val)

							y_val = df_full.iloc[row][y_value]
							y_index = y_categories.index(y_val)

							
							index_pair = (x_index,y_index)

							if index_pair in init_data_dict:
								init_data_dict[index_pair] +=1

							else: 
								init_data_dict[index_pair]=1

						simple_heat_map_data = list()
						for each in init_data_dict:
							sub_list= list()

							sub_list.append(each[0])
							sub_list.append(each[1])
							sub_list.append(init_data_dict[each])

							simple_heat_map_data.append(sub_list)



	d={'x_or_y_missing':x_or_y_missing,
	'repeated_variables':repeated_variables,
	'inputs_valid':inputs_valid,
	'data_simple_heat_map':simple_heat_map_data,
	'x_too_large':x_too_large,
	'y_too_large':y_too_large,
	'x_categories':x_categories,
	'y_categories':y_categories}

	return jsonify(**d)
#--------------------------------------------------------------
@app.route('/bivariate_percent_bars/')
def percent_bars():

	x_value = request.args.get("x_value", default = None, type=str)
	y_value = request.args.get('y_value', default = None, type=str)

	x_or_y_missing= False
	repeated_variables = False


	if x_value == '' or y_value == '':
		x_or_y_missing = True

	else: #both are not empty
		if x_value == y_value:
			repeated_variables = True

		else:#no repeated variables

			if x_value not in df_global.columns or y_value not in df_global.columns:
				inputs_valid = False

			else: #all inputs valid

				col_list = [x_value, y_value]
				df= df_global[col_list]
				df_full = df.dropna()

				x_categories = list(set(list(df_full[x_value])))

				n_rows = df_full.shape[0]

				points_list 
				for row in range(0, n_rows):
					pass
				




	d= {}

	return jsonify(**d)



#---------------------------------------------------------------------
 
if __name__ == '__main__':
	app.debug = True
	app.run()








