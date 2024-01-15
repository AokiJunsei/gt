// 「ヘルプ」のモーダルウィンドウ追加
function loadAndShowModal() {
	fetch('/gt/help/')
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
	// 新規追加の定義
	'current-location-icon': '現在位置を取得します。',
	'swap-icon': '中継地点を入れ替えます。',
	'swap-icon-updown': '出発地と目的地を入れ替えます。',
	'help-icon': 'ヘルプを表示します。',  // 既に定義されていると仮定
	'toggle-icon': '入力フォームの表示を切り替えます。',  // 既に定義されていると仮定
	'toggle-button': '経路の詳細パネルを開閉します。',  // 既に定義されていると仮定
	'departure-date': '出発する日付を選択してください。',
	'departure-time': '出発する時間を選択してください。',
};

// ヘルプテキストを表示する関数
function showHelpText(elementId, event) {
	if (!isHelpEnabled) {
		return; // ヘルプが無効の場合は何もしない
	}
	var helpText = helpTexts[elementId];
	var helpContainer = document.getElementById('help-container');
	var helpTextElement = document.getElementById('help-text');

	var mouseX = event.clientX;
	var mouseY = event.clientY;

	helpTextElement.textContent = helpText;
	helpContainer.style.display = 'block';
	helpContainer.style.left = mouseX + 'px';
	helpContainer.style.top = (mouseY + 25) + 'px';
}

// ヘルプテキストを非表示にする関数
function hideHelpText() {
	var helpContainer = document.getElementById('help-container');
	helpContainer.style.display = 'none';
}

// ヘルプアイコンのクリックイベントハンドラー
document.getElementById('help-icon').addEventListener('click', function () {
	loadAndShowModal();
	isHelpEnabled = !isHelpEnabled; // ヘルプ表示の有効/無効をトグルする
});

// ヘルプテキストを非表示にする関数
function hideHelpText() {
	var helpContainer = document.getElementById('help-container');
	helpContainer.style.display = 'none';
}

// ページがロードされた後にイベントリスナーを設定
window.onload = function () {
	// イベントリスナーの設定
	document.getElementById('start').addEventListener('mouseenter', function (event) {
		showHelpText('start', event);
	});
	document.getElementById('start').addEventListener('mouseleave', hideHelpText);

	document.getElementById('waypoint1').addEventListener('mouseenter', function (event) {
		showHelpText('waypoint1', event);
	});
	document.getElementById('waypoint1').addEventListener('mouseleave', hideHelpText);

	document.getElementById('waypoint2').addEventListener('mouseenter', function (event) {
		showHelpText('waypoint2', event);
	});
	document.getElementById('waypoint2').addEventListener('mouseleave', hideHelpText);

	document.getElementById('end').addEventListener('mouseenter', function (event) {
		showHelpText('end', event);
	});
	document.getElementById('end').addEventListener('mouseleave', hideHelpText);

	document.querySelector('.btn-border').addEventListener('mouseenter', function (event) {
		showHelpText('search', event);
	});
	document.querySelector('.btn-border').addEventListener('mouseleave', hideHelpText);
	document.getElementById('current-location-icon').addEventListener('mouseenter', function (event) {
		showHelpText('current-location-icon', event);
	});
	document.getElementById('current-location-icon').addEventListener('mouseleave', hideHelpText);

	document.getElementById('swap-icon').addEventListener('mouseenter', function (event) {
		showHelpText('swap-icon', event);
	});
	document.getElementById('swap-icon').addEventListener('mouseleave', hideHelpText);

	document.getElementById('swap-icon-updown').addEventListener('mouseenter', function (event) {
		showHelpText('swap-icon-updown', event);
	});
	document.getElementById('swap-icon-updown').addEventListener('mouseleave', hideHelpText);
	document.getElementById('help-icon').addEventListener('mouseenter', function (event) {
		showHelpText('help-icon', event);
	});
	document.getElementById('help-icon').addEventListener('mouseleave', hideHelpText);

	document.getElementById('toggle-icon').addEventListener('mouseenter', function (event) {
		showHelpText('toggle-icon', event);
	});
	document.getElementById('toggle-icon').addEventListener('mouseleave', hideHelpText);

	document.getElementById('toggle-button').addEventListener('mouseenter', function (event) {
		showHelpText('toggle-button', event);
	});
	document.getElementById('toggle-button').addEventListener('mouseleave', hideHelpText);

	var searchButton = document.querySelector('.btn-border');
	if (searchButton) {
		searchButton.addEventListener('mouseenter', function (event) {
			showHelpText('btn-border', event);
		});
		searchButton.addEventListener('mouseleave', hideHelpText);
	}
	// 出発日に対するイベントリスナー
	document.getElementById('departure-date').addEventListener('mouseenter', function (event) {
		showHelpText('departure-date', event);
	});
	document.getElementById('departure-date').addEventListener
		('mouseleave', hideHelpText);

	document.getElementById('departure-time').addEventListener('mouseenter', function (event) {
		showHelpText('departure-time', event);
	});
	document.getElementById('departure-time').addEventListener('mouseleave', hideHelpText);
	// 他の要素についても同様にイベントリスナーを設定
};