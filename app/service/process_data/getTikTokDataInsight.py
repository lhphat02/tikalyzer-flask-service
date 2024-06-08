import os
from dotenv import load_dotenv
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig, Tool, FunctionDeclaration
from vertexai.preview.generative_models import ToolConfig

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'doan-425516-5fde2ee9856a.json'

def generate_tiktok_insights(df):
    load_dotenv()  # Load environment variables
    vertexai.init(project=os.getenv('PROJECT_ID'), location=os.getenv('LOCATION'))
    global API_KEY
    API_KEY = os.getenv('API_KEY')

    extract_tiktok_insights_func = FunctionDeclaration(
        name="extract_tiktok_insights",
        description="Extract insights from a given TikTok channel.",
        parameters={
            "type": "string",
            "description": "The TikTok channel from which to extract insights."
        },
        # returns={
        #     "type": "string",
        #     "description": "HTML text containing data insights about the TikTok channel."
        # }
    )

    tiktok_tool = Tool(
        function_declarations=[extract_tiktok_insights_func],
    )

    tiktok_tool_config = ToolConfig(
        function_calling_config=ToolConfig.FunctionCallingConfig(
            mode=ToolConfig.FunctionCallingConfig.Mode.ANY,
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
            print(f"check API key coi co gi ben func: {API_KEY}")
            response = chat.send_message(f"Generate insights for this data: ```{row.to_dict()}```")
            fc = response.candidates[0].content.parts[0].function_call
            insight = type(fc).to_dict(fc)["args"]
            insights.append(insight)
        except Exception as e:
            print(f"Error sending message: {e}")

    insights_html = "<br>".join(str(insight) for insight in insights)

    return insights_html