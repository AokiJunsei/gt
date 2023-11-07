# ページ遷移の関数

### 下記がJSの関数及び遷移先の詳細です。

### URL一覧　画面遷移のみ

ex) gt:map_update の map_updateの部分を下記に記載します。

| url                    | 遷移先のHTMLファイルの名称          |
| ---------------------- | ---------------------------------- |
| map_change  object.pk  | admin_map_change.html              |
| map_delete  object.pk  | admin_map_delete.html              |
| map_register           | admin_map_register.html            |
| user_detail            | adminの利用者情報閲覧ページ         |
| map_detail   gt.pk     | admin_map_detail.html              |


### 関数起動あり

何かしらの関数（フォーム送信等）が起動して、最後に画面遷移するタイプの「関数」と「遷移先」を下記に記します。

| 関数                    | 最終的な遷移先のHTMLファイルの名称          |
| --------------------- - | ----------------------------------------- |
| 「admin_map_register.html 内の関数」 |  admin_top.html               |

```HTML
<form method="POST" enctype='multipart/form-data'>
    {% csrf_token %}
        <table class="table">
        {{ form.as_table }}
        </table>
        <button class="btn btn-primary" type="submit">作成</button>
</form>
```

