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
});


let map;
let time =5;
let distance =5;


document.getElementById("distance").textContent += " " +distance;
document.getElementById("time").textContent += " " +time;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {
            lat: 3.128401,
            lng: 101.650695
        },
        zoom: 13
    });

    let from = document.getElementById('pac-input');
    let to = document.getElementById('pac-input2');
    let card = document.getElementById("card")

    map.controls[google.maps.ControlPosition.TOP_RIGHT].push(card);

    let start = new google.maps.places.Autocomplete(from);
    let end = new google.maps.places.Autocomplete(to);
}


function drawPath(points) {
    // if points are null or undefined
    if (!points)
        return;
    let maps_coords = points.map(e => new google.maps.LatLng(e[0], e[1]));

    let path = new google.maps.Polyline({
        clickable: true,
        geodesic: true,
        path: maps_coords,
        strokeColor: "#6495ED",
        strokeOpacity: 1.000000,
        strokeWeight: 10
    });

    path.setMap(map);
}

loader = document.getElementById("loader");
function hideLoader() {
	loader.style.display = "none";
}
