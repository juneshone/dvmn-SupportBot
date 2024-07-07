from google.cloud import api_keys_v2, dialogflow_v2
from google.cloud.api_keys_v2 import Key
from environs import Env


def create_api_key(project_id: str) -> Key:
    client = api_keys_v2.ApiKeysClient()
    key = api_keys_v2.Key()
    key.display_name = 'API key'

    request = api_keys_v2.CreateKeyRequest()
    request.parent = f'projects/{project_id}/locations/global'
    request.key = key
    response = client.create_key(request=request).result()

    print(f'Successfully created an API key: {response.name}')
    return response


def detect_intent_text(project_id, session_id, text, language_code):
    session_client = dialogflow_v2.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow_v2.TextInput(text=text, language_code=language_code)
    query_input = dialogflow_v2.QueryInput(text=text_input)

    request = dialogflow_v2.DetectIntentRequest(
        session=session, query_input=query_input
    )
    response = session_client.detect_intent(request=request)
    return response.query_result.fulfillment_text, \
           response.query_result.intent.is_fallback


def main():
    env = Env()
    env.read_env()
    project_id = env.str('PROJECT_ID')
    with open('dialogflow_api_key.text', 'a') as api_key:
        api_key.write(f'{create_api_key(project_id)}')


if __name__ == '__main__':
    main()
