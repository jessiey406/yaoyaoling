import streamlit as st

# 1. 页面配置（标题和图标）
st.set_page_config(page_title="药药灵", page_icon="💊")

# 2. 初始界面：Logo、标题和 Slogan
st.image("https://cdn-icons-png.flaticon.com/512/3028/3028574.png", width=100)  # 找个在线临时图标
st.title("药药灵")
st.subheader("一眼看懂，安全用药")

# 3. 搜索框
query = st.text_input("", placeholder="输入药物名称，例如：感冒药")

# 4. 模拟数据库（你可以根据需要添加）
data = {
    "感冒药": {
        "meds": [
            {"name": "降压药", "effect": "血压骤降", "img": "https://via.placeholder.com/300x200.png?text=Medicine+Box",
             "reason": "某些感冒药含麻黄碱，会抵消降压药效果，造成循环波动。"},
        ],
        "foods": [
            {"name": "白酒/酒精", "effect": "严重肝损伤", "img": "https://via.placeholder.com/300x200.png?text=Alcohol",
             "reason": "对乙酰氨基酚在酒精诱导下会产生有毒代谢物。"},
        ]
    }
}

# 5. 显示搜索结果
if query:
    if query in data:
        st.divider()
        st.header(f"⚠️ 关于“{query}”的禁忌")

        # 药物部分
        st.subheader("🚫 严禁同服的药物")
        for item in data[query]["meds"]:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(item["img"])
            with col2:
                st.warning(f"**{item['name']}**")
                st.write(f"后果：{item['effect']}")
                with st.expander("点开看学术原理"):
                    st.info(item["reason"])

        # 食物部分
        st.subheader("❌ 避开这些食物")
        for item in data[query]["foods"]:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(item["img"])
            with col2:
                st.error(f"**{item['name']}**")
                st.write(f"后果：{item['effect']}")
                with st.expander("点开看学术原理"):
                    st.info(item["reason"])
    else:
        st.error("未找到该药物，请尝试输入‘感冒药’测试。")