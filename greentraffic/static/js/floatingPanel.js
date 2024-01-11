// 「ヘルプ」のモーダルウィンドウ追加
function loadAndShowModal() {
	fetch('help/')
		.then(response => response.text())
		.then(data => {
			document.querySelector('#helpModal .modal-body').innerHTML = data;
			var modal = new bootstrap.Modal(document.getElementById('helpModal'));
			modal.show();
		});
}

document.addEventListener('DOMContentLoaded', (event) => {
	document.getElementById('help-icon').addEventListener('click', loadAndShowModal);
});

var helpModal = document.getElementById('helpModal');

helpModal.addEventListener('hidden.bs.modal', function (event) {
// モーダルが閉じたら実行される
var backdrops = document.getElementsByClassName('modal-backdrop');
// modal-backdrop クラスを持つ要素がまだ存在するかどうか確認する
if (backdrops.length > 0) {
	// 存在する場合は、それらを削除する
	Array.from(backdrops).forEach(function (backdrop) {
	backdrop.remove();
	});
}
});


function toggleInputForm() {
	var x = document.getElementById('floating-panel');
	var icon = document.getElementById('toggle-icon');

	if (!x.style.display || x.style.display === 'block') {
		x.style.display = 'none'; // フォームを非表示にする
		icon.className = 'fas fa-eye-slash'; // アイコンを非表示アイコンに変更
	} else {
		x.style.display = 'block'; // フォームを表示にする
		icon.className = 'fas fa-eye'; // アイコンを表示アイコンに変更
	}
}

/*検索結果のタブの開閉*/
// 初期状態では詳細パネルを非表示にする
let directionsPanelVisible = false;

// パネルを表示/非表示切り替える関数
function toggleDirectionsPanel() {
	const directionsPanel = document.getElementById("directions-panel");
	const contentTab = document.getElementById("content-tab");
	const detailsTab = document.getElementById("details-tab");

	if (!directionsPanelVisible) {
	// パネルを表示
	directionsPanel.style.display = "block";
	contentTab.classList.add("active");
	detailsTab.classList.remove("active");
	} else {
	// パネルを非表示
	directionsPanel.style.display = "none";
	}

	// 表示状態を反転させる
	directionsPanelVisible = !directionsPanelVisible;
}


function toggleTab(tabName) {
	const contentTab = document.getElementById("content-tab");
	const detailsTab = document.getElementById("details-tab");

	if (tabName === "content") {
	contentTab.classList.add("active");
	detailsTab.classList.remove("active");
	} else {
	contentTab.classList.remove("active");
	detailsTab.classList.add("active");
	}
}

/*出発地と到着地の内容を入れ替える関数*/
function swapStartEnd() {
	const startInput = document.getElementById("start");
	const endInput = document.getElementById("end");

	// 入れ替えボタン
	const temp = startInput.value;
	startInput.value = endInput.value;
	endInput.value = temp;
}

function toggleWaypoints() {
	var waypoint1 = document.getElementById('waypoint1-group');
	var waypoint2 = document.getElementById('waypoint2-group');
	var waypointLabel = document.getElementById('waypointLabel'); // ラベルの正しいIDを確認してください

	// 中継地点が現在表示されているかどうかを判定
	var isDisplayed = waypoint1.style.display !== 'none';

	// 中継地点の表示・非表示を切り替え
	waypoint1.style.display = isDisplayed ? 'none' : 'block';
	waypoint2.style.display = isDisplayed ? 'none' : 'block';

	// ラベルの表示・非表示も切り替える（条件が逆になる）
	waypointLabel.style.display = isDisplayed ? 'block' : 'none';
}

var initialLeft = 20; // 左端からの距離
var initialTop = 20;  // 上端からの距離

document.addEventListener('DOMContentLoaded', function() {
	var floatingPanel = document.getElementById('floating-panel');
	var isDragging = false;
	var offsetX, offsetY;

	floatingPanel.addEventListener('mousedown', function(e) {
		isDragging = true;
		offsetX = e.clientX - floatingPanel.getBoundingClientRect().left;
		offsetY = e.clientY - floatingPanel.getBoundingClientRect().top;
		window.getSelection().removeAllRanges();
	});

	document.addEventListener('mouseup', function() {
		isDragging = false;
	});

	document.addEventListener('mousemove', function(e) {
		if (isDragging) {
			var mouseX = e.clientX;
			var mouseY = e.clientY;
			var newLeft = mouseX - offsetX;
			// 画面の下部を超えないようにするために、newTop の値を制限します。
			var newTop = Math.min(mouseY - offsetY, window.innerHeight - floatingPanel.offsetHeight - 10); // 下部の余白を10pxに設定

			newLeft = Math.min(newLeft, window.innerWidth - floatingPanel.offsetWidth);
			newLeft = Math.max(newLeft, 0);

			floatingPanel.style.left = newLeft + 'px';
			floatingPanel.style.top = Math.max(0, newTop) + 'px';
		}
	});
	document.addEventListener('mousemove', function(e) {
		if (isDragging) {
			var mouseX = e.clientX;
			var mouseY = e.clientY;
			var newLeft = mouseX - offsetX;
			// 画面の下部を超えないようにするために、newTop の値を制限します。
			var newTop = Math.min(mouseY - offsetY, window.innerHeight - floatingPanel.offsetHeight - 65); // 下部の余白を10pxに設定

			newLeft = Math.min(newLeft, window.innerWidth - floatingPanel.offsetWidth);
			newLeft = Math.max(newLeft, 0);

			floatingPanel.style.left = newLeft + 'px';
			floatingPanel.style.top = Math.max(0, newTop) + 'px';
		}
	});
	window.addEventListener('resize', function() {
		// ウィンドウのリサイズ時に、右端を超えないように位置を調整する
		var rightEdge = window.innerWidth - floatingPanel.offsetWidth;
		var currentLeft = parseInt(floatingPanel.style.left, 10);
		if (currentLeft > rightEdge) {
			floatingPanel.style.left = rightEdge + 'px';
		}
	});
});
document.addEventListener('DOMContentLoaded', function() {
    var floatingPanel = document.getElementById('floating-panel');
    var isDragging = false;
    var offsetX, offsetY;
	
    // タッチイベントとマウスイベントの両方をサポート
    function startDrag(e) {
        isDragging = true;
        var event = e.type === 'touchstart' ? e.touches[0] : e;
        offsetX = event.clientX - floatingPanel.getBoundingClientRect().left;
        offsetY = event.clientY - floatingPanel.getBoundingClientRect().top;
        window.getSelection().removeAllRanges();
    }

    function endDrag() {
        isDragging = false;
    }

    function doDrag(e) {
        if (isDragging) {
            var event = e.type === 'touchmove' ? e.touches[0] : e;
            var mouseX = event.clientX;
            var mouseY = event.clientY;
            var newLeft = mouseX - offsetX;
            var newTop = mouseY - offsetY;

            newLeft = Math.max(0, Math.min(newLeft, window.innerWidth - floatingPanel.offsetWidth));
            newTop = Math.max(0, Math.min(newTop, window.innerHeight - floatingPanel.offsetHeight));

            floatingPanel.style.left = newLeft + 'px';
            floatingPanel.style.top = newTop + 'px';
        }
    }

    // タッチイベントリスナーを追加
    floatingPanel.addEventListener('touchstart', startDrag);
    floatingPanel.addEventListener('mousedown', startDrag);
    document.addEventListener('touchend', endDrag);
    document.addEventListener('mouseup', endDrag);
    document.addEventListener('touchmove', doDrag);
    document.addEventListener('mousemove', doDrag);
});