import streamlit as st

# 页面配置
st.set_page_config(page_title="药药灵", page_icon="💊", layout="centered")

# 自定义样式：让搜索栏更整齐
st.markdown("""
<style>
    .stButton>button { width: 100%; border-radius: 10px; height: 3rem; }
    .reportview-container .main .block-container { padding-top: 2rem; }
    .cate-box { padding: 15px; border-radius: 10px; background-color: #f0f2f6; margin-bottom: 10px;}
</style>
""", unsafe_allow_html=True)

# --- 1. 标题与Logo ---
st.title("💊 药药灵")
st.caption("简洁搜索，安全用药。")

# --- 2. 状态初始化 ---
if 'show_second_slot' not in st.session_state:
    st.session_state.show_second_slot = False
if 'search_clicked' not in st.session_state:
    st.session_state.search_clicked = False

# --- 3. 核心搜索区域 ---
col_input, col_tool = st.columns([4, 1])

with col_input:
    # 第一个输入框
    input_a = st.text_input("药品 A", placeholder="输入药品名称...", label_visibility="collapsed")
    
    # 如果点击了加号，显示第二个输入框
    input_b = ""
    if st.session_state.show_second_slot:
        st.write("➕")
        input_b = st.text_input("药品/食物 B", placeholder="输入另一个对比项...", label_visibility="collapsed")

with col_tool:
    # 拍照和加号按钮并排
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📷"): st.toast("模拟相机启动...")
    with c2:
        if st.button("➕"):
            st.session_state.show_second_slot = not st.session_state.show_second_slot
            st.rerun()
    
    # 大大的搜索按键
    if st.button("🚀 点击搜索"):
        st.session_state.search_clicked = True

# --- 4. 模拟数据库 ---
db = {
    "感冒药": {"banned": ["酒精", "降压药"], "type": "解热镇痛类"},
    "头孢": {"banned": ["酒精"], "type": "抗生素类"},
    "酒精": {"type": "饮品/溶剂"}
}

# --- 5. 结果逻辑展示 ---
if st.session_state.search_clicked:
    st.divider()
    
    # 场景一：双框对比模式
    if st.session_state.show_second_slot and input_a and input_b:
        st.subheader(f"💡 比对：{input_a} vs {input_b}")
        
        # 简单碰撞逻辑
        is_conflict = False
        if input_a in db and input_b in db[input_a]["banned"]:
            is_conflict = True
        
        if is_conflict:
            st.error("❌ 警告：这两者不可同时食用！")
            with st.expander("📝 点击查看学术原理（科普）"):
                st.write(f"【学术原理】{input_a}中的成分会干扰{input_b}的代谢酶，导致血液中毒素堆积...")
                st.write(f"【同类提醒】如果您服用了{input_a}，那么类似的{db[input_a]['type']}也需注意。")
        else:
            st.success("✅ 暂未发现两者有直接冲突。")

    # 场景二：单框搜索模式
    elif input_a and not st.session_state.show_second_slot:
        st.subheader(f"🔍 {input_a} 的禁忌清单")
        if input_a in db:
            st.warning(f"服用{input_a}时，请避开：{', '.join(db[input_a]['banned'])}")
            # 展示同类
            st.info(f"所属类别：{db[input_a]['type']}")
        else:
            st.error("抱歉，暂未收录该药物。")

# 每次操作后重置搜索点击状态，除非需要持久显示
# st.session_state.search_clicked = False
