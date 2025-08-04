from WatsonxAPI import WatsonxAPI
from dotenv import load_dotenv
import os 
from ibm_watson_machine_learning.foundation_models.utils.enums import DecodingMethods


watsonx_orchestrate_config = {
    "orchestrate_config": {
        "api_key": os.getenv("WATSON_ORCHESTRATE_API_KEY"),
        "base_url": os.getenv("WATSON_ORCHESTRATE_BASE_URL", "https://your-orchestrate-instance.com"),
        "agent_id": os.getenv("WATSON_ORCHESTRATE_AGENT_ID"),
        "environment_id": os.getenv("WATSON_ORCHESTRATE_ENV_ID"),
        "version": 1
    }
}

def generate_natural_response(user_message: str, thread_id: str = None):
    watson_obj = WatsonxAPI(watsonx_orchestrate_config)
    
    # Stream the response
    response_chunks = []
    for chunk in watson_obj.chat_with_agent_stream(user_message, thread_id):
        if chunk.get('event') == 'message':
            response_chunks.append(chunk.get('data', ''))
    
    return ''.join(response_chunks)
