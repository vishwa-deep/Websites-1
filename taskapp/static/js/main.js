$(document).ready(function(){


    $('form').on('submit', function() {

        console.log("the form has beeen submitted");


        var valueOne = $('input[name="task"]').val();
        console.log(valueOne);

        $.ajax({
            type: "POST",
            url: "/addTask/",
            data : { task: valueOne },
            success: function(results) {
                var task_obj_len = results.tasks.length;
                var del_task = "/delete_task/"+results.tasks[task_obj_len-1].task_id+'/';
                $('#results').append('<div class="well in-task"><p class="the-task">'+results.tasks[task_obj_len-1].task+'</p>&nbsp;&nbsp;'+
                '<a name="'+results.tasks[task_obj_len-1].task_id+'" href="'+del_task+'"><span class="glyphicon glyphicon-remove-circle"></span></a>&nbsp;&nbsp;</div>');
                $('input').val('');

            },
            error: function(error) {
              console.log(error)
            }
        });

    });

/*

    $('a').on('click', function(){
        var link_id = $(this).attr('name');
        console.log(link_id);

        $.ajax({
            type: 'GET',
            url: '/delete_task/' + link_id + '/',
            success: function(del_results){
                console.log(del_results);
                var output = '';
                for(var i = 0; i < del_results.tasks.length; i++){
                    console.log(del_results.tasks[i].task);
                    var del_task = "/delete_task/"+del_results.tasks[i].task_id+'/';
                    output += '<div class="well in-task"><p class="the-task">'+del_results.tasks[i].task+'</p>&nbsp;&nbsp;'+
                        '<a name="'+del_results.tasks[i].task_id+'" onclick="return false;" href="'+del_task+'"><span class="glyphicon glyphicon-remove-circle"></span></a>&nbsp;&nbsp;</div>';
                    console.log(del_results.tasks[i].task);
                }
                //console.log(output);
                $('#results').html(output);
            },
            error: function(error){
                console.log(error);
            }
        });
    });
*/


});