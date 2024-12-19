function initMap(elem, latlng, zoom) {
  const map = L.map(elem).setView(latlng, zoom)

  L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: '© <a href="https://www.mapbox.com/about/maps/">Mapbox</a> © <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> <strong><a href="https://www.mapbox.com/map-feedback/" target="_blank">Improve this map</a></strong>',
    tileSize: 512,
    maxZoom: 18,
    id: 'mapbox.streets',
    zoomOffset: -1,
    id: 'mapbox/streets-v11',
    accessToken: 'pk.eyJ1IjoidGVycmFwZXV0ZXMiLCJhIjoiY2p0N3IxZjRhMDB5bDQ1cW52Z2s2MnVnNCJ9.Ism1OhdYA3qPFom2htkx8w'
  }).addTo(map)
  return map
}
