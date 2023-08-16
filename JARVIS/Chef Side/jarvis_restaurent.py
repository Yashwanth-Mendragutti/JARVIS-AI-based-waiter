#!/usr/bin/env python
# coding: utf-8

# In[1]:


import socket

def get_address():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        sock.connect(("8.8.8.8", 80))
        
        address = sock.getsockname()[0]
        
        return address
    except socket.error :
        return None
    finally:
        sock.close()
ipv4 = get_address()
if ipv4:
    print("ipv4 = ",ipv4)
else:
    print("unable to access ipv4 . sorrrrrrrrrrrrrrrrrrrrry")


# In[ ]:


# import socket
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import pyttsx3
from nltk.tokenize import word_tokenize
import pandas as pd

data_storage = pd.read_excel("C:/Users/Shaik Shahid Hussain/Desktop/order_book.xlsx")
global orders
orders = []
global order_status
def speak_response(response):
    engine = pyttsx3.init()
    engine.say(response)
    engine.runAndWait()

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the server's IP address and port number
server_address = ('192.168.39.54', 10000)

# Bind the socket to the server address
server_socket.bind(server_address)
print("Listening...")

# Listen for incoming connections
server_socket.listen(1)

# Create a Tkinter window
window = tk.Tk()

# Set the window title
window.title("Server")

# Maximize the window to full screen
window.attributes("-fullscreen", True)

# Load the background image
background_image = Image.open("cheif.jpg")  # Replace with your image file path
background_image = background_image.resize((window.winfo_screenwidth(), window.winfo_screenheight()))#, Image.ANTIALIAS)
background_photo = ImageTk.PhotoImage(background_image)

# Create a label to display the background image
background_label = tk.Label(window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create a label to display status messages
status_label = tk.Label(window, text="Waiting for order...", font=("Arial", 24), bg="white")
status_label.pack(pady=50)

# Create an entry field for the response
response_entry = tk.Entry(window, font=("Arial", 18), state=tk.DISABLED)
response_entry.pack(pady=20)

# Create a Listbox to display pending orders
orders_listbox = tk.Listbox(window, font=("Arial", 16), width=30)
orders_listbox.pack(side=tk.RIGHT, padx=50, pady=50)  
orders_listbox.place(x=770,y=300)

# Function to update the status label text with order details
def update_status_label(text):
    global order_status
    if order_status == 0:
        status_label.config(text=f"{text}\nOrder Details: {order_details}")
    else:
        status_label.config(text=f"{text}")
def update_status_label2(text):
    if order_status == 0:
        status_label.config(text=f"{text}")
    else:
        status_label.config(text=f"{text}")

# Function to update the orders listbox with new orders
def update_orders_listbox():
    order = orders[-1]
    print(order)
    orders_listbox.insert(tk.END, order)

# Function to handle client connections
def handle_client_connection():
    global order_details
    global client_socket
    global client_address
    global order_status
    order_details = []
    while True:
        try:
            # Accept a client connection
            client_socket, client_address = server_socket.accept()
            print("Client connection accepted.")
            
            order_details = client_socket.recv(1024).decode()
            order_status = 0
            # Update the status label
            update_status_label("Order received.")
            response = "order received sir.\n your order is {}".format(order_details)
            speak_response(response)
            
            # Enable the response entry field
            response_entry.config(state=tk.NORMAL)
            response_entry.delete(0, tk.END)
            response_entry.focus()
            print("dummy 1")
            # Update the orders listbox
            orders.append(order_details)
            update_orders_listbox()
            print("dummy 2")
            
        except socket.error:
            # No client connection available
            pass

# Function to handle sending the response
def send_response():
    global response
    response = response_entry.get()
    
    response = response + " minutes"
    
    # Clear the entry field
    response_entry.delete(0, tk.END)
    
    # Disable the response entry field
    response_entry.config(state=tk.DISABLED)
    
    # Create a new thread to send the response to the client
    threading.Thread(target=send_response_to_client, args=(response,)).start()

# Function to send the response to the client
def send_response_to_client(response):
    global order_status
    try:
        # Send the response to the client
        client_socket.send(response.encode())
        order_status = 5
        
        # Update the status label
        update_status_label("Waiting for order...")
        
        # Close the client socket connection
        client_socket.close()
        
        print("Response sent to the client:", response)
    except socket.error:
        print("Failed to send response to the client.")

def data_storage(command):
    items = word_tokenize(command)

# Create a button to send the response
send_button = tk.Button(window, text="Send Response", font=("Arial", 18), command=send_response)
send_button.pack()
send_button.place(relx=0.43,rely=0.3)

# Create a thread to handle client connections
threading.Thread(target=handle_client_connection, daemon=True).start()

# Start the Tkinter event loop
window.mainloop()

# Close the server socket
server_socket.close()


# In[ ]:





# In[ ]:




