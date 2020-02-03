import os
import numpy as numpy
import cv2
import subprocess
from tqdm import tqdm
import time
import csv
from ISR.models import RDN, RRDN

headers = ["Video name", "Execution time in sec", "PSNR", "VMAF"]
with open("result.csv", "w", newline="") as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)

model = RRDN(weights="gans")

base = os.getcwd()
reference_videos_path = os.path.join(base, "reference_videos")
video_names = sorted(os.listdir(reference_videos_path))

for video_name in video_names:
    tmp = "_".join(["480x270",video_name]) + ".mov"
    video_path = os.path.join(reference_videos_path, video_name, tmp)

    cap = cv2.VideoCapture(video_path)
    no_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    t = tqdm(total=no_frame)
    i = 1

    print("Processing:", video_name)
    start = time.time()
    while True:
        ret, frame = cap.read()
        if not(ret):
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        sr_frame = model.predict(frame,by_patch_of_size=100)
        sr_frame = cv2.cvtColor(sr_frame, cv2.COLOR_RGB2BGR)
        frame_path = os.path.join(reference_videos_path, video_name, "frame_480x270_{:04d}.png".format(i))
        cv2.imwrite(frame_path, sr_frame)
        i += 1
        t.update()
    cap.release()

    os.chdir(os.path.join(reference_videos_path, video_name))
    command = "ffmpeg -framerate 24 -i frame_480x270_%04d.png sr_1920x1080_480x270_{}.mov".format(video_name)
    subprocess.call(command, shell=True)
    stop = time.time()

    os.chdir(base)
    with open("result.csv", "a", newline="") as f:
        f_csv = csv.writer(f)
        f_csv.writerow([tmp, round((stop-start),2)])

