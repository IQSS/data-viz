$(document).ready(function(){
	$('.reset').on('click',function(){

		alert(first_time);
		$('#variable-list').val('');
		first_time = true


		link_obj.css('background-color', 'rgb(240, 248, 270)');
		$('#chart svg').empty();
		$('#multi_bar').hide();
		$('#stacked_area').hide();
		$('#pie_chart').hide();
		$('#line').hide();
		$('#scatter_plot_continuous').hide();
		$('hr').hide();
		$('#json_popup').hide();
		$('#sum_stats_preview').empty();
	});
});