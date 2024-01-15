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
	'start': '出発地点を入力してください。現在地を取得するにはコンパスアイコンをクリックします。',
	'waypoint1': '中継地点1を入力してください。経路に追加されます。',
	'waypoint2': '中継地点2を入力してください。経路に追加されます。',
	'end': '目的地を入力してください。',
	'search': '入力した情報に基づいて経路を検索します。',
	// その他の要素についても同様に追加
};

// ヘルプテキストを表示する関数
function showHelpText(elementId) {
	if (!isHelpEnabled) {
		return; // ヘルプが無効の場合は何もしない
	}
	var helpText = helpTexts[elementId];
	var helpContainer = document.getElementById('help-container');
	var helpTextElement = document.getElementById('help-text');

	helpTextElement.textContent = helpText;
	helpContainer.style.display = 'block';
}

// ヘルプテキストを非表示にする関数
function hideHelpText() {
	var helpContainer = document.getElementById('help-container');
	helpContainer.style.display = 'none';
}

// ヘルプアイコンのクリックイベントハンドラー
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
	// 各要素にイベントリスナーを追加
	document.getElementById('start').addEventListener('mouseenter', function () {
		showHelpText('start');
	});
	document.getElementById('start').addEventListener('mouseleave', hideHelpText);

	// waypoint1に対するイベントリスナー
	document.getElementById('waypoint1').addEventListener('mouseenter', function () {
		showHelpText('waypoint1');
	});
	document.getElementById('waypoint1').addEventListener('mouseleave', hideHelpText);

	// waypoint2に対するイベントリスナー
	document.getElementById('waypoint2').addEventListener('mouseenter', function () {
		showHelpText('waypoint2');
	});
	document.getElementById('waypoint2').addEventListener('mouseleave', hideHelpText);

	// endに対するイベントリスナー
	document.getElementById('end').addEventListener('mouseenter', function () {
		showHelpText('end');
	});
	document.getElementById('end').addEventListener('mouseleave', hideHelpText);

	// searchボタンに対するイベントリスナー
	document.querySelector('.btn-border').addEventListener('mouseenter', function () {
		showHelpText('search');
	});
	document.querySelector('.btn-border').addEventListener('mouseleave', hideHelpText);
	// ...
};