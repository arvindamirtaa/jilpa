import json
import time
from typing import Type

from lumaai import LumaAI
from pydantic import BaseModel

from crewai_tools.tools.base_tool import BaseTool


class VideoExtendPromptSchema(BaseModel):
    """Input for Dream Machine Gen Tool."""

    video_id:str = "Video ID for which the new prompt will extend the video"
    scene_ext_prompt: str = "Prompt for the initial video to be generated by Lumaai dream machine API"


class LumaAIExtendTool(BaseTool):
    name: str = "LumaAIExtendTool"
    description: str = "Dream Machine Video Extending Tool that uses Lumaai API to extend a 5sec video from the source vedio id and given input prompt."
    args_schema: Type[BaseModel] = VideoExtendPromptSchema

    def _run(self, **kwargs) -> str:
        client = LumaAI()
        video_id = kwargs.get("video_id")
        scene_gen_prompt = kwargs.get("scene_ext_prompt")
        if not scene_gen_prompt:
            return "Scene gen prompt is required."
        generation = client.generations.create(
          prompt=scene_gen_prompt,
          keyframes={
                "frame0": {
                    "type": "generation",
                    "id": video_id
                }
            }
        )
        completed = False
        while not completed:
          generation = client.generations.get(id=generation.id)
          if generation.state == "completed":
            completed = True
          elif generation.state == "failed":
            raise RuntimeError(f"Generation failed: {generation.failure_reason}")
          print("Extending video...")
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
