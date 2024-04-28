from g4f.client import Client


class ChatSession:
    def __init__(self):
        self.client = Client()
        self.messages = []

    def send_message(self, content):
        # Сохраняем сообщение пользователя
        self.messages.append({"role": "user", "content": content})

        # Создаём запрос к модели
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )

        # Получаем ответ от модели
        bot_message = response.choices[0].message.content

        # Сохраняем ответ модели
        self.messages.append({"role": "assistant", "content": bot_message})

        # Возвращаем ответ модели
        return bot_message


# Использование класса
session = ChatSession()
while True:
    user_input = input("Enter your message: ")
    if user_input.lower() == 'exit':
        break
    print("Bot:", session.send_message(user_input))
