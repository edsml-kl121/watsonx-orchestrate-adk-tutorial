from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_ai.foundation_models.utils import Toolkit
from ibm_watsonx_ai.foundation_models import APIClient

# vector_index for HR Thai leave policies
vector_index_id = "dab02075-f619-431f-9031-0ad6d105900c"
# Replace with your actual project ID and credentials
project_id = "25fa3eb1-4800-4807-bb88-69f2b7d56b30"

credentials = {
    # get them from your IBM Cloud account (IAM API keys)
    "apikey": "3sC1oQ7MYpMU4j-2UwmvZ33gjJ6F0Fj4Vppx7W-E6Y8o",
    # the URL for the IBM Watsonx studio machine learning instance
    "url": "https://us-south.ml.cloud.ibm.com"
}

def proximity_search(query: str) -> str:
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

@tool
def get_my_policies(user_query: str = None) -> str:
    # Uses vector index RAG to retrieve relevant HR policy info based on user query.

    # Validate user query
    if not user_query:
        return "Please provide a specific policy topic, e.g., 'maternity leave' or 'unpaid leave'."

    return proximity_search(user_query)
