document.addEventListener('DOMContentLoaded', (event) => {
    const video = document.getElementById('background-video');
    const hasVideoPlayed = sessionStorage.getItem('hasVideoPlayed');

    if (!hasVideoPlayed) {
        video.style.display = 'block'; // ビデオを表示
        video.play(); // ビデオを再生

        video.onended = function(e) {
            this.classList.add('video-fade-out'); // フェードアウトアニメーションを追加
            this.addEventListener('animationend', () => {
                this.style.display = 'none'; // アニメーションが完了したらビデオを非表示にする
                sessionStorage.setItem('hasVideoPlayed', 'true');
            }, { once: true }); // イベントリスナーを一度だけ実行
        };
    }
});



$(document).ready(function() {
    // モーダルが開かれたときのイベント
    $("#logoutModal").on('show.bs.modal', function() {
        // 以前のoverflowの状態を保存
        var originalBodyOverflow = $('body').css('overflow');
        $(this).data('originalBodyOverflow', originalBodyOverflow);

        // bodyのoverflowをvisibleに設定してスクロールを維持
        $('body').css('overflow', 'visible');
    });

    // モーダルが閉じられたときのイベント
    $("#logoutModal").on('hidden.bs.modal', function() {
        // 保存しておいた以前のoverflowの状態に戻す
        var originalBodyOverflow = $(this).data('originalBodyOverflow');
        $('body').css('overflow', originalBodyOverflow);
    });


    // キャンセルボタンと×マークに同じ挙動を設定
    $("#logoutModal .btn-secondary, #logoutModal .close").on('click', function() {
        console.log("キャンセルまたは×マークがクリックされました。");
        $("#logoutModal").modal('hide');
    });
});


// ヘッダー日付
document.addEventListener("DOMContentLoaded", function() {
    const timeElement = document.getElementById("time");
    timeElement.innerHTML = showNow();
    setTimeout(() => {
        timeElement.style.opacity = '1'; // 要素を徐々に表示する
    }, ); // すぐに実行されるタイマーで微妙な遅延を設定

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


// ローディングアニメーションを非表示にする関数
function hideLoadingAnimation() {
    setTimeout(function() {
        var loadingContainer = document.getElementById('loading-container');
        loadingContainer.style.display = 'none';
    }, 3000); // 3000ミリ秒（3秒）後にローディングアニメーションを非表示にする
}

// TypingInit関数の定義
var arr = []; // arr配列の初期化
function TypingInit() {
    $('.js_typing').each(function (i) { // js_typingクラスを全て処理する
        arr[i] = new ShuffleText(this); // 動作させるテキストを配列に格納
    });
}

// ページが完全にロードされた後に実行されるイベントリスナー
window.addEventListener('load', function() {
    hideLoadingAnimation(); // ローディングアニメーションを非表示にする関数を呼び出す
    TypingInit(); // TypingInit関数を呼び出す
});
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

