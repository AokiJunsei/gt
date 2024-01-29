var map, infowindow, service, markers = [];

//マップ情報
function initMap() {
  var Marker;
  const initial_location = { lat: 35.689, lng: 139.692 };

  map = new google.maps.Map(document.getElementById("map"), {
    zoom: 17,
    center: initial_location,
  });

  infowindow = new google.maps.InfoWindow();
  // service の初期化をここに移動
  service = new google.maps.places.PlacesService(map);

    setupSearchButton(); // initMap が完了したら検索ボタンをセットアップ
        checkAndExecuteTrainTF(); // 追加機能のチェックと実行
}

/*上記までがinitMap()*/

// 検索機能
function searchPlaces() {
  if (!map) {
    console.error("Map is not initialized yet.");
    return;
  }
  var searchInput = document.getElementById("map-search-input").value;

        // 検索クエリが空でないことを確認
        if (!searchInput.trim()) {
            alert("検索クエリを入力してください。");
            return;
        }

  service.textSearch({
    query: searchInput,
    location: map.getCenter(),
    radius: 5000
  }, function(results, status) {
    if (status === google.maps.places.PlacesServiceStatus.OK) {
      clearMarkers();
      results.forEach(place => {
        createMarker(place);
                    displayPlaceDetails(place.place_id); // ここで displayPlaceDetails を呼び出す
                    expandPanel()
      });
    } else {
      alert('Place search failed: ' + status);
    }
  });
}

function createMarker(place) {
		var marker = new google.maps.Marker({
				map: map,
				position: place.geometry.location
		});

		google.maps.event.addListener(marker, 'click', function() {
				infowindow.setContent('<div><strong>' + place.name + '</strong><br>' +
						'Address: ' + place.formatted_address + '</div>');
				infowindow.open(map, this);
		});
		// 地図の中心をマーカーの位置に設定する
	map.setCenter(marker.getPosition());
}

function displayPlaceDetails(placeId) {
		service.getDetails({
		placeId: placeId
		}, function(place, status) {
		if (status === google.maps.places.PlacesServiceStatus.OK) {
				// ランダムな色を生成
				var headerBackgroundColor = getRandomColor(); // カードヘッダーの背景色にランダムな色を適用
				var headerTextColor = '#FFFFFF'; // 白色
				var linkColor = '#007BFF'; // Bootstrapのプライマリーカラー

				// 写真がある場合、最初の写真のURLを取得
				var photoUrl = place.photos && place.photos.length ? place.photos[0].getUrl({maxWidth: 400, maxHeight: 200}) : null;

				// Bootstrapのカードコンポーネントを使用してUIを改善
				var detailsHTML = `
				<div class="card border-info mb-3">
				<div class="card-header" style="background-color: ${headerBackgroundColor}; color: ${headerTextColor};">${place.name}</div>
				<div class="card-body text-info">
						<h5 class="card-title">${place.formatted_address}</h5>
						${photoUrl ? `<img src="${photoUrl}" class="card-img-top" alt="Place image">` : ''}
						<p class="card-text">
						<strong>電話番号:</strong> ${place.formatted_phone_number || '情報なし'}<br>
						<strong>評価:</strong> ${place.rating || '情報なし'}<br>
						<strong>ウェブサイト:</strong> ${place.website ? `<a href="${place.website}" target="_blank" style="color: ${linkColor};">ウェブサイトへ</a>` : '情報なし'}<br>
						<strong>レビュー:</strong> ${place.reviews ? place.reviews.map(review => `<blockquote class="blockquote">${review.text}</blockquote>`).join('') : '情報なし'}<br>
						<strong>価格レベル:</strong> ${place.price_level || '情報なし'}<br>
						<strong>営業時間:</strong> <br>${place.opening_hours ? place.opening_hours.weekday_text.join('<br>') : '情報なし'}
						</p>
				</div>
				</div>`;

				document.getElementById("place-details").innerHTML = detailsHTML;
		} else {
				document.getElementById("place-details").innerHTML = '<div>詳細情報を表示できませんでした。</div>';
				console.error('Google Places API returned status: ' + status);
		}
		});
}

// ランダムな色を生成する関数
function getRandomColor() {
		var letters = '0123456789ABCDEF';
		var color = '#';
		for (var i = 0; i < 6; i++) {
		color += letters[Math.floor(Math.random() * 16)];
		}
		return color;
}

function clearMarkers() {
// すべてのマーカーをループしてマップから削除
for (var i = 0; i < markers.length; i++) {
  markers[i].setMap(null);
}
markers = []; // 配列をリセット
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

window.addEventListener('load', function() {
  initMap();
  checkAndExecuteTrainTF();
});

function checkAndExecuteTrainTF() {
  if (!map) {
    console.error("Map object is not initialized yet.");
    return;
  }
  setupSearchButton()
}

// initMap が完了したら、検索ボタンにイベントリスナーを設定します。
function setupSearchButton() {
		document.getElementById('search-button').addEventListener('click', searchPlaces);
}


function toggleDirectionsPanel() {
		var panel = document.getElementById('directions-panel');
		if (panel.style.display === 'none') {
				panel.style.display = 'block';
		} else {
				panel.style.display = 'none';
		}
}

document.addEventListener('DOMContentLoaded', (event) => {
		// 全てのタブコンテンツを非表示にする
		var tabContents = document.getElementsByClassName('tab-content');
		for (var i = 0; i < tabContents.length; i++) {
				tabContents[i].style.display = 'none';
		}

		// 特定のタブコンテンツだけを表示する
		var defaultTabContent = document.getElementById('place-details');
		if (defaultTabContent) {
				defaultTabContent.style.display = 'block';
		}
});

