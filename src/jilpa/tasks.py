from crewai import Task
from textwrap import dedent
from .dream_machine_generate_tool import LumaAIGenTool
from .dream_machine_extend_tool import LumaAIExtendTool


luma_gen_tool = LumaAIGenTool()
luma_extend_tool = LumaAIExtendTool()



class CustomTasks:
    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a will be nomiated for acadamey awards for this category.!"

    def generate_character(self, agent, world_description):
        return Task(
            description=dedent(
                f"""
                You will create novel characters that will be used in a open world story to navigate in a First Person Point of View.
            Please use the below world description to analyze the world and create the necessary characters.

            World Description
            ------------------
            {world_description}

            {self.__tip_section()}
        """
            ),
            agent=agent,
            expected_output="Output should include character name, qualities and appearance",
            context=world_description
        )

    def generate_story(self, agent, context_tasks):
        return Task(
            description=dedent(
                f"""
            Generate the next scene in an open world story. if the story recap section exist use it as context and
            make sure the scene you generate continues after the recap. If not generate a new scene as if its the opening scene,
            such that can be expanded in the next iteration.

            {self.__tip_section()}
        """
            ),
            agent=agent,
            expected_output="Output should a cohesive next scene and nothing else.",
            context=context_tasks
        )

    def generate_world_elements(self, agent, user_prompt):
        return Task(
            description=dedent(
                f"""
            Take the input from the user prompt section to generate an open world with characters, interactable elements,
            observable elements, climate, backdrop, lighting, time period, etc.

            User Prompt
			------------
			{user_prompt}

            {self.__tip_section()}
        """
            ),
            agent=agent,
            expected_output="""Output should contain details of the world and immediate surroundings, characters in the scene, interactable and observable elements. It should be like a prompt for an image / video generation model - to be around 1000 characters and nothing else."""
        )
    
    def generate_world_video(self, agent, context_tasks):
        return Task(
            description=dedent(
                f"""Use the context from the generated world elements and use that to create a video of the world.
                
                {self.__tip_section()}"""   
            ),
            expected_output="The output should be the video id and URL of the generated video and nothing else.",
            agent=agent,
            context=context_tasks,
            tools=[luma_gen_tool]
        )
    
    def generate_story_frames(self, agent, context_tasks):
        return Task(
            description=dedent(
                f"""
            Take the input of the generated scene. Then, split it into a series of frames that can be used to animate the scene. 

            {self.__tip_section()}
        """
            ),
            agent=agent,
            expected_output="Output should be a series of frames. Each frame should be a prompt for an image / video generation model - to be around 1000 characters and nothing else.",
            context=context_tasks
        )

    def generate_story_frame_video(self, agent, context_tasks):
        return Task(
            description=dedent(
                f"""For each frame in the generate_story_frames output, extend the most recently generated video. Use the context from the generated world elements if this is the first frame.
                
                {self.__tip_section()}"""   
            ),
            expected_output="The output should be the video id and URL of the generated video and nothing else.",
            agent=agent,
            context=context_tasks,
            tools=[luma_extend_tool]
        )

    def summarize_story(self, agent):
        return Task(
            description=dedent(
                f"""
            Take the input from task 1 and do something with it.

            {self.__tip_section()}

            Make sure to do something else.
        """
            ),
            agent=agent,
            expected_output="Output should be a 140 word text summary and nothing else."
        )
