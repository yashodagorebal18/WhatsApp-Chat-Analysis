"""
Advanced Analytics Module for WhatsApp Chat Analysis
Contains sentiment analysis, word frequency, and advanced statistics
"""
import pandas as pd
from textblob import TextBlob
from collections import Counter
import re
import numpy as np

def analyze_sentiment(selected_user, df):
    """
    Analyze sentiment of messages
    Returns positive, negative, neutral percentages
    """
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    sentiments = []
    for message in df['message']:
        blob = TextBlob(message)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            sentiments.append('Positive')
        elif polarity < -0.1:
            sentiments.append('Negative')
        else:
            sentiments.append('Neutral')
    
    sentiment_counts = Counter(sentiments)
    return sentiment_counts

def get_most_active_hours(selected_user, df):
    """Get which hours are most active"""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    hourly_activity = df.groupby('hour').size().reset_index(name='count')
    return hourly_activity.sort_values('count', ascending=False).head(10)

def get_word_frequency(selected_user, df, top_n=20):
    """Get top N frequent words"""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    words = []
    for message in df['message']:
        # Remove URLs and special characters, convert to lowercase
        message = re.sub(r'http\S+|www\S+|https\S+', '', message, flags=re.MULTILINE)
        message = re.sub(r'[^a-zA-Z\s]', '', message)
        word_list = message.lower().split()
        words.extend(word_list)
    
    # Remove common words
    common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                   'of', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had',
                   'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
                   'i', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who', 'when',
                   'where', 'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most',
                   'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
                   'than', 'too', 'very', 'just', 'that', 'this', 'as', 'if', 'me', 'him', 'her'}
    
    filtered_words = [word for word in words if len(word) > 2 and word not in common_words]
    word_freq = Counter(filtered_words).most_common(top_n)
    
    return pd.DataFrame(word_freq, columns=['word', 'frequency'])

def get_conversation_stats(selected_user, df):
    """Get detailed conversation statistics"""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    stats = {
        'total_messages': len(df),
        'avg_message_length': df['message'].str.len().mean(),
        'max_message_length': df['message'].str.len().max(),
        'min_message_length': df['message'].str.len().min(),
        'avg_words_per_message': df['message'].str.split().str.len().mean(),
        'unique_dates': df['only_date'].nunique(),
        'date_range_days': (df['date'].max() - df['date'].min()).days,
        'active_hours': df['hour'].nunique(),
    }
    
    return stats

def get_response_time_analysis(selected_user, df):
    """Analyze average time between messages"""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    df = df.sort_values('date')
    time_diffs = df['date'].diff().dt.total_seconds() / 60  # Convert to minutes
    
    return {
        'avg_response_time_minutes': time_diffs.mean(),
        'median_response_time_minutes': time_diffs.median(),
        'max_gap_minutes': time_diffs.max(),
        'min_gap_minutes': time_diffs.min()
    }

def get_daily_message_distribution(selected_user, df):
    """Get distribution of messages across days of week"""
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    day_dist = df.groupby('day_name').size().reindex(['Monday', 'Tuesday', 'Wednesday', 
                                                        'Thursday', 'Friday', 'Saturday', 'Sunday'])
    return day_dist
