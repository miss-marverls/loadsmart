origin = document.getElementById('id_origin_city');
destination = document.getElementById('id_destination_city');
autocomplete_origin = new google.maps.places.Autocomplete(origin);
autocomplete_destination = new google.maps.places.Autocomplete(destination);

var price = document.getElementById('id_shipper_price');
var directionsService = new google.maps.DirectionsService();

function calc_price() {
    var request = {
        origin: origin.value,
        destination: destination.value,
        travelMode: google.maps.TravelMode.DRIVING,
        unitSystem: google.maps.UnitSystem.IMPERIAL,
    }

    directionsService.route(request, function (result, status) {
        if (status == google.maps.DirectionsStatus.OK) {
            distance = result.routes[0].legs[0].distance.value * 0.0006213712;
            price.value = (distance * 1.5).toFixed(2);
        }
    });
}