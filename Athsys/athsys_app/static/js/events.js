function listevents(){
    $.ajax({
        url: "/event_get/",
        type: "post",
        data: $('#buscador').serialize(),
        dataType: "json",
        success: function(response){
            console.log(response);
            $('#content-table').empty();
            if(response.length>0){
                $.each(response, function(index, dates) {
                    $('#content-table').append('<tr><td>Login</td><td>'+dates.timestamp+'</td></tr>');
                });
            }else{
                $('#content-table').append('<tr><td colspan=2>No Results</td></tr>');
            }
            
        },
        error: function(error){
            console.log(error);
        }
    })
}