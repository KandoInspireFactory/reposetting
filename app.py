import streamlit as st
import requests
from datetime import datetime
import pandas as pd

# 選択肢を作成
city_code_list = {
    "東京都": "130010",
    "大阪": "270000",
}

# st.titleとst.writeでタイトルと説明を表示
st.title("天気アプリ")
st.write("調べたい地域を選んでください。")

# st.selectboxを使って地域を選択
city_code_index = st.selectbox("地域を選んでください。", list(city_code_list.keys()))

# 選択された地域のcityコードを取得
city_code = city_code_list[city_code_index]

# 選択中の地域を直接表示
st.write(f"選択中の地域: {city_code_index}")

# APIにリクエストするURLを作成
url = f"https://weather.tsukumijima.net/api/forecast/city/{city_code}"

try:
    # 天気情報を取得
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    weather_json = response.json()

    # 現在時刻を取得
    now_hour = datetime.now().hour

    # 現在の降水確率を取得
    if 0 <= now_hour < 6:
        weather_now = weather_json['forecasts'][0]['chanceOfRain']['T00_06']
    elif 6 <= now_hour < 12:
        weather_now = weather_json['forecasts'][0]['chanceOfRain']['T06_12']
    elif 12 <= now_hour < 18:
        weather_now = weather_json['forecasts'][0]['chanceOfRain']['T12_18']
    else:
        weather_now = weather_json['forecasts'][0]['chanceOfRain']['T18_24']

    # 現在時刻の降水確率を表示
    st.write(f"現在の降水確率 : {weather_now}")

    # 今日、明日、明後日の降水確率をDataFrameに格納
    df1 = pd.DataFrame(weather_json['forecasts'][0]['chanceOfRain'], index=["今日"])
    df2 = pd.DataFrame(weather_json['forecasts'][1]['chanceOfRain'], index=["明日"])
    df3 = pd.DataFrame(weather_json['forecasts'][2]['chanceOfRain'], index=["明後日"])

    # DataFrameを結合して表示
    df = pd.concat([df1, df2, df3])
    st.dataframe(df)

except requests.exceptions.RequestException as e:
    st.error(f"天気情報の取得中にエラーが発生しました: {e}")
except KeyError as e:
    st.error(f"APIレスポンスのデータ構造が予期せぬものでした: {e}")
except Exception as e:
    st.error(f"予期せぬエラーが発生しました: {e}")