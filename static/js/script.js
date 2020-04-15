$(document).ready(function () {
    $("#myForm").on('submit', function (event) {

        $.ajax({
            data: {
                start: $('#pac-input').val(),
                end: $('#pac-input2').val()
            },
            type: 'POST',
            url: '/'
        })
            .done(function (data) {
                if (data.error) {
                    alert(data.error);

                } else {
                    drawPath(data.data);
                }
            });
        event.preventDefault();
    });

    $('#getDatabaseBtn').on('click', function (event) {
        $.ajax({
            type: 'GET',
            url: '/graphdata'
        })
            .done(function (data) {
                drawDatabasePath(data);
            });
        event.preventDefault();
    });

    //Whenever the user start typing for the first or the second it'll start show options
    $('#pac-input').keydown(function () {
        addListAtt(this.id);
    });
    $('#pac-input2').keydown(function () {
        addListAtt(this.id);
    });

});


let map;
let current_path;
let database_paths;

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

function drawDatabasePath(data) {

    let paths = data['paths'];
    // remove any path
    if (current_path) {
        current_path.setMap(null);
        current_path = null
    }
    if (database_paths) {
        database_paths.forEach(e => {
            e.setMap(null)
        });
        database_paths = null
    }

    const mapColors = {
        "walking": "#6495ED",
        "bus": "#ed896b",
        "train": "#52ff32"
    };

    database_paths = paths.map(e => {
        let color = mapColors[e.pop()];
        let path = e.map(ee => new google.maps.LatLng(ee[0], ee[1]));
        return new google.maps.Polyline({
            clickable: true,
            geodesic: true,
            path: path,
            strokeColor: color,
            strokeOpacity: 1.000000,
            strokeWeight: 10
        });
    });

    let bounds = new google.maps.LatLngBounds(
        data.bounds['southwest'], data.bounds['northeast']);
    map.fitBounds(bounds);

    database_paths.forEach(e => {
        e.setMap(map)
    });
}

loader = document.getElementById("loader");

function hideLoader() {
    loader.style.display = "none";
}

function addListAtt(id) {
    $('#' + id).attr('list', 'locations');
}
