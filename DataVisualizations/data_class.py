plottype_list = list()

class Data(object):

	def __init__(self, variable_list,unique_plottypes,number_of_variables):
		self.number_of_variables = number_of_variables
		self.unique_plottypes = unique_plottypes

		if len(unique_plottypes) == 1 and 'bar' in unique_plottypes:
			self.all_plot_types = 'bars_only'
		elif (len(unique_plottypes) == 1 and 'continuous' in unique_plottypes):
			self.all_plot_types = 'continuous_only'
		else:
			self.all_plot_types = 'mixed'