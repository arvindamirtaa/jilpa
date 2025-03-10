import json
import time
from typing import Type

from lumaai import LumaAI
from pydantic import BaseModel

from crewai_tools.tools.base_tool import BaseTool


class VideoGenPromptSchema(BaseModel):
    """Input for Dream Machine Gen Tool."""

    scene_gen_prompt: str = "Prompt for the initial video to be generated by Lumaai dream machine API"


class LumaAIGenTool(BaseTool):
    name: str = "LumaAIGenTool"
    description: str = "Dream Machine Video Generation Tool that uses Lumaai API to generate a 5sec video from the input prompt."
    args_schema: Type[BaseModel] = VideoGenPromptSchema

    def _run(self, **kwargs) -> str:
        client = LumaAI()

        scene_gen_prompt = kwargs.get("scene_gen_prompt")
        if not scene_gen_prompt:
            return "Scene gen prompt is required."
        generation = client.generations.create(
          prompt=scene_gen_prompt,
        )
        completed = False
        while not completed:
          generation = client.generations.get(id=generation.id)
          if generation.state == "completed":
            completed = True
          elif generation.state == "failed":
            raise RuntimeError(f"Generation failed: {generation.failure_reason}")
          print("Dreaming")
          time.sleep(3)

        video_id = generation.id
        video_url = generation.assets.video

        video_data = json.dumps(
            {
                "id": video_id,
                "url": video_url,
            }
        )

        return video_data
