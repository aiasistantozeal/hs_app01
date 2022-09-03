### 事前準備 ###
#
# イベントフォルダに移動して…
#
# python -m venv .hs    ← 新しい仮想環境「.hs」を生成する
#
# .hs\Scripts\activate.bat    ← 新しい仮想環境「.hs」を起動する
# (.hs) > python -m pip install --upgrade pip     ←pip更新
# (.hs) > python -m pip install -r requirements.txt   ← ライブラリの一括インストール
# ※一括インストールは時間がかかりますので(2分～？）休み時間の前などに実行するとよいでしょう
#
# requirements.txt の内容
#   streamlit             ← 毎度、おなじみ
#   typing_extensions     ← これがないとエラーが出ることがあるので一応
#   numpy                 ← 毎度、おなじみ
#   pandas                ← 毎度、おなじみ
#   folium                ←地図表示用
#   streamlit-folium      ←地図表示用
#
# (.hs) > streamlit run testapp01.py    ← Webアプリ（testapp01.py）を起動

### アプリの原案
# 安積疏水の水路に沿ったウォーキングアプリ
# 目的：安積疏水の歴史に触れながら家族団らんや運動の機会を設ける。
# 機能
# ・現在地点をリアルタイムに取得しアプリ上に反映させる。
# ・距離に応じたランク制度を設けて競争心を出しやすくする。
# ・宝探しイベントを開催し、キーワードを集めて景品と交換できるようにする
# 				↓↑OR
# ・目標距離を達成するとポイントがもらえ貯めて景品と交換できる。
# ・エリアが分かれているので地域別もしくは、全エリア制覇型にする。
# 景品
# ・安積疏水は農業などにも利用されてきた歴史があるので
# 県産の野菜や米といった地域にゆかりがあるものや
# 宿泊券、クーポンなどを利用できるようにする。
# クーポン
# ・公共の交通機関で現地に向かう場合に割引されるものがあると利用者が増えそう。
# 管理
# ・県もしくは市区町村に委託する
# （宝探しの問題は地域の学生から募っても面白そう）
#

### やること ###
#
# 1.距離の計算、どのくらい歩いた
# 2.現在地を取得
# 3.チェックポイント　位置情報マッピング
# 参考URL（https://qiita.com/akatin/items/fbc0fe6b23ce514acd0f）
# 参考URL2(https://chayarokurokuro.hatenablog.com/entry/2020/09/02/212350)
# マップアイコンの種類公式（https://glyphsearch.com/?library=glyphicons）
# 4.掲示板機能　風景写真の投稿など

#############
#####^^^^####
###^######^##
###^######^##
#####^^^^####



#
# -----------------------------------------------------

# ライブラリのインポート
from sys import _xoptions
import streamlit as st
from PIL import Image, ImageOps
import numpy as np

# 地図表示ライブラリ
import folium #pip install folium
from streamlit_folium import folium_static # pip install streamlit-folium
# import streamlit as st
import pandas as pd

#------------------------------------------------------
# 中間ポイント用の緯度経度データを作成する
checkPoint = pd.DataFrame(
    data=[[37.4,140.3],
          [37.5,140.3],
          [37.5,140.25],
          [37.5,140.2]],
    index=["中間ポイント１","中間ポイント２","中間ポイント３","中間ポイント４"],
    columns=["x","y"]
)

# 現在地用の緯度経度データ
yourLocation = pd.DataFrame(
    data=[[37.3,140.2]],
    index=["現在地"],
    columns=["x","y"]
)

#-------------------------------------------------------
# データを地図に渡す関数を作成する
def AreaMarker(df,m,rad):
    for index, r in df.iterrows(): 

        # ピンをおく
        folium.Marker(
            location=[r.x, r.y],
            popup=index,
            icon = folium.Icon(color="blue",icon="star")
        ).add_to(m)

        # 円を重ねる
        folium.Circle(
            radius=rad*1000,
            location=[r.x, r.y],
            popup=index,
            color="yellow",
            fill=True,
            fill_opacity=0.07
        ).add_to(m)

# 現在地を地図に渡す関数を作成する
def YourLocationMarker(df,m,rad):
    for index, r in df.iterrows(): 

        # ピンをおく
        folium.Marker(
            location=[r.x, r.y],
            popup=index,
            icon=folium.Icon(color='red',icon="map-marker")
        ).add_to(m)

        # 円を重ねる
        folium.Circle(
            radius=rad*10,
            location=[r.x, r.y],
            popup=index,
            color="red",
            fill=True,
            fill_opacity=0.07
        ).add_to(m)



#サンプル画像の答え合わせ
def quiz(Hoge: str, Hoge_Int: int):
    st.write(Hoge)
    st.write(Hoge_Int)
    st.write("----------------------------")
    st.write("スライダーサンプル")
    quiz_answer = ["A","B","C","D","E","F","G","H"]
    max_value= 8
    min_value= 1
    slider=st.slider("サンプル番号選択", min_value, max_value, min_value, 1)
    st.write(quiz_answer[slider -1])
 

# メインモジュール
def main():
    # 地図表示
    st.title("安積疏水の水路に沿ったウォーキングアプリ") # タイトル
    rad = st.slider('拠点を中心とした円の半径（km）',
                value=40,min_value=5, max_value=50) # スライダーをつける
    st.subheader("各拠点からの距離{:,}km".format(rad)) # 半径の距離を表示
    m = folium.Map(location=[yourLocation["x"],yourLocation["y"]], zoom_start=9) # 地図の初期設定
    AreaMarker(checkPoint ,m,rad) # データを地図渡す
    YourLocationMarker(yourLocation, m,rad) #現在地を地図に渡す
    folium_static(m) # 地図情報を表示


    # アップローダの作成
    uploaded_file = st.file_uploader("Choose a Image...", type="jpg")
  
    # チェックボックス
    You_answer = st.radio(label='画像のタイトル',
                 options=('サンプル１', 'サンプル２'),
                 index=0,
                 horizontal=True,)
    
    # 画像がアップロードされた場合...
    if uploaded_file is not None:
            # 画像を画面に表示
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image.', use_column_width=True)
            st.write("")
            st.write("Classifying...")

            # ユーザの選択の表示
            st.write("----------------------------")
            st.write(f'あなた：は{You_answer}を選択しました。')

            # 関数の使い方
            Hoge = "hoge"
            Hoge_Int = 1
            quiz(Hoge,Hoge_Int)
    else:
        st.write("※画像をアップロードしてください!")



# mainの起動
if __name__ == "__main__":
    main()


#=============================================================================#
# 氏名：佐藤光
# 学校：国際情報工科自動車大学校
# 学科：AIシステム科
# 学年：２年
#
#=============================================================================#
