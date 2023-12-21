import os
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tk
import webbrowser
from tkinter import messagebox



HOST = '192.168.43.181' # localhost
PORT = 33000
BUFSIZ = 4096
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)




def receive(event=None):
    """Handles receiving of messages."""
    while True:
        try:
            html_content = ""

            while True:
                partial_msg = client_socket.recv(BUFSIZ).decode("utf-8")
                html_content += partial_msg

                # Eğer HTML içeriği tamamlandıysa, döngüden çık
                if "</html>" in html_content:
                    break

            # Tam HTML içeriğini alındı, dosyaya yaz ve aç
            with open("temp.html", "w", encoding='utf-8') as file:
                file.write(html_content)

            webbrowser.open_new_tab("temp.html")


            print(partial_msg)
            msg_list.insert(tk.END, partial_msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):
    """Handles sending of messages."""
    msg = my_msg.get()


    # Eğer mesaj ".html" uzantılı değilse gönderme
    if not msg.endswith(".html") and not msg == "{quit}":
        messagebox.showwarning("Uyari", "Geçersiz dosya uzantisi. Lütfen '.html' uzantili bir mesaj giriniz.")
        return


    # Eğer dosya bulunmuyorsa hata mesajı göster
    if not os.path.isfile(msg) and not msg == "{quit}":
        messagebox.showwarning("Dosya bulunamadi", f"'{msg}' server'da mevcut değil.")
        return

    my_msg.set("")  # Giriş alanını temizle.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        app.destroy() # GUI'yi kapat



def on_closing():
    my_msg.set("{quit}")
    send()
    app.destroy()



app = tk.Tk()
app.title("Records")

# Message Frame
message_frame = tk.Frame(app, padx=10, pady=10)
message_frame.pack()

# Scrollbar and Message List
scrollbar = tk.Scrollbar(message_frame)
msg_list = tk.Listbox(message_frame, height=15, width=50, yscrollcommand=scrollbar.set, bg="#f0f0f0", selectbackground="#a6a6a6")
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)

# Entry Field
entry_frame = tk.Frame(app, padx=10, pady=10)
entry_frame.pack()

my_msg = tk.StringVar()
my_msg.set("Type html file name here.")

entry_field = tk.Entry(entry_frame, textvariable=my_msg, width=40, bd=5, font=('Arial', 12))
entry_field.bind("<Return>", send)
entry_field.grid(row=0, column=0, sticky="nsew")

# Send Button
send_button = tk.Button(entry_frame, text="Send", command=send, width=10, height=2, bg="#4CAF50", fg="white", font=('Arial', 12, 'bold'))
send_button.grid(row=0, column=1, padx=(10, 0), sticky="nsew")

# Close Window Protocol
app.protocol("WM_DELETE_WINDOW", on_closing)


receive_thread = Thread(target=receive)
receive_thread.start()
app.mainloop()  # Starts GUI execution.