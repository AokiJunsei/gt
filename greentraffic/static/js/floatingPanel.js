function toggleInputForm() {
	var x = document.getElementById('floating-panel');
	var icon = document.getElementById('toggle-icon');

	if (!x.style.display || x.style.display === 'block') {
		x.style.display = 'none'; // フォームを非表示にする
		icon.className = 'fas fa-eye-slash'; // アイコンを非表示アイコンに変更
	} else {
		x.style.display = 'block'; // フォームを表示にする
		icon.className = 'fas fa-eye'; // アイコンを表示アイコンに変更
	}
}

/*検索結果のタブの開閉*/
// 初期状態では詳細パネルを非表示にする
let directionsPanelVisible = false;

// パネルを表示/非表示切り替える関数
function toggleDirectionsPanel() {
    const directionsPanel = document.getElementById("directions-panel");
    const toggleButton = document.getElementById("toggle-button"); // アイコンの要素を取得

    if (!directionsPanelVisible) {
        // パネルを表示
        directionsPanel.style.display = "block";
        toggleButton.className = 'fas fa-solid fa-arrow-left'; // アイコンを矢印に変更
    } else {
        // パネルを非表示
        directionsPanel.style.display = "none";
        toggleButton.className = 'fas fa-slash'; // アイコンをスラッシュに変更
    }

    // 表示状態を反転させる
    directionsPanelVisible = !directionsPanelVisible;
}


function toggleTab(tabName) {
	const contentTab = document.getElementById("content-tab");
	const detailsTab = document.getElementById("details-tab");

	if (tabName === "content") {
	contentTab.classList.add("active");
	detailsTab.classList.remove("active");
	} else {
	contentTab.classList.remove("active");
	detailsTab.classList.add("active");
	}
}

/*出発地と到着地の内容を入れ替える関数*/
function swapStartEnd() {
	const startInput = document.getElementById("start");
	const endInput = document.getElementById("end");

	// 入れ替えボタン
	const temp = startInput.value;
	startInput.value = endInput.value;
	endInput.value = temp;
}

function toggleWaypoints() {
	var waypoint1 = document.getElementById('waypoint1-group');
	var waypoint2 = document.getElementById('waypoint2-group');
	var waypointLabel = document.getElementById('waypointLabel'); // ラベルの正しいIDを確認してください

	// 中継地点が現在表示されているかどうかを判定
	var isDisplayed = waypoint1.style.display !== 'none';

	// 中継地点の表示・非表示を切り替え
	waypoint1.style.display = isDisplayed ? 'none' : 'block';
	waypoint2.style.display = isDisplayed ? 'none' : 'block';

	// ラベルの表示・非表示も切り替える（条件が逆になる）
	waypointLabel.style.display = isDisplayed ? 'block' : 'none';
}

var initialLeft = 20; // 左端からの距離
var initialTop = 20;  // 上端からの距離

document.addEventListener('DOMContentLoaded', function() {
	var floatingPanel = document.getElementById('floating-panel');
	var isDragging = false;
	var offsetX, offsetY;

	floatingPanel.addEventListener('mousedown', function(e) {
		isDragging = true;
		offsetX = e.clientX - floatingPanel.getBoundingClientRect().left;
		offsetY = e.clientY - floatingPanel.getBoundingClientRect().top;
		window.getSelection().removeAllRanges();
	});

	document.addEventListener('mouseup', function() {
		isDragging = false;
	});

	document.addEventListener('mousemove', function(e) {
		if (isDragging) {
			var mouseX = e.clientX;
			var mouseY = e.clientY;
			var newLeft = mouseX - offsetX;
			// 画面の下部を超えないようにするために、newTop の値を制限します。
			var newTop = Math.min(mouseY - offsetY, window.innerHeight - floatingPanel.offsetHeight - 10); // 下部の余白を10pxに設定

			newLeft = Math.min(newLeft, window.innerWidth - floatingPanel.offsetWidth);
			newLeft = Math.max(newLeft, 0);

			floatingPanel.style.left = newLeft + 'px';
			floatingPanel.style.top = Math.max(0, newTop) + 'px';
		}
	});
	document.addEventListener('mousemove', function(e) {
		if (isDragging) {
			var mouseX = e.clientX;
			var mouseY = e.clientY;
			var newLeft = mouseX - offsetX;
			// 画面の下部を超えないようにするために、newTop の値を制限します。
			var newTop = Math.min(mouseY - offsetY, window.innerHeight - floatingPanel.offsetHeight - 65); // 下部の余白を10pxに設定

			newLeft = Math.min(newLeft, window.innerWidth - floatingPanel.offsetWidth);
			newLeft = Math.max(newLeft, 0);

			floatingPanel.style.left = newLeft + 'px';
			floatingPanel.style.top = Math.max(0, newTop) + 'px';
		}
	});
	window.addEventListener('resize', function() {
		// ウィンドウのリサイズ時に、右端を超えないように位置を調整する
		var rightEdge = window.innerWidth - floatingPanel.offsetWidth;
		var currentLeft = parseInt(floatingPanel.style.left, 10);
		if (currentLeft > rightEdge) {
			floatingPanel.style.left = rightEdge + 'px';
		}
	});
});
document.addEventListener('DOMContentLoaded', function() {
    var floatingPanel = document.getElementById('floating-panel');
    var isDragging = false;
    var offsetX, offsetY;
	
	function startDrag(e) {
		var target = e.target;
	
		// イベントの発生源がinput, button, i (アイコン) 要素でない場合にのみドラッグを開始
		if (target.tagName !== 'INPUT' && target.tagName !== 'BUTTON' && target.tagName !== 'I'&& target.tagName !== 'SELECT') {
			isDragging = true;
			var event = e.type === 'touchstart' ? e.touches[0] : e;
			offsetX = event.clientX - floatingPanel.getBoundingClientRect().left;
			offsetY = event.clientY - floatingPanel.getBoundingClientRect().top;
			window.getSelection().removeAllRanges();
			e.preventDefault(); // デフォルトのタッチイベント（ページのスクロールなど）を防ぐ
		}
	}

    function endDrag() {
        isDragging = false;
    }

    function doDrag(e) {
        if (isDragging) {
            var event = e.type === 'touchmove' ? e.touches[0] : e;
            var mouseX = event.clientX;
            var mouseY = event.clientY;
            var newLeft = mouseX - offsetX;
            var newTop = mouseY - offsetY;

            newLeft = Math.max(0, Math.min(newLeft, window.innerWidth - floatingPanel.offsetWidth));
            newTop = Math.max(0, Math.min(newTop, window.innerHeight - floatingPanel.offsetHeight));

            floatingPanel.style.left = newLeft + 'px';
            floatingPanel.style.top = newTop + 'px';
        }
    }

	// タッチイベントリスナーを追加
	floatingPanel.addEventListener('touchstart', startDrag, {passive: false}); // 変更: passiveオプションをfalseに設定
	floatingPanel.addEventListener('mousedown', startDrag);
	document.addEventListener('touchend', endDrag);
	document.addEventListener('mouseup', endDrag);
	document.addEventListener('touchmove', doDrag, {passive: false}); // 変更: passiveオプションをfalseに設定
	document.addEventListener('mousemove', doDrag);
});
class LivePattern {
    constructor() {
      this.canvas = document.getElementById('canvas');
      this.context = this.canvas.getContext('2d');
      this.colors = [252, 251, 249, 248, 241, 240];
      this.animationFrameId = null;
    }
  
    init() {
      this.setupEventListeners();
      this.onResize();
      this.animate();
    }
  
    setupEventListeners() {
      window.addEventListener('resize', () => this.onResize());
    }
  
    onResize() {
      this.updateDimensions();
      this.drawBackground();
    }
  
    updateDimensions() {
      this.cols = Math.floor(window.innerWidth / 24);
      this.rows = Math.floor(window.innerHeight / 24) + 1;
      this.canvas.width = window.innerWidth;
      this.canvas.height = window.innerHeight;
    }
  
    drawTriangle(x, y, color, inverted = false) {
      this.context.beginPath();
      this.context.moveTo(x, y);
      this.context.lineTo(inverted ? x - 22 : x + 22, y + 11);
      this.context.lineTo(x, y + 22);
      this.context.fillStyle = `rgb(${color}, ${color}, ${color})`;
      this.context.fill();
      this.context.closePath();
    }
  
    getColor() {
      return this.colors[Math.floor(Math.random() * this.colors.length)];
    }
  
    drawBackground() {
      this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
      for (let x = 0; x < this.cols; x++) {
        for (let y = 0; y < this.rows; y++) {
          const eq = x % 2;
          const destY = eq === 1 ? Math.round((y - 0.5) * 24) : y * 24;
          this.drawTriangle(x * 24 + 2, destY, this.getColor());
          this.drawTriangle(x * 24, destY, this.getColor(), true);
        }
      }
    }
  
    animate() {
      // アニメーションの中断を防ぐために、アニメーションフレームIDをキャンセルします。
      if (this.animationFrameId) {
        cancelAnimationFrame(this.animationFrameId);
      }
  
      const animateLoop = () => {
        this.animationFrameId = requestAnimationFrame(animateLoop);
        const x = Math.floor(Math.random() * this.cols);
        const y = Math.floor(Math.random() * this.rows);
        const eq = x % 2;
        const color = this.getColor();
  
        if (eq === 1) {
          this.drawTriangle(x * 24, Math.round((y - 0.5) * 24), color, true);
        } else {
          this.drawTriangle(x * 24 + 2, y * 24, color);
        }
      };
  
      this.animationFrameId = requestAnimationFrame(animateLoop);
    }
  }
  
  document.addEventListener('DOMContentLoaded', () => {
    const pattern = new LivePattern();
    pattern.init();
  });