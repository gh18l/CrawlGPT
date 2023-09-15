# CrawlGPT

⚡ Fully automated web crawler. Crawling all information you want on the Internet with GPT-3.5. Built with 🦜️🔗[LangChain](https://github.com/hwchase17/langchain)👍👍⚡

## Simple Demo
https://github.com/gh18l/CrawlGPT/assets/16774158/593fc8f3-71d1-45fb-aca1-0bfc6a92a996

## What it can do?

- Fully automated web crawler. Simulate the process of humans searching for data as much as possible.
- Automatically collect all specified details across the entire internet or given web domain based on a given theme.
- Automatically search for answers on the internet to fill in missing specified details while crawling.
- ✍️👇A simple exmple👇✍️
    - Input: 
        - the theme you want to crawl: `Cases of mergers and acquisitions of fast food industry enterprises in America after 2010`
        - 0-th specific detail: `When the merger occurred`
        - 1-th specific detail: `Acquirer`
        - 2-th specific detail: `Acquired party`
        - 3-th specific detail: `The CEO of acquirer`
        - 4-th specific detail: `The CEO of acquired party`
        - (Optional) Limited web domain: `["nytimes.com", "cnn.com"]`
    - Output: JSON containing all specified details about the theme. The format of output is
        ```
        {
            "events_num": N,
            "details":  ### The length of this list is N.
            [ 
                {
                    "When the merger occurred": <answer>,
                    "Acquirer": <answer>,
                    "Acquired party": <answer>,
                    "The CEO of acquirer": <answer>,
                    "The CEO of acquired party": <answer>,
                    "source_url": <url>
                },
                {
                    "When the merger occurred": <answer>,
                    "Acquirer": <answer>,
                    "Acquired party": <answer>,
                    "The CEO of acquirer": <answer>,
                    "The CEO of acquired party": <answer>,
                    "source_url": <url>
                },
                ..............
            ]
        }
        ```

## Why web crawler need GPT?
- GPT can extract the necessary information by directly understanding the content of each webpage, rather than writing complex crawling rules.
- GPT can connect to the internet to determine the accuracy of crawler results or supplement missing information.

## How it do?

0. Thinking about suitable Google search queries based on the theme with GPT-3.5.
1. Simulate Google search in entire Internet or given web domain(if any) using each query.
2. Browse every website.
3. Extract specific details of the theme from the content of the website with GPT-3.5.
4. Similar to Auto-GPT, it will independently search for missing details on the Internet based on the langchain implementation of [MRKL](https://arxiv.org/abs/2205.00445) and [ReAct](https://arxiv.org/abs/2210.03629).
5. Encapsulate all results into a JSON.

## Quick Install

- `OPENAI_API_KEY`: You must have a openai api key and modify `os.environ["OPENAI_API_KEY"]` in `pipeline.py`.
- `SERPER_API_KEY`: For searching correct and real-time information, you need have a [google serper api key](https://serper.dev/). It will take you a short time to register. Modify `os.environ["SERPER_API_KEY"]` in `pipeline.py` and you have 1000 queries for free every month.
- Hyper Parameters:
    - `QUERY_NUM`: The Number of Google searches with different query. Default is 2.
    - `QUERY_RESULTS_NUM`: The number of results returned per search. Default is 4.
    - `THEME`: The theme of web crawler.
    - `DETAIL_LIST`: The specific details of the web crawler theme.
    - `(Optional) URL_DOMAIN_LIST`: The valid web domain or url prefix.
- Install `python3.11`.
- Install necessary dependencies: `pip install -r requirements.txt`
- Run it: `python pipeline.py > output.txt`.
- Read results from `final_dict.json`.


## TODO

- [x] Support crawl in given list of web domain.
- [ ] The langchain implementation of [MRKL](https://arxiv.org/abs/2205.00445) and [ReAct](https://arxiv.org/abs/2210.03629) carries the risk of divergent output. That is, the content of response may exceed our limit.
- [ ] Automatically write research reports based on crawling results.
- [ ] GPT consumes a huge amount of token while browsing webpage😢. Reduce the consumption.
- [ ] Browse the PDF files from the pdf link in website.
- [ ] Modify the entire pipeline to registration free(except for OpenAI).

## Contact me
I am currently working as an AI engineer at Alibaba in Beijing, China. I think communication can eliminate information gaps.

I am interested in llm applications, such as conversational search, AI agent, external data enhancement, etc. Welcome to communicate via email(hanxyz1818@gmail.com) or WeChat (if you have one).

I am also preparing to make an actual product. My most immature ideas recently is about llm+tweet, llm+crypto and llm+code. If you are also interested in them or you have some other ideas, also welcome to communicate.

![微信](./image/HanXYZ.jpg)


