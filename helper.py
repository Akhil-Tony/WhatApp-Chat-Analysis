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
import warnings
warnings.filterwarnings('ignore')

#******************************************************************************

d_t_format=['%d/%m/%Y, %I:%M %p','%d/%m/%y, %I:%M %p','%m/%d/%y, %I:%M %p']
date=re.compile('\d{1,2}/\d{1,2}/\d{2,4}')

y=lambda x:x.year
emg_extrct=lambda x:''.join(re.findall(emoji.get_emoji_regexp(),x))
count_w=lambda x:len(x.split())
count_emoji=lambda x:len(list(x))
get_date=lambda x:x.date()
em_name=lambda x:emoji.demojize(x).strip(':')
get_date=lambda x:x.date()
get_hr=lambda x:x.hour

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
            df.iloc[-1].message=df.iloc[-1].message+' '+chat

    return df

def data_preperation(df):

    df.dropna(inplace=True)
    df=df[~(df['message']=='<Media omitted>')]
    df['day']=df['date_time'].apply(pd.Timestamp.day_name)
    df['month']=df['date_time'].apply(pd.Timestamp.month_name)
    df['year']=df['date_time'].apply(y)    #(pd.Timestamp.year)
    df['time']=df['date_time'].apply(pd.Timestamp.time)
    df['emoji_used']=df.message.apply(emg_extrct)
    df['word_count']=df.message.apply(count_w)
    df['emoji_count']=df.emoji_used.apply(count_emoji)

    return df

class analyse:

    stop_words =['message','deleted']+['i','me','my','myself','we','our','ours','ourselves','you',"you're","you've","you'll","you'd",'your','yours','yourself','yourselves','he','him','his','himself','she',
     "she's",'her','hers','herself','it',"it's",'its','itself','they','them','their','theirs','themselves','what','which','who','whom','this','that',"that'll",'these',
     'those','am','is','are','was','were','be','been','being','have','has','had','having','do','does','did','doing','a','an','the','and','but','if','or','because','as','until',
     'while','of','at','by','for','with','about','against','between','into','through','during','before','after','above','below','to','from','up','down','in','out','on','off',
     'over','under','again','further','then','once','here','there','when','where','why','how','all','any','both','each','few','more','most','other','some','such','no','nor',
     'not','only','own','same','so','than','too','very','s','t','can','will','just','don',"don't",'should',"should've",'now','d',
     'll','m','o','re','ve','y','ain','aren',"aren't",'couldn',"couldn't",'didn',"didn't",'doesn',"doesn't",'hadn',"hadn't",'hasn',"hasn't",'haven',"haven't",'isn',"isn't",
     'ma','mightn',"mightn't",'mustn',"mustn't",'needn',"needn't",'shan',"shan't",'shouldn',"shouldn't",'wasn',"wasn't",'weren',"weren't",'won',"won't",'wouldn',"wouldn't"]

    def __init__(self,chats):

        self.df=data_preperation( list_to_DF(chats) )

    #GRAPHS

    # line polar graph
    def linepolar(self):

        date=self.df.date_time.apply(get_date)
        avg_counts=self.df.groupby(['day',date],sort=False).size().unstack('date_time').mean(1)

        fig2=px.line_polar(avg_counts,r=avg_counts,theta=avg_counts.index,line_close=True,title='Activity Level Per WeekDay',
        color_discrete_sequence=px.colors.sequential.Rainbow,template='plotly_dark',height=500,width=500)
        fig2.update_traces(fill='toself')

        return fig2

    # Calender graph
    def calmapp(self):
        temp=self.df.copy()
        temp.date_time=temp.date_time.apply(lambda x:pd.Timestamp(x.date()))
        temp.set_index('date_time',inplace=True)
        cal_df=temp.groupby('date_time').size()#['word_count'].sum()  # <-------- why use a .size() here no of texts make sense
        fg=plt.figure(figsize=(16,10),dpi=80,facecolor='grey')
        year=max(self.df['year'])
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

    #treemap
    def treemap(self):

        emoji_count=dict(Counter(list(''.join(self.df.emoji_used))))
        emoji_count=sorted(emoji_count.items(),key=lambda x:x[1],reverse=True)
        emo_df=pd.DataFrame(emoji_count,columns=['emoji','count'])

        emo_df['name']=emo_df.emoji.apply(em_name)

        fig=px.treemap(emo_df,path=['emoji'],values=emo_df['count'].tolist(),
        title='Emoji TreeMap',hover_data=['count','name'],template='gridon',
        height=620,width=850)
        fig.data[0].hovertemplate='%{label}<br>%{customdata[1]}<br>%{value}'

        return fig

    # histogram
    def histogram(self):

        date=self.df['date_time'].apply(get_date)
        time=self.df['time'].apply(get_hr)
        active_hours=self.df.groupby([date,time]).size().unstack('date_time').mean(1)
        dummy=pd.Series([0]*24)
        active_hours=np.add(dummy,active_hours).fillna(0).astype(int)

        fg=px.histogram(x=active_hours.index,y=active_hours,nbins=24,height=450,width=610,range_x=[0,23],
        title='Activity Level Per Time Hour',color_discrete_sequence=['violet'])
        fg.update_xaxes(nticks=28)
        fg.data[0]['hovertemplate']='Time: %{x}hr<br>%{y} Messages'
        fg.data[0]['showlegend']=True
        fg.update_layout(xaxis_title='Time Hour in 24hour Format',
        yaxis_title='Average Number of Messages',legend_itemclick=False)
        fg.data[0]['name']='Messages'

        return fg

