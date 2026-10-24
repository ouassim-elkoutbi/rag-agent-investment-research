from langchain_core.tools import tool
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()


@tool
def compound_interest(principal: float, annual_rate: float, years: float) -> str:
    """Calculate the future value of an investment with compound interest.

    Args:
        principal: the initial amount invested (e.g. 1000)
        annual_rate: the annual interest rate as a percentage (e.g. 7 for 7%)
        years: the number of years the money is invested

    Returns:
        A string with the final amount after compound growth.
    """
    rate = annual_rate / 100
    final_amount = principal * (1 + rate) ** years
    gain = final_amount - principal
    return (
        f"Starting with {principal:.2f}, at {annual_rate}% per year for {years} years, "
        f"the investment grows to {final_amount:.2f} (a gain of {gain:.2f})."
    )


# Load the vector database once (shared by the tool)
_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
_vectorstore = Chroma(persist_directory="chroma_db", embedding_function=_embeddings)


@tool
def search_investment_documents(query: str) -> str:
    """Search the investment and risk documents to answer conceptual questions
    about investing, risk, diversification, stocks, bonds, ETFs, crypto, scams, etc.
    Use this for 'what is' / 'how does' / 'explain' type questions.

    Args:
        query: the user's question or search terms.

    Returns:
        The most relevant text passages found in the documents.
    """
    results = _vectorstore.similarity_search(query, k=4)
    if not results:
        return "No relevant information found in the documents."
    
    return "\n\n".join(doc.page_content for doc in results)