from ai_services.chat_service import chatbot_reply

# while True:
#     msg = input("You: ")
#     if msg.lower() in ["quit", "exit"]:
#         break
#     print("BloomBuddy:", chatbot_reply(msg))
print("--- Simulating Free-Text User Queries ---")
print(chatbot_reply(user_message="My tomato leaves have dark spots and yellow rings."))
print("\n")
print(chatbot_reply(user_message="What's wrong with my apple tree, it has olive spots?"))
print("\n")
print(chatbot_reply(user_message="My basil plant has tiny green bugs."))
print("\n")
print(chatbot_reply(user_message="hii!"))
print("\n")
print(chatbot_reply(user_message="Thanks for the info."))
print("\n")