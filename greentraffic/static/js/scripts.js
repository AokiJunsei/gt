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

// ドロップダウンをホバーで開くように編集
$(document).ready(function(){
    $('.nav-item.dropdown').hover(function() {
        $(this).find('.dropdown-menu').stop(true, true).delay(200).fadeIn(500);
    }, function() {
        $(this).find('.dropdown-menu').stop(true, true).delay(200).fadeOut(500);
    });
});
window.onload = function() {
    setTimeout(function() {
        var loadingContainer = document.getElementById('loading-container');
        loadingContainer.style.display = 'none';
    }, 3000); // 3000ミリ秒（3秒）後にローディングアニメーションを非表示にする
};

