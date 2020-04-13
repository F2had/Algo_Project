$(document).ready(function() {
    $("#myForm").on('submit', function(event) {

        $.ajax({
                data: {
                    start: $('#pac-input').val(),
                    end: $('#pac-input2').val()
                },
                type: 'POST',
                url: '/'
            })
            .done(function(data) {
                if (data.error) {
                    alert(data.error);

                } else {
                    drawPath(data.data);
                }
            });
        event.preventDefault();
    });

    writeLocations();
    //Whenever the user start typing for the first or the second it'll start show options
    $('#pac-input').keydown(function(){addListAtt(this.id);});
    $('#pac-input2').keydown(function(){addListAtt(this.id);});

});


let map;
let current_path;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {
            lat: 3.128401,
            lng: 101.650695
        },
        zoom: 13
    });

    let card = document.getElementById("time-distance-card");

    map.controls[google.maps.ControlPosition.LEFT_TOP].push(card);

}


function drawPath(data) {
    // if points are null or undefined
    let points = data.path;
    if (!points)
        return;
    let maps_coords = points.map(e => new google.maps.LatLng(e[0], e[1]));

    // removing the old path from the map
    if (current_path)
        current_path.setMap(null);

    current_path = new google.maps.Polyline({
        clickable: true,
        geodesic: true,
        path: maps_coords,
        strokeColor: "#6495ED",
        strokeOpacity: 1.000000,
        strokeWeight: 10
    });

    let bounds = new google.maps.LatLngBounds(
        data.bounds['southwest'], data.bounds['northeast']);
    map.fitBounds(bounds);

    current_path.setMap(map);

    let time = data.time;
    let distance = data.distance;

    $('#distance').text(`Distance: ${distance}`);
    $('#time').text(`Time: ${time}`);
    $('#time-distance-card').css("display", "block");
}

loader = document.getElementById("loader");

function hideLoader() {
    loader.style.display = "none";
}

// Write locations to the data-list for the autocomplete.
function writeLocations(loca) {
//        FIXME
// replace list the the actual locations list
        let loc = ['Pantai Hill Park', 'Pantai Panorama', 'UM Central', 'KK8', 'KK12'];
        let option = '';
        for (let i = 0; i < loc.length; i++) {
            option += '"<option value="' + loc[i] + '"></option>';
        }
        $("#locations").html(option);

    }
// When called add the list attribute with value locations
function addListAtt(id){
    $('#'+id).attr('list', 'locations');
}
