import streamlit as st

# --- 1. 极致 UI 优化 (药丸圆润风格) ---
st.set_page_config(page_title="药药灵 Pro", page_icon="💊")
st.markdown("""
<style>
    .stTextInput input { border-radius: 30px !important; border: 2px solid #2ecc71 !important; }
    .status-card { padding: 20px; border-radius: 20px; margin: 10px 0; color: white; }
    .danger { background-color: #e74c3c; border-left: 10px solid #c0392b; }
    .warning { background-color: #f39c12; border-left: 10px solid #e67e22; }
    .safe { background-color: #2ecc71; border-left: 10px solid #27ae60; }
    .science-box { background: #f9f9f9; color: #333; padding: 15px; border-radius: 10px; font-size: 0.9em; border: 1px solid #ddd; }
</style>
""", unsafe_allow_html=True)

# --- 2. 医学底层数据库 (多维标签化) ---
# ingredients: 物理成分 | path: 代谢路径 | effect: 药理作用
MED_LIBRARY = [
    {
        "keywords": ["感冒灵", "感康", "泰诺", "百服宁", "氨酚"],
        "display_name": "含‘对乙酰氨基酚’药物",
        "ingredients": ["APAP"], 
        "path": "CYP2E1",
        "effect": "解热镇痛",
        "banned_paths": ["ALCOHOL"], # 不能碰酒
        "science": "学术原理：这类药和酒精都通过肝脏CYP2E1酶代谢。酒会诱导该酶产生毒性物质NAPQI，导致急性肝坏死。此外，严禁与其他含APAP成分的感冒药同服，以免剂量叠加中毒。"
    },
    {
        "keywords": ["头孢", "甲硝唑"],
        "display_name": "双硫仑反应抗生素",
        "ingredients": ["CEPH"],
        "path": "ALDH_INHIBIT", # 抑制乙醛脱氢酶
        "effect": "抗菌",
        "banned_paths": ["ALCOHOL"],
        "science": "学术原理：它会‘锁死’肝脏处理酒精的关键机器（乙醛脱氢酶），导致酒精代谢停留在‘乙醛’阶段。乙醛是有毒的，积聚在体内会引起休克。"
    },
    {
        "keywords": ["酒", "酒精", "藿香正气水"],
        "display_name": "含乙醇物品",
        "ingredients": ["ETHANOL"],
        "path": "ALCOHOL",
        "effect": "溶剂/兴奋",
        "science": "酒精是肝脏代谢的‘大户’，会显著干扰抗生素、感冒药、降压药的正常代谢。"
    }
]

# --- 3. 交互界面 (按你要求的位移逻辑) ---
if 'compare_mode' not in st.session_state: st.session_state.compare_mode = False

st.title("💊 药药灵 Pro")
st.caption("基于‘成分-路径’双重校验的用药安全系统")

# 布局处理
col_a, col_plus = st.columns([4, 1])
with col_a:
    input_a = st.text_input("A", placeholder="输入第一种药名", label_visibility="collapsed")
with col_plus:
    if not st.session_state.compare_mode:
        if st.button("➕"): st.session_state.compare_mode = True; st.rerun()

input_b = ""
if st.session_state.compare_mode:
    # 按钮居中
    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        c1, c2 = st.columns(2)
        do_search = c1.button("🚀 搜索")
        do_photo = c2.button("📷 拍照")
    
    col_b, col_minus = st.columns([4, 1])
    with col_b:
        input_b = st.text_input("B", placeholder="输入第二种药/食", label_visibility="collapsed")
    with col_minus:
        if st.button("➖"): st.session_state.compare_mode = False; st.rerun()
else:
    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        c1, c2 = st.columns(2)
        do_search = c1.button("🚀 搜索")
        do_photo = c2.button("📷 拍照")

# --- 4. 底层判定引擎 (这是核心！) ---
def analyze(text):
    if not text: return None
    for item in MED_LIBRARY:
        if any(kw in text for kw in item["keywords"]):
            return item
    return None

if do_search:
    st.divider()
    m1 = analyze(input_a)
    m2 = analyze(input_b)

    if st.session_state.compare_mode and m1 and m2:
        # 逻辑 1：成分重复检查 (Ingredients Overlap)
        # 只要有两个药的成分标签有任何一个重合，就是重复用药
        overlap = set(m1["ingredients"]) & set(m2["ingredients"])
        
        # 逻辑 2：代谢路径冲突检查 (Path Conflict)
        # 检查 m1 是否禁止 m2 的路径，反之亦然
        conflict = (m2["path"] in m1.get("banned_paths", [])) or (m1["path"] in m2.get("banned_paths", []))

        if overlap:
            st.markdown(f"""<div class="status-card danger">
                <h3>🛑 极度危险：重复用药</h3>
                <p>识别到相同有效成分。这会导致药量翻倍，造成严重肝肾中毒！</p>
                </div>""", unsafe_allow_html=True)
        elif conflict:
            st.markdown(f"""<div class="status-card warning">
                <h3>⚠️ 警告：药效冲突 / 代谢受阻</h3>
                <p>这两者在肝脏中使用同一代谢路径，或药理作用相互抵消。</p>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="status-card safe">
                <h3>✅ 暂未发现明确冲突</h3>
                <p>请遵循医嘱，建议服药间隔 2 小时以上。</p>
                </div>""", unsafe_allow_html=True)
        
        # 统一科普展示
        with st.expander("🔬 点击查看深度学术科普"):
            st.write(f"**关于 {input_a}:** {m1['science']}")
            st.write(f"**关于 {input_b}:** {m2['science']}")

    elif m1: # 单药查询
        st.subheader(f"🔍 {input_a} 的用药须知")
        st.info(f"所属类别：{m1['display_name']}")
        st.warning(f"严禁同服：所有含 {', '.join(m1.get('banned_paths', []))} 的物品，以及同类药物。")
        with st.expander("🔬 查看详细科学原理"):
            st.write(m1['science'])
