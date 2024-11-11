import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from PIL import Image, ImageTk, ImageEnhance
from tkinter import filedialog


# scale_int = tk.IntVar(value=20)

class ImageEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        style = Style(theme='solar')
        style.master = self
        
        self.brightness_scale_var = tk.DoubleVar(value=1.0)
        self.contrast_scale_var = tk.DoubleVar(value=1.0)
        self.sharpness_scale_var = tk.DoubleVar(value=1.0)
        self.color_scale_var = tk.DoubleVar(value=1.0)
        
        self.geometry("800x500")
        self.title("Image Editor!")
        self.resizable(False, False)

        self.image = "image.jpg"
        
        self.columnconfigure(0, weight=2, uniform="a")
        self.columnconfigure(1, weight=1, uniform="a")
        self.rowconfigure(0, weight=1, uniform="a")
        
        self.left_frame = tk.Frame(self)
        self.right_frame = tk.Frame(self)

        self.right_frame.columnconfigure((0,1), weight= 1, uniform= "a")
        self.right_frame.rowconfigure((0,1,2,3,4,5,6,7,8), weight=1, uniform= "a")
        
        self.left_frame.rowconfigure(0, weight=1, uniform="a")
        self.left_frame.rowconfigure(1, weight=9, uniform="a")
        self.left_frame.columnconfigure(0, weight=1, uniform="a")
        
        self.putting_image()
        self.creating_widgets()
        self.packing_widgets()
        
        self.mainloop()
        
    def creating_widgets(self):
        self.brightness_label = ttk.Label(self.right_frame, text=f"Change Brightness: {'{:.1f}'.format(self.brightness_scale_var.get() - 1)}")
        self.contrast_label = ttk.Label(self.right_frame, text=f"Change Contrast: {'{:.1f}'.format(self.contrast_scale_var.get() - 1)}")
        self.sharpness_label = ttk.Label(self.right_frame, text=f"Change Sharpness: {'{:.1f}'.format(self.sharpness_scale_var.get() - 1)}")
        self.color_label = ttk.Label(self.right_frame, text=f"Change Color:  {'{:.1f}'.format(self.color_scale_var.get() - 1)}")
        self.revert_button = ttk.Button(self.right_frame, text="Revert all", command=self.revert_all)
        self.save_image_button = ttk.Button(self.right_frame, text="Save Image", command=self.save_image)
        self.change_image_button = ttk.Button(self.left_frame, text="Change Image", command=self.change_image)
        self.image_label = tk.Label(self.left_frame, image=self.tk_image, bd=2, relief="ridge")
        self.brightness_scale = ttk.Scale(self.right_frame, command=self.edit_image, from_ = 0.0, to = 2.0, length=100, orient="horizontal", variable=self.brightness_scale_var)
        self.contrast_scale = ttk.Scale(self.right_frame, command=self.edit_image, from_ = 0.0, to = 2.0, length=100, orient="horizontal", variable=self.contrast_scale_var)
        self.sharpness_scale = ttk.Scale(self.right_frame, command=self.edit_image, from_ = 0.0, to = 2.0, length=100, orient="horizontal", variable=self.sharpness_scale_var)
        self.color_scale = ttk.Scale(self.right_frame, command=self.edit_image, from_ = 0.0, to = 2.0, length=100, orient="horizontal", variable=self.color_scale_var)

    
    def packing_widgets(self):
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        self.left_frame.grid(row=0, column=0, sticky="nsew")
        self.image_label.grid(row = 1, column=0, padx=10, pady=10)
        # pack(expand = True, padx=10, pady=10)
        
        self.brightness_label.grid(row = 0, column= 0, sticky= "nsew", columnspan=2, padx= 10)
        self.brightness_scale.grid(row = 1, column=0, sticky="nsew", padx= 10, columnspan=2)
        
        self.contrast_label.grid(row = 2, column= 0, sticky= "nsew", columnspan=2, padx= 10)
        self.contrast_scale.grid(row = 3, column=0, sticky="nsew", padx= 10, columnspan=2)
        
        self.sharpness_label.grid(row = 4, column= 0, sticky= "nsew", columnspan=2, padx= 10)
        self.sharpness_scale.grid(row = 5, column=0, sticky="nsew", padx= 10, columnspan=2)
        
        self.color_label.grid(row = 6, column= 0, sticky= "nsew", columnspan=2, padx= 10)
        self.color_scale.grid(row = 7, column=0, sticky="nsew", padx= 10, columnspan=2)
        
        self.change_image_button.grid(row = 0, column = 0, sticky="nsew", padx=(10,10), pady=(10,0))
        
        self.revert_button.grid(row = 8, column=0)
        self.save_image_button.grid(row = 8, column=1)
        
    def putting_image(self): 
        original_image = Image.open(self.image)
        frame_width = 800 * 0.67  
        frame_height = 400  
        original_image.thumbnail((frame_width, frame_height), Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(original_image)

        
    def edit_image(self, value):
        self.brightness_label.config(text=f"Change Brightness: {'{:.1f}'.format(self.brightness_scale_var.get() - 1)}")
        self.contrast_label.config(text=f"Change Contrast: {'{:.1f}'.format(self.contrast_scale_var.get() - 1)}")
        self.sharpness_label.config(text=f"Change Sharpness: {'{:.1f}'.format(self.sharpness_scale_var.get() - 1)}")
        self.color_label.config(text=f"Change Color: {'{:.1f}'.format(self.color_scale_var.get() - 1)}")

        
        img = Image.open(self.image)
        
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(self.brightness_scale_var.get())
        
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(self.contrast_scale_var.get())
    
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(self.sharpness_scale_var.get())
        
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(self.color_scale_var.get())
        
        self.update_image(img)

    def update_image(self, img):
        frame_width = 800 * 0.67  
        frame_height = 400
        img.thumbnail((frame_width, frame_height), Image.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.tk_image)
        
        
    def revert_all(self):
        self.brightness_scale_var.set(1.0)
        self.contrast_scale_var.set(1.0)
        self.sharpness_scale_var.set(1.0)
        self.color_scale_var.set(1.0)
        
        self.edit_image(1)
        
    def change_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.image = file_path
            self.putting_image()
            self.image_label.config(image=self.tk_image)
            self.revert_all()
            
            
    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", 
                                                filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            img = Image.open(self.image)
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(self.brightness_scale_var.get())
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(self.contrast_scale_var.get())
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(self.sharpness_scale_var.get())
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(self.color_scale_var.get())
            img.save(file_path)

        
        
        
        
                    

ImageEditor()
