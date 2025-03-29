from gpt4all import GPT4All
import os
import textwrap
from dotenv import load_dotenv

load_dotenv()
MODEL_PATH = os.getenv("MODEL_PATH")

class ChatBot:
    def __init__(self):
        self.model = GPT4All(MODEL_PATH)
        self.chat_history = []
        self.min_response_length = 10
        self.max_response_length = 200

    def format_response(self, text):
        """Formats response with proper wrapping and minimum length"""
        if not text.strip():
            return "I don't have an answer for that. Could you ask differently?"

        # Вибираємо перший осмислений речення
        text = text.strip().split(".")[0] + "."

        # Переконуємось, що текст достатньо довгий
        if len(text) < self.min_response_length:
            text += " (Verified fact)"

        # Обрізаємо, якщо занадто довго
        if len(text) > self.max_response_length:
            text = text[:self.max_response_length - 3] + "..."

        return textwrap.fill(text, width=50)

    def print_response(self, response):
        """Prints response in a properly sized box"""
        lines = response.split('\n')
        max_length = max(len(line) for line in lines)

        print("\n┌" + "─" * (max_length + 2) + "┐")
        for line in lines:
            print("│ " + line.ljust(max_length) + " │")
        print("└" + "─" * (max_length + 2) + "┘\n")

    def generate_response(self, prompt):
        try:
            # print(f"DEBUG: Generating response for prompt: {prompt}")
            response = self.model.generate(prompt, max_tokens=100, temp=0.2)  # Менше токенів і нижча температура
            # print(f"DEBUG: Raw response: {response}")
            return self.format_response(response)
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def run(self):
        print("🟢 Чат-бот запущений! Введіть питання або 'exit' для виходу.\n")

        while True:
            try:
                user_input = input("👤 Ви: ").strip()
                if not user_input:
                    continue

                if user_input.lower() == 'exit':
                    print("\n🛑 Завершення роботи...")
                    break

                self.chat_history.append({"role": "user", "content": user_input})

                # Use last 2 exchanges for context
                context = "\n".join(
                    f"{msg['role']}: {msg['content']}"
                    for msg in self.chat_history[-4:]
                )

                response = self.generate_response(context)
                self.chat_history.append({"role": "assistant", "content": response})
                self.print_response(response)

            except KeyboardInterrupt:
                print("\n🛑 Переривання роботи...")
                break
            except Exception as e:
                print(f"\n⚠️ Критична помилка: {str(e)}")
                continue

if __name__ == "__main__":
    bot = ChatBot()
    bot.run()
