import os
from dotenv import load_dotenv
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_ai.foundation_models.utils import Toolkit
from ibm_watsonx_ai import APIClient, Credentials


# Get absolute path to `.env` in the same directory as this script
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=env_path)

try:
    # Load and validate environment variables

    # vector_index for HR Thai leave policies make sure it exists in the same project_id
    vector_index_id = os.getenv("WATSONX_VECTOR_INDEX_ID")
    # Replace with your actual project ID and credentials
    project_id = os.getenv("WATSONX_PROJECT_ID")
    # the URL for the IBM Watsonx studio machine learning instance
    watsonx_url = os.getenv("WATSONX_URL")
    # get them from your IBM Cloud account (IAM API keys)
    watsonx_api_key = os.getenv("WATSONX_API_KEY")
    if not vector_index_id:
        raise EnvironmentError("❌ WATSONX_VECTOR_INDEX_ID environment variable not found")
    if not project_id:
        raise EnvironmentError("❌ WATSONX_PROJECT_ID environment variable not found")
    if not watsonx_url:
        raise EnvironmentError("❌ WATSONX_URL environment variable not found")
    if not watsonx_api_key:
        raise EnvironmentError("❌ WATSONX_API_KEY environment variable not found")
    
    credentials = Credentials(
        url=watsonx_url,
        api_key=watsonx_api_key,
    )
except EnvironmentError as e:
    raise RuntimeError(f"Environment variable error: {e}")



def proximity_search(query: str) -> str:
    try:
        api_client = APIClient(
            project_id=project_id,
            credentials=credentials,
        )

        document_search_tool = Toolkit(api_client).get_tool("RAGQuery")

        config = {
            "vectorIndexId": vector_index_id,
            "projectId": project_id
        }

        results = document_search_tool.run(
            input=query,
            config=config
        )

        return results.get("output")
    except Exception as e:
        raise RuntimeError(f"Error during RAG proximity search: {e}")

@tool
def get_my_policies_rag(user_query: str = None) -> str:
    """
    This tool accept's user query to perform a Retrieval-Augmented Generation (RAG) search to extract relevant content from the company’s HR policy documentation.

    :returns: A plain-text string containing one or more relevant policy excerpts. These may include bullet points, guidelines, eligibility rules, or approval steps. The output is not formatted or curated, and is intended solely as contextual input for the LLM agent.
    """
    try:
        if not user_query:
            return "Please provide a specific policy topic, e.g., 'maternity leave' or 'unpaid leave'."

        return proximity_search(user_query)
    except Exception as e:
        return RuntimeError(f"Failed to retrieve HR policy content: {e}")
        


# Example usage
# This is for testing purposes and can be removed in production code.
"""if __name__ == "__main__":
    try:
        # Change the query below to test different topics
        test_query = "leave types"
        result = get_my_policies_rag(test_query)
        print("Query:", test_query)
        print("Result:", result)
    except Exception as e:
        print("Error:", e)"""