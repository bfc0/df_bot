from google.cloud import dialogflow
import logging

logger = logging.getLogger("tg bot")


def df_response(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    reply = response.query_result.fulfillment_text
    is_default = response.query_result.intent.is_fallback
    logger.debug(f"replying {reply}")
    return reply, is_default
