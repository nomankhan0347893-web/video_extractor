import os
from langchain_mistralai  import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough,RunnableLambda
from core.vector_store import build_vector_store, load_vector_store, get_retriever
from operator import itemgetter

def get_llm():
    return ChatMistralAI(model="mistral-small-latest",mistral_api_key=os.getenv("MISTRAL_API_KEY"),temperature=0.3)

def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])
def build_rag_chain(transcript:str):
    vector_store=build_vector_store(transcript)
    retriever=get_retriever(vector_store,k=4)
    llm=get_llm()

    prompt=ChatPromptTemplate.from_messages([
        ("system","""You are an expert meeting assitant.Answer the user's question
         based only on the meeting transcript context provide below.
         if the answer is not found im=n the context,say:
            i could not find this information .if quoting someone ,mention it clearly.

            context from meeting transcipt:
            {context}
         """,
        ),
        ('human',"{question}"),
    ]
    )
    #full LCEL Rag pipeline
    rag_chain = (
    {
        "context": itemgetter("question") | retriever | RunnableLambda(format_docs),
        "question": itemgetter("question"),
    }
    | prompt
    | llm
    | StrOutputParser()
    )   
    return rag_chain

def load_rag_chain():
    vector_store=load_vector_store()
    retriever=get_retriever()
    llm=get_llm()

    prompt=ChatPromptTemplate.from_messages([("system","""You are an expert meeting assitant.Answer the user's question
             based only on the meeting transcript context provide below.
             if the answer is not found im=n the context,say:
                i could not find this information .if quoting someone ,mention it clearly.
    
                context from meeting transcipt:
                {context}
             """,
            ),
            ('human',"{question}"),
        ]
        )

    #full LCEL Rag pipeline

    rag_chain = (
    {
        "context": itemgetter("question") | retriever | RunnableLambda(format_docs),
        "question": itemgetter("question"),
    }
    | prompt
    | llm
    | StrOutputParser()
    ) 
    return rag_chain

def ask_question(rag_chain,question:str)->str:
    print(f"Question: {question}")
    answer=rag_chain.invoke({"question":question})
    print(f"Answer: {answer}")
    return answer