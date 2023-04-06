import time
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, LLMPredictor, PromptHelper
import pandas as pd
import datetime as dt
import math
import numpy as np
import os
import openai
import streamlit as st
from llama_index import GPTSimpleVectorIndex, GPTListIndex, PromptHelper, LLMPredictor, ServiceContext, SimpleDirectoryReader,  QuestionAnswerPrompt
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI


openai.api_key = os.environ["OPENAI_API_KEY"]

def main():

    st.title("Labor Knowledge Q&A Bot")
    st.text("Labor knowledge bot trained on a limited set of documents.")
# # load from disk
    index = GPTSimpleVectorIndex.load_from_disk('laborlawdocsv2.json')



    # define prompt helper
    # set maximum input size
    max_input_size = 6000
    # set number of output tokens
    num_output = 512
    # set maximum chunk overlap
    max_chunk_overlap = 512

    prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)

    llm_predictor = LLMPredictor(llm=ChatOpenAI(
        temperature=.5, model_name="gpt-3.5-turbo"))
    # llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-003"))
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)


    # Query your index!
    # response = index.query("What is process of filing EEOC complaint?",mode ="embedding", service_context = service_context)
    # print(response)

    with st.form(key='question_form',clear_on_submit=False):
        query_str = st.text_input("Enter your questions here 🎯 ")
        submit_button = st.form_submit_button(label='Ask' )


    QA_PROMPT_TMPL = (

            "Context information is below. \n"
            "---------------------\n"
                    "{context_str}"
            "\n---------------------\n" 
            "Given this information, please answer the question: {query_str}\n"
            )

    QA_PROMPT = QuestionAnswerPrompt(QA_PROMPT_TMPL)



# Query with Spinner
# question = st.text_input("Enter your questions here 💭 ")
# if st.button('Ask'):
#     with st.spinner('Waiting for response...'):
#         response = index.query(question, service_context=service_context)
#         st.write(response)


# Query with Progress Bar
# question = st.text_input("Enter your questions here 🎯 ")
# if st.button('Ask') and question is not None:
#     with st.empty():
#         progress_bar = st.progress(0)
#         for i in range(100):
#             time.sleep(0.1)
#             progress_bar.progress(i + 1)
#         response = index.query(question, response_mode ="compact", service_context=service_context)
#         st.markdown(response)




    if submit_button and query_str is not None:
        with st.empty():
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.15)
                progress_bar.progress(i + 1)
            response = index.query(query_str, response_mode ="compact",  text_qa_template=QA_PROMPT, service_context=service_context)
            st.markdown(response)
    



    st.markdown('##')
    st.markdown('##')
    st.markdown('##')
    st.markdown('##')
    st.markdown('##')
    st.markdown('##')
    st.markdown('##')
    st.markdown('##')
    st.caption('''Experimental - Confirm accuracy.  How does this work?  Several publicaly available documents are trained using Open AI's Embeddings Model. 
               The embeddings model assigns words and phrases a high dimensional vector.  Words and phrases that are similar will have similar vector values. Cosine Similarity is used
               to match vectors from the user input to the closest similarity within the document database. This bot is trained on a very small set of documents (less than 100 pdfs).            
               dspears''')
    st.markdown('##')
    st.markdown('##')
   
    # st.latex(r'''\cos ({\bf t},{\bf e})= {{\bf t} {\bf e} \over \|{\bf t}\| \|{\bf e}\|} = \frac{ \sum_{i=1}^{n}{{\bf t}_i{\bf e}_i} }{ \sqrt{\sum_{i=1}^{n}{({\bf t}_i)^2}} \sqrt{\sum_{i=1}^{n}{({\bf e}_i)^2}} }''')
    # st.code('Cosine Similarity Function')

if __name__ == "__main__":
    main()