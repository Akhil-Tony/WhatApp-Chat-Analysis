import streamlit as st
from PIL import Image
from helper import analyse
import io
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

title_img=Image.open('header.jpg')
end_img=Image.open('workflow.jpg')
guide_img=Image.open('guideline2.jpg')

def about():
     with st.expander('Privacy and Policy'):
         col1,col2,col3=st.columns(3)

         with col1:
             st.subheader('Privacy')
             st.markdown('''This Application is merely a data processing pipeline to help you visualize your chat data,
             This application do not store any of your private information nor any parts the chat data''')

             st.subheader('App Permission')
             st.markdown('For Analysing your local data WhatsApp Chat Analysis may require permission to read your device internal storage')

         with col2:


             st.subheader('Developer Contact')
             st.markdown('In case any issues,suggestions or feedbacks mail me at akhiltony17@gmail.com ')

         with col3:
             st.subheader('Acknowledgements')
             st.markdown('................')
          
def dash_board(object):
    col1,col2=st.columns([1.5,1])

    with col1:
        st.write(object.linepolar())
    with col2:
        st.write(object.histogram())

    col1,col2=st.columns([.3,1])
    with col1:
        st.markdown('Its funny that i was wondering whether these emojis had any sentimental feelings :sleeping:')
    with col2:
        st.write(object.treemap())

    st.subheader('Calender Plot')
    st.markdown('This Calender talks the intensity of the chat conversation in each day of the year by month')
    st.write(object.calmapp())

    st.subheader('Frequency Word Plot')
    st.write(object.plott(object.get_wordcloud()))

    st.subheader('Project WorkFlow')
    st.image(end_img)


st.image(title_img)

st.write('''
To analyse your own personal or group chats follow the below guideline and click the Browse file option :sunglasses:''')

st.image(guide_img)

file=st.file_uploader('select your "WhatsApp Chat with _name_.txt" file',type=['txt'])
if file!=None:
 raw_text=io.TextIOWrapper(file,encoding='utf-8')
 chats=raw_text.readlines()

 main_analysis=analyse(chats)
 dash_board(main_analysis)
 about()

else:
 st.markdown("Or if you only intend to see a live demonstration ,select any chats from the below dropdown")

 available_chat_files=['No File Selected','WhatsApp Chat with BCA 2019 Official.txt']

 file = st.selectbox('select from available demo chat files',available_chat_files)

 if file != 'No File Selected':
     f=open(file,encoding='utf-8')
     demo_chat=f.readlines()

     demo_analysis=analyse(demo_chat)
     dash_board(demo_analysis)
     about()

