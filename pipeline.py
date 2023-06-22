import os
import json
from typing import List
os.environ["OPENAI_API_KEY"] = "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"
# import openai
# from dotenv import dotenv_values
# config = dotenv_values('.env')
# openai.api_key = config['OPENAI_API_KEY']
# os.environ['OPENAI_API_KEY'] = config['OPENAI_API_KEY']
os.environ["SERPER_API_KEY"] = "1ab03c5884c2bc2dd5f2df3ddb8d86684716cbd4"  # only used by testing
from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.agents import load_tools, AgentExecutor
from langchain.llms import OpenAI
from langchain.agents.mrkl_crawl.base import ZeroShotAgent
from langchain.document_loaders import WebBaseLoader
import requests
# splitter
from langchain.text_splitter import TokenTextSplitter

# Note 
QUERY_NUM = 3
QUERY_RESULTS_NUM = 5

# The web crawler must crawl in specific web domain or url prefix. Refer to the usage of "site" in google search: https://developers.google.com/search/docs/monitor-debug/search-operators/all-search-site    query+site:url
URL_DOMAIN_LIST = [""]
if len(URL_DOMAIN_LIST) == 0:
    URL_DOMAIN_LIST.append("")

THEME = "Cases of mergers and acquisitions of fast food industry enterprises in China after 2010"
DETAIL_LIST = ["When the merger occurred", "Acquirer", "Acquired party", "The CEO of acquirer", "The CEO of acquired party"]

def get_google_query_chain() -> LLMChain:
    """get a google query chain.
    
    Given a theme and queried records, google search chain outputs a new query.
    """
    template_for_google_query = """I want to google for "{theme}", your task is to give me the best search query. I have already queried {queried} before. Please output a new query which only contains letters. The new query should be as different as possible from my past queries. Just output the query without other word."""
    google_query_prompt = PromptTemplate(template=template_for_google_query, input_variables=["theme", "queried"])
    google_query_chain = LLMChain(prompt=google_query_prompt, llm=OpenAI(temperature=0), verbose=False) 
    return google_query_chain

def get_details_extractor_chain(detail_list: List) -> LLMChain:
    """get a details extractor chain.
    
    Given the raw content, theme and the details you want to crawl, details extractor chain outputs extract results.
    """
    
    detail_str = ", ".join(detail_list)
    template_for_details_extractor = """Context information is below:
---------------------
{context}
---------------------

Translate the context into English(don't output it), read and think sentence by sentence carefully, try to find all specific details of """
    
    template_for_details_extractor = template_for_details_extractor + detail_str
    
    template_for_details_extractor = template_for_details_extractor + """ about {theme} from the context as much as possible and respond in JSON format as described below:
---------------------
RESPONSE FORMAT:
{{
    "details":
    [
        {{"""
    
    detail_parse = ""
    for d in detail_list:
        detail_parse = detail_parse + """
            "{}": <answer>,""".format(d)
    template_for_details_extractor = template_for_details_extractor + detail_parse[:-1]
    
    template_for_details_extractor = template_for_details_extractor + """
        }}
    ]
}}
---------------------
Ensure the response can be parsed by Python json.loads. The list length of the "details" in the response depends on how many pieces of information you find about {theme} from context. You should find as much information as possible.

Unless you are very sure the specific details appear in context and the specific details is absolutely correct, replace the <answer> with "XXX", don't try to make up any answer."""
    details_extractor_prompt = PromptTemplate(template=template_for_details_extractor, input_variables=["context", "theme"])
    details_extractor_chain = LLMChain(prompt=details_extractor_prompt, llm=OpenAI(temperature=0, max_tokens=-1), verbose=False) 
    
    return details_extractor_chain

def get_details_completer_agent() -> AgentExecutor:
    """get a details completer agent
    
    complete details with correct information
    """         
    llm=OpenAI(temperature=0, max_tokens=-1)  
    tools = load_tools(["google-serper"], llm=llm)
    agent_executor = ZeroShotAgent.from_llm_and_tools(llm, tools)
    details_completer_agent = AgentExecutor.from_agent_and_tools(agent=agent_executor, tools=tools, verbose=False)
    return details_completer_agent

def get_google_query(google_query_chain: LLMChain, theme: str, queried: str, is_first: bool) -> str:
    if is_first:
        return theme
    else:
        return google_query_chain.predict(theme=theme, queried=queried).replace("\n", "").replace("\r", "")

def google_search(query: str, num: int, url_domain: str = "") -> List:
    """Return the results of a google search"""
    
    query_for_search = query.replace('"', '').replace("+", "%2B").replace(' ', '%20').replace("&", "%26").replace("/", "%2F").replace("?", "%3F").replace("#", "%23").replace("=", "%3D")
    if url_domain == "": 
        url_for_search = f"https://google.com/search?q={query_for_search}"
    else:
        url_for_search = f"https://google.com/search?q={query_for_search}%20site:url_domain"
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
    headers = {"user-agent" : USER_AGENT}
    resp = requests.get(url_for_search, headers=headers)

    from bs4 import BeautifulSoup
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.content, "html.parser")
        results = []
        for g in soup.find_all('div', class_='g'):
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                title = g.find('h3').text
                item = {
                    "title": title,
                    "href": link
                }
                results.append(item)
                if len(results) == num:
                    break
    else:
        return []
    return results

def get_website_content_with_bs(url: str) -> str:
    loader = WebBaseLoader(url)
    data = loader.load()
    text = data[0].page_content
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = "\n".join(chunk for chunk in chunks if chunk)
    return text

def split_text_economical(text: str, chunk_size: int = 2000, chunk_overlap: int = 100):
    text_splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    text_list = text_splitter.split_text(text)
    return text_list

def check_dict(json_input: str) -> bool:
    """
    Ensure the content is extracted 
    """
    for dic in json_input:
        for v in dic.values():
            if v != "XXX":
                return True
    return False

def main():
    final_list = []
    queried_list = []
    visited_url = []
    
    print(">>>>>>>>>>>The theme of web crawler is: ", THEME)
    print(">>>>>>>>>>>The specific details of the web crawler theme are: ", DETAIL_LIST)
    print(">>>>>>>>>>>The valid web domain or url prefix is: ", URL_DOMAIN_LIST)
    print("\n\n\n")

    # get google query chain
    google_query_chain = get_google_query_chain()
    details_extractor_chain = get_details_extractor_chain(DETAIL_LIST)
    details_completer_agent = get_details_completer_agent()
    
    # start google query
    for q in range(QUERY_NUM):
        queried = ", ".join(queried_list)
        current_query = get_google_query(google_query_chain, THEME, queried, 0==q)
        print("............Searching using Google.......... ")
        print(current_query)
        for domain in URL_DOMAIN_LIST:
            url_list = google_search(query=current_query, num=QUERY_RESULTS_NUM, url_domain=domain)
            
            # browse each website
            for index, url_dict in enumerate(url_list):
                url = url_dict["href"]
                if ".pdf" in url:
                    # print("The {}-th url of {}-th query is pdf, currently don't support resolve pdf".format(index, q))
                    continue
                if url in visited_url:
                    # print("The {}-th url of {}-th query is repeated".format(index, q))
                    continue
                print("............Reading url content.......... ")
                print(url)
                # get raw content from website
                website_content = get_website_content_with_bs(url)

                # split website content if it is too long
                website_content_list = split_text_economical(website_content, chunk_size=1000, chunk_overlap=20)
                
                # extract specific details from each website chunk
                for chunk in website_content_list:
                    chain_output = details_extractor_chain.predict(context=chunk, theme=THEME)
                    chain_output_parse = json.loads(chain_output[chain_output.find("{"):])
                    details_extracted = chain_output_parse["details"]
                    if check_dict(details_extracted):
                        for ind, detail in enumerate(details_extracted):
                            if "XXX" in detail.values():
                                _detail = json.dumps(detail, indent=4, ensure_ascii=False)
                                completed_detail = details_completer_agent.run(_detail)
                                completed_detail_dict = json.loads(completed_detail[completed_detail.find("{"):])
                            else:
                                completed_detail_dict = detail
                            completed_detail_dict["source_url"] = url
                            final_list.append(completed_detail_dict)
                visited_url.append(url)
        queried_list.append(current_query)
    final_dict = {"events_num":len(final_list), "details": final_list}
    # save dict 
    with open("final_dict.json", "w") as f:
        json.dump(final_dict, f, indent=4, ensure_ascii=False)

if  __name__ == "__main__":
    main()