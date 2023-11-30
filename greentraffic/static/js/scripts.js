// ログアウトのモーダルウィンドウ
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


// ヘッダー日付
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("text").innerHTML = showNow();

    function showNow() {
    var now = new Date();
    var nowyear = now.getFullYear();
    var nowmonth = now.getMonth() + 1;
    var nowdate = now.getDate();
    var text = nowyear + "/" + nowmonth + "/" + nowdate;
    return text;
    }
});
