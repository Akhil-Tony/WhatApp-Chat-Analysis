import streamlit as st
from PIL import Image
from helper import analyse
import io
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

title_img=Image.open('header.jpg')
end_img=Image.open('workflow.jpg')
guide_img=Image.open('guideline2.jpg')

def about():
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
 st.markdown("Or if you want to see a live demonstration ,select any chats from the below dropdown")

 available_chat_files=['No File Selected','WhatsApp Chat with Psychology Pedagogy.txt','WhatsApp Chat with DataScience(MG).txt']

 file = st.selectbox('select from available demo chat files',available_chat_files)

 if file != 'No File Selected':
     f=open(file,encoding='utf-8')
     demo_chat=f.readlines()

     demo_analysis=analyse(demo_chat)
     dash_board(demo_analysis)
     about()

