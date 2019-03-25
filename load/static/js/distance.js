var origin = document.getElementById('origin').value;
var destination = document.getElementById('destination').value;
var price = document.getElementById('price');
var directionsService = new google.maps.DirectionsService();

function calc_distance() {
    var request = {
            origin: document.getElementById("origin").value,
            destination: document.getElementById("destination").value,
            travelMode: google.maps.TravelMode.DRIVING,
            unitSystem: google.maps.UnitSystem.IMPERIAL,
    }

    directionsService.route(request, function (result, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            distance = result.routes[0].legs[0].distance.text.slice(0,-3).replace(",",".");
            price.value = distance * 150 / 100
        }
        else{
            alert("Can't find road! Please try again!");
        }
    });
}

/*function calculate_price() {
    distance = calc_distance().replace(",",".");
    return 1.5 * distance;
}

function change_price() {
    price.value = calculate_price()
}*/