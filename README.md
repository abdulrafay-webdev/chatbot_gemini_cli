# chatbot_gemini_cli
 This application is a fully interactive web-based chatbot created using Python's Streamlit library. It connects directly to Google's Gemini API using the
  official google-generativeai package, ensuring a robust and efficient connection. For security, your API key is safely loaded from a local .env file and
  is never exposed in the code. The chatbot's primary feature is its conversational memory, which is achieved through a sophisticated prompting strategy.
  With every new message you send, the application sends the entire conversation history back to the Gemini model. This history is automatically prepended
  with a hidden system instruction that defines the chatbot's friendly and helpful personality. By having the full context of our discussion, the model can
  provide remarkably coherent responses that "remember" what was said earlier. As a convenient bonus feature, a "Clear Chat History" button is always
  available on the interface, which allows you to easily reset the conversation and begin a new topic whenever you wish.
