var map;
let directionsService, directionsRenderer;
let currentLocationMarker;

function initMap() {
	var Marker;
	const initial_location = { lat: 35.689, lng: 139.692 };

	/*現在地更新を5000秒ごとに繰り返す*/
	// setInterval(updateCurrentLocation, 5000);

	map = new google.maps.Map(document.getElementById("map"), {
		zoom: 17,
		center: initial_location,
	});

	/*交通情報*/
	const trafficLayer = new google.maps.TrafficLayer();
	trafficLayer.setMap(map);

	//検索結果を左のタブに表示
	directionsService = new google.maps.DirectionsService();
	directionsRenderer = new google.maps.DirectionsRenderer({
		map: map,
		panel: document.getElementById("content-tab"),
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
				//document.getElementById("start").value = "現在地" ;
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
	// Remove existing marker if any
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
	// If the marker doesn't exist, create it
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
	var maxWidth = 936; // パネルの最大幅
	var maxHeight = 400; // パネルの最大高さ
  
	var newWidth = startWidth + (e.clientX - startX);
	var newHeight = startHeight + (e.clientY - startY);
  
	// 新しい幅と高さが最小値と最大値の範囲内にあることを確認
	newWidth = Math.max(Math.min(newWidth, maxWidth), minWidth);
	newHeight = Math.max(Math.min(newHeight, maxHeight), minHeight);
  
	directionsPanel.style.width = newWidth + 'px';
	directionsPanel.style.height = newHeight + 'px';
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