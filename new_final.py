import io
import streamlit as st
import pandas as pd
import re
import numpy as np
from collections import Counter
from datetime import datetime
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import calmap
import emoji
from wordcloud import WordCloud,STOPWORDS
import warnings
warnings.filterwarnings('ignore')
#*****************************************************
def dash_board():
    pass
#*****************************************************
d_t_format=['%d/%m/%Y, %I:%M %p','%d/%m/%y, %I:%M %p','%m/%d/%y, %I:%M %p']
date=re.compile('\d{1,2}/\d{1,2}/\d{2,4}')

def list_to_DF(_list,f=0):
    df=pd.DataFrame(columns=['date_time','author','message'])
    for chat in _list:   #LOcK HERE
        if date.match(chat):
            datetym,conversation=re.split('-',chat,maxsplit=1)
            try:
                aut,msg=re.split(':',conversation,maxsplit=1)
            except ValueError:
                aut=np.nan
                msg=str.strip(conversation)
            d=str.strip(datetym)
            try:
                d_t=datetime.strptime(str.strip(datetym),d_t_format[f])
            except ValueError:
                return list_to_DF(_list,f+1)
            df=df.append({'date_time':d_t,'author':aut,'message':str.strip(msg)},ignore_index=True)
        else:
            df.iloc[-1].message = df.iloc[-1].message + ' ' + chat

    return df

def data_preperation(df):

    y=lambda x:x.year
    emg_extrct=lambda x:''.join(re.findall(emoji.get_emoji_regexp(),x))
    count_w=lambda x:len(x.split())
    count_emoji=lambda x:len(list(x))

    df.dropna(inplace=True)
    df['day']=df['date_time'].apply(pd.Timestamp.day_name) #<--- added () to day_name
    df['month']=df['date_time'].apply(pd.Timestamp.month_name)
    df['year']=df['date_time'].apply(y)    #(pd.Timestamp.year)
    df['time']=df['date_time'].apply(pd.Timestamp.time)
    df['emoji_used']=df.message.apply(emg_extrct)
    df['word_count']=df.message.apply(count_w)
    df['emoji_count']=df.emoji_used.apply(count_emoji)

    return df
#*****************************************************
def dash_board(object):

    new_title = '<p style="font-family:sans-serif; color:Green; font-size: 28px;">{}</p>'.format('Analysis for the Author : {}'.format(object.name))
    st.markdown(new_title, unsafe_allow_html=True)

    total_emojis = object.df.emoji_count.sum()
    total_medias = (object.df.message=='<Media omitted>').sum()
    total_messages = len(object.df)

    Overview = pd.DataFrame({'Total no of Messages':total_messages,'Total no of Medias':total_medias,
                             'Total no of Emojis':total_emojis},index=[0])

    st.markdown('Overview')
    st.dataframe(Overview)
    st.write('\n')

    st.subheader('Calender Plot')
    st.markdown('This Calender talks the intensity of the chat conversation in each day of the year by month')
    st.write(object.calmapp())
    st.write('\n')

    st.write(object.linepolar())
    st.write(object.histogram())

    st.write(object.emoji_pie())

    st.subheader('Frequency Word Plot')
    st.write(object.plott(object.get_wordcloud()))

    # st.subheader('Project WorkFlow')
    # st.image(end_img)
#*****************************************************
get_date=lambda x:x.date()
get_hr=lambda x:x.hour
em_name=lambda x:emoji.demojize(x).strip(':')
#*****************************************************
class analyse:

    stop_words =['message','deleted']+list(STOPWORDS)+['Media','omitted']

    def __init__(self,chats,name):

        self.df=chats
        self.name=name

    #GRAPHS

    # line polar graph
    def linepolar(self):

        date=self.df.date_time.apply(get_date)
        avg_counts=self.df.groupby(['day',date],sort=False).size().unstack('date_time').mean(1)

        fig2=px.line_polar(avg_counts,r=avg_counts,theta=avg_counts.index,line_close=True,
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,template='seaborn',height=500,width=500)

        fig2.update_layout(
        title={
        'text': "Activity Level vs WeekDays",
        'y':1,
        'x':0,
        'xanchor': 'left',
        'yanchor': 'top'})

        fig2.update_traces(fill='toself')

        return fig2

    # Calender graph
    def calmapp(self):
        temp=self.df.copy()
        temp.date_time=temp.date_time.apply(lambda x:pd.Timestamp(x.date()))
        temp.set_index('date_time',inplace=True)
        cal_df=temp.groupby('date_time').size()#['word_count'].sum()  # <-------- why use a .size() here no of texts make sense
        fg=plt.figure(figsize=(16,10),dpi=80,facecolor='grey')
        year=max(self.df['year'])    # <---- change here to gain multi year display
        f=calmap.yearplot(cal_df,year=year,monthly_border=True,cmap='terrain_r')
        fg.colorbar(f.get_children()[1],ax=f,orientation='vertical',aspect=10,shrink=.2)

        return fg

    #Word cloud
    def get_wordcloud(self):

        text=' '.join(self.df.message.values)
        email_re=r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        stp_wrds=self.stop_words
        text= re.sub(email_re,'URL',text)

        cloud=WordCloud(width=3000,height=1700,stopwords=stp_wrds,background_color='black',
                        max_words=500,min_word_length=4,colormap='Set1').generate(text)
        return cloud

    #Word cloud plotting
    def plott(self,img):
        a=plt.figure(figsize=(20,10))
        plt.axis('off')
        plt.imshow(img)
        return a

    #emoji pie plot

    def emoji_pie(self):

        emoji_count = dict(Counter(list(''.join(self.df.emoji_used))))
        emoji_count = sorted(emoji_count.items(),key=lambda x:x[1],reverse=True)
        emo_df = pd.DataFrame(emoji_count,columns=['emoji','count'])
        emo_df['name'] = emo_df.emoji.apply(em_name)

        fig = px.pie(emo_df,values='count',names='emoji',title='Emoji Pie Chart')
        fig.update_traces(textposition = 'inside', textinfo='percent+label')
        fig.update_layout( margin = dict(l=5,r=5) )
        fig.update(layout_showlegend=True)

        if len(emo_df) == 0:
            st.subheader('This guy is a Emoji hater !!!')
        else:
            return fig


    # histogram
    def histogram(self):

        date=self.df['date_time'].apply(get_date)
        time=self.df['time'].apply(get_hr)
        active_hours=self.df.groupby([date,time]).size().unstack('date_time').mean(1)
        dummy=pd.Series([0]*24)
        active_hours=np.add(dummy,active_hours).fillna(0).astype(int)

        fg=px.histogram(x=active_hours.index,y=active_hours,nbins=24,height=450,width=610,range_x=[0,23],
        title='Activity Level Per Time Hour',color_discrete_sequence=['skyblue'])
        fg.update_xaxes(nticks=28)
        fg.data[0]['hovertemplate']='Time: %{x}hr<br>%{y} Messages'
        fg.data[0]['showlegend']=True
        fg.update_layout(xaxis_title='Time Hour in 24hour Format',
        yaxis_title='Average Number of Messages',legend_itemclick=False)
        fg.data[0]['name']='Messages'

        return fg

#**********************MAIN PROGRAM*******************************

st.sidebar.subheader('Overview')
st.sidebar.markdown('''This Application is merely a data processing pipeline to help you visualize your chat data,
This application do not store any of your private information nor any parts the chat data''')
st.sidebar.subheader('Contact')
st.sidebar.markdown('In case any issues,suggestions or feedbacks mail me at akhiltony17@gmail.com ')
file = st.file_uploader('select your "WhatsApp Chat with _name_.txt" file',type=['txt'])
st.title('WhatsApp Chat Analysis')

if file == None:

    st.markdown('Showing a Demonstration by analysing BCA 2019 WhatsApp Group Chat')
    Name = 'BCA Official 2019'
    chats = pd.read_csv('BCA_2019.csv')
    #********************************************
    chats.drop(columns='Unnamed: 0',inplace =True)
    chats.date_time = chats.date_time.apply(lambda date : pd.Timestamp(date))
    #********************************************
    chat_dataframe = data_preperation( chats )
    #********************************************
    authors = list(chats.author.unique())
    authors.insert(0,'All')

    selected_author = st.selectbox(label = "SELECT WHO'S STATS YOU WANT TO SEE ?" ,options = authors)
    st.cache(allow_output_mutation=True)
    if selected_author != 'All':

        demo_analysis = analyse( chat_dataframe[  chat_dataframe.author==selected_author  ],   selected_author)
        dash_board(demo_analysis)

    else:

       demo_analysis = analyse(chat_dataframe,Name)
       dash_board(demo_analysis)
else:
    raw_text=io.TextIOWrapper(file,encoding='utf-8')
    chats=raw_text.readlines()
    Name=raw_text.name[18:-4]
    chat_dataframe = data_preperation(    list_to_DF(chats)   )

    authors = list(chat_dataframe.author.unique())
    authors.insert(0,'All')

    selected_author = st.selectbox(label = "SELECT WHO'S STATS YOU WANT TO SEE ?" ,options = authors)
    st.cache(allow_output_mutation=True)
    if selected_author != 'All':

        main_analysis = analyse( chat_dataframe[  chat_dataframe.author==selected_author  ],   selected_author)
        dash_board(main_analysis)

    else:

       main_analysis = analyse(chat_dataframe,Name)
       dash_board(main_analysis)
