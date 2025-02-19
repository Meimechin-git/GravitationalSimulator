# GravitationalSimulater

## 概要
・説明：万有引力をシミュレートするPythonのGUIアプリケーションです。GUIのライブラリはPySideを利用しています。

・制作時間：15時間

## 利用マニュアル
・main.pyを実行してアプリケーションを起動
![Image](https://github.com/user-attachments/assets/713e88eb-a9a1-4030-b6f4-ff696dcc609a)
↑初期画面

・「World Properties」ボタンで世界の設定を指定
![Image](https://github.com/user-attachments/assets/ddea19c3-b087-4200-b95a-ba62baf9026b)
↑世界の設定のタブ

・「New Object」ボタンで新しいオブジェクトを追加
![Image](https://github.com/user-attachments/assets/273a248f-1294-43a0-8917-82dae96af63a)
↑新しいオブジェクトの追加のタブ

・「Start」ボタンで開始「Stop」ボタンで停止
![Image](https://github.com/user-attachments/assets/77aad9a4-04ed-4435-ad69-d564f05dd5c9)
↑「Start」ボタンと「Stop」ボタン

・「Clear」ボタンですべてのオブジェクトを削除
![Image](https://github.com/user-attachments/assets/0498d8dd-fb7e-4343-a99c-70a25eb42a1b)
↑「Clear」ボタンのタブ

## シミュレーションの例
GravitationalSimulaterを用いると惑星の起動などをシミュレートできますが、事前に計算を行う必要があります。
その手間を省きたいという方の為に各パラメーターの例を紹介します。

### 例：恒星と惑星
・世界の設定：初期のまま

・オブジェクト１(恒星)：(質量:1000,半径:100,その他のパラメーター:0)※色は自由

・オブジェクト２(惑星)：(質量:10,半径:10,初期位置X:0,初期位置Y:500,初期速度X:150,初期速度Y:0)※色は自由

・オブジェクト３(惑星)：(質量:10,半径:10,初期位置X:0,初期位置Y:-500,初期速度X:-150,初期速度Y:0)※色は自由