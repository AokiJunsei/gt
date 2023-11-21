$(document).ready(function() {
    // モーダルが開かれたときのイベント
    $("#logoutModal").on('shown.bs.modal', function() {
        console.log("ログアウトモーダルが表示されました。");
    });

    // モーダルが閉じられたときのイベント
    $("#logoutModal").on('hidden.bs.modal', function() {
        console.log("ログアウトモーダルが閉じられました。");
    });

    // キャンセルボタンと×マークに同じ挙動を設定
    $("#logoutModal .btn-secondary, #logoutModal .close").on('click', function() {
        console.log("キャンセルまたは×マークがクリックされました。");
        $("#logoutModal").modal('hide');
    });
});
