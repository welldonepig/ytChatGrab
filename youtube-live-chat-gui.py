import sys
import os
import re
import webbrowser
sys.path.append('C:\\Users\\welld\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python312\\site-packages')

from googleapiclient.discovery import build
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import time

# 初始化全局變量
stop_flag = False
save_file_path = "youtube_live_chat.txt"

def get_live_chat_id(youtube, video_id):
    try:
        request = youtube.videos().list(
            part="liveStreamingDetails",
            id=video_id
        )
        response = request.execute()
        live_chat_id = response['items'][0]['liveStreamingDetails']['activeLiveChatId']
        return live_chat_id
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get live chat ID: {e}")
        return None

def fetch_live_chat_messages(youtube, live_chat_id):
    global stop_flag
    next_page_token = None
    with open(save_file_path, "a", encoding="utf-8") as file:
        while not stop_flag:
            try:
                request = youtube.liveChatMessages().list(
                    liveChatId=live_chat_id,
                    part="snippet,authorDetails",
                    pageToken=next_page_token
                )
                response = request.execute()
                
                for item in response['items']:
                    try:
                        chat_message = item['snippet']['displayMessage']
                        author_name = item['authorDetails']['displayName']
                        published_time = item['snippet']['publishedAt']
                        file.write(f"{published_time} [{author_name}]: {chat_message}\n")
                        file.flush()
                    except KeyError as e:
                        # 跳過沒有 displayMessage 屬性的消息
                        continue
                
                next_page_token = response.get('nextPageToken')
                time.sleep(5)  # 防止 API 過載
            except Exception as e:
                messagebox.showerror("Error", f"Failed to fetch live chat messages: {e}")
                stop_flag = True
                break
    messagebox.showinfo("Info", "Chat fetching stopped.")

def start_fetching(api_key, video_url):
    global stop_flag
    stop_flag = False
    status_label.config(text="運作中", fg="green")

    youtube = build('youtube', 'v3', developerKey=api_key)
    video_id = extract_video_id(video_url)
    if not video_id:
        messagebox.showerror("Error", "Invalid YouTube URL")
        status_label.config(text="停止", fg="red")
        return

    live_chat_id = get_live_chat_id(youtube, video_id)
    if live_chat_id:
        messagebox.showinfo("Info", "Successfully started fetching chat messages.")
        fetch_thread = threading.Thread(target=fetch_live_chat_messages, args=(youtube, live_chat_id))
        fetch_thread.start()
    else:
        status_label.config(text="停止", fg="red")

def stop_fetching():
    global stop_flag
    stop_flag = True
    status_label.config(text="停止", fg="red")

def open_file():
    if os.path.exists(save_file_path):
        webbrowser.open(save_file_path)
    else:
        messagebox.showerror("Error", "File does not exist.")

def set_save_file_path():
    global save_file_path
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        save_file_path = file_path
        file_path_label.config(text=f"儲存位置: {save_file_path}")

def extract_video_id(url):
    # 提取YouTube影片ID的正則表達式
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    return match.group(1) if match else None

# 建立 GUI 界面
root = tk.Tk()
root.title("YouTube Live Chat Fetcher")
root.geometry("500x250")  # 設置窗口大小

# 設置主框架
main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(expand=True, fill="both")

# 添加 API Key 和 YouTube Video URL 輸入框
tk.Label(main_frame, text="API Key:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
api_key_entry = tk.Entry(main_frame, width=50)
api_key_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(main_frame, text="YouTube Video URL:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
video_url_entry = tk.Entry(main_frame, width=50)
video_url_entry.grid(row=1, column=1, padx=10, pady=10)

# 添加按鈕框架
button_frame = tk.Frame(main_frame)
button_frame.grid(row=2, column=0, columnspan=2, pady=10)

start_button = tk.Button(button_frame, text="開始", width=15, command=lambda: start_fetching(api_key_entry.get(), video_url_entry.get()))
start_button.grid(row=0, column=0, padx=10)

stop_button = tk.Button(button_frame, text="停止", width=15, command=stop_fetching)
stop_button.grid(row=0, column=1, padx=10)

# 添加儲存位置設置和顯示
file_path_button = tk.Button(main_frame, text="設定儲存位置", command=set_save_file_path)
file_path_button.grid(row=3, column=0, columnspan=2, pady=5)

file_path_label = tk.Label(main_frame, text=f"儲存位置: {save_file_path}", fg="blue", cursor="hand2")
file_path_label.grid(row=4, column=0, columnspan=2)
file_path_label.bind("<Button-1>", lambda e: open_file())

# 添加狀態標籤
status_label = tk.Label(main_frame, text="停止", fg="red")
status_label.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
