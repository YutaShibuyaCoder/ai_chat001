
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key


# st.session_stateを使いメッセージのやりとりと使用回数を保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたは優秀なアシスタントAIです。"}
        ]
if "count" not in st.session_state:
    st.session_state["count"] = 0  # 初期化

# チャットボットとやりとりする関数
def communicate():
    if st.session_state["count"] < 5:  # 使用回数が5以下の時のみ通信
        messages = st.session_state["messages"]

        user_message = {"role": "user", "content": st.session_state["user_input"]}
        messages.append(user_message)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )  

        bot_message = response["choices"][0]["message"]
        messages.append(bot_message)

        st.session_state["user_input"] = ""  # 入力欄を消去
        st.session_state["count"] += 1  # 使用回数を増やす
    else:
        st.warning("チャットの使用回数が上限の5回に達しました。")

# ユーザーインターフェイスの構築
st.title("My AI Assistant")
st.write("ChatGPT APIを使ったチャットボットです。")

user_input = st.text_input("メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
