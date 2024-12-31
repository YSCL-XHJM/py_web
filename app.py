import streamlit as st
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import jieba
from collections import Counter
from pyecharts.charts import WordCloud, Bar, Line, Pie, Scatter, TreeMap, Funnel
from pyecharts import options as opts
import plotly.express as px
import pandas as pd
import numpy as np
import altair as alt
import streamlit.components.v1 as components


# Helper function to fetch and parse the URL content with enhanced error handling
def fetch_text_from_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = Request(url=url, headers=headers)
        response = urlopen(req)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        text = ''.join(soup.stripped_strings)
        return text
    except Exception as e:
        st.error(f"Error fetching the URL: {e}")
        return ""


# Function to tokenize and count word frequency
def tokenize_and_count(text):
    words = jieba.lcut(text)
    filtered_words = [word for word in words if len(word) >= 2]  # Only consider two characters or more as a word
    word_counts = Counter(filtered_words)
    return word_counts


# Initialize session state variables
if 'text' not in st.session_state:
    st.session_state.text = ""
if 'word_counts' not in st.session_state:
    st.session_state.word_counts = None

# Streamlit app layout
st.title("Word Cloud Generator")

url = st.text_input("Enter article URL:")
if st.button("Fetch and Analyze"):
    with st.spinner('Fetching and analyzing...'):
        text = fetch_text_from_url(url)
        if text:
            st.success("Text fetched successfully!")
            st.session_state.text = text
            st.session_state.word_counts = tokenize_and_count(text)

if st.session_state.word_counts is not None:
    # 获取词频最高的前20个词
    top_20_words = st.session_state.word_counts.most_common(20)

    # 对这20个词按频率升序排序
    sorted_top_20_asc = sorted(top_20_words, key=lambda item: item[1])

    # Show top 20 words in ascending order of frequency
    st.write("Top 20 Words (Ascending Order by Frequency):")
    st.table(pd.DataFrame(sorted_top_20_asc, columns=['Word', 'Frequency']))


    # Sidebar with chart selection
    chart_type = st.sidebar.selectbox(
        "Select Chart Type",
        [
            "Word Cloud",
            "Scatter",
            "Bar Chart",
            "Line Chart",
            "Pie Chart",
            "Scatter Chart",
            "Funnel"
        ]
    )

    min_freq = st.sidebar.slider("Filter words with minimum frequency:", 1, max(st.session_state.word_counts.values()),
                                 1)

    filtered_word_counts = {k: v for k, v in st.session_state.word_counts.items() if v >= min_freq}
    df = pd.DataFrame(list(filtered_word_counts.items()), columns=['word', 'freq'])

    # Plot selected chart type
    if chart_type == "Word Cloud":
        wordcloud = WordCloud()
        wordcloud.add("", list(filtered_word_counts.items()), word_size_range=[20, 100], shape="circle")
        wordcloud.set_global_opts(title_opts=opts.TitleOpts(title="Word Cloud"))
        components.html(wordcloud.render_embed(), width=800, height=600)

    elif chart_type == "Scatter":
        fig = px.scatter(df, x='word', y='freq', size='freq', text='word', size_max=60)
        fig.update_traces(textposition='top center')
        fig.update_layout(showlegend=False, title="Scatter Plot Word Cloud")
        st.plotly_chart(fig)

    elif chart_type == "Bar Chart":
        bar = Bar()
        bar.add_xaxis(list(filtered_word_counts.keys()))
        bar.add_yaxis("", list(filtered_word_counts.values()))
        bar.set_global_opts(title_opts=opts.TitleOpts(title="Bar Chart"))
        components.html(bar.render_embed(), width=800, height=600)

    elif chart_type == "Line Chart":
        line = Line()
        line.add_xaxis(list(filtered_word_counts.keys()))
        line.add_yaxis("", list(filtered_word_counts.values()))
        line.set_global_opts(title_opts=opts.TitleOpts(title="Line Chart"))
        components.html(line.render_embed(), width=800, height=600)

    elif chart_type == "Pie Chart":
        pie = Pie()
        pie.add("", list(filtered_word_counts.items()))
        pie.set_global_opts(title_opts=opts.TitleOpts(title="Pie Chart"))
        components.html(pie.render_embed(), width=800, height=600)

    elif chart_type == "Scatter Chart":
        scatter = Scatter()
        scatter.add_xaxis(list(filtered_word_counts.keys()))
        scatter.add_yaxis("", list(filtered_word_counts.values()))
        scatter.set_global_opts(title_opts=opts.TitleOpts(title="Scatter Chart"))
        components.html(scatter.render_embed(), width=800, height=600)


    elif chart_type == "Funnel":
        funnel = Funnel()
        funnel.add("", list(filtered_word_counts.items()))
        funnel.set_global_opts(title_opts=opts.TitleOpts(title="Funnel"))
        components.html(funnel.render_embed(), width=800, height=600)