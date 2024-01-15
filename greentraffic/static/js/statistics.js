// Google Charts ライブラリの読み込み
google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawCharts);

function drawCharts() {
  // 地理的分布のチャートを描画
  var stateData = google.visualization.arrayToDataTable([
    ['State', 'Count'],
    ...window.stateData.map(item => [item.state, item.count])
  ]);
  var stateChart = new google.visualization.PieChart(document.getElementById('state_chart'));
  stateChart.draw(stateData, {title: '地理的分布'});

  // アカウント作成日の統計のチャートを描画（月別）
  var creationData = new google.visualization.DataTable();
  creationData.addColumn('string', 'Month');  // 日付ではなく、月を表す文字列として扱う
  creationData.addColumn('number', 'Count');
  window.creationData.forEach(function (item) {
    // item.month は 'YYYY-MM' 形式であることを想定しています。
    // バックエンドからこの形式でデータが渡されるようにしてください。
    creationData.addRow([item.month, item.count]);
  });
  var creationChart = new google.visualization.ColumnChart(document.getElementById('creation_chart'));
  creationChart.draw(creationData, {
    title: 'アカウント作成日の統計（月別）',
    hAxis: {title: 'Month'},
    vAxis: {title: 'Count'}
  });

  // 地理的座標の分析のチャートを描画
  var coordinatesData = new google.visualization.DataTable();
  coordinatesData.addColumn('number', 'Latitude');
  coordinatesData.addColumn('number', 'Longitude');
  coordinatesData.addColumn('number', 'Count');
  window.coordinatesData.forEach(function (item) {
    coordinatesData.addRow([item.latitude, item.longitude, item.count]);
  });
  var coordinatesChart = new google.visualization.ScatterChart(document.getElementById('coordinates_chart'));
  coordinatesChart.draw(coordinatesData, {
    title: '地理的座標の分析',
    hAxis: {title: 'Latitude'},
    vAxis: {title: 'Longitude'}
  });
}

function initMap() {
  // 地図の初期設定
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 8,  // ズームレベル
    center: {lat: 35.6895, lng: 139.6917}  // 地図の中心点（ここでは東京都庁を例としています）
  });

  // 地理的座標データのピンを地図に追加
  window.coordinatesData.forEach(function (item) {
    var marker = new google.maps.Marker({
      position: {lat: item.latitude, lng: item.longitude},
      map: map,
			icon: {
				path: google.maps.SymbolPath.CIRCLE,
				fillColor: 'Blue',
				fillOpacity: 0.8,
				scale: 8,
				strokeColor: 'white',
				strokeWeight: 2
		}
    });
  });
}

// ページ読み込み後に地図を初期化
google.charts.setOnLoadCallback(initMap);

