def get_llm_response(prompt, llm_model):
    """Get an LLM response using the retrieved context and user input."""
    print("🤔 Getting the LLM response, man...")

    return llm_model.invoke(prompt).content
