# flake8: noqa
PREFIX = """Replace each XXX one by one in the original JSON with correct information. You must consider each XXX separately. Your output need to maintain the same JSON format. You have access to the following tools:"""
FORMAT_INSTRUCTIONS = """Use the following format:

Original JSON: the original JSON
Thought: you should always think about what to do
Action: the action to take, must be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I have found correct information of all XXX
Final JSON Output: the final JSON that you should output"""
SUFFIX = """Begin!

Original JSON: {input}
Thought:{agent_scratchpad}"""
