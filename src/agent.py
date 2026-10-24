from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from tools import compound_interest, search_investment_documents

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-flash-lite-latest")

tools = [compound_interest, search_investment_documents]

system_prompt = (
    "You are an investment research assistant for educational purposes. "
    "SUPPORTED REQUESTS: answer general conceptual questions about investing and risk "
    "using the search_investment_documents tool, and use the compound_interest tool for "
    "compound-interest calculations. Base answers only on the tool results and never "
    "invent facts, figures or sources. "
    "UNSUPPORTED REQUESTS: do not tell users whether to buy, sell or hold a specific asset; "
    "do not recommend a specific investment to maximize returns; do not predict future "
    "market movements or prices; do not provide real-time data such as current prices; "
    "do not answer unrelated topics such as weather or cooking. "
    "For any UNSUPPORTED request, or when the answer is not available in your tools, "
    "reply with a message that STARTS with exactly 'ABSTAIN:' followed by a brief reason. "
    "For SUPPORTED requests, never start your answer with 'ABSTAIN:'."
)

agent = create_react_agent(llm, tools, prompt=system_prompt)


def ask(question: str):
    print(f"\nQuestion: {question}\n")

    result = agent.invoke({"messages": [("user", question)]})
    final_answer = result["messages"][-1].text
    print(f"Answer:\n{final_answer}")

def ask_raw(question: str) -> str:
    """Run the agent and return the answer as text (used for evaluation)."""
    result = agent.invoke({"messages": [("user", question)]})
    return result["messages"][-1].text


if __name__ == "__main__":
    ask("How much does 1000 grow at 7% in 10 years?")