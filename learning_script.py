import json

from google.cloud import dialogflow_v2
from environs import Env


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow_v2.IntentsClient()

    parent = dialogflow_v2.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow_v2.Intent.TrainingPhrase.Part(
            text=training_phrases_part
        )

        training_phrase = dialogflow_v2.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow_v2.Intent.Message.Text(text=[message_texts])
    message = dialogflow_v2.Intent.Message(text=text)

    intent = dialogflow_v2.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message]
    )
    request = dialogflow_v2.CreateIntentRequest(
        parent=parent,
        intent=intent,
    )
    response = intents_client.create_intent(request=request)
    print("Intent created: {}".format(response))


def main():
    env = Env()
    env.read_env()
    project_id = env.str('PROJECT_ID')
    training_phrases = env.path('TRAINING_PHRASES')
    with open(training_phrases, 'r', encoding='UTF-8') as message_texts:
        intents_json = message_texts.read()
    intents = json.loads(intents_json)
    for intent, message_text in intents.items():
        create_intent(
            project_id,
            intent,
            message_text['questions'],
            message_text['answer']
        )


if __name__ == '__main__':
    main()
