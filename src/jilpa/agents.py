from crewai import Agent
from textwrap import dedent
from langchain.llms import OpenAI, Ollama
from langchain_openai import ChatOpenAI
from .user_input_tool import UserInputTool

user_input_tool = UserInputTool()


class CustomAgents:
    def __init__(self):
        self.OpenAIGPT4oMini = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
        # self.Ollama = Ollama(model="openhermes")

    def story_writer(self):
        return Agent(
            role="Senior Story Writer",
            backstory=dedent(f"""You are an experienced story writer who has written stories for many open world scenarios,
                you have created many creative characters and world elements that are very unique an engaging"""),
            goal = dedent(f"""
                Your primary objective is to create a dynamic screenplay that brings the characters and world elements to life. You must build the narrative step by step, integrating user input at key decision points. 
                The 'user_input_tool' should ONLY be used to gather input from the user when transitioning between scenes or when a key decision is required to move the story forward. 
                Under no circumstances should the tool be used for any other purpose. Continue seeking user input and evolving the story until the user explicitly says 'stop'.
                
                1. Generate the core world elements and characters.
                2. Build the first scene and present it to the user.
                3. At the end of each scene, call the 'user_input_tool' to gather input for transitioning to the next scene or to make critical narrative decisions.
                4. Repeat the process until the user says 'stop', ensuring each scene connects smoothly to the next and the story flows cohesively.
            """),
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4oMini,
            max_iter=3,
            tools=[user_input_tool],
        )

    def animator(self):
        return Agent(
            role="Creative Animator",
            backstory=dedent(f"""You are an experienced animator who has worked for top animation studios which emphasis on novel and creative character and world building.
                You have collaborated with senior story writes who have developed open world stories with capbilities to expand the story infinitly."""),
            goal=dedent(f""" 1. Receive the key frames from Agent 2.
            2. Review the current video sequence and the incoming key frames.
            3. Call the 'video_extension_tool' to add new key frames that extend the video while maintaining consistency in animation.
            4. Repeat this process continuously, ensuring smooth transitions and creative expansion of the story."""),
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4oMini,
        )
