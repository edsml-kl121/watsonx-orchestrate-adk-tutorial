from WatsonxAPI import WatsonxAPI
from dotenv import load_dotenv
import os 
from ibm_watson_machine_learning.foundation_models.utils.enums import DecodingMethods

load_dotenv()

ibm_cloud_url = os.getenv("ibm_cloud_url", None)
watson_ai_project_id = os.getenv("watson_ai_project_id", None)
watson_ai_api_key = os.getenv("watson_ai_api_key", None)

print(watson_ai_api_key)
model_id = "mistralai/mistral-large"

watsonx_answer_genration_config = {
    "genAI_config": {
        
        "decoding_method" : DecodingMethods.GREEDY,
        "api_key": watson_ai_api_key,
        "url": "https://us-south.ml.cloud.ibm.com",
        "project_id": watson_ai_project_id,# need to make project in watsonx.ai 
        "max_tokens": 4096,
        "temperature": 0.0,#OPTIONAL
        "repetition_penalty":1.1,
        "min_tokens" : 10,
        "stop_sequences":[],
        "return_options": {'input_tokens': True,'generated_tokens': True, 'token_logprobs': True, 'token_ranks': True, }
    }
}

def generate_natural_response(data):
    watson_obj_ans_generate = WatsonxAPI(watsonx_answer_genration_config)
    prompt_template = """You are an HR agent. Generate a natural short answer using the given json data of a user in a conversational manner. Do not use any other information that is not given in json data.
    json_data : {}
    output:
    """

    prompt = prompt_template.format(data)
    ans = watson_obj_ans_generate._generate_text(prompt,model_id =model_id)

    return ans
