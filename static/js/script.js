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
                    if (Array.isArray(data.data))
                        current_data = data.data.slice(0, 12);
                    else
                        current_data = [data.data];

                    drawPaths(current_data);
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
let polylines = [];
let database_paths;
let current_data;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {
            lat: 3.128401,
            lng: 101.650695
        },
        zoom: 13
    });

    let options = document.getElementById("options");
    let route = document.getElementById("route");
    let routes = $("#routes");
    routes.hide();

    map.controls[google.maps.ControlPosition.TOP_CENTER].push(options);
    map.controls[google.maps.ControlPosition.LEFT_TOP].push(route);
}

function convert_time_t_hours_minutes_string(time) {
    let hours = Math.floor(time / 60 / 60);
    let mins = Math.floor(time / 60) % 60;

    let s = "";
    if (hours > 0) {
        s += `${hours} h`;
        s += ' '
    }
    if (mins < 10 && mins >= 0)
        s += '0';
    s += `${mins} min`;

    return s;
}

function drawPaths(paths) {

    let routes = $("#routes");

    $('#routes > *').remove();

    for (let i = 0; i < paths.length; i++) {
        routes.append(`<div class="col-sm-1 mt-1"><button class="btn btn-sm btn-outline-dark w-100 h-100" onclick="select_path(${i}, this)">` +
            `${convert_time_t_hours_minutes_string(paths[i]['time'])}</button></div>`);
    }

    if (paths.length > 0) {
        select_path(0); // TODO: add object
    }
}

function select_path(i, object) {
    // we are in the current range
    if (i < current_data.length) {
        // reset to all primary
        $('#routes > * > *').removeClass("active");

        $(object).addClass('active');
        drawPath(current_data[i]);
    }
}


function drawPath(data) {
    // if points are null or undefined
    let points = data.path;
    if (!points)
        return;

    let maps_coords = points.map(e => new google.maps.LatLng(e[0], e[1]));

    var trans = [];
    for (const mode in data.directions) {
        trans[mode] = data.directions[mode][1];
    }

    const mapColors = {
        "Walking": "#6495ED",
        "Bus": "#ed896b",
        "Train": "#52ff32",
        "Car": "#8a42f5"
    };

    // removing the old path from the map
    if (polylines)
        for (let i = 0; i < polylines.length; i++) {
            polylines[i].setMap(null);
        }

    // delete database
    if (database_paths) {
        database_paths.forEach(e => {
            e.setMap(null)
        });
        database_paths = null
    }

    for (let i = 0; i < maps_coords.length - 1; i++) {
        polylines[i] = new google.maps.Polyline({
            clickable: true,
            geodesic: true,
            path: [maps_coords[i], maps_coords[i + 1]],
            strokeColor: mapColors[trans[i + 1]],
            strokeOpacity: 1.000000,
            strokeWeight: 10
        });
        polylines[i].setMap(map);
    }

    let bounds = new google.maps.LatLngBounds(
        data.bounds['southwest'], data.bounds['northeast']);
    map.fitBounds(bounds);


    let distance = data.distance / 1000;

    $('#distance').text(`Distance: ${distance} KM`);
    $('#time').text(`Time: ${convert_time_t_hours_minutes_string(data.time)}`);
    $('#time-distance-card').css("display", "block");

    // remove all children before adding directions
    $('#directions_holder > *').remove();
    data.directions.forEach((point_connection, i) => {
        if (i === 0) {
            $('#directions_holder').append(
                `<li class=\"list-group-item\">Start from <strong>${point_connection[0]}</strong></li>`
            );
        } else {
            $('#directions_holder').append(
                `<li class=\"list-group-item\">Go to <strong>${point_connection[0]}</strong> BY <strong>${point_connection[1]}</strong></li>`
            );
        }
    });
    $('#route').show();
    $("#routes").show();

}

function drawDatabasePath(data) {

    let paths = data['paths'];

    $('#route').hide();
    $("#routes").hide();

    // remove any path
    if (polylines)
        for (let i = 0; i < polylines.length; i++) {
            polylines[i].setMap(null);
        }
    if (database_paths) {
        database_paths.forEach(e => {
            e.setMap(null)
        });
        database_paths = null
    }

    const mapColors = {
        "Walking": "#6495ED",
        "Bus": "#ed896b",
        "Train": "#52ff32",
        "Car": "#8a42f5"
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
