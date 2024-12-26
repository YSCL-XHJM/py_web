import streamlit as st
import requests
from bs4 import BeautifulSoup
import jieba
from collections import Counter
import re
from pyecharts.charts import WordCloud, Bar, Line, Pie, Scatter, Radar, Tree
from pyecharts import options as opts
import streamlit.components.v1 as components

# Streamlit页面配置
st.set_page_config(page_title="文本分析工具", page_icon=":memo:", layout="wide")

# Streamlit侧边栏选择器
chart_type = st.sidebar.selectbox("选择图表类型", ["词云", "柱状图", "折线图", "饼图", "散点图", "雷达图", "树形图"])


# 定义图表函数...
def show_wordcloud(word_freq):
    """生成词云图"""
    wc = (
        WordCloud()
        .add("", list(word_freq.items()), word_size_range=[20, 100], shape="circle")
        .set_global_opts(title_opts=opts.TitleOpts(title="词云"))
    )
    return wc

def show_bar_chart(word_freq):
    """生成柱状图，并显示词语和词频"""
    bar = (
        Bar()
        .add_xaxis(list(word_freq.keys()))
        .add_yaxis("词频", list(word_freq.values()), label_opts=opts.LabelOpts(is_show=True))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="词频-柱状图"),
            xaxis_opts=opts.AxisOpts(name="词语", axislabel_opts=opts.LabelOpts(rotate=-45)), # 旋转X轴标签以便阅读
            yaxis_opts=opts.AxisOpts(name="词频")
        )
    )
    return bar

def show_line_chart(word_freq):
    """生成折线图，并显示词语和词频"""
    line = (
        Line()
        .add_xaxis(list(word_freq.keys()))
        .add_yaxis("词频", list(word_freq.values()), label_opts=opts.LabelOpts(is_show=True))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="词频-折线图"),
            xaxis_opts=opts.AxisOpts(name="词语", axislabel_opts=opts.LabelOpts(rotate=-45)),
            yaxis_opts=opts.AxisOpts(name="词频")
        )
    )
    return line

def show_pie_chart(word_freq):
    """生成饼图，并显示词语和词频"""
    pie = (
        Pie()
        .add("", [list(z) for z in zip(word_freq.keys(), word_freq.values())])
        .set_global_opts(title_opts=opts.TitleOpts(title="词频-饼图"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))
    )
    return pie

def show_scatter_chart(word_freq):
    """生成散点图，并显示词语和词频"""
    scatter = (
        Scatter()
        .add_xaxis(list(range(1, len(word_freq)+1)))
        .add_yaxis(
            "词频",
            list(word_freq.values()),
            label_opts=opts.LabelOpts(is_show=True, formatter=lambda x: f"{list(word_freq.keys())[x.data-1]}: {x.value}")
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="词频-散点图"),
            xaxis_opts=opts.AxisOpts(name="词汇排名"),
            yaxis_opts=opts.AxisOpts(name="词频")
        )
    )
    return scatter

def show_radar_chart(word_freq):
    """生成雷达图（注意：雷达图适合展示多个维度的数据，对于词频可能不太适用）"""
    # 取前6个高频词来适应雷达图
    top_6_words = dict(list(word_freq.items())[:6])
    radar = (
        Radar()
        .add_schema(
            schema=[opts.RadarIndicatorItem(name=k, max_=max(top_6_words.values())) for k in top_6_words.keys()]
        )
        .add("词频", [[v for v in top_6_words.values()]], label_opts=opts.LabelOpts(is_show=True))
        .set_global_opts(title_opts=opts.TitleOpts(title="词频-雷达图"))
    )
    return radar


def show_tree_chart(word_freq):
    """生成树形图，并显示词语和词频"""
    # 创建一个根节点，所有词语作为其子节点
    root = {
        "name": "词频",
        "children": [{"name": word, "value": freq} for word, freq in word_freq.items()]
    }

    tree = (
        Tree()
        .add("", [root], label_opts=opts.LabelOpts(is_show=True))
        .set_global_opts(title_opts=opts.TitleOpts(title="词频-树形图"))
    )
    return tree
# 辅助函数将pyecharts图表嵌入到Streamlit中https://www.yjwujian.cn/
def st_pyecharts(chart):
    chart_html = chart.render_embed()
    components.html(chart_html, height=600)


# 文本输入框
url = st.text_input('请输入文章URL:', '')

# 提交按钮
if st.button('提交'):
    if url:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text()

            # 清洗文本数据
            cleaned_text = re.sub(r'\s+', ' ', text).strip()

            # 分词
            words = jieba.lcut(cleaned_text)

            # 过滤掉单个字符的词语 - 仅保留两个字及以上的词语
            filtered_words = [word for word in words if len(word) >= 2]

            # 统计词频
            word_counts = Counter(filtered_words)

            # 统计词频并限制为前20个高频词
            top_words = dict(word_counts.most_common(20))

            # 调试信息输出
            st.write(f"Top 20 Words: {top_words}")

            # 根据用户选择显示不同的图表
            chart_func_map = {
                "词云": show_wordcloud,
                "柱状图": lambda wf: show_bar_chart(wf),
                "折线图": lambda wf: show_line_chart(wf),
                "饼图": lambda wf: show_pie_chart(wf),
                "散点图": lambda wf: show_scatter_chart(wf),
                "雷达图": lambda wf: show_radar_chart(wf),
                "树形图": lambda wf: show_tree_chart(wf),
            }

            selected_chart_func = chart_func_map.get(chart_type)
            if selected_chart_func:
                chart = selected_chart_func(top_words)
                st_pyecharts(chart)
            else:
                st.write("所选图表类型暂不支持，请重新选择。")

        except Exception as e:
            st.error(f"发生错误: {e}")

# 运行Streamlit应用
if __name__ == '__main__':
    st.write("请在上面输入文章URL并点击提交开始分析。")
#streamlit run D:\pythonpro\实训1\app.py