import tkinter as tk
from tkinter import END, messagebox

# Function to evaluate the mathematical expression
def evaluate_expression(expression):
    try:
        # Manually evaluate the expression using a custom algorithm
        result = eval_expression(expression)
        return result
    except Exception as e:
        return "Error"

# Function to manually evaluate the expression
def eval_expression(expression):
    # Clean up spaces
    expression = expression.replace(' ', '')
    
    # Helper function to apply an operation and return the result
    def apply_operation(operators, values):
        operator = operators.pop()
        right = values.pop()
        left = values.pop()
        if operator == '+':
            values.append(left + right)
        elif operator == '-':
            values.append(left - right)
        elif operator == '*':
            values.append(left * right)
        elif operator == '/':
            values.append(left / right)

    # Operator precedence
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    operators = []
    values = []
    i = 0
    
    while i < len(expression):
        if expression[i].isdigit():
            value = 0
            while i < len(expression) and expression[i].isdigit():
                value = value * 10 + int(expression[i])
                i += 1
            values.append(value)
            i -= 1
        elif expression[i] == '(':
            operators.append(expression[i])
        elif expression[i] == ')':
            while operators and operators[-1] != '(':
                apply_operation(operators, values)
            operators.pop()  # remove '(' from stack
        else:
            while (operators and operators[-1] in precedence and
                   precedence[operators[-1]] >= precedence[expression[i]]):
                apply_operation(operators, values)
            operators.append(expression[i])
        i += 1
    
    while operators:
        apply_operation(operators, values)

    return values[-1]

# Function to handle button clicks for numbers and operators
def button_click(value):
    current = e.get()
    e.delete(0, END)
    e.insert(0, current + str(value))

# Function to clear the calculator display
def button_clear():
    e.delete(0, END)

# Function to handle the equal operation
def button_equal():
    expression = e.get()
    result = evaluate_expression(expression)
    e.delete(0, END)
    if result == "Error":
        messagebox.showerror("Error", "Invalid Expression")
    else:
        e.insert(0, str(result))

# Create the main window
root = tk.Tk()
root.title("Simple Calculator")
root.geometry("559x574")
root.resizable(1, 1)
root.configure(bg="#0a0a0a")

# Create an Entry widget for the calculator display
e = tk.Entry(root, font=("arial", 24), bg="#0a0a0a", fg="white")
e.place(x=0, y=30, width=553, height=40)

# Create button widgets for various operations and numbers
button_clear1 = tk.Button(root, font=("arial", 12), text="C", padx=53, pady=20, bd=1, fg="#fff", bg="#a3a09d", command=button_clear)
button_clear1.place(x=10, y=100)

button_divide1 = tk.Button(root, font=("arial", 12), text="/", padx=53, pady=20, fg="#fff", bg="#a3a09d", command=lambda: button_click("/"))
button_divide1.place(x=150, y=100)

button_percentage1 = tk.Button(root, font=("arial", 12), text="%", padx=53, pady=20, fg="#fff", bg="#a3a09d", command=lambda: button_click("%"))
button_percentage1.place(x=290, y=100)

button_multiply1 = tk.Button(root, font=("arial", 13), text="*", padx=53, pady=20, fg="#fff", bg="#FE9037", command=lambda: button_click("*"))
button_multiply1.place(x=430, y=100)

button7 = tk.Button(root, font=("arial", 12), width=5, height=1, text="7", padx=40, pady=20, fg="#fff", bg="#45403c", command=lambda: button_click(7))
button7.place(x=10, y=200)

button8 = tk.Button(root, font=("arial", 12), width=5, height=1, text="8", padx=40, pady=20, fg="#fff", bg="#45403c", command=lambda: button_click(8))
button8.place(x=150, y=200)

button9 = tk.Button(root, font=("arial", 12), width=5, height=1, text="9", padx=40, pady=20, fg="#fff", bg="#45403c", command=lambda: button_click(9))
button9.place(x=290, y=200)

button_difference1 = tk.Button(root, font=("arial", 12), width=5, height=1, text="-", padx=40, pady=20, fg="#fff", bg="#FE9037", command=lambda: button_click("-"))
button_difference1.place(x=430, y=200)

button4 = tk.Button(root, font=("arial", 12), width=5, height=1, text="4", padx=40, pady=20, fg="#fff", bg="#45403c", command=lambda: button_click(4))
button4.place(x=10, y=300)

button5 = tk.Button(root, font=("arial", 12), width=5, height=1, text="5", padx=40, pady=20, fg="#fff", bg="#45403c", command=lambda: button_click(5))
button5.place(x=150, y=300)

button6 = tk.Button(root, font=("arial", 12), width=5, height=1, text="6", padx=40, pady=20, fg="#fff", bg="#45403c", command=lambda: button_click(6))
button6.place(x=290, y=300)

button_add1 = tk.Button(root, font=("arial", 12), width=5, height=1, text="+", padx=39, pady=20, fg="#fff", bg="#FE9037", command=lambda: button_click("+"))
button_add1.place(x=430, y=300)

button1 = tk.Button(root, font=("arial", 12), width=5, height=1, text="1", padx=40, pady=20, fg="#fff", bg="#45403c", command=lambda: button_click(1))
button1.place(x=10, y=400)

button2 = tk.Button(root, font=("arial", 12), width=5, height=1, text="2", padx=40, pady=20, fg="#fff", bg="#45403c", command=lambda: button_click(2))
button2.place(x=150, y=400)

button3 = tk.Button(root, font=("arial", 12), width=5, height=1, text="3", padx=40, pady=20, fg="#fff", bg="#45403c", command=lambda: button_click(3))
button3.place(x=290, y=400)

button0 = tk.Button(root, font=("arial", 12), width=11, height=1, text="0", padx=80, pady=20, fg="#fff", bg="#45403c", command=lambda: button_click(0))
button0.place(x=10, y=500)

button_point = tk.Button(root, font=("arial", 12), text=".", padx=58, pady=20, fg="#fff", bg="#45403c", command=lambda: button_click("."))
button_point.place(x=290, y=500)

button_equal1 = tk.Button(root, font=("arial", 12), text="=", padx=53, pady=70, fg="#fff", bg="#FE9037", command=button_equal)
button_equal1.place(x=430, y=400)

# Start the Tkinter event loop
root.mainloop()
