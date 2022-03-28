import streamlit as st
import Preprocessor
import Helper
import matplotlib.pyplot as plt
import plotly.express as px

st.sidebar.title('WhatsApp Chat Analyzer')

uploaded_file=st.sidebar.file_uploader('Choose a file')
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue() 
    data=bytes_data.decode('utf-8') 
    df=Preprocessor.preprocessing(data)

    user_list = df['user'].unique().tolist() 
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, 'Overall') 

    selected_user = st.sidebar.selectbox('Show analysis wrt', user_list) 

    if st.sidebar.button('Start Analysis'):  
        number_of_messages, number_of_emojis, number_of_medias, number_of_links = Helper.fetch_stats(selected_user, df)
        st.title('Top Statistics') 
        col1, col2, col3, col4 = st.columns(4) 
        with col1:
            st.header('Total Message') 
            st.header(number_of_messages)
        with col2:
            st.header('Total Emoji')
            st.header(number_of_emojis)
        with col3:
            st.header('Total Media')
            st.header(number_of_medias)
        with col4:
            st.header('Total Hyperlinks')
            st.header(number_of_links)

        st.title('Timeline')

        st.header('Monthly Timeline')
        month_timeline=Helper.monthly_timeline(selected_user,df)
        st.dataframe(month_timeline)
        fig, ax = plt.subplots()
        ax.plot(month_timeline['time'],month_timeline['message'],color='blue')
        plt.xticks(rotation=50)
        plt.xlabel('Months',fontsize=15)
        plt.ylabel('Number of Messages',fontsize=15)
        st.pyplot(fig)

        st.header('Daily Timeline')
        day_timeline=Helper.daily_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(day_timeline['only_date'],day_timeline['message'], color='red')
        plt.xticks(rotation=50)
        plt.xlabel('Dates',fontsize=15)
        plt.ylabel('Number of Messages',fontsize=15)
        st.pyplot(fig)

        st.title('Activity Map')

        st.header('Most Active Day')
        active_day=Helper.week_activity_map(selected_user,df)
        fig, ax = plt.subplots()
        ax.bar(active_day.index,active_day.values, color='green')
        plt.xlabel('Days',fontsize=15)
        plt.ylabel('Number of Messages',fontsize=15)
        st.pyplot(fig)

        st.header('Most Active Month')
        active_month = Helper.month_activity_map(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(active_month.index, active_month.values,color='orange')
        plt.xlabel('Months', fontsize=15)
        plt.ylabel('Number of Messages', fontsize=15)
        st.pyplot(fig)

        if selected_user == 'Overall':

            st.title('Most Active Users')
            most_active_users_df, percentage_df = Helper.fetch_most_active_users(df)
            fig, ax = plt.subplots()
            ax.barh(most_active_users_df.index, most_active_users_df.values,color='magenta')
            plt.xlabel('Number of Messages',fontsize=15)
            plt.ylabel('Users',fontsize=15)
            st.pyplot(fig) 

            values = percentage_df['Percent']
            names = percentage_df['User']
            fig = px.pie(percentage_df, values=values, names=names)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig)

        st.title('Word Cloud')
        wordcloud_image = Helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud_image,interpolation='bilinear')
        plt.axis('off')
        st.pyplot(fig)

        st.title("Most Common Emoji ")
        emoji_df = Helper.most_used_emoji(selected_user, df)
        values=emoji_df['Count']
        names=emoji_df['Emoji']
        fig = px.pie(emoji_df, values=values, names=names)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig)