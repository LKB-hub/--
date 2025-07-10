import requests
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk

def send_question():
    question = entry.get().strip()
    if not question:
        messagebox.showwarning("警告", "请输入一个问题。")
        return
    
    api_key = get_api_key()
    if not api_key:
        messagebox.showerror("错误", "API密钥未设置。")
        return
    
    payload = {
        "model": "Qwen/QwQ-32B",
        "messages": [
            {"role": "user", "content": question}
        ]
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post("https://api.siliconflow.cn/v1/chat/completions", json=payload, headers=headers)
        response.raise_for_status()
        answer = response.json()['choices'][0]['message']['content']
        
        chat_history.config(state=tk.NORMAL)
        chat_history.insert(tk.END, f"你: {question}\n\n")
        chat_history.insert(tk.END, f"教授: {answer}\n\n")
        chat_history.config(state=tk.DISABLED)
        chat_history.yview(tk.END)
        
        entry.delete(0, tk.END)
    except requests.exceptions.HTTPError as http_err:
        messagebox.showerror("HTTP 错误", f"HTTP 错误发生: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        messagebox.showerror("连接错误", f"连接错误发生: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        messagebox.showerror("超时错误", f"请求超时: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        messagebox.showerror("请求错误", f"请求失败: {req_err}")

def get_api_key():
    return "sk-ycfzygvuzqlirmkqltrzpkknnoaikxzbsmdgvxxrvbacvwra"

root = tk.Tk()
root.title("数学问题解答器")
root.geometry("800x600") 
style = ttk.Style(root)
style.theme_use('clam')
chat_history_font = ('Arial', 14)
chat_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=75, height=25, state=tk.DISABLED, bg='white', fg='black', font=chat_history_font)
chat_history.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.7)

entry_frame = tk.Frame(root, bg='white')
entry_frame.place(relx=0.05, rely=0.8, relwidth=0.9, relheight=0.05)

entry_font = ('Arial', 14)
entry = tk.Entry(entry_frame, width=60, bg='white', fg='black', font=entry_font)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

send_button = ttk.Button(entry_frame, text="发送", command=send_question)
send_button.pack(side=tk.RIGHT, padx=5)

root.mainloop()