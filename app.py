import streamlit as st
import time

# 页面配置
st.set_page_config(page_title="药药灵", page_icon="💊", layout="centered")

# 极简 CSS：强化“槽位”感
st.markdown("""
<style>
    .slot-box { border: 3px dashed #bdc3c7; border-radius: 20px; padding: 20px; text-align: center; background-color: #f8f9fa; }
    .vs-text { font-size: 40px; font-weight: bold; color: #7f8c8d; margin-top: 20px; }
    .result-card { padding: 20px; border-radius: 15px; border: 2px solid #e74c3c; background-color: #fff5f5; }
</style>
""", unsafe_allow_html=True)

st.title("💊 药药灵")
st.caption("第一种放左边，第二种放右边，相冲一眼便知。")

# 初始化状态
if 'slot1' not in st.session_state: st.session_state.slot1 = ""
if 'slot2' not in st.session_state: st.session_state.slot2 = ""

# --- 第一层：两个巨大的交互槽位 ---
col1, col_vs, col2 = st.columns([5, 1, 5])

with col1:
    st.markdown('<div class="slot-box">物品 A</div>', unsafe_allow_html=True)
    st.session_state.slot1 = st.text_input("输入药名", value=st.session_state.slot1, key="in1", label_visibility="collapsed")
    if st.button("📷 拍照识 A"):
        st.session_state.slot1 = "头孢" # 模拟识别
        st.rerun()

with col_vs:
    st.markdown('<div class="vs-text">+</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="slot-box">物品 B</div>', unsafe_allow_html=True)
    st.session_state.slot2 = st.text_input("输入药/食", value=st.session_state.slot2, key="in2", label_visibility="collapsed")
    if st.button("📷 拍照识 B"):
        st.session_state.slot2 = "白酒" # 模拟识别
        st.rerun()

# --- 第二层：逻辑判断与展示 ---
# 模拟简单的禁忌库
database = {
    ("头孢", "白酒"): "严重双硫仑反应，可能导致休克甚至死亡！",
    ("感冒药", "降压药"): "血压波动过大，增加心血管风险。",
    ("感冒药", "酒精"): "严重肝损伤，乙酰氨基酚中毒风险。"
}

# 清空按钮
if st.button("🔄 全部清空"):
    st.session_state.slot1 = ""
    st.session_state.slot2 = ""
    st.rerun()

st.divider()

# 逻辑：只要有输入就显示
s1 = st.session_state.slot1
s2 = st.session_state.slot2

if s1 and s2:
    # 情况 A：两者都在，判断是否相冲
    st.subheader("🏁 判定结果")
    # 模糊匹配逻辑（简单演示）
    found = False
    for pair, warning in database.items():
        if (s1 in pair[0] or pair[0] in s1) and (s2 in pair[1] or pair[1] in s2):
            st.error(f"⚠️ **{s1}** 与 **{s2}** 相冲！")
            st.markdown(f"<div class='result-card'>{warning}</div>", unsafe_allow_html=True)
            with st.expander("🔬 为什么不能一起吃？"):
                st.info("学术解释：药物成分在肝脏代谢时共用同一路径，导致代谢受阻，产生毒性堆积...")
            found = True
            break
    if not found:
        st.success(f"✅ 暂未发现 **{s1}** 与 **{s2}** 有明确冲突。")

elif s1 or s2:
    # 情况 B：只填了一个，显示该项的所有常见禁忌
    target = s1 if s1 else s2
    st.subheader(f"🔍 关于“{target}”的常见避忌")
    st.info(f"这里会列出所有与 {target} 相冲的常见药物和食物图片。")
    # 这里可以复用你之前的列表展示逻辑
    col_a, col_b = st.columns(2)
    with col_a:
        st.error("避开这些药：")
        st.image("https://via.placeholder.com/150", caption="某种禁忌药盒")
    with col_b:
        st.error("避开这些食物：")
        st.image("https://via.placeholder.com/150", caption="某种禁忌食物")
