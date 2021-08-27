import streamlit as st
from PIL import Image
import helper as help
import io
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

title_img=Image.open('header.jpg')
end_img=Image.open('workflow.jpg')
guide_img=Image.open('guideline2.jpg')
demo_img=Image.open('demo.jpg')
st.image(title_img)

st.markdown('''
WhatsApp is a free messaging application. According to [WhatsApp 2021 user statistics](https://backlinko.com/whatsapp-users)
 people in India using WhatsApp is larger than any country [390.1 million users]
  ''')
st.markdown('Analysing WhatsApp chats may lead to many surprising insights')
st.image(guide_img)

file=st.file_uploader('select your "WhatsApp Chat with _name_.txt" file',type=['txt'])
if file!=None:
 raw_text=io.TextIOWrapper(file,encoding='utf-8')
 chats=raw_text.readlines()

 df=help.list_to_DF(chats)
 df=help.data_preperation(df)


 col1,col2=st.columns([1.5,1])

 with col1:
     st.write(help.linepolar(df))
 with col2:
     st.write(help.histogram(df))

 col1,col2=st.columns([.3,1])
 with col1:
     st.markdown('Its funny that i was wondering whether these emojis had any sentimental feelings')
 with col2:
     st.write(help.treemap(df))

 st.subheader('Calender Plot')
 st.markdown('This Calender talks the intensity of the chat conversation in each day of the year by month')
 st.write(help.calmapp(df))

 st.subheader('Most Frequent Word Plot')
 st.markdown('Even i have no idea on what sense these most frequently used words can give you about your chat conversation')
 st.write(help.plott(help.get_wordcloud(df)))

 st.subheader('WorkFlow')
 st.image(end_img)

 with st.expander('About'):
     col1,col2,col3=st.columns(3)

     with col1:
         st.subheader('Developer Contact')
         st.markdown('we love to hear your feedback or incase any suggestions, mail me at akhi_mwon@gmail.com')

         st.subheader('info')
         st.markdown('released on 22 june 2021')

         st.subheader('App Permission')
         st.markdown('WhatsApp Chat Analysis may require permission to read your device internal storage')

     with col2:

         st.subheader('a_t logics')
         st.markdown('a_t logics is a non profitable company owned and maintained by Mr.Akhil Tony')

         st.subheader('Licence')
         st.markdown('a_t logics is currently running as a non recognized software company')

     with col3:
         st.subheader('Acknowledgements')
         st.markdown('Thanks to my dearest friend Sona Martin for her help and support')
else:
 if st.button('Demo'):
  st.image(demo_img)
