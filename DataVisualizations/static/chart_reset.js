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

		return
		return
	});
});