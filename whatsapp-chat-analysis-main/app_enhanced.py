import streamlit as st
import pandas as pd
import preprocessor
import helper
import advanced_analytics
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📱 WhatsApp Chat Analyzer")
st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader("📤 Choose a WhatsApp chat file", type=['txt'])

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Sidebar - User Selection
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("👤 Select User", user_list)

    # Delete simulation state
    if 'deleted_message_ids' not in st.session_state:
        st.session_state.deleted_message_ids = []

    delete_mode = st.sidebar.checkbox("🗑️ Enable delete simulation")
    if delete_mode:
        # Filter by selected user for message listing - EXCLUDE already deleted ones
        messages_for_selection = df[df['user'] == selected_user] if selected_user != 'Overall' else df
        available_messages = messages_for_selection[~messages_for_selection['message_id'].isin(st.session_state.deleted_message_ids)]

        selected_to_delete = st.sidebar.multiselect(
            "Select messages to delete:",
            options=available_messages['message_id'].tolist(),
            format_func=lambda mid: f"{mid}: {available_messages.loc[available_messages['message_id'] == mid, 'message'].iloc[0][:50]}",
            key="delete_selector"
        )

        if st.sidebar.button("✅ Delete Selected"):
            if selected_to_delete:
                st.session_state.deleted_message_ids.extend(selected_to_delete)
                st.session_state.deleted_message_ids = list(set(st.session_state.deleted_message_ids))
                st.sidebar.success(f"✅ {len(selected_to_delete)} message(s) permanently deleted. Total deleted: {len(st.session_state.deleted_message_ids)}")
            else:
                st.sidebar.warning("⚠️ No messages selected to delete.")

        # Show deleted messages count
        if st.session_state.deleted_message_ids:
            st.sidebar.markdown("---")
            st.sidebar.write(f"### 🗑️ Deleted Messages ({len(st.session_state.deleted_message_ids)})")
            
            deleted_df = df[df['message_id'].isin(st.session_state.deleted_message_ids)]
            for _, row in deleted_df.iterrows():
                st.sidebar.caption(f"ID {row['message_id']}: {row['message'][:40]}...")
            
            st.sidebar.markdown("---")
            if st.sidebar.button("🔄 Restore ALL deleted messages"):
                st.session_state.deleted_message_ids = []
                st.sidebar.success("✅ All deleted messages restored! Re-run analysis.")

    # Ensure we always use filtered df for analysis
    if st.session_state.deleted_message_ids:
        filtered_df = df[~df['message_id'].isin(st.session_state.deleted_message_ids)]
    else:
        filtered_df = df

    # Analysis Type Selection
    analysis_type = st.sidebar.radio(
        "📊 Select Analysis Type",
        ["Overview", "Detailed Analytics", "Advanced Insights", "Comparisons"]
    )

    st.sidebar.markdown("---")

    if st.sidebar.button("🔍 Generate Analysis", use_container_width=True):
        
        # Show deletion status if messages are deleted
        if st.session_state.deleted_message_ids:
            st.warning(f"⚠️ **{len(st.session_state.deleted_message_ids)} message(s) are permanently deleted** and excluded from this analysis. Click 'Restore ALL' in the sidebar to recover them.")
        
        if analysis_type == "Overview":
            st.title(f"📊 Chat Overview - {selected_user}")
            
            # Stats Area
            num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, filtered_df)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Messages", num_messages, delta="messages")
            with col2:
                st.metric("Total Words", words, delta="words")
            with col3:
                st.metric("Media Shared", num_media_messages, delta="files")
            with col4:
                st.metric("Links Shared", num_links, delta="links")

            st.markdown("---")

            # Monthly Timeline
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📈 Monthly Timeline")
                timeline = helper.monthly_timeline(selected_user, filtered_df)
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=timeline['time'],
                    y=timeline['message'],
                    mode='lines+markers',
                    line=dict(color='#1f77b4', width=3),
                    marker=dict(size=8)
                ))
                fig.update_layout(
                    xaxis_title="Month",
                    yaxis_title="Number of Messages",
                    hovermode='x unified',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.subheader("📅 Daily Timeline")
                daily_timeline = helper.daily_timeline(selected_user, filtered_df)
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=daily_timeline['only_date'],
                    y=daily_timeline['message'],
                    mode='lines',
                    line=dict(color='#2ca02c', width=2)
                ))
                fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Number of Messages",
                    hovermode='x unified',
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")

            # Activity Maps
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🔥 Most Busy Day")
                busy_day = helper.week_activity_map(selected_user, filtered_df)
                fig = px.bar(x=busy_day.index, y=busy_day.values,
                            labels={'x': 'Day', 'y': 'Messages'},
                            color=busy_day.values,
                            color_continuous_scale='Viridis')
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.subheader("📆 Most Busy Month")
                busy_month = helper.month_activity_map(selected_user, filtered_df)
                fig = px.bar(x=busy_month.index, y=busy_month.values,
                            labels={'x': 'Month', 'y': 'Messages'},
                            color=busy_month.values,
                            color_continuous_scale='Blues')
                st.plotly_chart(fig, use_container_width=True)

            # Heatmap
            st.subheader("🔥 Weekly Activity Heatmap")
            user_heatmap = helper.activity_heatmap(selected_user, filtered_df)
            if not user_heatmap.empty:
                fig, ax = plt.subplots(figsize=(12, 6))
                sns.heatmap(user_heatmap, cmap='YlOrRd', ax=ax, cbar_kws={'label': 'Messages'})
                st.pyplot(fig)
            else:
                st.info("No heatmap data available")

            # Most Busy Users (Group level)
            if selected_user == 'Overall':
                st.markdown("---")
                st.subheader("👥 Most Busy Users in Group")
                x, new_df = helper.most_busy_users(filtered_df)
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    fig = px.bar(x=x.index, y=x.values,
                                labels={'x': 'User', 'y': 'Messages'},
                                color=x.values,
                                color_continuous_scale='Reds')
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.dataframe(new_df, use_container_width=True)

        elif analysis_type == "Detailed Analytics":
            st.title(f"🔬 Detailed Analytics - {selected_user}")
            
            # Emoji Analysis
            st.subheader("😊 Emoji Analysis")
            emoji_df = helper.emoji_helper(selected_user, filtered_df)
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Top Emojis Used**")
                st.dataframe(emoji_df.head(10), use_container_width=True)
            
            with col2:
                if not emoji_df.empty:
                    fig = px.pie(emoji_df.head(10), 
                                values='count', 
                                names='emoji',
                                title="Top 10 Emojis Distribution")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No emojis found in chat")

            st.markdown("---")

            # Word Cloud
            st.subheader("☁️ Word Cloud")
            words_str = " ".join(df[df['user'] == selected_user]['message'] 
                                if selected_user != 'Overall' else df['message'])
            
            if len(words_str) > 0:
                wordcloud = WordCloud(width=800, height=400, 
                                     background_color='white',
                                     colormap='viridis').generate(words_str)
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
            else:
                st.info("Not enough text for word cloud")

            st.markdown("---")

            # Word Frequency
            st.subheader("📊 Top Words Used")
            word_freq = advanced_analytics.get_word_frequency(selected_user, filtered_df, top_n=15)
            if not word_freq.empty:
                fig = px.bar(word_freq, x='word', y='frequency',
                            labels={'word': 'Word', 'frequency': 'Frequency'},
                            color='frequency',
                            color_continuous_scale='Teal')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No words to analyze")

        elif analysis_type == "Advanced Insights":
            st.title(f"💡 Advanced Insights - {selected_user}")
            
            # Conversation Stats
            st.subheader("📈 Conversation Statistics")
            stats = advanced_analytics.get_conversation_stats(selected_user, filtered_df)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Avg Message Length", f"{stats['avg_message_length']:.1f} chars")
            with col2:
                st.metric("Avg Words/Message", f"{stats['avg_words_per_message']:.1f}")
            with col3:
                st.metric("Max Message Length", f"{stats['max_message_length']} chars")
            with col4:
                st.metric("Unique Dates", stats['unique_dates'])

            st.markdown("---")

            # Response Time Analysis
            st.subheader("⏱️ Response Time Analysis")
            response_stats = advanced_analytics.get_response_time_analysis(selected_user, filtered_df)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Avg Response Time", f"{response_stats['avg_response_time_minutes']:.1f} min")
            with col2:
                st.metric("Median Response Time", f"{response_stats['median_response_time_minutes']:.1f} min")
            with col3:
                st.metric("Max Gap", f"{response_stats['max_gap_minutes']:.0f} min")
            with col4:
                st.metric("Min Gap", f"{response_stats['min_gap_minutes']:.1f} min")

            st.markdown("---")

            # Activity by Day of Week
            st.subheader("📅 Activity by Day of Week")
            day_dist = advanced_analytics.get_daily_message_distribution(selected_user, filtered_df)
            fig = px.bar(x=day_dist.index, y=day_dist.values,
                        labels={'x': 'Day', 'y': 'Messages'},
                        color=day_dist.values,
                        color_continuous_scale='Purples')
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("---")

            # Sentiment Analysis
            st.subheader("😊 Sentiment Analysis")
            sentiment_counts = advanced_analytics.analyze_sentiment(selected_user, filtered_df)
            
            if sentiment_counts:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Positive Messages", sentiment_counts.get('Positive', 0))
                with col2:
                    st.metric("Neutral Messages", sentiment_counts.get('Neutral', 0))
                with col3:
                    st.metric("Negative Messages", sentiment_counts.get('Negative', 0))
                
                fig = px.pie(
                    values=list(sentiment_counts.values()),
                    names=list(sentiment_counts.keys()),
                    color_discrete_map={'Positive': '#00cc96', 'Neutral': '#ababab', 'Negative': '#ef553b'},
                    title="Message Sentiment Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)

        elif analysis_type == "Comparisons":
            st.title("🔄 User Comparison Analysis")
            
            if selected_user == 'Overall':
                st.info("Select a specific user for comparison or view all users")
                
                # Compare all users
                st.subheader("Compare All Users")
                user_messages = df[df['user'] != 'group_notification'].groupby('user').size().sort_values(ascending=False)
                
                fig = px.bar(x=user_messages.index, y=user_messages.values,
                            labels={'x': 'User', 'y': 'Messages'},
                            color=user_messages.values,
                            color_continuous_scale='Spectral',
                            title="Messages by User")
                st.plotly_chart(fig, use_container_width=True)
                
                # Word statistics comparison
                st.subheader("Words Count by User")
                word_counts = {}
                for user in user_list[1:]:  # Skip 'Overall'
                    user_df = df[df['user'] == user]
                    words = user_df['message'].str.split().str.len().sum()
                    word_counts[user] = words
                
                word_df = pd.DataFrame(list(word_counts.items()), columns=['User', 'Words'])
                fig = px.bar(word_df, x='User', y='Words',
                            color='Words',
                            color_continuous_scale='Blues')
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(f"Detailed comparison for {selected_user}")
                st.metric("Messages", helper.fetch_stats(selected_user, filtered_df)[0])

else:
    st.title("💬 WhatsApp Chat Analyzer")
    st.markdown("""
    ### Welcome to Advanced WhatsApp Chat Analysis Platform!
    
    This application provides comprehensive analysis of your WhatsApp conversations with:
    
    ✨ **Features:**
    - 📊 **Overview**: Message statistics, timelines, and activity maps
    - 🔬 **Detailed Analytics**: Emoji usage and word clouds
    - 💡 **Advanced Insights**: Sentiment analysis and response times
    - 🔄 **Comparisons**: Compare users and analyze patterns
    
    📝 **How to use:**
    1. Upload a WhatsApp chat export file (.txt)
    2. Select a user to analyze (or view overall)
    3. Choose an analysis type
    4. Click "Generate Analysis"
    
    **Export your chat:**
    - Open WhatsApp > Long press chat > More > Export chat (without media)
    """)

import pandas as pd
