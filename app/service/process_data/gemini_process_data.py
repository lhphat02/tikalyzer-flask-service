import os
from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig, Tool, FunctionDeclaration
from vertexai.preview.generative_models import ToolConfig

def generate_tiktok_insights(df):
    load_dotenv()  # Load environment variables
    vertexai.init(project=os.getenv('PROJECT_ID'), location=os.getenv('LOCATION'))

    # Define your function, tool, and tool config here as in the process_job function
    channel_name = df.get('channel_name', "")
    if channel_name == "":
        print("Channel name is empty")
        return
    
    channel_name = channel_name.replace("\"", "\'")

    extract_tiktok_insights_func = FunctionDeclaration(
        name="extract_tiktok_insights",
        description="Extract insights from a given TikTok channel.",
        parameters={
            "type": "string",
            "description": "The TikTok channel from which to extract insights."
        },
        returns={
            "type": "string",
            "description": "HTML text containing data insights about the TikTok channel."
        }
    )

    # Define a tool that includes the above functions
    tiktok_tool = Tool(
        function_declarations=[extract_tiktok_insights_func],
    )

    # Define a tool config for the above functions
    tiktok_tool_config = ToolConfig(
        function_calling_config=ToolConfig.FunctionCallingConfig(
            # ANY mode forces the model to predict a function call
            mode=ToolConfig.FunctionCallingConfig.Mode.ANY,
            # List of functions that can be returned when the mode is ANY.
            # If the list is empty, any declared function can be returned.
            allowed_function_names=["extract_tiktok_insights"],
        )
    )

    model = GenerativeModel('gemini-1.5-pro-preview-0409',
                            generation_config=GenerationConfig(temperature=0),
                            tools=[tiktok_tool],
                            tool_config=tiktok_tool_config
                            )
    chat = model.start_chat()

    insights = []
    for _, row in df.iterrows():
        try:
            response = chat.send_message(f"Generate insights for this data: ```{row.to_dict()}```")
            fc = response.candidates[0].content.parts[0].function_call
            insight = type(fc).to_dict(fc)["args"]
            insights.append(insight)
        except Exception as e:
            print(f"Error sending message: {e}")

    return insights
