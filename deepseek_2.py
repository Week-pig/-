# deepseek_client.py
import os
from openai import OpenAI


def _get_api_key():
    # 优先读 Streamlit secrets，其次读环境变量
    key = os.environ.get("DEEPSEEK_API_KEY")
    if key:
        return key
    try:
        import streamlit as st
        return st.secrets["DEEPSEEK_API_KEY"]
    except Exception:
        return None


def _get_client():
    api_key = _get_api_key()
    if not api_key:
        raise RuntimeError(
            "未找到 DEEPSEEK_API_KEY，请在 .streamlit/secrets.toml "
            "或环境变量中设置。"
        )
    return OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )


def chat_stream(messages, model="deepseek-chat"):
    """流式生成器，供 Streamlit 的 st.write_stream 使用"""
    client = _get_client()
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


# 只在命令行直接运行时才进入交互循环，
# 被 import 时不会执行
if __name__ == "__main__":
    client = _get_client()
    messages = [{"role": "system", "content": "you are a helpful assistant"}]
    print("开始对话（输入 exit 退出）：")
    while True:
        word = input("> ")
        if word.strip().lower() in ("exit", "quit"):
            break
        messages.append({"role": "user", "content": word})
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
            stream=False,
        )
        reply = resp.choices[0].message.content
        print(f"大肥鱼: {reply}\n")
        messages.append({"role": "assistant", "content": reply})