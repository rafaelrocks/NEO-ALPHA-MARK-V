import sqlite3
import pandas as pd
import streamlit as st

st.set_page_config(page_title="NEO Alpha Dashboard", layout="wide")
st.title("🤖 NEO Alpha Dashboard")

conn = sqlite3.connect("neo_alpha.db")
df = pd.read_sql("SELECT * FROM chats", conn)
if df.empty:
    st.warning("No chats yet, talk to NEO Alpha first")
    st.stop()

df["time"] = pd.to_datetime(df["time"])
df["day"] = df["time"].dt.date

a, b, c = st.columns(3)
a.metric("Total messages", len(df))
b.metric("You said", int((df.who == "You").sum()))
c.metric("Days active", df["day"].nunique())

st.subheader("Messages per day")
st.bar_chart(df.groupby("day").size())

st.subheader("Busiest hours")
st.bar_chart(df.groupby(df["time"].dt.hour).size())

st.subheader("Your most-used words")
skip = {"that", "this", "what", "with", "have", "like", "from", "your", "about", "neo", "alpha", "please"}
words = df[df.who == "You"].message.str.lower().str.findall(r"[a-z']{4,}").explode().dropna()
words = words[~words.isin(skip)]
st.bar_chart(words.value_counts().head(10))

st.subheader("Latest chats")
st.dataframe(df.sort_values("time", ascending=False).head(15)[["time", "who", "message"]])