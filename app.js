function getGpsData() {
  $.get('http://10.0.0.238/get_csv', {
    delimiter: 'semicolon',
    fields: 'Time;GPS_Latitude;GPS_Longitude', 
	mode: 'no-cors'
  }).done(function(data) {
    const gpsData = data.split(';');
    const latitude = gpsData[1];
    const longitude = gpsData[2];
    const message = `Latitude: ${latitude}<br>Longitude: ${longitude}`;
    $('#gps-data').html(message);
  }).fail(function() {
    console.error('Failed to fetch GPS data from Phyphox.');
  });
}