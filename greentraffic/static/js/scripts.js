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

//$(document).ready(function(){
    //$('.nav-item.dropdown.custom-dropdown').mouseenter(function() {
    //    $(this).find('.dropdown-menu').stop(true, true).fadeIn(500);
    //}).mouseleave(function() {
    //    $(this).find('.dropdown-menu').stop(true, true).fadeOut(500);
    //});
//});


window.onload = function() {
    setTimeout(function() {
        var loadingContainer = document.getElementById('loading-container');
        loadingContainer.style.display = 'none';
    }, 3000); // 3000ミリ秒（3秒）後にローディングアニメーションを非表示にする
};
var arr = []
//初期値の設定
function TypingInit() {
	$('.js_typing').each(function (i) { //js_typingクラスを全て処理をおこなう
		arr[i] = new ShuffleText(this);//動作させるテキストを配列に格納
	});
}
//スクロールした際のアニメーションの設定
function TypingAnime() {
	$(".js_typing").each(function (i) {
		var elemPos = $(this).offset().top - 50;//要素より、50px上の
		var scroll = $(window).scrollTop();
		var windowHeight = $(window).height();
		if (scroll >= elemPos - windowHeight) {
			if(!$(this).hasClass("endAnime")){//endAnimeのクラスがあるかチェック
				arr[i].start();//配列で登録テキストのアニメーションをおこなう
				arr[i].duration = 800;//テキストが最終変化するまでの時間※規定値600
				$(this).addClass("endAnime");//１度アニメーションした場合はendAnimeクラスを追加
			}
		}else{
			$(this).removeClass("endAnime"); //範囲外にスクロールした場合はendAnimeのクラスを削除
		}
	});
}

// 画面をスクロールをしたら動かしたい場合の記述
$(window).scroll(function () {
	TypingAnime();/* アニメーション用の関数を呼ぶ*/
});// ここまで画面をスクロールをしたら動かしたい場合の記述

// 画面が読み込まれたらすぐに動かしたい場合の記述
$(window).on('load', function () {
	TypingInit(); //初期設定
	TypingAnime();/* アニメーション用の関数を呼ぶ*/
});// ここまで画面が読み込まれたらすぐに動かしたい場合の記述
