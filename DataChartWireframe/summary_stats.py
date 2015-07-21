

class SummaryStats(object):

    def __init__(self, args):

        # initialized, to be defined later
        #
        self.data_multibar = None
        self.data_stackedarea = None
        self.data_pie = None
        self.data_scatter_continuous = None
        self.all_plot_types = None
        self.difference_domains_multibar = None
        self.warning_multibar = None
        self.warning_stackedarea = None
        self.line_data = None

        # first to be initialized
        self.new_variable = None
        self.variable_list_string = None
        self.number_of_variables = None

        self.unique_plottypes = None

        # err msgs
        self.error_found = False
        self.err_msg = None

        self.calculate_stats(args)

    def add_error(self, msg):
        self.error_found = True
        self.err_msg = msg


    def calculate_stats(self, args):

        if args is None:
            self.add_error("No args found")
            return

        self.new_variable = request.args.get("new_variable", default = None, type=str)
        self.variable_list_string = request.args.get("variable_list_string", default = None, type = str)
        self.variable_list = variable_list_string.split('||')
        self.number_of_variables = len(variable_list)

        # Load plot types
        if not self.load_plot_types():
            return

        # Make plots
        self.make_plots()

    def load_plot_types(self):

        plottype_list = list()

        for var in self.variable_list:

            metadata_variable_series = metadata_all[var]
            metadata_variable = pandas.DataFrame(metadata_variable_series)

            is_plottype = metadata_variable.index == "plottype"
            plottype_df = metadata_variable[is_plottype]
            plottype = str(plottype_df.ix[0,0])

            #adding each plottype to the 'plottype' list:
            plottype_list.append(plottype)

        #create a list with all the UNIQUE plottypes:
    	self.unique_plottypes = list(set(plottype_list))

        if len(self.unique_plottypes == 0):
            self.add_error("Sorry!  No plots found (WTF)")
            return False

        return True

    def make_plots(self):

        if len(unique_plottypes) == 1:
            if 'bar' in unique_plottypes:
                self.make_bar_plot()


    def make_bar_plot(self):
        pass


    def get_dict_for_web(self):
        return self.__dict__
        """
        d = {}
        for k, v in self.__dict__.items():
            d[k] = v
        return d
        """

if __name__=='__main__':
    args = None
    s = SummaryStats(args)
    if s.error_found:
        print 'Error found!'
        print s.err_msg

    print s.get_dict_for_web()
