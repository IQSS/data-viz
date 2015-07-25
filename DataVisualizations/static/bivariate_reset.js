
function bind_reset_bivariate(){
	$('.reset_bivariate').unbind('click');
	$('.reset_bivariate').on('click',function(){
		$("#container").html('');
		$('.form-control').val('');
	});
}