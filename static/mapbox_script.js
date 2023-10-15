
mapboxgl.accessToken = 'pk.eyJ1IjoiamluYXNoIiwiYSI6ImNsbnFzODNmeTBsbHEya28xYzE2OGU5cTMifQ.Ih41FVVHRlj1OivWpjBMPg';


var map = new mapboxgl.Map({
    container: 'map', 
    style: 'mapbox://styles/mapbox/streets-v11', 
    center: [-84.3880, 33.7490], 
    zoom: 10, 
});

var marker = new mapboxgl.Marker()
    .setLngLat([-84.3880, 33.7490]) 
    .addTo(map);
