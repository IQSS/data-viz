function switch_to_preview(){
	$('.switch_preview_mode').on('click',function(){


			$('#chart').html('<svg></svg>');
			$('.switch').remove();
			$('.chart_options').prepend('<button type="button" class="btn btn-sm btn-default switch switch_bivariate" id="btnAddItem"  title="Bivariate Mode"><span class="glyphicon glyphicon-transfer" style="color:#818181;"></span> Switch To Plot Mode</button>');
			//$('.reset_bivariate').addClass('reset').removeClass('reset_bivariate');
			$('[title="Select Chart"]').show();
			$('.variable').css('cursor','');
			$('.variable').draggable( 'disable' )
			
			$('#scatter_controls').fadeOut();
			$('#range_area_controls').fadeOut();
			$('#simple_heat_map_controls').fadeOut();
			$('#stacked_percent_controls').fadeOut();
			$('#stacked_count_controls').fadeOut();
			$('#basic_bar_controls').fadeOut();
			$('#simple_area_controls').fadeOut();
			$("#simple_line_controls").fadeOut();

			$('#right_panel_title').html('Data Tools');





	})
}