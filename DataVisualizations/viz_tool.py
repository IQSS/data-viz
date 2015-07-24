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
from data_class import Data
from helper_functions import *




# Create the application.
app = flask.Flask(__name__)



#___________________________________________________________________________________________ landpage
#landpage: User inputs tworavens URL
@app.route('/')
def landpage():
	d = {}

	return render_template ('landpage.html', **d)

#___________________________________________________________________________________________ landpage

#------------------------------------------------------------------------------------------- data specific page
@app.route('/<fileid>/')
def preview(fileid):


	download_url = 'http://dataverse.harvard.edu/api/access/datafile/' + str(fileid)
	request = requests.get(download_url)
	d =  request.text


	data_unicode = unicodedata.normalize("NFKD", d).encode("ascii",'ignore')
	data_string = StringIO(data_unicode)
	df = pd.read_table(data_string)

	global df_global
	df_global = df

	
    #create variable names for varaible table
	variables = df.columns   

	total_rows = df.shape[0]
	total_cols = df.shape[1]
   #Create HTML of pandas dataframe
	df.index += 1 
	df_html = df.to_html()
	start = df_html.find('class="dataframe"')
	df_html = df_html[:start] + 'id = "preview_DataTable"' + df_html[start+1:]
	
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


	d = {"data": df_html, 'variables' : variables, 'fileid':str(fileid), 'variable_info_dict':variable_info_dict, 'total_rows':total_rows, 'total_cols':total_cols}

	return render_template('gui2.html', **d)
#------------------------------------------------------------------------------------------- data specific page

@app.route('/data_info/')
def data_info():
	new_variable = request.args.get("new_variable", default = None, type=str)
	variable_list_string = request.args.get("variable_list_string", default = None, type = str)

	global variable_list
	variable_list = variable_list_string.split('||')
	number_of_variables = len(variable_list)

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

	selected_data = Data(variable_list,unique_plottypes,number_of_variables)




	d= {'all_plot_types': selected_data.all_plot_types, 'number_of_variables':selected_data.number_of_variables, 'new_variable':new_variable, 'variable_list':variable_list}
	return jsonify(**d)


# preview graph options -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --  preview graph options


# multi-bar chart __________________________________________________________multi_bar chart
@app.route('/multi_bar/')
def multi_bar():
	warning_multibar = None
	
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

	if difference_domains_multibar != None and difference_domains_multibar > 30.:
		warning_multibar = '<div class="alert alert-warning alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button><strong>Warning:</strong> chart created but may be misleading. <strong>'+ str(difference_domains_multibar) + "%</strong> of the selected variables's domains to do not intersect. Please be cautious before inferring any relationship between these variables.</div>"

	data_json_multibar = json.dumps(data_multibar)

	d = {'data_json_multibar': data_json_multibar, 'warning_multibar':warning_multibar}
	return jsonify(**d)
# multi-bar chart __________________________________________________________multi_bar chart


#pie chart _____^_____^_____^_____^_____^_____^_____^_____^_____^_____^____ pie chart
@app.route('/pie_chart/')
def pie_chart():

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
		data_json_pie = json.dumps(data_pie)
	return jsonify({'data_json_pie': data_json_pie})


#pie chart _____^_____^_____^_____^_____^_____^_____^_____^_____^_____^____ pie chart

# stacked area =========================================================== stacked area

@app.route('/stacked_area/')
def stacked_area():

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
		data_json_stackedarea= json.dumps(data_stackedarea)

		return jsonify({'data_json_stackedarea': data_json_stackedarea})

# stacked area =========================================================== stacked area

#scatter continuous --__------__------__------__------__------__------scatter continuous'
@app.route('/scatter_plot_continuous/')
def scatter():

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

	data_json_scatter_continuous = json.dumps(data_scatter_continuous)

	return jsonify ({'data_json_scatter_continuous': data_json_scatter_continuous})


#scatter continuous --__------__------__------__------__------__------scatter continuous

#multibar continuous --------   --------   --------   --------   ---- multibar coninuous

@app.route('/multibar_continuous/')
def continuous_multibar():
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

	data_json_multibar = json.dumps(data_multibar)

	return jsonify({'data_json_multibar': data_json_multibar})


#multibar continuous --------   --------   --------   --------   ---- multibar coninuous

#density line____+____+____+____+____+____+____+____+____+____+____+____+____+ density line

@app.route('/continuous_line/')
def cont_line():
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
	data_json_line = json.dumps(line_data)

	return jsonify({'data_json_line': data_json_line})

#density line____+____+____+____+____+____+____+____+____+____+____+____+____+ density line



#modal content ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ modal content

@app.route('/metadata_modals/')
def metadata_modals():

	metadata_modals_buttons = '<h4> Selected Variables Metadata</h4>'
	metadata_modals_content=""

	for var in variable_list:
		metadata_variable_series = metadata_all[var]
		metadata_variable = pandas.DataFrame(metadata_variable_series)
		var_html = metadata_variable.to_html(header = False)

		#pdb.set_trace()
		metadata_modals_buttons += '<button type="button" class="btn btn-default sumstats_modals" data-toggle="modal" data-target=".' + var + '_sumstats' +'"><strong>' +var + '</strong> metadata' + '</button>'
		metadata_modals_content += '<div class="modal fade ' +var + '_sumstats' + '" tabindex="-1" role="dialog"><div class="modal-dialog modal-sm"><div class="modal-content">'+ var_html+'</div></div></div>'

	return jsonify({'metadata_modals_buttons': metadata_modals_buttons,
    'metadata_modals_content':metadata_modals_content})

#modal content ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ modal content

# preview graph options -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --  preview graph options



# __--____--____--____--____--____--____--____--____--____--____--____--____--____--____--____--____--____--____--__ end data_preview mode

'''Here begins the data manipulation for the multivariate graphs'''

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
	is_area_chart = request.args.get('is_area_chart', default=None, type=str)


	x_or_y_missing= False
	repeated_variables = False
	x_too_large = False
	y_too_large = False
	y_var_character = False
	series = None
	x_categories = None
	inputs_valid = True


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

				if is_area_chart == 'false':
					if len(x_categories) > 20:
						x_too_large = True

				
				y_categories = list(set(list(df_full[y_value])))
				if len(y_categories) > 20:
					y_too_large = True

				else: # y not too large

					if pandas.Series(y_categories).dtype != 'float64' and pandas.Series(y_categories).dtype != 'int64':
						y_var_character = True
					else:

						if pandas.Series(x_categories).dtype == 'float64' or pandas.Series(x_categories).dtype == 'int64':
							x_categories.sort()


						n_rows = df_full.shape[0]

						points_dict = dict()
						for row in range(0, n_rows):
							point = (df_full.iloc[row][x_value],df_full.iloc[row][y_value])

							if point in points_dict:
								points_dict[point] += 1
							else:
								points_dict[point] = 1

						freq_list = list()
						for i in points_dict:
							freq_list.append({i[1]:[i[0],points_dict[i]]})

						series= list()
						len_categories = len (x_categories)

						
						for i in y_categories:
							series.append({'name':str(i), 'data': [0]*len_categories})

						
						for i in freq_list:
							for each in series:
								key = i.keys()
								key = str(key)
								key = key.replace('[','')
								key = key.replace(']','')
								if each['name'] == key:
									index_x = x_categories.index(i.values()[0][0])
									each['data'][index_x] = i.values()[0][1]



	



	d= {'x_or_y_missing':x_or_y_missing,
	'x_too_large': x_too_large,
	'y_too_large': y_too_large,
	'repeated_variables': repeated_variables,
	'x_categories' : x_categories,
	'series': series,
	'inputs_valid':inputs_valid}

	return jsonify(**d)
#---------------------------------------------------------------------

@app.route('/simple_line/')
def simple_line():

	x_value = request.args.get("x_value", default = None, type=str)
	var_one = request.args.get('var_one', default = None, type=str)
	var_two = request.args.get('var_two', default = None, type=str)
	var_three = request.args.get('var_three', default = None, type=str)
	var_four = request.args.get('var_four', default = None, type=str)


	x_or_y_missing = False
	repeated_variables = False
	inputs_valid = True
	y_vars_numeric = True
	series = None
	x_categories = None


	if x_value == '' or var_one == '':
		x_or_y_missing = True

	else: #check any variables are repeated
		var_list = list()
		for each in [var_one,var_two,var_three,var_four] :
			if each != '':
				var_list.append(each)

		all_var = [x_value]
		for x in var_list:
			all_var.append(x)
		if len(set(all_var)) < len(all_var):
			repeated_variables = True

		if repeated_variables ==False: #all variables different

			for var in all_var:
				if var not in df_global.columns:
					inputs_valid = False
					break
			if inputs_valid == True: #all inputs valid

				df= df_global[all_var]
				df_full = df.dropna()

				y_vars_numeric = all_var_numeric(var_list,df_full)

				if y_vars_numeric == True:
					
					x_categories = list(set(list(df_full[x_value])))
					if pandas.Series(x_categories).dtype == 'int64' or pandas.Series(x_categories).dtype =='float64':
						x_categories.sort()

					n_rows = df_full.shape[0]
					len_x = len(x_categories)

					series= list()
					for var in var_list:

						var_dict = dict()
						var_dict['name']= var
						var_dict['data'] = [0]*len_x

						for row in range(0,n_rows):
							x_val = df_full.iloc[row][x_value]
							y_val = df_full.iloc[row][var]

							x_index = x_categories.index(x_val)
							var_dict['data'][x_index] += y_val

						series.append(var_dict)



	d={'x_or_y_missing':x_or_y_missing, 'y_vars_numeric':y_vars_numeric, 'inputs_valid': inputs_valid, 'x_categories': x_categories, 'series':series, 'repeated_variables':repeated_variables}
	return jsonify (**d)



#---------------------------------------------------------------------
 
if __name__ == '__main__':
	app.debug = True
	app.run()








