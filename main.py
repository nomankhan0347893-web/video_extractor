from dotenv import load_dotenv
from utils.audio_processor import process_input
from core.transcribe import transcribe_all
from core.summarize import summarize,generate_title
from core.extracter import extract_action_items,extract_key_decision,extract_question
from core.Rag_engine import build_rag_chain,ask_question

load_dotenv

def run_pipeline(source: str,language: str = "english")->dict:
    print("starting AI video Assitant")

    chunks=process_input(source)

    transcript=transcribe_all(chunks,language=language)

    print(f"raw transcription (first 300 characters){transcript[:300]}")

    title=generate_title(transcript)

    summary=summarize(transcript)

    action_items=extract_action_items(transcript)

    key_decisions=extract_key_decision(transcript)

    question=extract_question(transcript)

    rag_chain=build_rag_chain(transcript)

    return {"title":title,"summary":summary,"action_items":action_items,"key_decisions":key_decisions,"question":question,"rag_chain":rag_chain}


if __name__ == "__main__":

    source=input("Enter the youtube video URL or path to the audio file: ").strip()
    language=input("language (english/hinglish): ").strip() or "english"
    result=run_pipeline(source,language)

    print(f"\n"+"-"*50)
    print(f"Title: {result['title']}")
    print(f"\n"+"-"*50)
    print(f"Summary: {result['summary']}")
    print("\n"+"-"*50)
    print(f"Action Items: {result['action_items']}")
    print("\n"+"-"*50)
    print(f"Key Decisions: {result['key_decisions']}")
    print(f"\n"+"-"*50)
    print(f"Question: {result['question']}")
    print(f"\n"+"="*50)

   #phase 2
    print("\n Chat with your meeting (type 'exit' to quit)\n")

    rag_chain=result["rag_chain"]

    while True:
        question=input("You: ").strip()
        if question.lower() in ['exit','quit','q']:
            break
        if not question:
            continue
        answer=ask_question(rag_chain,question)
        print(f"AI: {answer}")