from win10toast import ToastNotifier
import os


def windows_notification(sender_name, file_dir):
    file_dir = os.getcwd() + file_dir
    toaster = ToastNotifier()
    toaster.show_toast(f"Voice Assistant Messaging System",
                       f"New message from {sender_name}",
                       callback_on_click= lambda: os.startfile(file_dir),
                       duration=20)