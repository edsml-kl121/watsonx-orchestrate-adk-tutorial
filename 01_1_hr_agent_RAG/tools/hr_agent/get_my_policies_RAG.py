from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_ai.foundation_models.utils import Toolkit
from ibm_watsonx_ai import APIClient, Credentials

# First define the vector index ID, project ID, and credentials.
# These are used to connect to the IBM Watsonx AI service and access the vector index.

# vector_index for HR Thai leave policies
vector_index_id = "dab02075-f619-431f-9031-0ad6d105900c"
# Replace with your actual project ID and credentials
project_id = "25fa3eb1-4800-4807-bb88-69f2b7d56b30"

credentials = Credentials(
    # the URL for the IBM Watsonx studio machine learning instance
    url="https://us-south.ml.cloud.ibm.com",
    # get them from your IBM Cloud account (IAM API keys)
    api_key="3sC1oQ7MYpMU4j-2UwmvZ33gjJ6F0Fj4Vppx7W-E6Y8o"
)

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
def get_my_policies_rag(user_query: str = None) -> str:
    # """
    # Retrieves relevant HR policy content from a vector index using a Retrieval-Augmented Generation (RAG) search.

    # This tool accepts a refined query (e.g., "maternity leave") and returns matching content from company policy documents.
    # It is intended to provide unformatted grounding text for use by the agent's language model, which will handle summarization,
    # markdown formatting, and final response generation.

    # :param user_query: A focused HR policy topic interpreted by the agent (e.g., "parental leave", "unpaid leave", "leave types", "leave frequency", "maternity policy").

    # :returns: A plain-text string containing relevant policy content. This may include lists, entitlements, leave types,
    #           or approval requirements. The output is unstructured and intended for downstream formatting by the agent.
    # """
    """
    Retrieves relevant HR policy content from a vector index using a Retrieval-Augmented Generation (RAG) search.

    This tool accepts a refined, focused query about a specific HR topic—such as types of leave, entitlements, 
    or request procedures—and returns matching policy content from the company’s HR documentation.

    The returned content is intended to serve as unformatted grounding for the agent’s language model. 
    Final response formatting, summarization, or markdown rendering is handled downstream by the agent.

    :param user_query: A concise HR-related topic interpreted by the agent 
    (e.g., "parental leave", "unpaid leave", "leave types", "leave frequency", "maternity policy", "sick leave eligibility").

    :returns: A plain-text string containing one or more relevant policy excerpts. These may include bullet points, guidelines, eligibility rules, or approval steps. The output is not formatted or curated, and is intended solely as contextual input for the LLM agent.
    """
    # Validate user query
    if not user_query:
        return "Please provide a specific policy topic, e.g., 'maternity leave' or 'unpaid leave'."

    return proximity_search(user_query)
