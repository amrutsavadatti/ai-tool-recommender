from fastapi import FastAPI, HTTPException
from app.schemas import RecommendRequest, RecommendResponse, WorkflowRecommendation, Tool
from app.openai_chain import get_ai_recommendations
from app.search_utils import search_youtube_tutorials


app = FastAPI()

@app.post("/recommend", response_model=RecommendResponse)
async def recommend_tools(request: RecommendRequest):
    try:
        parsed = get_ai_recommendations(
            request.job_title,
            request.job_responsibility,
            request.workflows_to_automate
        )

        real_results = []

        for workflow_group in parsed.get("recommendations", []):
            workflow_name = workflow_group.get("workflow")
            tools_list = workflow_group.get("tools", [])

            real_tools = []
            for tool in tools_list:
                tool_name = tool["tool_name"]

                real_tutorials = search_youtube_tutorials(tool_name)

                real_tool = Tool(
                    tool_name=tool_name,
                    website_link=tool.get("website_link"),
                    features=tool.get("features", []),
                    youtube_tutorials=real_tutorials or tool.get("youtube_tutorials", []),
                    x_handles=tool.get("x_handles", [])
                )

                real_tools.append(real_tool)

            real_results.append(WorkflowRecommendation(
                workflow=workflow_name,
                tools=real_tools
            ))

        return RecommendResponse(recommendations=real_results)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")
