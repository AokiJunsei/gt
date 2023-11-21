$(document).ready(function() {
    // モーダルが開かれたときに実行されるイベント
    $("#logoutModal").on('shown.bs.modal', function() {
        console.log("ログアウトモーダルが表示されました。");
    });

    // モーダルが閉じられるときに実行されるイベント
    $("#logoutModal").on('hidden.bs.modal', function() {
        console.log("ログアウトモーダルが閉じられました。");
    });

    // キャンセルボタンにイベントハンドラを設定（必要に応じて）
    $("#logoutModal .btn-secondary").on('click', function() {
        console.log("キャンセルボタンがクリックされました。");
        $("#logoutModal").modal('hide');
    });
});
