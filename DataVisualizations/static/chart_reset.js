$(document).ready(function(){

	$('.reset').on('click',function(){

		$('#variable-list').attr('value', '');
		first_time = true
		selected_graph = null

		$('.variable').css('background-color', 'rgb(240, 248, 270)');
		$('#chart svg').empty();
		$('#multi_bar').hide();
		$('#stacked_area').hide();
		$('#pie_chart').hide();
		$('#line').hide();
		$('#scatter_plot_continuous').hide();
		$('hr').hide();
		$('#json_popup').hide();
		$('#sum_stats_preview').empty();
		$('#multi_bar_continuous').hide();
		$('#button_row').show();

		return
		return
	});

	$('[title = "Select Chart"]').on('click', function(){

		$('#button_row').show();
				$.getJSON('http://127.0.0.1:5000/data_info/', {new_variable: new_variable, variable_list_string:variable_list_string}, function(data){

			all_plot_types = data.all_plot_types;
			number_of_variables = data.number_of_variables;
			varialble_list = data.varialble_list;

			if (all_plot_types == 'bars_only'){

				$("#multi_bar").show();
				$('#pie_chart').show();

				$('#stacked_area').hide();
				$('#multi_bar_continuous').hide();
				$('#scatter_plot_continuous').hide();
				$('#line').hide();
				$('#no_mixed').hide();
			}
			else if(all_plot_types == 'continuous_only'){
				$('#stacked_area').show();
				$('#multi_bar_continuous').show();
				$('#scatter_plot_continuous').show();
				$('#line').show();

				$("#multi_bar").hide();
				$('#pie_chart').hide();
				$('#no_mixed').hide();


			}
			else{
				$('.chart_button').hide();
				$('#chart').prepend("<div id='no_mixed' class= 'alert alert-warning alert-dismissible'> <button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button>Sorry, no preview charts for mixed variable types available. Please view the summary stats and pick varaibles of plot-type 'bar' or 'continuous'.</div>");
			}

			if(number_of_variables != 1){
				$('#pie_chart').hide();
				$('#stacked_area').hide();
			}

		});
	});
});