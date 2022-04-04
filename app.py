import pandas as pd
import streamlit as st

"""
# Linked Insights
"""
import time

metrics = {}


st.caption('First you will need to dowload all the messages on your LinkedIn to CSV file format')


def upload_messages_file():
    uploaded_file = st.file_uploader("Upload her your LinkedIn messages file in CSV format")
    if uploaded_file is not None:
        start_time = time.time()
        dataframe = pd.read_csv(uploaded_file)
        dataframe["DATE"] = pd.to_datetime(dataframe["DATE"])
        dataframe = dataframe.sort_values(by="DATE")

        stop_time = time.time()

        st.write("## Date range")
        st.write("Start time:", dataframe["DATE"].iloc[0].to_pydatetime())
        st.write("End time:", dataframe["DATE"].iloc[-1].to_pydatetime())

        st.subheader("LinkedIn messages metrics")
        metrics["number_of_messages"] = len(dataframe)
        metrics["number_of_conversations"] = len(pd.unique(dataframe['CONVERSATION ID']))
        metrics["number_of_senders"] = len(pd.unique(dataframe['TO']))
        col1, col2, col3 = st.columns([1, 1, 1])


        with col1:
            st.metric(label="Number of conversations", value=metrics["number_of_conversations"])
        with col2:
            st.metric(label="Number of contacts", value=metrics["number_of_senders"])
        with col3:
            st.metric(label="Number of messages", value=metrics["number_of_messages"])

        chart_data = dataframe.groupby(dataframe.DATE.dt.to_period("M")).size()
        st.line_chart(chart_data)

        show = st.checkbox('Show original CSV file')
        if show:
            st.write(dataframe)
        duration = stop_time - start_time
        st.write("loaded in %s sec" % duration)


upload_messages_file()
