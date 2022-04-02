import streamlit as st
import preprocessor
import matplotlib.pyplot as plt
import task
import time
import emoji
import seaborn as sns

st.sidebar.title("whatsapp chat analyser")
uploaded_file=st.sidebar.file_uploader(label="Upload Whatsapp Chat")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    #st.text(data)
    df = preprocessor.preprocess(data)
    #st.dataframe(df)
    userlist=df.User.unique().tolist()
    userlist.remove("Notification")
    userlist.sort()
    userlist.insert(0,"Overall")
    selected_user=st.sidebar.selectbox(label="Select User For Analysis",options=userlist,index=0)
    check=st.sidebar.button(label="Run")


    if check:
        with st.spinner('Wait for it...'):
            time.sleep(5)
        st.success('Done!')
        st.header(f"Showing analysis for {selected_user}")
        col1, col2, col3, col4 = st.columns(4)
        num_msg=task.data_analysis(selected_user,df)
        num_words=task.count_words(selected_user,df)
        num_media=task.media_count(selected_user,df)
        num_links=task.url_count(selected_user,df)

        with col1:
            st.header("Total Messages")
            st.title(num_msg)
        with col2:
            st.header("Total Words")
            st.title(num_words)
        with col3:
            st.header("Media Shared")
            st.title(num_media)
        with col4:
            st.header("Links Shared")
            st.title(num_links)
    # chat analysis

        # col1=st.columns(1)
        y = task.most_busyusers(df)
        x=y.head()
        fig, ax=plt.subplots()
        #
        # with col1:
        st.header("Most Busy Users")
        ax.bar(x.index, x.values, color="#E97451")
        plt.xticks(rotation="vertical")
        ax.set_facecolor("black")

        plt.xlabel("Users")
        # plt.xticks(fontsize=16)
        plt.ylabel("Messages")
        # plt.yticks(fontsize=16)
        st.pyplot(fig)
        with st.expander("Message Contribution in Chat"):
            # st.header("Message Contribution in Chat")
            new_df = round((y / df.shape[0] * 100).reset_index(), 2)
            new_df.rename(columns={'index': 'User', 'User': "No of Messages"}, inplace=True)
            st.dataframe(new_df.style.hide_index())

    #frequent word analysis

        if selected_user!="Overall":
            st.subheader(f"Most Frequent Words Used in The Chat by {selected_user}")
        else:
            st.subheader("Most Frequent Words Used in The Chat ")


        # col1 = st.columns(1)
        #col2, col3
        # with col1:
        mdy_df = task.most_used_words(df, selected_user)
        mdy_df.rename(columns={0: "Word", 1: "Frequency"}, inplace=True)

        fig, ax = plt.subplots()
        ax.set_facecolor("black")
        ax.bar(mdy_df["Word"], mdy_df["Frequency"])
        plt.xticks(rotation="vertical")
        plt.xlabel("Words Used")
        plt.ylabel("Frequency")
        st.pyplot(fig)
        with st.expander("Most Comman Words Used In Chat"):
            st.dataframe(mdy_df)

        cole1,cole2 = st.columns(2)

        with cole1:
            from matplotlib.font_manager import FontProperties

            prop = FontProperties(fname='/System/Library/Fonts/Apple Color Emoji.ttc')
            plt.rcParams['font.family'] = prop.get_family()

            emoji_df = task.emojis(df, selected_user)

            fig, ax = plt.subplots()
            ax.pie(emoji_df[0].head(), labels=emoji_df["index"].head(), autopct='%1.2f%%')
            st.subheader("Emojis Used In The Chat")
            st.pyplot(fig)
        with cole2:
            st.subheader("Emojis Used In The Chat (Tabular Format)")
            st.dataframe(emoji_df.sort_values(by=[0], ascending=False), width=500, height=800)





    #day and time analysis


        st.subheader("Daily Timeline")
        df_daily_timeline= task.daily_timeline(df,selected_user)
        fig, ax = plt.subplots()
        ax.plot(df_daily_timeline["date"], df_daily_timeline["Message"],color="green")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)


    # day vs message

        st.header("Activity Maps")

        col1,col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            day_df = task.day_analysis(df, selected_user)
            day_df = day_df.sort_values(by="Day", ascending=False)
            # st.dataframe(day_df)
            fig, ax = plt.subplots()
            ax.set_facecolor("black")
            ax.bar(day_df["index"], day_df["Day"],color="#FFF89A")
            plt.xticks(rotation="vertical")
            plt.xticks(fontsize=16)
            plt.yticks(fontsize=16)
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            month_df=task.month_analysis(df,selected_user)
            # st.dataframe(month_df)
            fig, ax = plt.subplots()
            ax.set_facecolor("black")
            ax.bar(month_df["index"], month_df["Month"],color="#C1F8CF")
            plt.xticks(rotation="vertical")
            plt.xticks(fontsize=16)
            plt.yticks(fontsize=16)
            st.pyplot(fig)

        if selected_user=="Overall":
            st.subheader("Activity Of The Users")
            user_heatmap = task.heat_map(df, selected_user)
            fig, ax = plt.subplots()
            ax = sns.heatmap(user_heatmap)
            st.pyplot(fig)












