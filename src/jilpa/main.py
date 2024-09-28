from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from textwrap import dedent
from .agents import CustomAgents
from .tasks import CustomTasks

import agentops

load_dotenv()

class JilpaCrew:
    def __init__(self, user_prompt):
        self.user_prompt = user_prompt

    def run(self):
        # Define your custom agents and tasks in agents.py and tasks.py
        agents = CustomAgents()
        tasks = CustomTasks()

        # Define your custom agents and tasks here
        story_writer_agent = agents.story_writer()
        animator_agent = agents.animator()

        # Custom tasks include agent name and variables as input
        generate_world_elements_task = tasks.generate_world_elements(
            story_writer_agent,
            self.user_prompt
        )

        generate_character_task = tasks.generate_character(
            story_writer_agent,
            [generate_world_elements_task]
        )

        generate_story_task = tasks.generate_story(
            story_writer_agent,
            [generate_world_elements_task, generate_character_task]
        )

        generate_story_frames_task = tasks.generate_story_frames(
            story_writer_agent,
            [generate_world_elements_task, generate_character_task, generate_story_task]
        )

        generate_world_video_task = tasks.generate_world_video(
            animator_agent,
            [generate_world_elements_task, generate_character_task]
        )
        
        generate_story_frame_video_task = tasks.generate_story_frame_video(
            animator_agent,
            [generate_world_elements_task, generate_character_task, generate_story_task, generate_world_video_task, generate_story_frames_task]
        )

        # Define your custom crew here
        crew = Crew(
            agents=[story_writer_agent, animator_agent],
            tasks=[generate_world_elements_task, generate_character_task, generate_world_video_task, generate_story_task, generate_story_frames_task, generate_story_frame_video_task],
            verbose=True,
        )

        result = crew.kickoff()
        return result


# This is the main function that you will use to run your custom crew.
if __name__ == "__main__":
    agentops.init()
    print("## Welcome to Jilps AI")
    print("-------------------------------")
    user_prompt = input(dedent("""Enter a scenario: """))

    custom_crew = JilpaCrew(user_prompt)
    result = custom_crew.run()
    print("\n\n########################")
    print("## Here is you custom crew run result:")
    print("########################\n")
    print(result)
