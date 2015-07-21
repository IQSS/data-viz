//this is when I started to kill the dreaded barline

var fileid = {fileid};
first_time = true;
active = false;




$(document).ready(function(){

  $(function () {
  $('[data-toggle="popover"]').popover()
});


// set up what's needed to accumulate varaible names in the hidden input
  VARIABLE_LIST_DELIMITER = '||';


$(function(){

//BY DEFAULT, I WANT ALL THE BUTTONS TO BE HIDDEN. 
$('#multi_bar').hide();
$('#stacked_area').hide();
$('#pie_chart').hide();
$('#json_popup').hide();
$('#warning').show();
$('#scatter_plot_continuous').hide();
$('#line').hide();
$('hr').hide();
$("#scatter_controls").hide();
$('#range_area_controls').hide();
$('#simple_heat_map_controls').hide();
$('#stacked_percent_controls').hide();
$('#stacked_count_controls').hide();
$("#basic_bar_controls").hide();
$('#simple_area_controls').hide();



//turn varaible clicking capability on
$('.variable').on();



// Here we create the hidden input field, which stores the highlightd varaibles
//___________________________________________________________________________________________
    $('.variable').on('click',function(){

      
      active = true;
      var new_variable = $(this).attr('id');

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


      var variable_list_string = $('#variable-list').val();
      // alert(variable_list_string);
      
      //___________________________________________________________________________________________






 $.getJSON('http://127.0.0.1:5000/summary_stats/',{new_variable: $(this).attr('id'), variable_list_string: variable_list_string},function(data){
        // $('#sum_stats_preview').html(data.metadata_html);

       
        

      



// bars only~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ bars only
  if (data.all_plot_types == 'bars_only'){

    if(first_time == true){

            $("#multi_bar").show();
            $('#pie_chart').show();


           

            


  // Some graphs need there to be only one variable. 
    if (data.number_of_variables == 1){
        $('#pie_chart').on('click', function(){
            $('#multi_bar').hide();
            $('#stacked_area').hide();
            $('#pie_chart').hide();
            $('hr').show();

            $('#sum_stats_preview').html(data.metadata_modals_buttons);
            $("#modal_content_div").html(data.metadata_modals_content);
            $('#sum_stats_preview').fadeIn();


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

    }else{
     
      $('#pie_chart').hide();

      $('#json_popup').hide()
    }






//If the user selects the 'multi-bar' option on his/her first pick:
//-  -  -  -  --  -  -  -  --  -  -  -  --  -  -  -  --  -  -  -  --  -  -  -  --  -  -  -  -
        $('#multi_bar').on('click', function(){
          $('svg').empty();
          $('#multi_bar').hide();
          $('#stacked_area').hide();
          $('#pie_chart').hide();
          $('#json_popup').fadeIn()
          $('hr').show();
          $('#sum_stats_preview').fadeIn();

          $('#sum_stats_preview').html(data.metadata_modals_buttons);
          $("#modal_content_div").html(data.metadata_modals_content);
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


        
        // must set this variable tho indicate what to do 
        //when "first_time" == false.




        });
    }//end of the "first_time == true" statement"


//I know this isn't the user's firt time around, but I need to 
//access the "selected_graph" variable to remember what variable the user picked the first
// time around. 
    else{ 
      if(selected_graph === "#multi_bar"){

        $('#sum_stats_preview').html(data.metadata_modals_buttons);
        $("#modal_content_div").html(data.metadata_modals_content);
        $('#warning').empty();
        $('#warning').html(data.warning_multibar);

                  $('#json_popup').click(function popup(){
                  var generator=window.open('','name','height=300,width=400');

                  generator.document.write('<!DOCTYPE html><html>')
                  generator.document.write(data.data_json_multibar);
                  generator.document.write('</html>');
                  generator.document.close();
                });



        $(function(){ 
          $('#multi_bar').hide();
          $('#stacked_area').hide();
          $('#pie_chart').hide();
        var chart = nv.models.multiBarChart().stacked(true).showControls(true);

        chart.yAxis
        .tickFormat(d3.format(',.1f'));
        chart.reduceXTicks(false);
        chart.showLegend(true);
        chart.stacked(false);
        d3.select('#chart svg').datum(
        JSON.parse(data.data_json_multibar)

        ).transition().duration(500).call(chart);
        nv.utils.windowResize(chart.update);

        });
      };


    }; 
        
  } //close "if data.all_plot_types == bars"
// bars only~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ bars only

// continuous only --------^--------^--------^--------^--------^--------^--------^--------^--------^ continuous only
    else if (data.all_plot_types == "continuous_only"){ // only continuous

      if(data.number_of_variables == 1){

        $('#stacked_area').show();
        $('#stacked_area').on('click', function(){

          $('#scatter_plot_continuous').hide();

          $('#sum_stats_preview').html(data.metadata_modals_buttons);
          $("#modal_content_div").html(data.metadata_modals_content);
          $('#sum_stats_preview').fadeIn();
          $('#line').hide();
          $('hr').show();


                    $('#json_popup').fadeIn();
                    $('#json_popup').click(function popup(){
                    var generator=window.open('','name','height=300,width=400');

                    generator.document.write('<!DOCTYPE html><html>')
                    generator.document.write(data.data_json_stackedarea);
                    generator.document.write('</html>');
                    generator.document.close();
                  });

              $('#multi_bar').hide();
              $('#stacked_area').hide();
              $('#pie_chart').hide();

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


            });




      }else{

        $('#stacked_area').hide();
      }



        if(first_time == true){
//alert('got to the firsttime statement');
          $('#multi_bar').show();
          $('#scatter_plot_continuous').show();
          $('#line').show();



// scatter_continuous (first_time) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^scatter_continuous (first_time)

      $('#scatter_plot_continuous').on('click', function(){
                  $('svg').empty();
                  $('#multi_bar').hide();
                  $('#scatter_plot_continuous').hide();
                  $('#pie_chart').hide()
                  $('#stacked_area').hide();
                  $('#line').hide();
                  $('hr').show();




                $('#sum_stats_preview').html(data.metadata_modals_buttons);
                $("#modal_content_div").html(data.metadata_modals_content);
                $('#sum_stats_preview').fadeIn();

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

                    first_time = false;
                  
                  selected_graph = "#scatter_plot_continuous";
              });
// scatter_continuous (first_time) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^scatter_continuous (first_time)







// continuous multibar (first_time) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ continuous multibar(first_time)

      $('#multi_bar').on('click', function(){
        $('svg').empty();
        $('#sum_stats_preview').html(data.metadata_modals_buttons);
        $("#modal_content_div").html(data.metadata_modals_content);
        $('#sum_stats_preview').fadeIn();

        $('#scatter_plot_continuous').hide();
        $('#stacked_area').hide();
        $('hr').show();


            $('#json_popup').fadeIn();
                  $('#json_popup').click(function popup(){
              var generator=window.open('','name','height=300,width=400');

              generator.document.write('<!DOCTYPE html><html>')
              generator.document.write(data.data_json_multibar);
              generator.document.write('</html>');
              generator.document.close();
            });



          first_time = false;
          selected_graph = '#multi_bar';

            $('#multi_bar').hide();
            $('#pie_chart').hide();
            $('#line').hide();



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



      });

// continuous multibar (first_time) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ continuous multibar(first_time)

//line chart (first_time) ============================================== line chart (first_time) 

      $('#line').on('click', function(){

        $('svg').empty();
        $('#sum_stats_preview').html(data.metadata_modals_buttons);
        $("#modal_content_div").html(data.metadata_modals_content);
        $('#sum_stats_preview').fadeIn();
        $('#scatter_plot_continuous').hide();
        $('#stacked_area').hide();
        $('hr').show();


            $('#json_popup').fadeIn();
                  $('#json_popup').click(function popup(){
              var generator=window.open('','name','height=300,width=400');

              generator.document.write('<!DOCTYPE html><html>')
              generator.document.write(data.data_json_line);
              generator.document.write('</html>');
              generator.document.close();
            });



          first_time = false;
          selected_graph = '#line';

            $('#multi_bar').hide();
            $('#pie_chart').hide();
            $('#line').hide();

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
//line chart (first_time) ============================================== line chart (first_time) 


        }//end (if first_time == true)


  else{ //first_time == false


//scatterplot_continuous (first_time = false) -------------- scatterplot_continuous (first_time = false)

        if(selected_graph == "#scatter_plot_continuous"){
                $('#stacked_area').hide();
                $('#sum_stats_preview').html(data.metadata_modals_buttons);
                $("#modal_content_div").html(data.metadata_modals_content);

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


            }
//scatterplot_continuous (first_time = false) -------------- scatterplot_continuous (first_time = false)


//continuous multibar (first_time = false) ~~~~~~~~~~~~~~~~~~~~~ continuous multibar (first_time = false)

         else if (selected_graph === '#multi_bar'){

          $('#sum_stats_preview').html(data.metadata_modals_buttons);
          $("#modal_content_div").html(data.metadata_modals_content);
          $('#stacked_area').hide();

            $('#json_popup').fadeIn();
                  $('#json_popup').click(function popup(){
              var generator=window.open('','name','height=300,width=400');

              generator.document.write('<!DOCTYPE html><html>')
              generator.document.write(data.data_json_stackedarea);
              generator.document.write('</html>');
              generator.document.close();
            });


         

              $(function(){
                 nv.addGraph(function() {


                    var chart = nv.models.multiBarChart();
                    

                    chart.xAxis
                        .tickFormat(d3.format(',f'));
                        

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


                      });


          }

//continuous multibar (first_time = false) ~~~~~~~~~~~~~~~~~~~~~ continuous multibar (first_time = false)

//line (firsttime = false) _____________-----_____________-----_____________----line (firsttime = false)

          else if (selected_graph === '#line'){

              $('#sum_stats_preview').html(data.metadata_modals_buttons);
              $("#modal_content_div").html(data.metadata_modals_content);
              $('#stacked_area').hide();
              $('#scatter_plot_continuous').hide();
              $('hr').show();


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



          }

//line (firsttime = false) _____________-----_____________-----_____________----line (firsttime = false)


      }// end (else{}, as in first_time = false;)
      
  }//end "else if (data.all_plots == continuous)"
// continuous only --------^--------^--------^--------^--------^--------^--------^--------^--------^ continuous only



// mixed types _________---------_________---------_________---------_________---------_________--- mixed types
        else{
          $('.chart_button').hide();
        }
// mixed types _________---------_________---------_________---------_________---------_________--- mixed types


      });
      return false;
    });
    });
    });


// $(function(){
  
// $(".reset").on('click', function() {location.reload();
//       });
// });