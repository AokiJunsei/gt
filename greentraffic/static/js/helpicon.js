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

