import streamlit as st
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")

# Initialize LLM (replace with your Ollama or OpenAI API key)
llm = ChatGroq(temperature=0,model_name="llama-3.1-70b-versatile")

# Sidebar for interview configuration
st.sidebar.header("Configure Interview")

# Dropdown for selecting tech stack (multiselect)
tech_stack = st.sidebar.multiselect(
    "Select Tech Stack",
    ["Java", "Python", "React", "Node.js", "C++", "SQL"],
    default=["Python"]
)

# Dropdown for selecting years of experience
years_of_experience = st.sidebar.selectbox(
    "Years of Experience",
    range(1, 21),
    index=2  # Default to 3 years of experience
)

# Dropdown for selecting interview duration (in minutes)
interview_duration = st.sidebar.selectbox(
    "Interview Duration (Minutes)",
    [5, 10, 15, 20, 30, 45, 60],
    index=3  # Default to 20 minutes
)

# Start interview button
if st.sidebar.button("Start Interview"):
    # Display the selected options
    st.write(f"Tech Stack: {', '.join(tech_stack)}")
    st.write(f"Years of Experience: {years_of_experience} years")
    st.write(f"Interview Duration: {interview_duration} minutes")
    
    # Prepare the LLM prompt
    prompt = f"""
    You are conducting a {interview_duration}-minute technical interview for a candidate 
    with {years_of_experience} years of experience in {', '.join(tech_stack)}. 
    Ask questions based on this.
    """
    
    # Generate the first interview question using the LLM
    question = llm.invoke(prompt)
    
    st.write(f"Question: {question}")

    # Text area for user's answer
    user_response = st.text_area("Your Answer:")

    if st.button("Submit Answer"):
        # Analyze user's response with LLM
        feedback_prompt = f"Analyze this response: {user_response}. Provide feedback."
        feedback = llm.generate(feedback_prompt)
        st.write(f"Feedback: {feedback}")

else:
    st.write("Configure the interview options in the sidebar and click 'Start Interview' to begin.")
