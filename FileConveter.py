import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import concurrent.futures
import os

# Increase the decompression bomb threshold
Image.MAX_IMAGE_PIXELS = None  # Removes the limit

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Resizer")
        self.root.geometry("500x400")  # Set a window size
        self.root.configure(bg="#f0f0f0")  # Light gray background

        # File list
        self.files = []
        
        # GUI Components
        self.create_widgets()

    def create_widgets(self):
        # Frame for file selection and conversion options
        frame1 = tk.Frame(self.root, bg="#e0e0e0", padx=20, pady=20)
        frame1.pack(fill="x")

        # File Selection Button
        self.select_button = tk.Button(frame1, text="Select Images", command=self.select_files, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
        self.select_button.pack(pady=10, side="left")

        # Resize Options
        tk.Label(frame1, text="Width:", bg="#e0e0e0", font=("Helvetica", 12)).pack(pady=5, side="left")
        self.width_entry = tk.Entry(frame1, width=10, font=("Helvetica", 12))
        self.width_entry.pack(pady=5, side="left")

        tk.Label(frame1, text="Height:", bg="#e0e0e0", font=("Helvetica", 12)).pack(pady=5, side="left")
        self.height_entry = tk.Entry(frame1, width=10, font=("Helvetica", 12))
        self.height_entry.pack(pady=5, side="left")

        # Start and Cancel Buttons
        button_frame = tk.Frame(self.root, bg="#e0e0e0", padx=20, pady=10)
        button_frame.pack(fill="x")

        self.start_button = tk.Button(button_frame, text="Start Resizing", command=self.start_resizing, bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"))
        self.start_button.pack(pady=10, side="left")

        self.cancel_button = tk.Button(button_frame, text="Cancel", command=self.cancel_resizing, bg="#f44336", fg="white", font=("Helvetica", 12, "bold"))
        self.cancel_button.pack(pady=10, side="left")

        # Progress Bar and Status Bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

        self.status_label = tk.Label(self.root, text="Status: Waiting for input", bg="#e0e0e0", font=("Helvetica", 12))
        self.status_label.pack(pady=10)

        # Initialize state variables
        self.cancel_flag = False
        self.executor = None

    def select_files(self):
        self.files = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")])
        if self.files:
            self.status_label.config(text=f"{len(self.files)} files selected.")

    def resize_image(self, file_path, width, height):
        try:
            # Ensure the resized_images directory exists
            os.makedirs("resized_images", exist_ok=True)

            with Image.open(file_path) as img:
                img = img.resize((width, height), Image.ANTIALIAS)
                
                # Save the resized image to the resized_images directory
                base_name = os.path.basename(file_path)
                new_file_path = os.path.join("resized_images", base_name)
                img.save(new_file_path)
                
                return True, file_path
        except Exception as e:
            return False, file_path

    def start_resizing(self):
        if not self.files:
            messagebox.showwarning("No Files Selected", "Please select image files to resize.")
            return

        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid dimensions.")
            return
        
        # Reset progress
        self.progress["value"] = 0
        self.progress["maximum"] = len(self.files)
        
        # Initialize thread pool
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)
        self.cancel_flag = False

        futures = []
        for file in self.files:
            if self.cancel_flag:
                break
            future = self.executor.submit(self.resize_image, file, width, height)
            future.add_done_callback(self.update_progress)
            futures.append(future)
        
        self.executor.shutdown(wait=False)
        self.check_completion(futures)

    def update_progress(self, future):
        success, file_path = future.result()
        if success:
            self.progress["value"] += 1
            self.status_label.config(text=f"Processed: {os.path.basename(file_path)}")
        else:
            self.status_label.config(text=f"Failed: {os.path.basename(file_path)}")

    def check_completion(self, futures):
        def check():
            if all(f.done() for f in futures):
                if self.cancel_flag:
                    self.status_label.config(text="Resizing cancelled.")
                else:
                    self.status_label.config(text="All images processed successfully!")
            else:
                self.root.after(100, check)
        
        self.root.after(100, check)

    def cancel_resizing(self):
        if self.executor:
            self.cancel_flag = True
            self.executor.shutdown(wait=False)
            self.status_label.config(text="Cancelling...")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageResizerApp(root)
    root.mainloop()
