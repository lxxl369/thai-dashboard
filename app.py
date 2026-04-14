import streamlit as st
import pandas as pd

# 设置网页基本信息
st.set_page_config(page_title="泰国店铺销量看板", layout="wide", page_icon="📊")

st.title("📊 泰国店铺 (Kreain Nature) - Top 10 销量看板")
st.write("数据自动从最新的 FastMoss 报表中抓取渲染。")

# 1. 读取数据
@st.cache_data
def load_data():
    # 自动尝试读取 data.csv 或 data.xlsx
    try:
        df = pd.read_csv("data.csv")
    except Exception:
        try:
            df = pd.read_excel("data.xlsx")
        except Exception:
            st.error("未找到数据文件！请确保您上传了名为 data.csv 的文件。")
            return pd.DataFrame()
    
    # 提取销量并转化为数字，取前 10 名
    df['[28天]销量'] = pd.to_numeric(df['[28天]销量'], errors='coerce').fillna(0)
    top_10 = df.sort_values(by='[28天]销量', ascending=False).head(10)
    return top_10

df_top10 = load_data()

if not df_top10.empty:
    # 2. 绘制顶部柱状图
    st.subheader("📈 销量趋势一览")
    chart_data = df_top10[['商品标题', '[28天]销量']].set_index('商品标题')
    st.bar_chart(chart_data)

    st.divider() # 分割线

    # 3. 动态展示带图片的商品详情
    st.subheader("📦 排行榜详细图文")
    rank = 1
    for index, row in df_top10.iterrows():
        # 使用 Streamlit 的列布局，左边图片，右边文字
        col1, col2 = st.columns([1, 4]) 
        
        with col1:
            img_url = str(row.get('商品图片链接', ''))
            if img_url.startswith('http'):
                st.image(img_url, use_container_width=True)
            else:
                st.info("暂无图片")
                
        with col2:
            st.markdown(f"### Top {rank}")
            st.write(f"**商品标题:** {row.get('商品标题', '未知')}")
            st.write(f"**28天总销量:** <span style='color:red; font-size:20px; font-weight:bold;'>{int(row['[28天]销量'])}</span> 件", unsafe_allow_html=True)
        
        st.markdown("---")
        rank += 1