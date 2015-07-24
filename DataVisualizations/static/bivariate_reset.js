$(document).ready(function(){
	$('.reset_bivariate').on('click',function(){
		$("#container").empty();
		$('.highcharts-container').html('');
		$('.form-control').val('');
	})
})