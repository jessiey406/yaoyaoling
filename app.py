import streamlit as st

# 1. UI 样式美化
st.set_page_config(page_title="药药灵", page_icon="💊", layout="centered")
st.markdown("""
<style>
    .stTextInput input { border-radius: 25px !important; }
    .stButton>button { border-radius: 20px !important; width: 100%; }
    .result-box { padding: 20px; border-radius: 15px; margin-top: 20px; border: 2px solid #ff4b4b; background-color: #fff5f5; }
    .science-box { background-color: #f0f2f6; padding: 15px; border-radius: 10px; font-size: 0.9em; }
</style>
""", unsafe_allow_html=True)

# --- 2. 核心数据库（你可以随时在这里添加新药） ---
# 格式：{"药物名": {"禁忌物": "后果描述", "原理": "学术解释"}}
DRUG_DB = {
    "感冒灵颗粒": {
        "复方氨酚烷胺片": {"effect": "严重肝损伤，甚至危及生命！", "science": "都含有乙酰氨基酚成分，连用将增加肝肾毒性和中枢神经过度反应。"},
            },
    "头孢": {
        "酒精": {"effect": "双硫仑样反应（剧烈头痛、呼吸困难、休克）。", "science": "头孢抑制乙醛脱氢酶，导致酒精代谢产生的‘乙醛’在体内堆积中毒。"},
        "藿香正气水":{"effect":"双硫仑样反应（剧烈头痛、呼吸困难、休克）。","science":"藿香正气水含酒精，头孢类抗生素与酒精发生双硫仑反应。"}
    }
}

# --- 3. 界面状态管理 ---
if 'compare_mode' not in st.session_state:
    st.session_state.compare_mode = False

# --- 4. 标题 ---
st.title("💊 药药灵")
st.caption("首页极简，功能强大。请输入“感冒药”或“头孢”进行测试。")

# --- 5. 交互布局 ---
# 第一行：输入框 A
col_a, col_plus = st.columns([4, 1])
with col_a:
    input_a = st.text_input("药品 A", placeholder="输入第一种药品...", label_visibility="collapsed")
with col_plus:
    if not st.session_state.compare_mode:
        if st.button("➕"):
            st.session_state.compare_mode = True
            st.rerun()

# 动态布局：如果是对比模式，中间插入 [搜索] 和 [拍照]
input_b = ""
if st.session_state.compare_mode:
    # 按钮居中
    c_empty, c_btns, c_empty2 = st.columns([1, 2, 1])
    with c_btns:
        col_s, col_p = st.columns(2)
        do_search = col_s.button("🚀 搜索")
        do_photo = col_p.button("📷 拍照")

    # 第二行：输入框 B
    col_b, col_minus = st.columns([4, 1])
    with col_b:
        input_b = st.text_input("药品 B", placeholder="输入第二种药品/食物...", label_visibility="collapsed")
    with col_minus:
        if st.button("➖"):
            st.session_state.compare_mode = False
            st.rerun()
else:
    # 初始模式：搜索和拍照在下面
    c_empty, c_action, c_empty2 = st.columns([1, 2, 1])
    with c_action:
        col_s, col_p = st.columns(2)
        do_search = col_s.button("🚀 搜索")
        do_photo = col_p.button("📷 拍照")

# --- 6. 核心逻辑判断 ---
if do_search:
    st.divider()

    # 清洗用户输入的文字，去掉空格
    a = input_a.strip()
    b = input_b.strip()

    # 情况一：两个框都有内容（判断是否相冲）
    if st.session_state.compare_mode and a and b:
        # 定义一个变量来存储找到的结果
        found_result = None

        # 第一步：检查 A 的禁忌里有没有 B
        if a in DRUG_DB and b in DRUG_DB[a]:
            found_result = DRUG_DB[a][b]

        # 第二步：如果第一步没找到，检查 B 的禁忌里有没有 A（对称性检查）
        elif b in DRUG_DB and a in DRUG_DB[b]:
            found_result = DRUG_DB[b][a]

        # 展示结果
        if found_result:
            st.error(f"⚠️ 警告：{a} + {b} 判定相冲！")
            st.markdown(f"<div class='result-box'><b>后果：</b>{found_result['effect']}</div>", unsafe_allow_html=True)
            with st.expander("🔬 点击查看学术科普"):
                st.markdown(f"<div class='science-box'>{found_result['science']}</div>", unsafe_allow_html=True)
        else:
            st.success(f"✅ 暂未发现 {a} 与 {b} 有直接冲突，请遵医嘱。")

    # 情况二：只有一个框有内容（显示禁忌列表）
    elif a:
        if a in DRUG_DB:
            st.subheader(f"🔍 {a} 的避忌清单")
            for target, info in DRUG_DB[a].items():
                st.warning(f"❌ 别碰【{target}】：{info['effect']}")
        else:
            st.info("库中暂无此药，请尝试输入‘感冒灵颗粒’。")
