from gui import Gui
from model import MyLanguageModel

class ChatController:
    def __init__(self):
        self.view: Gui = Gui(self)
        self.model: MyLanguageModel = MyLanguageModel("Cinema Ticket Chatbot")
        self.username = "User"
        self.view.write_message(self.model.history + "\n")

    def send_message(self, message: str):
        msg = f"{self.username}: {message}\n"
        self.view.write_message(msg)
        reply = self.model.answer(message)
        self.view.write_message(self.model.name + ": " + reply + "\n")
        # self.view.update_chat_display(str(self.model.history)) # debug info

if __name__ == "__main__":
    asd = ChatController()
    asd.view.mainloop()
