#from gradio import ChatInterface
import streamlit as st
from settings import env
from openai import OpenAI

openai = OpenAI(api_key=env.OPENAI_API_KEY, base_url=env.OPENAI_BASE_URL)

#-------------------------------------------------
# System prompt
#-------------------------------------------------
system_prompt = "You are Sophia, a helpful assistant for Deloitte employees. You can answer questions about Deloitte's policies, procedures, and services. You can also provide information about Deloitte's history, culture, and values. You can also provide information about Deloitte's products and services."


# -------------------------------------------------
# Session state
# -------------------------------------------------
def get_messages():
    """Get or initialize the messages session state."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    return st.session_state.messages

# -------------------------------------------------
# Page config
# -------------------------------------------------
st.set_page_config(
    page_title="Sophia | Deloitte",
    layout="wide",
) #Chrome / Edge tab will show: Sophia | Deloitte

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
with st.sidebar:
    st.markdown("## **Deloitte.**  |  **Sophia**")
    st.divider()
    st.button("➕  Start a new chat", use_container_width=True)
    st.button("🕒  Chat history", use_container_width=True)
    st.button("🤖  Agents", use_container_width=True)
   # st.button("💡  Prompt library  NEW", use_container_width=True)
    st.divider()
    st.markdown(
    "<div class='footer'>Sophia &nbsp|&nbsp"
    "<span style='color:#6cc04a'>made by the AEFT Programme</span></div>",
    unsafe_allow_html=True,
    )

    #st.markdown("### 📁 File manager")
    #st.caption("Used space")
    #st.progress(0)
    #st.caption("0.00 MB of 150 MB used")

#-------------------------------------------------
# Header container 
#-------------------------------------------------
with st.container(border= True, horizontal= True):
    st.markdown(
        "**Agent:** Sophia &nbsp;&nbsp; • &nbsp;&nbsp; "
        "**Temperature:** Precise &nbsp;&nbsp; • &nbsp;&nbsp; "
        "**Model:** GPT‑4.1"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;Hello, **Bongamusahlakjd**"
    )

#-------------------------------------------------
# Main chat area container
#-------------------------------------------------
chat_area = st.container(border= True, horizontal= False, height= 379, autoscroll= True)
def refresh_chat_area():
    with chat_area:
        for msg in get_messages():
            if msg["role"] == "user" or msg["role"] == "assistant": #only display user and assistant messages, not system prompt or tools
                with st.chat_message(msg["role"]):
                        st.write(msg['content'])


#-------------------------------------------------
# Chat function to call OpenAI API  
#-------------------------------------------------
def chat(user_input): #chat_history = None)
    if not get_messages(): #if not chat_history, initialize with system prompt
        get_messages().append({"role": "system", "content": system_prompt})
    get_messages().append({"role": "user", "content": user_input}) #append user input to messages before sending to OpenAI API
    response = openai.chat.completions.create(model="gpt-4o-mini", messages=get_messages())
    reply = response.choices[0].message.content
    get_messages().append({"role": "assistant", "content": reply})

#-------------------------------------------------
# Message input container   
#-------------------------------------------------
message_input = st.container(border= True, horizontal= True)
with message_input:
    if user_input := st.text_input(" Send a message"):
        chat(user_input)  # Call the chat function 

#-------------------------------------------------
# Refresh chat area to display new messages after sending user input and receiving assistant response
#-------------------------------------------------
with chat_area:
    refresh_chat_area()