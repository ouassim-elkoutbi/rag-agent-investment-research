# Evaluation dataset: test questions with their expected behaviour.
# Each entry has:
#   - "question": what we ask the agent
#   - "type": concept / calculation / out_of_scope
#   - "expected": a clear reference answer (for the LLM judge)
#   - "expected_value" + "tolerance": only for calculation questions (numeric check)

TEST_QUESTIONS = [
    # Conceptual questions (answered using the documents)
    {
        "question": "What is diversification?",
        "type": "concept",
        "expected": "Spreading your investments across different assets or sectors so that if one loses value, others may offset the loss, reducing overall risk.",
    },
    {
        "question": "What is risk in investing?",
        "type": "concept",
        "expected": "The degree of uncertainty and potential financial loss involved in an investment decision.",
    },
    {
        "question": "What is an ETF?",
        "type": "concept",
        "expected": "An exchange-traded fund: a pooled investment that holds a basket of assets and trades on an exchange like a stock.",
    },
    {
        "question": "What are common investment scams?",
        "type": "concept",
        "expected": "Fraud techniques used to trick investors into handing over money, such as fake investments and relationship/trust-based scams.",
    },
    {
        "question": "What is asset allocation?",
        "type": "concept",
        "expected": "Dividing investments among different asset classes such as stocks, bonds and cash, based on risk tolerance and time horizon.",
    },
    {
        "question": "What is a mutual fund?",
        "type": "concept",
        "expected": "A pooled investment vehicle that invests many investors' money into a diversified basket of securities.",
    },
    {
        "question": "What is compound growth?",
        "type": "concept",
        "expected": "Earning returns not only on the original money invested but also on the returns that money has already earned.",
    },
    {
        "question": "What is inflation risk?",
        "type": "concept",
        "expected": "The risk that rising prices reduce the purchasing power of money, especially for fixed returns.",
    },
    {
        "question": "What is a bond?",
        "type": "concept",
        "expected": "A debt security where the investor lends money and receives interest payments and the return of principal.",
    },
    {
        "question": "What is a hedge fund?",
        "type": "concept",
        "expected": "A pooled investment fund that uses more advanced or aggressive strategies, typically for sophisticated investors.",
    },
    {
        "question": "What are crypto assets?",
        "type": "concept",
        "expected": "Digital assets issued or transferred using distributed ledger or blockchain technology, with varying characteristics and risks.",
    },
    {
        "question": "What is the relationship between risk and return?",
        "type": "concept",
        "expected": "Higher potential return generally comes with higher risk; safer investments typically offer lower returns.",
    },
    {
        "question": "What is a stock?",
        "type": "concept",
        "expected": "A share representing partial ownership in a company.",
    },
    {
        "question": "What is private equity?",
        "type": "concept",
        "expected": "Investing in companies that are not publicly traded on a stock exchange.",
    },
    {
        "question": "Why is long-term investing beneficial?",
        "type": "concept",
        "expected": "Because it allows compound growth to build wealth over time and helps ride out short-term market fluctuations.",
    },
    {
        "question": "What are annuities?",
        "type": "concept",
        "expected": "Financial contracts that provide a stream of income, often used for retirement.",
    },
    {
        "question": "How can investors manage risk?",
        "type": "concept",
        "expected": "Through strategies such as diversification and asset allocation, and by matching investments to their time horizon and risk tolerance.",
    },

    # Calculation questions (should use the compound interest tool)
    {
        "question": "What is the final value of 1000 invested at 7% annual compound interest for 10 years?",
        "type": "calculation",
        "expected": "about 1967.15",
        "expected_value": 1967.15,
        "tolerance": 1.0,
    },
    {
        "question": "What is the final value of 5000 invested at 5% for 20 years?",
        "type": "calculation",
        "expected": "about 13266",
        "expected_value": 13266.49,
        "tolerance": 2.0,
    },
    {
        "question": "What is the final value of 2000 invested at 3% annually for 15 years?",
        "type": "calculation",
        "expected": "about 3115",
        "expected_value": 3115.49,
        "tolerance": 2.0,
    },
    {
        "question": "What is the final value of 10000 invested at 8% per year for 5 years?",
        "type": "calculation",
        "expected": "about 14693",
        "expected_value": 14693.28,
        "tolerance": 2.0,
    },
    {
        "question": "What is the final value of 500 invested at 10% for 30 years?",
        "type": "calculation",
        "expected": "about 8724",
        "expected_value": 8724.70,
        "tolerance": 2.0,
    },
    {
        "question": "What is the final value of 100 invested at 6% per year for 40 years?",
        "type": "calculation",
        "expected": "about 1028",
        "expected_value": 1028.57,
        "tolerance": 2.0,
    },
    {
        "question": "What is the final value of 25000 invested at 4% for 12 years?",
        "type": "calculation",
        "expected": "about 40023",
        "expected_value": 40023.37,
        "tolerance": 3.0,
    },

    # Out-of-scope questions (should abstain, NOT make up an answer) 
    {
        "question": "What is the current price of Bitcoin today?",
        "type": "out_of_scope",
        "expected": "should abstain",
    },
    {
        "question": "Should I buy Tesla stock right now?",
        "type": "out_of_scope",
        "expected": "should abstain",
    },
    {
        "question": "What will the stock market do next week?",
        "type": "out_of_scope",
        "expected": "should abstain",
    },
    {
        "question": "Which specific ETF should I invest in for maximum returns?",
        "type": "out_of_scope",
        "expected": "should abstain",
    },
    {
        "question": "What is the weather in Munich today?",
        "type": "out_of_scope",
        "expected": "should abstain",
    },
    {
        "question": "How do I cook a paella?",
        "type": "out_of_scope",
        "expected": "should abstain",
    },
]