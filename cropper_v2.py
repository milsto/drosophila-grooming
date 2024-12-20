import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import subprocess
import csv

# Set the path to ffmpeg.exe
FFMPEG_PATH = r"C:\Users\milos\Desktop\src\ffmpeg.exe"

def select_bounding_boxes(video_path):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    if not ret:
        print("Failed to read video")
        return
    cap.release()
    root = tk.Tk()
    
    # Mode selection
    mode = tk.StringVar(value="manual")
    tk.Radiobutton(root, text="Manual", variable=mode, value="manual").pack(anchor=tk.W)
    tk.Radiobutton(root, text="Fixed", variable=mode, value="fixed").pack(anchor=tk.W)

    # Rectangle size inputs
    tk.Label(root, text="Rectangle Width:").pack(anchor=tk.W)
    rect_width = tk.Entry(root)
    rect_width.insert(0, "200")
    rect_width.pack(anchor=tk.W)
    tk.Label(root, text="Rectangle Height:").pack(anchor=tk.W)
    rect_height = tk.Entry(root)
    rect_height.insert(0, "200")
    rect_height.pack(anchor=tk.W)

    button = tk.Button(root, text="Done", command=root.quit)
    button.pack()
    
    orig_height, orig_width = frame.shape[:2]
    new_width = 1280
    new_height = 720
    scale_x = orig_width / new_width
    scale_y = orig_height / new_height
    frame = cv2.resize(frame, (new_width, new_height))
    canvas = tk.Canvas(root, width=new_width, height=new_height)
    canvas.pack()
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, image=photo, anchor=tk.NW)
    boxes = []
    box = []

    def on_click(event):
        nonlocal box
        if mode.get() == "manual":
            if len(box) == 4:
                box = []
            box.append(event.x * scale_x)
            box.append(event.y * scale_y)
            if len(box) == 4:
                x1, y1, x2, y2 = box
                canvas.create_rectangle(x1 / scale_x, y1 / scale_y, x2 / scale_x, y2 / scale_y, outline="red")
                boxes.append(box)
        else:
            box = []
            width = int(rect_width.get())
            height = int(rect_height.get())
            box = [event.x * scale_x, event.y * scale_y, (event.x + width) * scale_x, (event.y + height) * scale_y]
            canvas.create_rectangle(box[0] / scale_x, box[1] / scale_y, box[2] / scale_x, box[3] / scale_y, outline="red")
            boxes.append(box)

    def on_move(event):
        if mode.get() == "manual" and len(box) == 2:
            canvas.delete("preview")
            canvas.create_rectangle(box[0] / scale_x, box[1] / scale_y, event.x, event.y, outline="red", tag="preview")
        if mode.get() == "fixed":
            width = int(rect_width.get())
            height = int(rect_height.get())
            canvas.delete("preview")
            canvas.create_rectangle(event.x, event.y, event.x + width, event.y + height, outline="red", tag="preview")
    
    def on_leave(event):
        canvas.delete("preview")

    canvas.bind("<Button-1>", on_click)
    canvas.bind("<Motion>", on_move)
    canvas.bind("<Leave>", on_leave)

    root.mainloop()
    return boxes


def crop_videos(input_video_path, bounding_boxes, output_dir):
    for i, box in enumerate(bounding_boxes):
        x1, y1, x2, y2 = box
        width = x2 - x1
        height = y2 - y1
        output_path = os.path.join(output_dir, os.path.basename(input_video_path) + f'_cropped_{i}.mp4')
        command = f'{FFMPEG_PATH} -i "{input_video_path}" -filter:v "crop={width}:{height}:{x1}:{y1}" -c:a copy "{output_path}"'
        subprocess.call(command, shell=True)


def save_bounding_boxes(boxes, output_path):
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['x1', 'y1', 'x2', 'y2'])
        for box in boxes:
            writer.writerow(box)


if __name__ == "__main__":
    video_path = os.path.normpath(filedialog.askopenfilename(title="Select video file"))
    boxes = select_bounding_boxes(video_path)

    crop_videos(video_path, boxes, os.path.dirname(video_path))
    
    save_bounding_boxes(boxes, video_path + "_boxes.csv")

    print(boxes)