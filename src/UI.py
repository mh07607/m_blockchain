#Instructions:
#First create a block by typing a block number and then clicking add block:
#Then type the block number to which you want to add document. Then click add document. Browse will open which only accepts .txt files.
#Then Type the block number and click build block to construct a merkle tree.
#Verify document button can be clicked. All the documents added should appear in a dropdown menu below the button.

import tkinter as tk
from tkinter import filedialog, messagebox
from blockchain import*

File_Address_txt = [] # List of Tuples (Block Num, FileAddress)
block_num_lst = [] # List of Block Numbers
file_address_dropdown = None # Initializing
built_blocks=[]
# Blockchain.apppend(BuildBlock(B1))

def browse_file():
    filetypes = [('Text Files', '*.txt')] # Restricting FileType to txt 
    filename = filedialog.askopenfilename(filetypes=filetypes)
    if filename:
        block_number = block_number_entry.get()
        if block_number.isdigit(): # Checking if Block Number is integer
            if block_number not in block_num_lst: # Checking if Block number exists
                messagebox.showerror("Error", "Block Number does not exist")
                return
            File_Address_txt.append((block_number, filename)) # Creates a tuple of Block_number and File Address
            print(File_Address_txt)
            messagebox.showinfo("Success", "File added")
            update() # Updating Dropdown Menu's contents
        else:
            messagebox.showerror("Error", "Block Number is not an integer")
            return
    else:
        return
    
def add_block():
    block_number = block_number_entry.get()
    if block_number.isdigit() and block_number not in block_num_lst: # Error Checking/Repeatition Checking
        # Add block code here
        messagebox.showinfo("Success", "Block added")
        block_num_lst.append(block_number)
        return True
    else:
        messagebox.showerror("Error", "Invalid block number")
        return False
    
def build_block():
    block_number = block_number_entry.get()
    if not block_number.isdigit() or block_number not in block_num_lst: # Error Checking/Repeatition Checking
        messagebox.showerror("Error", "Invalid block number")
        return
    # Procures File addresses for the entered block num, and 
    file_addresses = [address[1] for address in File_Address_txt if address[0] == block_number]
    if not file_addresses:
        messagebox.showwarning("Warning", f"No files found for block {block_number}")
        return
    if block_number in built_blocks: # Avoiding Repeat Build
        messagebox.showwarning("Warning", f"Block was already built! You cannot make it again! {block_number}")
        return
    else:
        built_blocks.append(block_number) # Noting down Built merkle trees
    # Call Build Block Here!
    messagebox.showinfo("Success", "Merkle Tree Constructed! Block built!")
    
def verify_chain():
    # Verify chain code here
    blockchain = blockchain()
    is_valid = blockchain.verify()
    if(is_valid):
        print("The blockchain is valid")
        messagebox.showinfo("Success", "Blockchain is Valid!")
    else:
        print("The blockchain is not valid")
        messagebox.showerror("Error", "Invalid Blockchain! Correction Needed")

def verify_document():
    selected_file = file_address_selection.get()
    if not selected_file:
        messagebox.showerror("Error", "No file selected")
        return
    # Verify document code here
    print(f"Selected file: {selected_file}")
    messagebox.showinfo("Success", "Document verified")
    
def update():
    global file_address_dropdown  # Add a global declaration here
    file_addresses = [address[1] for address in File_Address_txt]
    file_address_selection.set("") # default value
    if file_addresses:
        if file_address_dropdown is not None:  # Check if it already exists and destroy it
            file_address_dropdown.destroy()
        file_address_dropdown = tk.OptionMenu(root, file_address_selection, *file_addresses)
        file_address_dropdown.pack()
    else:
        tk.Label(root, text="No files added yet").pack()
        
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root = tk.Tk()
root.geometry("400x450")
root.title("Merkle Tree Testing")
root.protocol("WM_DELETE_WINDOW", on_closing)

# Create a Label widget for the heading
heading_label = tk.Label(root, text="JunejoCoin", font=("Arial", 18))
heading_label.pack(side="top", fill="x", pady=10)

# Block number field
block_number_label = tk.Label(root, text="Block number:")
block_number_label.pack()
block_number_entry = tk.Entry(root)
block_number_entry.pack()

# Add block button
add_block_button = tk.Button(root, text="Add Block", command=add_block)
add_block_button.pack(pady=10)

# Browse button to select txt files
add_document_button = tk.Button(root, text="Add Document", command=browse_file)
add_document_button.pack(pady=10)

# Build Block Button
build_block_button = tk.Button(root, text="Build Block", command=build_block)
build_block_button.pack(pady=10)

# Verify chain button
verify_chain_button = tk.Button(root, text="Verify Chain", command=verify_chain)
verify_chain_button.pack(pady=10)

# Verify document button
verify_document_button = tk.Button(root, text="Verify Document", command=verify_document)
verify_document_button.pack(pady=10)

# File address selection dropdown
file_address_selection_label = tk.Label(root, text="Select file address:")
file_address_selection_label.pack()
file_address_selection = tk.StringVar(root)
file_address_selection.set("") # default value
if File_Address_txt:
    update()
else:
    tk.Label(root, text="").pack()
root.mainloop()
#UI se implement add verify
# Block chain mai it returns false everytime
# comparison of other data structures
# inter certifcates verifying