import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


load_dotenv()

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embeddings)

llm = ChatGoogleGenerativeAI(model="gemini-flash-lite-latest")

prompt = ChatPromptTemplate.from_template(
    """You are an investment research assistant.
Answer the question using ONLY the context provided below.
If the answer is not in the context, say exactly: "I could not find this information in the provided documents."
Do not use outside knowledge. Be clear and concise.

Context:
{context}

Question: {question}

Answer:"""
)


def answer_question(question: str):

    results = vectorstore.similarity_search(question, k=4)

    context = "\n\n".join(doc.page_content for doc in results)

    final_prompt = prompt.format(context=context, question=question)

    response = llm.invoke(final_prompt)

    print(f"\nQuestion: {question}")
    print(f"\nAnswer:\n{response.text}")

    print("\nSources:")
    sources = set(doc.metadata.get("source", "unknown") for doc in results)
    for s in sources:
        print(f" - {s}")


if __name__ == "__main__":
    answer_question("What are the risks of investing in crypto assets?")