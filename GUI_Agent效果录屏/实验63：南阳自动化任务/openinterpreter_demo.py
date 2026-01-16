def custom_language_model(messages, model, stream, max_tokens):
    """
    OpenAI-compatible completions function (this one just echoes what the user said back).
    To make it OpenAI-compatible and parsable, `choices` has to be the root property.
    The property `delta` is used to signify streaming.
    """
    users_content = messages[-1].get("content") # Get last message's content

    for character in users_content:
        yield {"choices": [{"delta": {"content": character}}]}

# Tell Open Interpreter to power the language model with this function

interpreter.llm.completions = custom_language_model