import os
import streamlit as st
import pandas as pd
from scrapp import scrape_website, split_dom_content, cleanBC, extract_body_content
from parse import parse_with_llm
import requests
from datetime import datetime

os.environ["GROQ_API_KEY"] = "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"
os.environ["GOOGLE_API_KEY"] = "AIzaSyC_oCg6ildF7YxMhXR8mXMO2VybhwEcX5Y"
os.environ["NEWS_API_KEY"] = "pub_53500605d985b9a375bbaa4c8af8c3a3378c0"
os.environ["ANTHROPIC_API_KEY"] = "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"
os.environ["OPENAI_API_KEY"] = "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"

st.set_page_config(layout="wide")
query='cybersecurity'
def fetch_cybersecurity_news():
    api_key = os.environ["NEWS_API_KEY"]
    url = f"https://newsdata.io/api/1/news?apikey={api_key}&q={query}&language=en"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['results']
    else:
        return []

def display_news_sidebar():
    st.sidebar.title("Cybersecurity News")
    news = fetch_cybersecurity_news()
    for article in news[:10]:  
        st.sidebar.markdown(f"**{article['title']}**")
        st.sidebar.write(article['description'])
        st.sidebar.markdown(f"[Read more]({article['link']})")
        st.sidebar.markdown("---")

def get_suggested_prompts():
    return [
        "Summarize the main points of the article",
        "List all technical terms and their definitions",
        "Extract dates of significant events mentioned",
        "Identify the primary topic of discussion",
        "Extract all mentioned company names along with their vulnerabilities and critical scores in a tabular form"
    ]


if 'search_history' not in st.session_state:
    st.session_state.search_history = []

st.title("SkrapeMind🧠")


col1, col2 = st.columns([3, 1])

with col1:
    url = st.text_input("ENTER THE URL OF THE WEBPAGE!!")
    model_choice = st.selectbox("Select the model for parsing", ("groq", "gemini","OpenAI","Claude"), index=0)

    if st.button("DIG IN"):
        if url:
            with st.spinner("Spiders are weaving their web... Please wait while I'm gathering the information for you!"):
                dom_content = scrape_website(url)
                body_content = extract_body_content(dom_content)
                cleaned_content = cleanBC(body_content)
                st.session_state.dom_content = cleaned_content
                st.session_state.search_history.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "url": url,
                    "content": cleaned_content
                })

            with st.expander("View DOM content"):
                st.text_area("DOM Content", cleaned_content, height=300)
        else:
            st.warning("Please enter a URL.")

    if "dom_content" in st.session_state:
        suggested_prompts = get_suggested_prompts()
        selected_prompt = st.selectbox("Suggested prompts:", [""] + suggested_prompts)
        parse_description = st.text_area("Describe what you want to learn about:", value=selected_prompt)

        if st.button("Tell Me!!"):
            if parse_description:
                with st.spinner("Analyzing the content... 🧠"):
                    dom_chunks = split_dom_content(st.session_state.dom_content)
                    result = parse_with_llm(dom_chunks, parse_description, model_choice)
                    st.write(result)

                    # Exporting side
                    export_data = pd.DataFrame({
                        'URL': [url],
                        'Timestamp': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                        'Raw Content': [st.session_state.dom_content],
                        'Parsed Result': [result]
                    })
                    csv = export_data.to_csv(index=False)
                    st.download_button(
                        label="Download results as CSV",
                        data=csv,
                        file_name="skrappy_results.csv",
                        mime="text/csv",
                    )
            else:
                st.warning("Please enter a description of what you want to learn.")

with col2:
    st.subheader("Search History")
    if st.session_state.search_history:
        selected_history = st.selectbox(
            "Select a past search:",
            options=range(len(st.session_state.search_history)),
            format_func=lambda i: f"{st.session_state.search_history[i]['timestamp']}: {st.session_state.search_history[i]['url']}"
        )
        st.write(f"URL: {st.session_state.search_history[selected_history]['url']}")
        st.write(f"Timestamp: {st.session_state.search_history[selected_history]['timestamp']}")
        with st.expander("View Content"):
            st.text_area("Content", st.session_state.search_history[selected_history]['content'], height=200)
    else:
        st.write("No search history yet.")


display_news_sidebar()
