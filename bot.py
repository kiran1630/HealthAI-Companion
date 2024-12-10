from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import os
from dotenv import load_dotenv
load_dotenv()
class MedicalAssistanceBot:
    def __init__(self, session_id):
        # Initialize LLM with Groq API
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-70b-versatile")

        # Define prompt template
        self.prompt_template = ChatPromptTemplate.from_messages(
            [
                ("system", """
    You are a medical assistant AI. Provide clear, concise answers to user questions about health. 
    in three lines , Do not diagnose or provide treatment plans. Always include this disclaimer: 
    "This is not professional medical advice. Consult a doctor for a proper diagnosis." only regarding to medical advice
                """),
                ("human", "{history}\nHuman:{input_message}")
            ]
        )

        # Initialize session store for conversation history
        self.store = {}
        self.config = {"configurable": {"session_id": session_id}}

    def get_session_history(self, session_id):
        # Maintain chat history for the session

        if session_id not in self.store:
            self.store[session_id] = InMemoryChatMessageHistory()  # Create history if it doesn't exist
        return self.store[session_id]

    def provide_assistance(self, session_id, input_message):
            conversation = RunnableWithMessageHistory(
                runnable=self.prompt_template | self.llm,
                get_session_history=self.get_session_history,
                input_messages_key="input_message",
                output_messages_key="output",
                history_messages_key="history"
            )

            # Pass current input and maintain history
            print("Session History Before:", self.store.get(session_id, "No history"))
            output = conversation.invoke(
                input={
                    "input_message": input_message,
                "history": self.get_session_history(session_id).messages 
                },
                config=self.config
            )
            print("Session History After:", self.store.get(session_id, "No history"))

            return output.content  


