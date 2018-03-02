ymaps.ready(initMap);

function initMap() {
    var myMap = new ymaps.Map("map", {
            center: [44.62, 33.52],
            zoom: 12
        }, {
            searchControlProvider: 'yandex#search'
        });

    myMap.geoObjects
        .add(new ymaps.Placemark([44.61410128, 33.52392752], {
            balloonContent: '<strong>Место:</strong> СОШ №265<br>' +
            '<strong>Дата и время:</strong> 20 марта 2018 года в 18:00 <br>' +
            '<strong>Мест осталось:</strong> 20/25 <br>' +
            '<a href="google.com">Перейти на страницу мероприятия</a>'
        }, {
            preset: 'islands#greenDotIconWithCaption',
            iconColor: '#735184'
        }));

    myMap.geoObjects
        .add(new ymaps.Placemark([44.60420179, 33.51472217], {
            balloonContent: '<strong>Место:</strong> СОШ №265<br>' +
            '<strong>Дата и время:</strong> 20 марта 2018 года в 18:00 <br>' +
            '<strong>Мест осталось:</strong> 20/25 <br>' +
            '<a href="google.com">Перейти на страницу мероприятия</a>'
        }, {
            preset: 'islands#greenDotIconWithCaption',
            iconColor: '#56844a'
        }));

    myMap.geoObjects
        .add(new ymaps.Placemark([44.59085137, 33.53995977], {
            balloonContent: '<strong>Место:</strong> СОШ №265<br>' +
            '<strong>Дата и время:</strong> 20 марта 2018 года в 18:00 <br>' +
            '<strong>Мест осталось:</strong> 20/25 <br>' +
            '<a href="google.com">Перейти на страницу мероприятия</a>'
        }, {
            preset: 'islands#greenDotIconWithCaption',
            iconColor: '#295e84'
        }));
}
