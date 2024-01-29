var map;
let directionsService;
let directionsRendererStartToShare;
let directionsRendererShareToShare;
let directionsRendererShareToEnd;

let currentLocationMarker;
let geocoder;
let waypoints = [];

//マップ情報
function initMap() {
  var Marker;
  const initial_location = { lat: 35.689, lng: 139.692 };

  /*現在地更新を5000秒ごとに繰り返す*/
  /*setInterval(updateCurrentLocation, 5000);*/

  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 13,
    center: initial_location,
  });

  /*交通情報*/
  const trafficLayer = new google.maps.TrafficLayer();
  trafficLayer.setMap(map);

	/*ジオコードインスタンス化*/
	geocoder = new google.maps.Geocoder();

  // 赤色を指定
  var polylineOptionsRed = {
    strokeColor: '#FF0000',
    strokeOpacity: 1.0,
    strokeWeight: 6 // 線の太さを6ピクセルに設定
	};

  //検索結果を左のタブに表示するためのインスタンス化
  directionsService = new google.maps.DirectionsService();
  directionsRendererStartToShare = new google.maps.DirectionsRenderer({
    map: map,
    panel: document.getElementById("content-tab"),
    polylineOptions : polylineOptionsRed
  });

  directionsRendererShareToShare = new google.maps.DirectionsRenderer({
    map: map,
    panel: document.getElementById("content-tab"),
  });

  directionsRendererShareToEnd = new google.maps.DirectionsRenderer({
    map: map,
    panel: document.getElementById("content-tab"),
    polylineOptions: polylineOptionsRed
	});

  //ジオコーディング
  function geocode(){  var geocoder = new google.maps.Geocoder();
    geocoder.geocode({ 'location': Marker.getPosition()},
      function(results, status) {
    if (status == google.maps.GeocoderStatus.OK && results[0]){
      document.getElementById('id_address').innerHTML =
          results[0].formatted_address.replace(/^日本, /, '');
    }else{
      document.getElementById('id_address').innerHTML =
        "Geocode 取得に失敗しました";
      alert("Geocode 取得に失敗しました reason: "
            + status);
    }
    });
  }

  //DBからwaypointsのデータを取得してマーカーを表示させる関数

  fetch('/gt/api/map_cars')
    .then(response => response.json())
    .then(data => {
        waypoints = data.map(waypoint => ({
            ...JSON.parse(waypoint.json_data),
            name: waypoint.name,
						address : waypoint.address
        }));
        addMarkers(map, waypoints);
    })
    .catch(error => {
        console.error('Error fetching waypoints:', error);
    });

  //waypoints全てにマーカーと情報ウィンドウを追加
  // ウェイポイントデータでマーカーと情報ウィンドウを追加する関数
  function addMarkers(map,waypoints) {
    waypoints.forEach(function(waypoint) {
        var marker = new google.maps.Marker({
            position: {lat: waypoint.lat, lng: waypoint.lng},
            map: map,
            title: waypoint.name,
            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                fillColor: 'Blue',
                fillOpacity: 0.8,
                scale: 8,
                strokeColor: 'white',
                strokeWeight: 2
            }
        });
				// アドレス情報を含む情報ウィンドウをマーカーに追加
				var infoWindow = new google.maps.InfoWindow({
          content: '<div><strong>' + waypoint.name + '</strong><br>' +
                  'Address: ' + waypoint.address + '</div>'
        });

        marker.addListener('click', function() {
            infoWindow.open(map, marker);
        });
    });
  }
}

/*現在地を出発地に指定*/
function getCurrentLocation() {
	if (navigator.geolocation) {
		navigator.geolocation.getCurrentPosition(
			(position) => {
				const currentLocation = {
					lat: position.coords.latitude,
					lng: position.coords.longitude,
				};

				// Set center and add marker
				map.setCenter(currentLocation);
				addCurrentLocationMarker(currentLocation);

				// Set the start input value
				document.getElementById("start").value = currentLocation.lat + ", " + currentLocation.lng;
			},
			() => {
				console.error("Error getting current location");
			}
		);
	} else {
		console.error("Geolocation is not supported by this browser");
	}
}

/*現在地に常時ピン差し一回目*/
function addCurrentLocationMarker(location) {
	if (currentLocationMarker) {
		currentLocationMarker.setMap(null);
	}

	// Add marker
	currentLocationMarker = new google.maps.Marker({
		position: location,
		map: map,
		title: "Current Location",
		icon: {
			path: google.maps.SymbolPath.CIRCLE,
			scale: 10,
			fillColor: "#4285F4",
			fillOpacity: 1,
			strokeColor: "#ffffff",
			strokeWeight: 2,
		},
	});
}

/*現在地を取得しマーカーを置く(2回目以降)*/
function updateCurrentLocationMarker(location) {
	if (!currentLocationMarker) {
		currentLocationMarker = new google.maps.Marker({
			map: map,
			title: "Current Location",
			icon: {
				path: google.maps.SymbolPath.CIRCLE,
				scale: 10,
				fillColor: "#4285F4",
				fillOpacity: 1,
				strokeColor: "#ffffff",
				strokeWeight: 2,
			},
		});
	}

	/*更新された現在地をマーカーにセットする*/
	currentLocationMarker.setPosition(location);

	/*地図の中央地を更新された現在地に変更する*/
	map.setCenter(location);
}

	/*リアルタイムで現在地を取得する*/
	function updateCurrentLocation() {
		if (navigator.geolocation) {
			navigator.geolocation.getCurrentPosition(
				(position) => {
					const currentLocation = {
						lat: position.coords.latitude,
						lng: position.coords.longitude,
					};
					/* 現在地のピンを打つ*/
					updateCurrentLocationMarker(currentLocation);
				},
				() => {
					console.error("Error getting current location");
				}
			);
		} else {
			console.error("Geolocation is not supported by this browser");
		}
	}

	window.onload = function() {
		initMap();
};

function expandPanel() {
	var panel = document.getElementById('directions-panel');
	panel.style.display = 'block'; // パネルを表示する
	panel.classList.add('expanded');
  }

// リサイズハンドルのイベントリスナーを設定
var resizeHandle = document.getElementById('resize-handle');
var startWidth, startHeight, startX, startY; // 初期サイズとマウス座標を保存する変数

resizeHandle.addEventListener('mousedown', function(e) {
  e.preventDefault();

  var directionsPanel = document.getElementById('directions-panel');
  // clientHeightを使用して初期の高さを取得する
  startWidth = directionsPanel.clientWidth;
  startHeight = directionsPanel.clientHeight;
  startX = e.clientX;
  startY = e.clientY;

  // リサイズ中はmax-heightスタイルを一時的に無効化する
  directionsPanel.style.maxHeight = 'none';

  window.addEventListener('mousemove', resizePanel);
  window.addEventListener('mouseup', stopResizing);
});

function resizePanel(e) {
  var directionsPanel = document.getElementById('directions-panel');
  var minWidth = 50; // パネルの最小幅
  var minHeight = 100; // パネルの最小高さ

  var newWidth = startWidth + (e.clientX - startX);
  var newHeight = startHeight + (e.clientY - startY);
  newHeight = Math.max(newHeight, minHeight);
  directionsPanel.style.height = newHeight + 'px';
  newWidth = Math.max(newWidth, minWidth);

  directionsPanel.style.width = newWidth + 'px';
}
// ウィンドウリサイズ時にパネルの幅を調整するイベントリスナー
window.addEventListener('resize', function() {
	var directionsPanel = document.getElementById('directions-panel');
	if (window.innerWidth <= 1000) {
	  // 画面幅が1000px以下の場合は幅を100%に設定
	  directionsPanel.style.width = '100%';
	} else {
	  // 画面幅が1000px以上の場合は、リサイズによって設定された幅を保持する
	  // 現在設定されている幅が100%でなければ、それを保持する
	  if (directionsPanel.style.width !== '100%') {
		directionsPanel.style.width = directionsPanel.style.width;
	  }
	}
  });
function stopResizing() {
  var directionsPanel = document.getElementById('directions-panel');
  window.removeEventListener('mousemove', resizePanel);
  window.removeEventListener('mouseup', stopResizing);
  // リサイズが終了したら、max-heightを再設定する
  directionsPanel.style.maxHeight = '';
}

/*電車かそれ否かを分ける関数*/
function trainTF(){
	if (!directionsService || !map || !geocoder) {
		console.error("Google Maps services are not initialized.");
		return;
	}
		calculateAndDisplayRoute(directionsService, directionsRendererStartToShare, directionsRendererShareToShare, directionsRendererShareToEnd, geocoder, waypoints);
}

/*住所から緯度経度に変換*/
function geocodeAddress(geocoder, address) {
	return new Promise((resolve, reject) => {
		geocoder.geocode({'address': address}, (results, status) => {
			if (status === 'OK') {
				resolve(results[0].geometry.location);
			} else {
				reject(new Error('住所のジオコーディングに失敗しました。理由: ' + status));
			}
		});
	});
}

// 最も近い中継地点を見つける関数
function findNearestWaypoint(location, waypoints) {
	let nearestWaypoint = null;
	let minDist = Infinity;

	waypoints.forEach(waypoint => {
		const dist = google.maps.geometry.spherical.computeDistanceBetween(
			location, new google.maps.LatLng(waypoint.lat, waypoint.lng));
		if (dist < minDist) {
			nearestWaypoint = waypoint;
			minDist = dist;
		}
	});

	if (!nearestWaypoint) {
		throw new Error('最寄りの中継地点が見つかりませんでした。位置情報が正しいか確認して、再試行してください。');
	}
	return nearestWaypoint;
}

/*検索結果をinnerHTMLで記載*/
function showRouteInformation(response) {
	const directionsPanel = document.getElementById("details-tab");
	directionsPanel.innerHTML = "";

	for (let i = 0; i < response.routes.length; i++) {
		const route = response.routes[i];

		const summary = document.createElement("div");
		summary.innerHTML = `<b>${route.summary}</b>`;
		directionsPanel.appendChild(summary);

		const steps = route.legs[0].steps;
		for (let j = 0; j < steps.length; j++) {
			const stepInfo = document.createElement("div");
			const stepLatLng = steps[j].end_location;
			stepInfo.innerHTML = `<a href="#" onclick="placeMarker(${stepLatLng.lat()}, ${stepLatLng.lng()});">${steps[j].instructions}</a>`;
			directionsPanel.appendChild(stepInfo);
		}
	}
}

function placeMarker(lat, lng) {
    const location = new google.maps.LatLng(lat, lng);
    new google.maps.Marker({
        position: location,
        map: map
    });

    // オプションで地図の中心を移動させる
    map.setCenter(location);
}
