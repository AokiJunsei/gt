function scrollToTop(e) {
    e.preventDefault(); // デフォルトのアンカー動作を防止
    window.scrollTo({
        top: 0, // ページのトップにスクロール
        behavior: 'smooth' // スムーズなスクロール動作
    });
}