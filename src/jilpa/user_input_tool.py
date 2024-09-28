from crewai_tools.tools.base_tool import BaseTool

class UserInputTool(BaseTool):
    name: str = "UserInputTool"
    description: str = "A tool to get input prompt from the user."

    def _run(self, **kwargs) -> str:
        user_prompt = input("""Enter a scenario to extend: """)
        return user_prompt
