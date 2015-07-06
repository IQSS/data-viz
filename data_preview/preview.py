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
	data_scatter_continuous = None
	all_plot_types = None
	difference_domains_multibar = None
	difference_domains_stackedarea = None
	difference_domains_barline = None
	warning_multibar = None
	warning_stackedarea = None
	warning_barline = None
	line_data = None



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
		list_of_max_min_lists = list()
		all_max_mins = list()
		for var in variable_list:
			metadata_variable_series = metadata_all[var]
			metadata_variable = pandas.DataFrame(metadata_variable_series)
			plotx_list = metadata_variable.ix['plotx',0]
			max_min_list = [int(max(plotx_list)), int(min(plotx_list))]
			list_of_max_min_lists.append(max_min_list)
			all_max_mins.append(int(max(plotx_list)))
			all_max_mins.append(int(min(plotx_list)))

		abs_max = max(all_max_mins)
		abs_min = min(all_max_mins)
		abs_range = set(range(abs_min,abs_max+1))
		abs_length =  len(abs_range)

		for each in list_of_max_min_lists:
			each_range = set(range(min(each), max(each)+1))
			abs_range = abs_range & each_range

		common_length = len(abs_range)
		difference_domains_stackedarea = 100*(1-(common_length/abs_length))




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

			if min(all_xvalues) not in plotx_list:
				plotx_list.append(min(all_xvalues))
				ploty_list.append(0)

			if max(all_xvalues) not in plotx_list:
				plotx_list.append(max(all_xvalues))
				ploty_list.append(0)

			# for each_x in all_xvalues:
			# 	if each_x not in xval_list:
			# 		plotx_list.append(each_x)
			# 		ploty_list.append(0)

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

#creating data for the list/bar chart
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ bar/line
		
		#pdb.set_trace()
		data_barline = list()
		all_xvalues = list()
		all_yvalues = list()
		for var in variable_list:
			is_bar = False
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
				

				for each in plotvalues_dict:
					all_xvalues.append(plotvalues_dict[each])
					all_yvalues.append(each)

			else: #if variable is continuous
				

				barline_plotx_list = metadata_variable.ix['plotx',0]
				barline_ploty_list = metadata_variable.ix['ploty',0]
				length = len(barline_plotx_list)

				for each in range(0, length):
		
					all_xvalues.append(barline_plotx_list[each])
					all_yvalues.append(barline_ploty_list[each])

		all_xvalues = list(set(all_xvalues))



		for var in variable_list:

			xvalues_list = list()
			yvalues_list = list()
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
				

				for each in plotvalues_dict:
					xvalues_list.append(plotvalues_dict[each])
					yvalues_list.append(each)

				is_bar = True

			else: #if variable is continuous
				
				barline_plotx_list = metadata_variable.ix['plotx',0]
				barline_ploty_list = metadata_variable.ix['ploty',0]
				length = len(barline_plotx_list)

				for each in range(0, length):

					xvalues_list.append(barline_plotx_list[each])
					yvalues_list.append(barline_ploty_list[each])

			for each_x in all_xvalues:
				if each_x not in xvalues_list:
					xvalues_list.append(each_x)
					yvalues_list.append(None)

			xy = zip(xvalues_list,yvalues_list)
			xy.sort()
			length_xy = len(xy)

			sub_data = dict()

			if is_bar:
				sub_data["bar"] = 'true'
			sub_data['key'] = var
			sub_data['values'] = list()
			for each in range(0,length_xy):
				sub_list = list()
				sub_list.append(xy[each][0])
				sub_list.append(xy[each][1])

				sub_data['values'].append(sub_list)

			data_barline.append(sub_data)

		
		list_of_max_min_lists = list()
		all_max_mins = list()
		for var in variable_list:
			metadata_variable_series = metadata_all[var]
			metadata_variable = pandas.DataFrame(metadata_variable_series)

			is_plottype = metadata_variable.index == "plottype"
			plottype_df = metadata_variable[is_plottype]
			barline_plottype = str(plottype_df.ix[0,0])

			if barline_plottype == 'bar':

				is_plotvalues = metadata_variable.index == "plotvalues"
				plotvalues_df = metadata_variable[is_plotvalues]
				plotvalues_unicode = plotvalues_df.ix[0,0]
				plotvalues_dict = dict(plotvalues_unicode)
				

				for each in plotvalues_dict:
					xvalues_list.append(plotvalues_dict[each])
				
				all_max_mins.append(int(max(xvalues_list)))
				all_max_mins.append(int(min(xvalues_list)))


			else:

				plotx_list = metadata_variable.ix['plotx',0]
				max_min_list = [int(max(plotx_list)), int(min(plotx_list))]
				list_of_max_min_lists.append(max_min_list)
				all_max_mins.append(int(max(plotx_list)))
				all_max_mins.append(int(min(plotx_list)))

		abs_max = max(all_max_mins)
		abs_min = min(all_max_mins)
		abs_range = set(range(abs_min,abs_max+1))
		abs_length =  len(abs_range)

		for each in list_of_max_min_lists:
			each_range = set(range(min(each), max(each)+1))
			abs_range = abs_range & each_range

		common_length = len(abs_range)
		difference_domains_barline = 100*(1-(common_length/abs_length))













#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ bar/line

		

#-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- mixed

	#pdb.set_trace()
	
	metadata_html = metadata_variable.to_html(header = False)

	header = '<h3>' + new_variable + ' summary stats</h3>'
	#add the bootsrap table classes
	start = metadata_html.find('class="')
	stop = metadata_html.find(">")
	metadata_html= header + metadata_html[:start] + 'class = "table-condensed table-striped>"' + '<thead><tr class = "metadata_header"><th>Summary Metric</th><th>Value</th></tr></thead>'+ metadata_html[stop+1:] 
	
#___________________________________________________________________________________________

	metadata_modals = str()

	for var in variable_list:
		metadata_variable_series = metadata_all[var]
		metadata_variable = pandas.DataFrame(metadata_variable_series)
		var_html = metadata_variable.to_html(header = False)

		metadata_modals += '<button type="button" class="btn btn-primary sumstats_modals" data-toggle="modal" data-target=".' + var + '_sumstats' +'"><strong>' +var + '</strong> summary stats' + '</button><div class="modal fade ' +var + '_sumstats' + '" tabindex="-1" role="dialog"><div class="modal-dialog modal-sm"><div class="modal-content">'+var_html+'</div></div></div>'



#___________________________________________________________________________________________

#___________________________________________________________________________________________
# warning messages 
	if difference_domains_multibar != None and difference_domains_multibar > 30.:
		warning_multibar = '<div class="alert alert-warning alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button><strong>Warning:</strong> chart created but may be misleading. <strong>'+ str(difference_domains_multibar) + "%</strong> of the selected variables's domains to do not intersect. Please be cautious before inferring any relationship between these variables.</div><hr>"

	if difference_domains_stackedarea != None and difference_domains_stackedarea >30.:

		warning_stackedarea = '<div class="alert alert-warning alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button><strong>Warning:</strong> chart created but may be misleading. <strong>'+ str(difference_domains_stackedarea) + "%</strong> of the selected variables's domains to do not overlap. Please be cautious before inferring any relationship between these variables.</div><hr>"

	if difference_domains_barline != None and difference_domains_barline > 30.:
		warning_barline = '<div class="alert alert-warning alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button><strong>Warning:</strong> chart created but may be misleading. <strong>'+ str(difference_domains_barline) + "%</strong> of the selected variables's domains to do not intersect. Please be cautious before inferring any relationship between these variables.</div><hr>"
#___________________________________________________________________________________________



#here we will construct the data json objects, compatible with specific graph types. 
#___________________________________________________________________________________________
	data_json_multibar = json.dumps(data_multibar)
	data_json_stackedarea= json.dumps(data_stackedarea)
	data_json_pie = json.dumps(data_pie)
	data_json_barline = json.dumps(data_barline)
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
	    'data_json_barline' : data_json_barline,
	    'data_json_scatter_continuous': data_json_scatter_continuous,
	    'data_json_line': data_json_line,
	    'metadata_modals': metadata_modals,
	    'warning_multibar':warning_multibar,
	    'warning_stackedarea': warning_stackedarea,
	    'warning_barline' : warning_barline}

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








