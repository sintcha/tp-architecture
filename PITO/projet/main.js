$(function (){

    var $booked = $('#booked');
    var $booking = $('#booking');
    var $flightList = $('#flightList')
    var $mailInput = $('#mail')
    var $mailRegInput = $('#regmail')
    var $name = $('#name')
    var $nation = $('#nation')
    var $dateInput = $('#date')

    $('#login').on('click',function() {

        $.ajax({
            type: 'GET',
            url: "http://127.0.0.1:5000/clients/" + $mailInput.val(),
            success: function(clients) {
                $.each(clients, function(i, client){
                    $.each(client.tickets, function(i, ticket){
                        $booked.append('<li>' + ticket.code +'<br>'+ ticket.date +'<br>'+ ticket.departure_airport_code +'<br>'+ ticket.arrival_airport_code +'<br>'+ '</li><br>');
                    });
                });
            },
            error: function() {
                alert('error loading tickets');
            }
        });
    });

    $('#register').on('click',function() {
        $.ajax({
            type: 'POST',
            url: "http://127.0.0.1:5000/clients/add",
            data : {
                name: $name.val(),
                mail: $mailRegInput.val(),
                nationality: $nation.val()
            }
        });
    });

    $.ajax({
        type: 'GET',
        url: "http://127.0.0.1:5000/tickets",
        success: function(tickets) {
            $.each(tickets, function(i, ticket){
                $flightList.append('<option>' + ticket.code + '</option>');
            });
        },
        error: function() {
            alert('error loading tickets');
        }
    });
    
    $.ajax({
        type: 'GET',
        url: "https://app-air-travel.azurewebsites.net/flights",
        success: function(tickets) {
            $.each(tickets, function(i, ticket){
                $flightList.append('<option>' + ticket.code + '</option>');
            });
        },
        error: function() {
            alert('error loading tickets');
        }
    });
    
    $('#flightList').on('change', function() {
        if($flightList.val().startsWith("AR")){
            $.ajax({
                type: 'GET',
                url: "http://127.0.0.1:5000/tickets/code/" + $flightList.val(),
                success: function(tickets) {
                    $.each(tickets, function(i, ticket){
                        $booking.empty();
                        $booking.append('<li>' + ticket.code +'<br>'+ ticket.date +'<br>'+ ticket.departure_airport_code +'<br>'+ ticket.arrival_airport_code +'<br>'+ '</li><br>');
                    });
                },
                error: function() {
                    alert('error loading tickets');
                }
            });
        }else if($flightList.val().startsWith("AF")){
            $.ajax({
                type: 'GET',
                url: "https://app-air-travel.azurewebsites.net/flights",
                success: function(tickets) {
                    $.each(tickets, function(i, ticket){
                        if(ticket.code==$flightList.val()){
                            $booking.empty();
                            $booking.append('<li>' + ticket.code +'<br>'+ ticket.departure +'<br>'+ ticket.arrival +'<br>'+ '</li><br>');
                        }
                    });
                },
                error: function() {
                    alert('error loading tickets');
                }
            });
        }
    });

    $('#date').on('change', function() {
        datestr="";
        datestr = datestr.concat($dateInput.val().toString().substr(8,9),"-",
                                 $dateInput.val().toString().substr(5,6).substr(0,2),"-",
                                 $dateInput.val().toString().substr(0,4));
        $booking.empty();
        $.ajax({
            type: 'GET',
            url: "http://127.0.0.1:5000/tickets/date/" + datestr,
            success: function(tickets) {
                $.each(tickets, function(i, ticket){
                    $booking.append('<li>' + ticket.code +'<br>'+ ticket.departure_airport_code +'<br>'+ ticket.arrival_airport_code +'<br>'+ '</li><br>');
                });
            }
        });
        
        $.ajax({
            type: 'GET',
            url: "https://app-air-travel.azurewebsites.net/flights/" + datestr,
            success: function(tickets) {
                $.each(tickets, function(i, ticket){
                    $booking.append('<li>' + ticket.flight.code +'<br>'+ ticket.flight.departure +'<br>'+ ticket.flight.arrival +'<br>'+ '</li><br>');
                });
            }
        });
    });
        

    $('#test').on('click',function() {
        console.log($dateInput.val().toString());
        datestr="";
        datestr = datestr.concat($dateInput.val().toString().substr(8,9),"-",
                                 $dateInput.val().toString().substr(5,6).substr(0,2),"-",
                                 $dateInput.val().toString().substr(0,4));
        console.log(datestr)
    });
});
