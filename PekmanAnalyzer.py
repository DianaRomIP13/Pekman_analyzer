import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import threading
from PIL import Image, ImageDraw, ImageFont
import cv2

def display_results_window(result, new_path):
    results_window = tk.Toplevel(root)
    results_window.title("Pekman analyzer")
    set_window_properties(results_window)

    view_result_button = tk.Button(results_window, text="View Result", command=lambda: view_result(new_path, result))
    view_result_button.pack(side="top", pady=20)

    save_result_button = tk.Button(results_window, text="Save Result", command=lambda: save_result(new_path, result))
    save_result_button.pack(pady=10)

    def on_close():
        root.destroy()

    def on_back():
        results_window.destroy()
        root.deiconify()

    results_window.protocol("WM_DELETE_WINDOW", on_close)

    back_button = tk.Button(results_window, text="Back", command=on_back)
    back_button.pack(side="left", padx=10, anchor="sw")

def view_result(new_path, result):
    if isinstance(result, str):
        img = Image.open(new_path)
        draw = ImageDraw.Draw(img)

        img_width, img_height = img.size

        # Choose the font size as a fraction of the image width
        font_size = max(1, int(img_width / 25))

        # Use the default font
        font = ImageFont.load_default().font_variant(size=font_size)

        text_color = 255

        draw.text((10, 10), result, text_color, font=font)

        img.show()

    elif isinstance(result, list):
        for frame in result:
            cv2.imshow('Processed Video', frame)
            if cv2.waitKey(30) & 0xFF == 27:  # Pressing 'Esc' to exit
                break

        cv2.destroyAllWindows()
def save_result(new_path, result):
    if isinstance(result, str):
        img = Image.open(new_path)
        draw = ImageDraw.Draw(img)

        img_width, img_height = img.size

        font_size = max(1, int(img_width / 25))

        font = ImageFont.load_default().font_variant(size=font_size)

        text_color = 255

        draw.text((10, 10), result, text_color, font=font)
        save_path = filedialog.asksaveasfilename(defaultextension=".jpeg", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
        if save_path:
            img.save(save_path)
    elif isinstance(result, list):
        save_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])
        if save_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            height, width, _ = result[0].shape
            video_writer = cv2.VideoWriter(save_path, fourcc, 30.0, (width, height))

            for frame in result:
                video_writer.write(frame)

            video_writer.release()


def open_next_window(choice):
    if choice.get() == 1:
        open_image_window()
        root.withdraw()
    elif choice.get() == 2:
        open_video_window()
        root.withdraw()


def open_image_window():
    image_window = tk.Toplevel(root)
    image_window.title("Pekman analyzer")
    set_window_properties(image_window)

    upload_button = tk.Button(image_window, text="Upload Image", command=lambda: upload_file(image_window, "image"))
    upload_button.pack(side="top", pady=20)

    next_button = tk.Button(image_window, text="Next", state=tk.DISABLED, command=lambda: process_file(image_window, "image"))
    next_button.pack(side="right", padx=10, anchor="se")

    def on_close():
        root.destroy()

    def on_back():
        image_window.destroy()
        root.deiconify()

    image_window.protocol("WM_DELETE_WINDOW", on_close)

    back_button = tk.Button(image_window, text="Back", command=on_back)
    back_button.pack(side="left", padx=10, anchor="sw")


def open_video_window():
    video_window = tk.Toplevel(root)
    video_window.title("Pekman analyzer")
    set_window_properties(video_window)

    upload_button = tk.Button(video_window, text="Upload Video", command=lambda: upload_file(video_window, "video"))
    upload_button.pack(side="top", pady=20)

    next_button = tk.Button(video_window, text="Next", state=tk.DISABLED, command=lambda: process_file(video_window, "video"))
    next_button.pack(side="right", padx=10, anchor="se")

    def on_close():
        root.destroy()

    def on_back():
        video_window.destroy()
        root.deiconify()

    video_window.protocol("WM_DELETE_WINDOW", on_close)

    back_button = tk.Button(video_window, text="Back", command=on_back)
    back_button.pack(side="left", padx=10, anchor="sw")


def upload_file(window, file_type):
    file_path = filedialog.askopenfilename()

    if file_path:
        if file_type == "image":
            if not file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                messagebox.showerror("Error", "Only upload images!")
                return
            if file_size(file_path) > 10:
                messagebox.showerror("Error", "The maximum image size should be less than 10 MB.")
            else:
                update_upload_button(window, file_path, file_type)
                update_next_button(window, file_path, file_type)
        elif file_type == "video":
            if not file_path.lower().endswith(('.mp4', '.avi', '.mov')):
                messagebox.showerror("Error", "Upload only videos!")
                return
            if file_size(file_path) > 100:
                messagebox.showerror("Error", "The maximum video size should be less than 100 MB.")
            else:
                update_upload_button(window, file_path, file_type)
                update_next_button(window, file_path, file_type)


def process_file(window, file_type):
    new_path = get_new_path(window)
    if new_path:
        progress_window = open_progress_window()
        thread = threading.Thread(target=run_main_script, args=(new_path, progress_window))
        thread.start()
    window.destroy()

def run_main_script(new_path, progress_window):
    if new_path:
        from processing import processing_file
        result = processing_file(new_path)
        # After completing the main script closing progress window
        progress_window.destroy()
        # After closing the progress window calling the function to display the results window
        display_results_window(result, new_path)


def update_progress(progress_bar, value):
    progress_bar['value'] = value
    root.update_idletasks()


def get_new_path(window):
    upload_button = [widget for widget in window.winfo_children() if isinstance(widget, tk.Button)][0]
    return upload_button.cget("text").split("\n")[-1]


def update_upload_button(window, file_path, file_type):
    upload_button = [widget for widget in window.winfo_children() if isinstance(widget, tk.Button)][0]
    upload_button.config(state=tk.DISABLED, text="The file has already been uploaded\n{}".format(file_path))


def update_next_button(window, file_path, file_type):
    next_button = [widget for widget in window.winfo_children() if isinstance(widget, tk.Button) and "Next" in widget.cget("text")][0]
    next_button.config(state=tk.NORMAL, command=lambda: process_file(window, file_type))


def process_file_and_pass_path(window, file_path, file_type):
    process_file(window, file_type)


def file_size(file_path):
    import os
    return os.path.getsize(file_path) / (1024 * 1024)  # Size in MB


def open_progress_window():
    progress_window = tk.Toplevel(root)
    progress_window.title("Pekman analyzer")
    set_window_properties(progress_window)
    progress_label = tk.Label(progress_window, text="Processing...")
    progress_label.pack(side="top", pady=20)

    progress_bar = ttk.Progressbar(progress_window, length=200, mode="indeterminate")
    progress_bar.pack(pady=10)
    progress_bar.start()

    def on_close():
        progress_window.destroy()

    progress_window.protocol("WM_DELETE_WINDOW", on_close)

    return progress_window

def set_window_properties(window):
    # Get the screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Centering the window in the center
    x_position = (screen_width - 400) // 2
    y_position = (screen_height - 300) // 2

    window.geometry(f"400x300+{x_position}+{y_position}")


def main():
    global root
    root = tk.Tk()
    root.title("Pekman analyzer")

    window_width = 400
    window_height = 300

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_position = (screen_width - window_width) // 2
    y_position = (screen_height - window_height) // 2

    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    label = tk.Label(root, text="Select the file type")
    label.pack(side="top", pady=20)

    choice = tk.IntVar()

    image_radio = tk.Radiobutton(root, text="Image", variable=choice, value=1)
    image_radio.pack()

    video_radio = tk.Radiobutton(root, text="Video", variable=choice, value=2)
    video_radio.pack()

    next_button = tk.Button(root, text="Next", command=lambda: open_next_window(choice))
    next_button.pack(side="bottom", pady=10, padx=10, anchor="se")

    root.mainloop()


if __name__ == "__main__":
    main()
