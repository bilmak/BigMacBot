from llm import chat_with_gpt

if __name__ == "__main__":
    while True:
        user_input = input(
            "Hi, my hungry friend, what do you want to order?\n")
        if user_input.lower() in ['bye']:
            break

        response = chat_with_gpt(user_input)
        print("Chatbot:", response)
