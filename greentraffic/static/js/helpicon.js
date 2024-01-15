// ヘルプ表示の有効/無効を管理するフラグ
var isHelpEnabled = false;

// ヘルプテキストのデータ
var helpTexts = {
	'start': '出発地点を入力してください。',
	'waypoint1': '中継地点1を入力してください。',
	'waypoint2': '中継地点2を入力してください。',
	'end': '目的地を入力してください。',
	'help-icon': 'ヘルプを表示します。',
	'toggle-icon': '入力フォームの表示を切り替えます。',
	'toggle-button': '経路の詳細パネルを開閉します。',
	'btn-border': '検索結果を表示します。',
	'current-location-icon': '現在位置を取得します。',
	'swap-icon': '中継地点を入れ替えます。',
	'swap-icon-updown': '出発地と目的地を入れ替えます。',
	'departure-date': '出発する日付を選択してください。',
	'departure-time': '出発する時間を選択してください。',
	'car-link': 'アイコンをクリックして、Anycaのウェブサイトを開きます。',
	'bike-link': 'アイコンをクリックして、HELLO CYCLINのウェブサイトを開きます。',
};

// ヘルプテキスト関連の要素の取得
var helpContainer = document.getElementById('help-container');
var helpTextElement = document.getElementById('help-text');
var helpIcon = document.getElementById('help-icon');

// ヘルプテキストを表示する関数
function showHelpText(elementId, event) {
	if (!isHelpEnabled) {
		return;
	}

	var helpText = helpTexts[elementId];
	helpTextElement.textContent = helpText;

	// テキストの幅を計算（テキストの表示前に一時的に表示）
	helpContainer.style.visibility = 'hidden'; // 一時的に非表示
	helpContainer.style.display = 'block';
	var containerWidth = helpContainer.offsetWidth;
	var containerHeight = helpContainer.offsetHeight;
	helpContainer.style.visibility = ''; // 元に戻す
	helpContainer.style.display = 'none';

	// 画面のサイズを取得
	var screenWidth = window.innerWidth;
	var screenHeight = window.innerHeight;

	// テキストの位置を調整
	var posX = event.clientX;
	var posY = event.clientY;

	// 画面の右端または下端にテキストがはみ出さないように調整
	if (posX + containerWidth > screenWidth) {
		posX -= containerWidth;
	}
	if (posY + containerHeight > screenHeight) {
		posY -= containerHeight;
	}

	// テキストの位置を更新
	helpContainer.style.left = posX + 'px';
	helpContainer.style.top = posY + 'px';

	// テキストを表示
	helpContainer.style.display = 'block';
}

function showHelpModeStatus() {
	var statusText = isHelpEnabled ? 'ヘルプモードが有効になりました' : 'ヘルプモードが無効になりました';
	var statusElement = document.getElementById('help-status');

	statusElement.textContent = statusText;
	statusElement.style.display = 'block';

	// 数秒後にテキストを非表示にする
	setTimeout(function () {
		statusElement.style.display = 'none';
	}, 3000); // 3秒後に非表示
}
// ヘルプテキストを非表示にする関数
function hideHelpText() {
	helpContainer.style.display = 'none';
}

// ヘルプアイコンの視覚的な更新を行う関数
function updateHelpIconVisual() {
	helpIcon.style.color = isHelpEnabled ? 'green' : 'black';
}

// ヘルプアイコンのクリックイベントハンドラー

helpIcon.addEventListener('click', function () {
	isHelpEnabled = !isHelpEnabled;
	updateHelpIconVisual();
	showHelpModeStatus(); // ヘルプモードの状態を示すテキストを表示
});

// イベントリスナーを追加する関数
function addEventListeners(id, mouseEnterHandler, mouseLeaveHandler) {
	var element = document.getElementById(id);
	if (element) {
		element.addEventListener('mouseenter', mouseEnterHandler);
		element.addEventListener('mouseleave', mouseLeaveHandler);
	}
}

// ページがロードされた後にイベントリスナーを設定
window.onload = function () {
	['start', 'waypoint1', 'waypoint2', 'end', 'current-location-icon',
		'swap-icon', 'swap-icon-updown', 'toggle-icon', 'toggle-button',
		'departure-date', 'departure-time', 'help-icon', 'car-link', 'bike-link'
	].forEach(function (id) {
		addEventListeners(id, function (event) {
			showHelpText(id, event);
		}, hideHelpText);
	});
	var searchButton = document.querySelector('.btn-border');
	if (searchButton) {
		searchButton.addEventListener('mouseenter', function (event) {
			showHelpText('btn-border', event);
		});
		searchButton.addEventListener('mouseleave', hideHelpText);
	}
};