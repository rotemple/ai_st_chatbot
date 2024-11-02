import streamlit as st 
import requests, json
from streamlit_option_menu import option_menu
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(layout='centered')


def get_messages(prompt,temp, p, k, max_tokens,repetition):

    url = "https://api.arliai.com/v1/chat/completions"
    
    payload = json.dumps({
      "model": "Meta-Llama-3.1-8B-Instruct",
      "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
        {"role": "assistant", "content": "Hi!, how can I help you today?"},
        {"role": "user", "content": prompt}
      ],
      "repetition_penalty": repetition,
      "temperature": temp,
      "top_p": p,
      "top_k": k,
      "max_tokens": max_tokens,
      "stream": False
    })
    headers = {
      'Content-Type': 'application/json',
      'Authorization': f"Bearer {st.secrets['ARLIAI_API_KEY']}"
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    message = json.loads(response.text)
    content = message['choices'][0]['message']['content']
    
    return content

def show_messages(text):
    messages_str = [
        f"{_['role']}: {_['content']}" for _ in st.session_state["messages"][1:]
    ]
    text.text_area("", value=str("\n".join(messages_str)), height=150)

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
    textarea p{ font-size:1.15rem !important;
                }

    textarea#text_area_2 {min-height:50px !important;
                    height:75px !important;
                    }
    """,unsafe_allow_html=True)
    

container = stylable_container(key="red_button",
        css_styles="""
        
           button {
               background-color: red;
               color: white;
               border-radius: 20px;
           }
        
                               """,
    )

col1,col2 = st.columns(2)

with container:
    st.markdown("""<h1 class="font">Llama 3.1 AI Paper/Panel Topic Generator</h1><h2>Built on <a href="https://www.arliai.com/">ARLI AI</a></h2>""", unsafe_allow_html=True)

with col1:
    st.markdown("## Chat")
    text = st.empty()
    show_messages(text)   
    prompt = st.text_area("Prompt:", value="Generate cutting-edge AI paper ideas for a conference presentation . . .",height=75,key='prompt')

with col2:
    st.markdown('## Model Parameters')
    #params
    temp = st.number_input('temperature',value=0.7)
    p = st.number_input('top p',value=.9)
    k = st.number_input('top k', value=40)
    repetition = st.number_input('repetition_penalty',1.1)
    max_tokens = st.number_input('max token length',value=512)


with st.container():
    if st.button("Send"):
        with st.spinner("Generating response..."):
            st.session_state["messages"] += [{"role": "You", "content": prompt}]
            print(st.session_state["messages"][-1]["content"])
                
            message_response = get_messages(st.session_state["messages"][-1]["content"],temp,p,k,max_tokens,repetition)
            st.session_state["messages"] += [
                    {"role": "AI", "content": message_response}
                ]
            show_messages(text)
    
    if st.button("Clear Chat"):
        st.session_state["messages"] = BASE_PROMPT
        show_messages(text)
    st.markdown('*Chatbot code adapted from : https://github.com/ajvikram/streamlit-gpt')
    
   
    st.markdown("""<h4>Caveats</h3><p style="font-size:1rem">For experimentation purposes only. The organizers cannot guarantee the veracity of outputs or warrant against potentially offensive output. This model does not record chat data or any personal information.</p><p>See <a href="https://huggingface.co/ArliAI">Arli AI Organization Card</a> for more information.</p>.
</p>""",unsafe_allow_html=True)

