"""
This script shows how to create a newsletter based on the latest Arxiv articles.
We're using an easy LangChain implementation to show how to use the different components of LangChain.
Copyright @Kanav Kahol 2023

"""
import os
from dotenv import load_dotenv
from langchain.document_loaders import ArxivLoader
from langchain.agents.agent_toolkits import GmailToolkit
from langchain import OpenAI
import os
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain import LLMChain
from langchain.callbacks import get_openai_callback
import arxiv

load_dotenv()


# Topic of the newsletter you want to write about
query = "chatbots using LLM"

# Set up the ArxivLoader
search = arxiv.Search(
  query = query,
  max_results = 5,
  sort_by = arxiv.SortCriterion.Relevance
)

# Initialize the docs variable
docs = ""

# Add all relevant information to the docs variable
for result in search.results():
    docs += "Title: " + result.title + "\n"
    docs += "Abstract: " + result.summary + "\n"
    docs += "Download URL: " + result.pdf_url + "\n"
    print(result.links)
    for link in result.links:
        docs += "Links: " + link.href + "\n"

# Track cost
with get_openai_callback() as cb:

    # Template for the newsletter
    prompt_newsletter_template = """
    You are a newsletter writer named Dr Sam so write as Dr Sam please. You write newsletters about scientific articles. You introduce the article and show a small summary to tell the user what the article is about.

    You're main goal is to write a newsletter which contains summaries to interest the user in the articles.

    --------------------
    {text}
    --------------------

    Start with the title of the article. Then, write a small summary of the article.

    Below each summary, include the link to the article containing /abs/ in the URL. Write the answer as Dr Sam. Also 
    make the summary to be 300 words and generate recommendations on how a  manager can use
    this information.

    Summaries:

    """

    PROMPT_NEWSLETTER = PromptTemplate(template=prompt_newsletter_template, input_variables=["text"])

    # Set the OpenAI API key
    os.environ['OPENAI_API_KEY'] = os.getenv("LANGCHAINKEY")

    # Initialize the language model
    llm = ChatOpenAI(temperature=0.6, model_name="gpt-3.5-turbo-16k", verbose=True)

    # Initialize the LLMChain
    newsletter_chain = LLMChain(llm=llm, prompt=PROMPT_NEWSLETTER, verbose=True)

    # Run the LLMChain
    newsletter = newsletter_chain.run(docs)

    # Write newsletter to a text file
    with open("newsletter.txt", "w") as f:
        f.write(newsletter)
    
    footer='''\n\nDo feel free to reach out to Dr Sam@Savormetrics. One email to  sales@savormetrics.com and we can work with you to implement the knowledge represented in these papers.'''
    final_string=newsletter+footer
    
    with open("newsletter.txt", "w") as f:
        f.write(final_string)
    
    #Set toolkit
    # toolkit = GmailToolkit() 

    # # Initialize the Gmail agent
    # agent = initialize_agent(
    #     tools=toolkit.get_tools(),
    #     llm=llm,
    #     agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    #     verbose=True
    # )

    # # Run the agent
    # instructions = f"""
    # Write a draft directed to kaholkanav@gmail.com, NEVER SEND THE EMAIL. 
    # The subject should be 'Dr Sam daily knowledge digest {query}'. 
    # The content should be the following: {newsletter}.
    # """
    # agent.run(instructions)
    # print(cb)