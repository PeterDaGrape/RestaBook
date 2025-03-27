mapboxgl.accessToken = 'pk.eyJ1IjoiYm81NW1hbjEiLCJhIjoiY204cWlhZGszMGxuaTJpc2M2aXd3MjdyNCJ9.0e-jAfXXCvuO_baCZjzrCw';

const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: [-4.2518, 55.8642],  // Default to Glasgow
    zoom: 12
});

// navigation controls
map.addControl(new mapboxgl.NavigationControl());

// Fetch restaurants from Django API and display them
fetch('/api/restaurants/')
    .then(response => response.json())
    .then(data => {
        data.forEach(restaurant => {
            const marker = new mapboxgl.Marker()
                .setLngLat([restaurant.longitude, restaurant.latitude])
                .setPopup(new mapboxgl.Popup().setText(restaurant.name))
                .addTo(map);
        });
    });
