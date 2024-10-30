import streamlit as st 


PATH = 'https://gpt4all.io/models/ggml-gpt4all-j.bin'
import streamlit as st
from gpt4allj import Model
from streamlit_option_menu import option_menu
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(layout='centered')

model = Model('https://gpt4all.io/models/ggml-gpt4all-j.bin')

def show_messages(text):
    
    messages_str = [
        f"{_['role']}: {_['content']}" for _ in st.session_state["messages"][1:]
    ]
    text.text_area("Chat", value=str("\n".join(messages_str)), height=150)
    


BASE_PROMPT = [{"role": "AI", "content": "You are an AI expert who helps researchers."}]



if "messages" not in st.session_state:
    st.session_state["messages"] = BASE_PROMPT

st.markdown(""" <style> 
            h4 {margin:0; padding:0}
           
            .font {
                    font-family: 'Verdana'; color: #000;
                    margin-bottom:0} 
                
    textarea {
                    font-size: 1.15rem !important;
                    height:250px !important;
                    
                }
    textarea p{ font-size:1.15rem !important}
    .st-emotion-cache-jkfxgf p {font-size: 1.25rem !important;
    }
    
    
                    </style> """, unsafe_allow_html=True)

container = stylable_container(key="red_button",
        css_styles="""
        
           button {
               background-color: red;
               color: white;
               border-radius: 20px;
           }
            
           
            

                               """,
    )
with container:
    st.markdown('<h1 class="font">GPT4ALLJ AI Paper/Panel Topic Generator</h1>', unsafe_allow_html=True)
   


    text = st.empty()
    show_messages(text)

    prompt = st.text_input("Prompt:", value="Generate cutting-edge AI paper ideas for a conference presentation . . .")
    
    if st.button("Send"):
        with st.spinner("Generating response..."):
            st.session_state["messages"] += [{"role": "You", "content": prompt}]
            print(st.session_state["messages"][-1]["content"])
            message_response = model.generate(st.session_state["messages"][-1]["content"])
            st.session_state["messages"] += [
                {"role": "AI", "content": message_response}
            ]
            show_messages(text)

    if st.button("Clear Chat"):
        st.session_state["messages"] = BASE_PROMPT
        show_messages(text)
    st.markdown('*Chatbot code adapted from : https://github.com/ajvikram/streamlit-gpt')
   
    st.markdown("""<h4>Caveats</h3><p style="font-size:1rem">For experimentation purposes only. The organizers cannot guarantee the veracity of outputs. This model does not record chat data or any personal information.</p><p>See <a href="https://huggingface.co/nomic-ai/gpt4all-j">GPT4All-J Model Card</a> for more information.</p><h4>GPT4All Paper</h4><p>Anand, Y., Nussbaum, Z., Duderstadt, B., & Schmidt, B. M. (n.d.). GPT4All-J: An Apache-2 Licensed Assistant-Style Chatbot.
</p>""",unsafe_allow_html=True)


# elif choose == "Contact":
#     st.markdown(""" <style> .font {
#             font-size:30px ; font-family: 'Cooper Black'; color: #02ab21;} 
#             </style> """, unsafe_allow_html=True)
#     st.markdown('<p class="font">Contact </p>', unsafe_allow_html=True)
#     st.header('')
#     st.write("")
    
    
    
    
    
    
    
