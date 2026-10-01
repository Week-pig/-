# app.py
import streamlit as st
from deepseek_2 import chat_stream

st.set_page_config(page_title="DeepSeek Chat", page_icon= "./鲸鱼娘.png")
st.title(" 与 神 对话")

# 1. 初始化对话历史
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是大肥鱼，一个可爱的中文助手，你在回答问题时会使用颜文字或者emoji表达情绪。"}
    ]

# 2. 渲染历史消息（system 不显示）
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 3. 接收输入
prompt = st.chat_input("说点什么...")
if prompt:
    # 显示用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 调用 DeepSeek，流式显示
    with st.chat_message("assistant"):
        try:
            response = st.write_stream(
                chat_stream(st.session_state.messages)
            )
        except Exception as e:
            response = f"出错了：{e}"
            st.error(response)

    # 存回历史
    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )