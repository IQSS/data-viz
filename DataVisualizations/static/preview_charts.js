first_time = true; 
active = false;

$(document).ready(function(){

	$(function () {
		$('[data-toggle="popover"').popover();
	});

	//by default, we want the buttons, modals, warnings, etc hidden until relevant. 
	$('#multi_bar').hide();
	$('#stacked_area').hide();
	$('#pie_chart').hide();
	$('#json_popup').hide();
	$('#warning').show();
	$('#scatter_plot_continuous').hide();
	$('#line').hide();
	$('#multi_bar_continuous').hide();
	$('hr').hide();
	$("#scatter_controls").hide();
	$('#range_area_controls').hide();
	$('#simple_heat_map_controls').hide();
	$('#stacked_percent_controls').hide();
	$('#stacked_count_controls').hide();
	$("#basic_bar_controls").hide();
	$('#simple_area_controls').hide();
	$('#simple_line_controls').hide();


	$('.variable').on('click',function(){

		active = true
		new_variable = $(this).attr('id');
		VARIABLE_LIST_DELIMITER = '||';

		function update_variable_list(new_var_name){	
			variable_list_string = $('#variable-list').val();
			if (variable_list_string == ''){
	            variable_array = [];  // new array
	        }else{            
	            variable_array = variable_list_string.split(VARIABLE_LIST_DELIMITER);            
	        }

	       // Do we have this new varialble in the hidden input already? 
	       link_obj = $('p[id="' + new_var_name  + '"]');
	        
	        if ($.inArray(new_var_name, variable_array ) > -1){ // YES, we have it
	            // remove item
	            variable_array.splice($.inArray(new_var_name, variable_array),1);
	            link_obj.css('background-color', 'rgb(240, 248, 270)') //blue – unselected

	        }else{  // NO - add it to array
	            variable_array.push(new_var_name);             
	            link_obj.css('background-color', "rgba(250, 128, 114, 0.5)");
	        }


	      

	      // Save it to hidden input
	        variable_list_string = variable_array.join(VARIABLE_LIST_DELIMITER);
	        $('#variable-list').val(variable_list_string);


		}
		update_variable_list(new_variable);
		variable_list_sting = $('#variable-list').val();


	
		

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

		if (first_time == true){

			//begin chart making for the first time on button click

			$('#multi_bar').on('click',function(){

				$('.chart_button').hide();
				$('hr').show();
				$('#json_popup').fadeIn()
				$('#sum_stats_preview').fadeIn();
				$('svg').empty();


				$.getJSON('http://127.0.0.1:5000/multi_bar/', function(data){

					$('#warning').html(data.warning_multibar);
					
					$('#json_popup').click(function popup(){
		              var generator=window.open('','name','height=300,width=400');

		              generator.document.write('<!DOCTYPE html><html>')
		              generator.document.write(data.data_json_multibar);
		              generator.document.write('</html>');
		              generator.document.close();
		            });

		            var chart = nv.models.multiBarChart().stacked(true).showControls(true);

			        chart.xAxis
			          .tickFormat(d3.format(',f'));

			        chart.yAxis
			        .tickFormat(d3.format(',.1f'));

			        chart.reduceXTicks(false);
			        chart.showLegend(true);
			        chart.stacked(false);
			        

			        d3.select('#chart svg').datum(
			        JSON.parse(data.data_json_multibar)

			        ).transition().duration(500).call(chart);
			        nv.utils.windowResize(chart.update);



			        first_time = false;
			        selected_graph = "#multi_bar";


				});

				$.getJSON('http://127.0.0.1:5000/metadata_modals/', function(data){

					$('#sum_stats_preview').html(data.metadata_modals_buttons);
					$("#modal_content_div").html(data.metadata_modals_content);
				});

				

			});

			$('#pie_chart').on('click',function(){

				$('svg').empty();
				$('.chart_button').hide();
				$('hr').show();
				$('#json_popup').fadeIn()
				$('#sum_stats_preview').fadeIn();

				$.getJSON('http://127.0.0.1:5000/pie_chart/',function(data){

					$('#json_popup').fadeIn();
		            $('#json_popup').click(function popup(){
		            var generator=window.open('','name','height=300,width=400');

		            generator.document.write('<!DOCTYPE html><html>')
		            generator.document.write(data.data_json_pie);
		            generator.document.write('</html>');
		            generator.document.close();
		          });

		            nv.addGraph(function() {
		              var chart = nv.models.pieChart()
		                  .x(function(d) { return d.label })
		                  .y(function(d) { return d.value })
		                  .showLabels(true);

		                  chart.pie.pieLabelsOutside(false).labelType("percent");


		                d3.select("#chart svg")
		                    .datum(
		                      JSON.parse(data.data_json_pie))
		                  .transition().duration(1200)
		                    .call(chart);

		              return chart;
		            });

				});

				$.getJSON('http://127.0.0.1:5000/metadata_modals/', function(data){

					$('#sum_stats_preview').html(data.metadata_modals_buttons);
					$("#modal_content_div").html(data.metadata_modals_content);
				});

			});
			
			$('#stacked_area').on('click', function(){

				$('.chart_button').hide();
				$('hr').show();
				$('#json_popup').fadeIn()
				$('#sum_stats_preview').fadeIn();
				$('svg').empty();

				$.getJSON('http://127.0.0.1:5000/stacked_area/',function(data){

					$('#json_popup').fadeIn();
                    $('#json_popup').click(function popup(){
                    var generator=window.open('','name','height=300,width=400');

                    generator.document.write('<!DOCTYPE html><html>')
                    generator.document.write(data.data_json_stackedarea);
                    generator.document.write('</html>');
                    generator.document.close();
                  });

                    nv.addGraph(function() {
		              var chart = nv.models.stackedAreaChart()
		                  .x(function(d) { return d[0] })
		                  .y(function(d) { return d[1] })
		                  .clipEdge(true)
		                  .showControls(false)
		                  .useInteractiveGuideline(false);

		                  chart.xAxis
		                      .showMaxMin(false);
		                      

		                  chart.yAxis
		                      .tickFormat(d3.format(',.2f'));

		                  d3.select('#chart svg')
		                    .datum(JSON.parse(data.data_json_stackedarea))
		                    .transition().duration(500).call(chart);

		                  nv.utils.windowResize(chart.update);
		                        
		                return chart;
		              });
                    first_time =false;

				});
				
				$.getJSON('http://127.0.0.1:5000/metadata_modals/', function(data){

					$('#sum_stats_preview').html(data.metadata_modals_buttons);
					$("#modal_content_div").html(data.metadata_modals_content);
				});

			});
			
			$('#scatter_plot_continuous').on('click',function(){

				$('.chart_button').hide();
				$('hr').show();
				$('#json_popup').fadeIn()
				$('#sum_stats_preview').fadeIn();
				$('svg').empty();

				$.getJSON('http://127.0.0.1:5000/scatter_plot_continuous/',function(data){

					$('#json_popup').fadeIn();
                  	$('#json_popup').click(function popup(){
                      var generator=window.open('','name','height=300,width=400');

                      generator.document.write('<!DOCTYPE html><html>')
                      generator.document.write(data.data_json_scatter_continuous);
                      generator.document.write('</html>');
                      generator.document.close();
                    });

                    nv.addGraph(function() {
                          var chart = nv.models.scatterChart()
                                        .showDistX(true)
                                        .showDistY(true)
                                      .sizeRange([50, 200])
                                        .color(d3.scale.category10().range());

                          chart.xAxis.tickFormat(d3.format('.02f'));
                          chart.yAxis.tickFormat(d3.format('.02f'));

                          d3.select('#chart svg')
                              .datum(JSON.parse(data.data_json_scatter_continuous))
                            .transition().duration(500)
                              .call(chart);

                          nv.utils.windowResize(chart.update);

                          return chart;
                        });

				});	
				$.getJSON('http://127.0.0.1:5000/metadata_modals/', function(data){

					$('#sum_stats_preview').html(data.metadata_modals_buttons);
					$("#modal_content_div").html(data.metadata_modals_content);
				});
				first_time = false;
				selected_graph = '#scatter_plot_continuous';		

			});

			$('#multi_bar_continuous').on('click',function(){

				$('.chart_button').hide();
				$('hr').show();
				$('#json_popup').fadeIn()
				$('#sum_stats_preview').fadeIn();
				$('svg').empty();

				$.getJSON('http://127.0.0.1:5000/multibar_continuous/', function(data){

					$('#json_popup').fadeIn();
                 	$('#json_popup').click(function popup(){
		              var generator=window.open('','name','height=300,width=400');

		              generator.document.write('<!DOCTYPE html><html>')
		              generator.document.write(data.data_json_multibar);
		              generator.document.write('</html>');
		              generator.document.close();
		            });

                 	nv.addGraph(function() {

			            var chart = nv.models.multiBarChart();
			            
			            chart.xAxis
			                .tickFormat(d3.format(',f'));
			                
			            chart.reduceXTicks(true);

			            chart.yAxis
			                .tickFormat(d3.format(',.1f'));


			            d3.select('#chart svg')
			                .datum(JSON.parse(data.data_json_multibar))
			                .transition().duration(500)
			                .call(chart)
			                ;

			            nv.utils.windowResize(chart.update);
			            return chart;
			        });
			        first_time = false
			        selected_graph = '#multi_bar_continuous'

				});
				$.getJSON('http://127.0.0.1:5000/metadata_modals/', function(data){

					$('#sum_stats_preview').html(data.metadata_modals_buttons);
					$("#modal_content_div").html(data.metadata_modals_content);
				});
				first_time = false;
			});

			$('#line').on('click',function(){

				$('.chart_button').hide();
				$('hr').show();
				$('#json_popup').fadeIn()
				$('#sum_stats_preview').fadeIn();
				$('svg').empty();

				$.getJSON('http://127.0.0.1:5000/continuous_line/', function(data){

					$('#json_popup').fadeIn();
                 	$('#json_popup').click(function popup(){
		              var generator=window.open('','name','height=300,width=400');

		              generator.document.write('<!DOCTYPE html><html>')
		              generator.document.write(data.data_json_line);
		              generator.document.write('</html>');
		              generator.document.close();
		            });

		            nv.addGraph(function() {
		                var chart = nv.models.lineWithFocusChart();

		                chart.xAxis
		                  .tickFormat(d3.format(',f'));

		                chart.yAxis
		                  .tickFormat(d3.format(',.2f'));

		                chart.y2Axis
		                  .tickFormat(d3.format(',.2f'));

		                d3.select('#chart svg')
		                  .datum(JSON.parse(data.data_json_line))
		                  .transition().duration(500)
		                  .call(chart)
		                  ;

		                nv.utils.windowResize(chart.update);

		                return chart;
		              });

				});
				$.getJSON('http://127.0.0.1:5000/metadata_modals/', function(data){

					$('#sum_stats_preview').html(data.metadata_modals_buttons);
					$("#modal_content_div").html(data.metadata_modals_content);
				});

				first_time = false;
				selected_graph = '#line'
				

			});
			

		}//end first_time = true
		else{
			if (selected_graph == '#multi_bar'){
				$('#multi_bar').click();
				$('#button_row').hide();
			}
			else if (selected_graph == '#scatter_plot_continuous'){
				$("#scatter_plot_continuous").click();
				$('#button_row').hide();
			}
			else if (selected_graph == "#multi_bar_continuous"){
				$('#multi_bar_continuous').click();
				$('#button_row').hide();
			}
			else if (selected_graph == '#line'){
				$("#line").click();
				$('#button_row').hide();
			}
		}


	});


});