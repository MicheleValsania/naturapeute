const SWITZERLAND_CENTER = [46.8182, 8.2275]
const SWITZERLAND_BOUNDS = [[45.818, 5.000], [47.808, 10.000]]
const DEFAULT_ZOOM = 8

function initMap(elem) {
    const map = L.map(elem, {
        center: SWITZERLAND_CENTER,
        zoom: DEFAULT_ZOOM,
        maxBounds: SWITZERLAND_BOUNDS,
        minZoom: 7,
        maxZoom: 18
    })

    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: '© <a href="https://www.mapbox.com/about/maps/">Mapbox</a> © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> <strong><a href="https://www.mapbox.com/map-feedback/" target="_blank">Improve this map</a></strong>',
        tileSize: 512,
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        zoomOffset: -1,
        accessToken: 'pk.eyJ1IjoidGVycmFwZXV0ZXMiLCJhIjoiY2p0N3IxZjRhMDB5bDQ1cW52Z2s2MnVnNCJ9.Ism1OhdYA3qPFom2htkx8w'
    }).addTo(map)

    return map
}

