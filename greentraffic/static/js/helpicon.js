// ヘルプ表示の有効/無効を管理するフラグ
var isHelpEnabled = false;

// ヘルプテキストのデータ
var helpTexts = {
	'start': '出発地を入力してください。',
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
	'id_start':'出発地を入力してください。',
	'spot-start-input-group': '出発地を選択してください。',
	'id_end':'目的地を入力してください。',
	'spot-end-input-group':'目的地を選択してください。',
	'travel_mode':'travel_modeを選択してください。',
	'content-tab':'コンテンツを表示する場所です。',
	'admin_top':'マップ情報一覧に推移します。',
	'gt-top':'車の検索に推移します。',
	'header-logo':'topページに推移します。',
	'footer-image':'広告を表示します。',
	'car-search':'車のオプションを選択できます。',
	'car-search-short':'車検索ページに推移します。',
	'walk-search':'歩きのオプションを選択できます。',
	'walk-search-short':'歩き検索ページに推移します。',
	'bike-search':'自転車のオプションを選択できます。',
	'bike-search-short':'自転車検索ページに推移します。',
	'train-search':'電車のオプションを選択できます。',
	'train-search-short':'電車検索最短ページに推移します。',
	'train-search-cheap':'電車検索最安ページ検索に推移します。',
	'share-car-search':'車シェアオプションを選択できます。',
	'share-car-search-car':'車で受け取りに行く検索に推移します。',
	'share-car-search-bike':'自転車で受け取りに行く検索に推移します。',
	'share-car-search-walk':'歩きで受け取りに行く検索に推移します。',
	'share-bike-search':'自転車シェアオプションを選択できます。',
	'share-bike-search-car':'車で受け取りに行く検索に推移します。',
	'share-bike-search-bike':'自転車で受け取りに行く検索に推移します。',
	'share-bike-search-walk':'歩きで受け取りに行く検索に推移します。',
	'Mymap-search':'mymapオプションを選択できます。',
	'Mymap-search-all':'mymap検索に推移します。',
	'register':'新規登録画面に推移します。',
	'register1':'新規登録画面に推移します。',
	'user-login':'ログイン画面に推移します。',
	'logout':'ログアウト画面に推移します。',
	'user-info':'ユーザー情報画面に推移します。',
	'user_spot_list':'スポット一覧画面に推移します。',
	'account_history':'履歴画面に推移します。',
	'setting':'ログイン時機能オプションを選択できます。',
	'username':'ログイン時に入力するidを入力してください。',
	'email':'認証確認メールを送信するためのメールアドレスを入力してください。',
	'password':'ログイン時に入力できるパスワードを入力してください。',
	'confirm_password':'パスワード確認のためにもう一度パスワードを入力してください。',
	'last_name':'苗字を入力してください。',
	'first_name':'名前を入力してください。',
	'zipcode':'郵便番号を入力してください。',
	'state':'都道府県を入力してください。',
	'city':'市区町村を入力してください。',
	'address_1':'番地を入力できます。',
	'address_2':'部屋番号を入力できます。',
	'back':'前の画面に戻ります。',
	'enregister':'入力した情報を保存し確認メールを送信します。',
	'userID':'userIDを入力してください。',
	'login-password':'パスワードを入力してください。',
	'login':'ログイン時のページに推移します。',
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
window.addEventListener('load', function() {
	
	['start', 'waypoint1', 'waypoint2', 'end', 'current-location-icon',
	'swap-icon', 'swap-icon-updown', 'toggle-icon', 'toggle-button',
	'departure-date', 'departure-time', 'help-icon', 'car-link', 'bike-link', 'id_start',
	'spot-start-input-group', 'id_end', 'spot-end-input-group', 'travel_mode', 'content-tab',
	'admin_top', 'header-logo', 'footer-image', 'car-search', 'car-search-short',
	'walk-search', 'walk-search-short', 
	'bike-search', 'bike-search-short', 
	'train-search', 'train-search-short', 'train-search-cheap', 
	'share-car-search', 'share-car-search-car', 'share-car-search-bike', 'share-car-search-walk', 
	'share-bike-search', 'share-bike-search-car', 'share-bike-search-bike', 'share-bike-search-walk',
	'Mymap-search', 'Mymap-search-all', 'register', 'user-login', 'logout', 
	'user-info', 'user_spot_list', 'account_history', 'setting',
	'username', 'email', 'password', 'confirm_password', 
	'last_name', 'first_name', 'zipcode', 'state', 'city', 
	'address_1', 'address_2','back','enregister','userID',
	'login-password','login','register1']
	.forEach(function (id) {
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
});