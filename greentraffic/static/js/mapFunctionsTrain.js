
var map;
let directionsService, directionsRenderer;
let currentLocationMarker;

//マップ情報
function initMap() {
  var Marker;
  const initial_location = { lat: 35.689, lng: 139.692 };

  /*現在地更新を5000秒ごとに繰り返す*/
  /*setInterval(updateCurrentLocation, 5000);*/

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

/*上記までがinitMap()*/

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

/*電車かそれ否かを分ける関数*/
function trainTF(){
  clearMapData();
  if (!map) {
    console.error("Map object is not initialized yet.");
    return;
  }
  /*fetchRouteAndDisplayOnMap();*/
	let coordinates = extractCoordinates(routeData);
   	displayRouteOnMap(coordinates, map);
   	displayRouteInfo(routeData);
   	expandPanel();
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

function displayRouteInfo(routeData) {
	const contentTab = document.getElementById("content-tab");
	contentTab.innerHTML = "";


	// 経路詳細を表示
	const summary = document.createElement("div");
	contentTab.appendChild(summary);
	routeData.NorikaeBizApiResult.body.route[0].path.forEach(segment => {
		const segmentInfo = document.createElement("div");

		segmentInfo.innerHTML += `<p class="segment-title segment-info">出発駅: ${segment.from}</p>`;
		segmentInfo.innerHTML += `<i class="fas fa-arrow-down"></i>`;
		segmentInfo.innerHTML += `<p class="segment-title segment-info">到着駅: ${segment.to}</p>`;
		segmentInfo.innerHTML += `<p class="segment-info">${segment.rosen} ${segment.lineType}(${segment.lineIndex}) 線</p>`;
		segmentInfo.innerHTML += `<p class="segment-info">所要時間: ${segment.jikan}分</p>`;
		segmentInfo.innerHTML += `<p class="segment-info">距離: ${segment.kyori}km</p>`;
		segmentInfo.innerHTML += `<p class="segment-info">乗車区分: ${segment.seatKubun.num}車両</p>`;
		segmentInfo.innerHTML += `<p class="segment-info">運賃きっぷ: ${segment.untin}円</p>`;
		segmentInfo.innerHTML += `<p class="segment-info">交通系IC: ${segment.icUntin}円</p>`;

		contentTab.appendChild(segmentInfo);
	});
}

	/*座標データの抽出*/
	function extractCoordinates(routeData) {
		let coordinates = [];
		routeData.NorikaeBizApiResult.body.route.forEach(route => {
				route.path.forEach(segment => {
						coordinates.push({
								from: segment.from,
								to: segment.to,
								fromX: segment.fromX,
								fromY: segment.fromY,
								toX: segment.toX,
								toY: segment.toY
						});
				});
		});
		return coordinates;
}

/*LatLngオブジェクトへ変換*/
function convertToLatLng(x, y) {
	let [degreesX, minutesX, secondsX, fractionX] = x.split(',').map(Number);
	let [degreesY, minutesY, secondsY, fractionY] = y.split(',').map(Number);

	// 経度と緯度を小数点形式に変換
	let lat = degreesY + minutesY / 60 + secondsY / 3600 + fractionY / 3600000;
	let lng = degreesX + minutesX / 60 + secondsX / 3600 + fractionX / 3600000;

	return new google.maps.LatLng(lat, lng);
}

/*情報ウィンドウテキストを生成*/
function createInfoWindowText(segment) {
	let text = '';

	if (segment.from) {
			text += `出発地点: ${segment.from}駅<br>`;
	}
	if (segment.to) {
			text += `到着地点: ${segment.to}駅<br>`;
	}
	if (segment.kyori) {
			text += `距離: ${segment.kyori} km<br>`;
	}
	if (segment.jikan) {
			text += `時間: ${segment.jikan} 分<br>`;
	}
	if (segment.untin) {
			text += `費用: ¥${segment.untin}<br>`;
	}
	if (segment.icUntin) {
			text += `ICカード運賃: ¥${segment.icUntin}<br>`;
	}

	return text;
}


/*マーカーと情報ウィンドウを配置する関数*/
function placeMarkersForPolyline(polyline, coordinates, map) {
	if (coordinates.length > 0) {
			var startSegment = coordinates[0];
			var endSegment = coordinates[coordinates.length - 1];

			if (startSegment && endSegment) {
					var startLatLng = convertToLatLng(startSegment.fromX, startSegment.fromY);
					var endLatLng = convertToLatLng(endSegment.toX, endSegment.toY);

					var startInfoText = createInfoWindowText(startSegment);
					var endInfoText = createInfoWindowText(endSegment);

					addMarkerWithInfoWindow(startLatLng, startInfoText, map);
					addMarkerWithInfoWindow(endLatLng, endInfoText, map);
			}
	}
}

/*電車のルートを地図上に描く*/
function displayRouteOnMap(coordinates, map) {
	console.log(coordinates);  // デバッグ情報
	if (!map) {
			console.error("Map object is not initialized");
			return;
	}

	var bounds = new google.maps.LatLngBounds();
	var routePath = new google.maps.Polyline({
			path: [],
			geodesic: true,
			strokeColor: '#0072BC',
			strokeOpacity: 1.0,
			strokeWeight: 2,
			map: map
	});

	coordinates.forEach(coord => {
		let from = convertToLatLng(coord.fromX, coord.fromY);
		let to = convertToLatLng(coord.toX, coord.toY);

		let infoText = createInfoWindowText(coord);

		// マーカーと情報ウィンドウを追加
		addMarkerWithInfoWindow(from, infoText, map);
		addMarkerWithInfoWindow(to, infoText, map);

		routePath.getPath().push(from);
		routePath.getPath().push(to);

		bounds.extend(from);
		bounds.extend(to);
});

	map.fitBounds(bounds);

	// ポリラインの両端にマーカーを配置
	placeMarkersForPolyline(routePath, map);
}

/*マーカーに情報ウィンドウを追加する関数*/
function addMarkerWithInfoWindow(latLng, contentString, map) {
	var marker = new google.maps.Marker({
			position: latLng,
			map: map
	});

	var infowindow = new google.maps.InfoWindow({
			content: contentString
	});

	marker.addListener('click', function() {
			infowindow.open(map, marker);
	});
}


// 地図上のマーカーを格納する配列
var markers = [];

// 地図上のポリラインを格納する配列
var polylines = [];

// 地図データをクリアする関数
function clearMapData() {
		// すべてのマーカーをクリア
		markers.forEach(function(marker) {
				marker.setMap(null);
		});
		markers = [];

		// すべてのポリラインをクリア
		polylines.forEach(function(polyline) {
				polyline.setMap(null);
		});
		polylines = [];
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

var routeData = {
	"NorikaeBizApiResult":{
			"head":{
					"functionCode":"sr",
					"errorCode":"0"
			},
			"body":{
					"num":"1",
					"storeData":"",
					"route":[{
							"id":"1",
							"hyouka":{
									"pathCnt":"2",
									"jikan":"21",
									"hiyou":"220",
									"icExist":"1",
									"icHiyou":"216",
									"kyori":"118",
									"norikaeCnt":"0",
									"status":{
											"hayai":"1",

											"yasui":"1",
											"raku":"1",
											"kuuro":"0",
											"shindai":"0",
											"kousoku":"0",
											"icCard":"1",
											"norikae":"1",
											"co2":"0",
											"syubetu":"0",
											"icYasui":"1",
											"value":"1,1,1,0,0,0,1,1,0,0,1"
									},
									"kubun":{
											"shinkansen":"0",
											"nozomi":"0",
											"tokkyu":"0",
											"shindai":"0",
											"kuuro":"0",
											"bus":"0",
											"kousoku":"0",
											"renraku":"0",
											"shinya":"0",
											"ferry":"0",
											"toho":"0",
											"yuryou":"0",
											"jr":"1",
											"value":"0,0,0,0,0,0,0,0,0,0,0,0,1"
									}
							},
					"path":[{
							"id":"1",
							"rosen":"中央線",
							"rosenSyubetu":"0",
							"from":"荻窪",
							"fromExt":"",
							"to":"新宿",
							"toExt":"",
							"kyori":"84",
							"jikan":"10",
							"mati":"0",
							"idou":"3",
							"norikae":"0",
							"direction":"0",
							"seatName":"",
							"seatCode":"",
							"seatKubun":{
									"num":"0"
							},
							"untin":"220",
							"untinOufuku":"0",
							"untinTuusan":"1",
							"tokkyu":"0",
							"tokkyuGreen":"0",
							"tokkyuShindai":"0",
							"tokkyuKisetu":"-1",
							"tokkyuWaribiki":"0",
							"tokkyuTuusan":"0",
							"icExist":"1",
							"icUntin":"216",
							"icUntinTuusan":"1",
							"icTokkyu":"0",
							"icTokkyuGreen":"0",
							"icTokkyuTuusan":"0",
							"airLine":"",
							"fromDate":"00000000",
							"fromTime":"",
							"fromTimeType":"-1",
							"toDate":"00000000",
							"toTime":"",
							"toTimeType":"-1",
							"lineName":"",
							"lineType":"快速",
							"lineIndex":"-1",
							"selectLine":"",

							"lineColor":{
									"type":"0",
									"num":"1",
									"rgb":[
											"ffa500"
									]
							},
							"haveDiagram":"1",
							"useDiagram":"0",
							"rosenCorp":"ＪＲ",
							"busCorp":"",
							"josyaText":"3・5・8・10 号車",
							"fromPlatform":"",
							"toPlatform":"",
							"tokurei":{
									"data":"256",
									"num":"1",
									"info":[{
											"code":"U_PASMOBETU",
											"name":"ＩＣカード別運賃",
											"text":"券売機や窓口できっぷを購入した場合の運賃です。IC カードを使用した場合とは異なります。",
											"id":"1"
									}]
							},
							"icTokurei":{
									"data":"512",
									"num":"1",
									"info":[{
											"code":"U_PASMO",
											"name":"ＩＣカード運賃",
											"text":"IC カードを使用した場合の運賃です。券売機で購入した場合とは異なります。",
											"id":"1"
									}]
							},
							"co2":"151",
							"fromX":"139,37,24,400",
							"fromY":"35,42,4,400",
							"toX":"139,42,13,400",
							"toY":"35,41,12,900"
							}]
					}]
			}
	}}