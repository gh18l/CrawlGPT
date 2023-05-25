# CrawlGPT

⚡ Crawling all information you want on the Internet with GPT-3.5. Built with 🦜️🔗[LangChain](https://github.com/hwchase17/langchain)👍👍⚡

## Simple Demo


## Quick Install

- `OPENAI_API_KEY`: You must have a openai api key and modify `os.environ["OPENAI_API_KEY"]` in `pipeline.py`.
- `SERPER_API_KEY`: For searching correct and real-time information, you need have a [google serper api key](https://serper.dev/). It will take you a short time to register. Modify `os.environ["SERPER_API_KEY"]` in `pipeline.py` and you have 1000 queries for free every month.
- `QUERY_NUM`: Number of queris of google searching. Default is 3.
- `QUERY_RESULTS_NUM`: Number of search results per query. Default is 5.
- Install `python3.11`.
- Install necessary dependencies: `pip install -r requirements.txt`
- Run it: `python pipeline.py > output.txt`.
- Read results from `final_dict.json`.

## What it can do?

- Simulate the process of humans searching for data as much as possible.
- Automatically collect specified details across the entire internet based on a given theme.
- Automatically search for answers on the internet to fill in missing specified details while crawling.
- Input and Output
    - Input: the theme and the specified details you want to crawl.
    - Output: JSON containing all specified details about the theme.

## How it do?

0. Thinking about suitable Google search queries based on the theme with GPT-3.5.
1. Simulate Google search using each query.
2. Browse every website.
3. Extract specific details of the theme from the content of the website with GPT-3.5.
4. Similar to Auto-GPT, it will independently search for missing details on the Internet based on the langchain implementation of [MRKL](https://arxiv.org/abs/2205.00445) and [ReAct](https://arxiv.org/abs/2210.03629).
5. Encapsulate all results into a JSON such as 
```
{
    "details_num": <N>,
    "details":
    [
        {
            "detail_0": <answer>,
            "detail_1": <answer>,
            "source_url": <url>
        },
        {
            "detail_0": <answer>,
            "detail_1": <answer>,
            "source_url": <url>
        },
        .......
    ]
}
```

## TODO

- [ ] The langchain implementation of [MRKL](https://arxiv.org/abs/2205.00445) and [ReAct](https://arxiv.org/abs/2210.03629) carries the risk of divergent output. That is, the content of response may exceed our limit.
- [ ] Automatically write research reports based on crawling results.
- [ ] GPT consumes a huge amount of token while browsing webpage😢. Reduce the consumption.
- [ ] Browse the PDF files from the pdf link in website.
- [ ] Modify the entire pipeline to registration free(except for OpenAI).