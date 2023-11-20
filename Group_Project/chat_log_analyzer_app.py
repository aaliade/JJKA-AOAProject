import tkinter as tk
from tkinter import filedialog
from chat_log_analyzer import ChatLogAnalyzer

class ChatLogAnalyzerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Student Participation Grade Calculator")

        # Create a text display area
        self.display_area = tk.Text(self.root, wrap=tk.WORD, height=20, width=60)
        self.display_area.pack()
        self.display_area.config(state="disabled")  # Disable text editing

        # Initialize a flag to track if the answer file is selected
        self.answer_file_selected = False

        # Create a "Select Answer File" button
        self.select_answer_button = tk.Button(self.root, text="Select Answer File", command=self.select_answer_file)
        self.select_answer_button.pack()

    def select_answer_file(self):
        # Check if the answer file is already selected
        if not self.answer_file_selected:
            # Initialize the ChatLogAnalyzer instance here
            self.chat_log_analyzer = ChatLogAnalyzer(tutor_name="arnett campbell")
            self.chat_log_analyzer.load_correct_answers()

            # Set the flag to indicate that the answer file is selected
            self.answer_file_selected = True

            # Destroy the "Select Answer File" button
            self.select_answer_button.destroy()

            # Create a "Select Chat Log File" button only if the answer file is selected
            self.create_select_chat_log_button()

    def create_select_chat_log_button(self):
        self.load_button = tk.Button(self.root, text="Select Chat Log File", command=self.update_display_area)
        self.load_button.pack()
    
    def update_display_area(self):
        chattimestamp = [] #to store all of chats
        chatsender = [] # To store all of senders
        chatmessage = [] # To store all of messages

        # Use filedialog only when the "Select Chat Log File" button is clicked
        file_path = filedialog.askopenfilename(title="Select Chat Log File")
        if not file_path:
            print("No file selected. Exiting.")
            return

        self.chat_log_analyzer.load_chat_logs(file_path)
        tutor_questions = self.chat_log_analyzer.extract_tutor_questions()

        result_text = "Tutor's Questions:\n"
        for i, question in enumerate(tutor_questions, start=1):
            question = question.strip()  # Remove leading and trailing spaces
            result_text += f"  {i}. {question}\n"

        # Filter out the tutor's messages and participation grade
        student_messages = [match[2] for match in self.chat_log_analyzer.matches if match[1].lower() != self.chat_log_analyzer.tutor_name.lower()]
        sender_messages = {}
        for match in self.chat_log_analyzer.matches:
            timestamp, sender, message = match
            chattimestamp.append(timestamp)
            chatsender.append(sender)
            chatmessage.append(message)
            if sender.lower() != self.chat_log_analyzer.tutor_name.lower():
                if sender not in sender_messages:
                    sender_messages[sender] = []
                sender_messages[sender].append(message)
        result_text += f"\nStudent Participation Results:\n"

        markedanswer = 0
        for sender, messages in sender_messages.items():
            correct_answers_count = sum(self.chat_log_analyzer.count_correct_answers_keywords(message) for message in messages)
            markedanswer  = self.chat_log_analyzer.get_correct_answers(chattimestamp, chatsender, chatmessage, sender)
            result_text += f" - {sender} \n      Grade: {markedanswer} \n      Questions Answered: {len(messages)} \n      Correct Answers: {correct_answers_count}\n"

        self.display_area.config(state="normal")
        self.display_area.delete("1.0", tk.END)  # Clear the text display area
        self.display_area.insert(tk.END, result_text)
        self.display_area.config(state="disabled")

    def run(self):
        self.root.mainloop()