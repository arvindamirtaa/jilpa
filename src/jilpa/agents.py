from crewai import Agent
from textwrap import dedent
from langchain.llms import OpenAI, Ollama
from langchain_openai import ChatOpenAI

class CustomAgents:
    def __init__(self):
        self.OpenAIGPT4oMini = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        # self.Ollama = Ollama(model="openhermes")

    def story_writer(self):
        return Agent(
            role="Senior Story Writer",
            backstory=dedent(f"""You are an experienced story writer who has written stories for many open world scenarios,
                you have created many creative characters and world elements that are very unique an engaging"""),
            goal=dedent(f"""Create the screenplay with characters and world elements"""),
            # tools=[tool_1, tool_2],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4oMini,
        )

    def animator(self):
        return Agent(
            role="Creative Animator",
            backstory=dedent(f"""You are an experienced animator who has worked for top animation studios which emphasis on novel and creative character and world building.
                You have collaborated with senior story writes who have developed open world stories with capbilities to expand the story infinitly."""),
            goal=dedent(f"""Define agent 2 goal here"""),
            # tools=[tool_1, tool_2],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4oMini,
        )
