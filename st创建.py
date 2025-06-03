import streamlit as st
from zhipuai import ZhipuAI

# 构造一个客户端
client_zp = ZhipuAI(api_key=st.secrets["ZHIPU_API_KEY"]) # 填写您自己的APIKey


def get_zp(text):  
        completion = client_zp.chat.completions.create(       
            model="glm-4-plus",
            messages=[
                {"role": "system", "content": "### 定位：语义歧视分析专家\n ### 任务：请对用户输入的句子进行歧视性分析，并用 1 到 5 之间的数字表示其歧视程度。1 表示没有歧视，5 表示极为歧视。\n ###输出 ：只输出数字，不需要额外解释。"},
                {"role": "user", "content": text}
          ]
        )
        return completion.choices[0].message.content



# 分析函数
def get_discrimination_level(text):
    completion = client_zp.chat.completions.create(
        model="glm-4-plus",
        messages=[
            {"role": "system", "content": "### 定位：语义歧视分析专家\n ### 任务：请对用户输入的句子进行歧视性分析，并用 1 到 5 之间的数字表示其歧视程度。1 表示没有歧视，5 表示极为歧视。\n ###输出 ：只输出数字，不需要额外解释。"},
            {"role": "user", "content": f"{text}"}
        ]
    )
    return completion.choices[0].message.content.strip()

st.set_page_config(page_title="语义歧视分析器", layout="centered")
st.title("🧠 语义歧视分析小工具")
user_input = st.text_area("请输入要分析的句子：", height=100)

# 当用户点击按钮时进行分析
if st.button("开始分111"):
    if user_input.strip() == "":
        st.warning("请输入一句话再分析哦。")
    else:
        with st.spinner("正在分析中..."):
            try:
                score = get_discrimination_level(user_input)
                st.success(f"🧾 歧视程度评分：**{score}**（1~5）")

                if score != "1":
                    try:
                        result = tiaozheng(user_input)
                        st.success(f"调整语气后的句子：{result}")
                    except Exception as e:
                        st.error("出错了，请稍后再试😂")

            except Exception as e:
                st.error("出错了，请稍后再试😂")
