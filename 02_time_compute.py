import os 
import subprocess
import time
from collections import defaultdict
import json
import glob
import logging
#if os.path.exists("demofile.txt"):
#  os.remove("demofile.txt")
#else:
#  print("The file does not exist")
logging.basicConfig(filename='time_compute.log', level=logging.DEBUG, 
                    format='%(asctime)s: %(message)s')

def Computation_Time(sample_video, algorithm, output_video):
    start = time.time()
    logging.debug("ffmpeg -i {} -vf scale=1920x1080:flags={} {}".format(sample_video, algorithm, output_video))
    subprocess.call(["ffmpeg -i {} -vf scale=1920x1080:flags={} {}".format(sample_video, algorithm, output_video)], shell=True)
    stop = time.time()
    
    computation_time = stop-start
    return round(computation_time, 3)

#get list of all directories contain original video and its downscaled videos
ref_vid_path = os.path.join(os.getcwd(),"reference_videos")
videos = list(filter(lambda x: x[0] != '.',os.listdir(ref_vid_path)))
videos = sorted(videos)

resolutions = ['768x432','960x540','1280x720']
algorithms = ["fast_bilinear", "bilinear", "bicubic", "experimental", "neighbor", "area", "bicublin", "gauss", "sinc", "lanczos", "spline"]

for video in videos:

    video_dir = os.path.join(ref_vid_path, video)
    
    #delete all videos which have word "new" in their name
    files_to_delete = glob.glob(os.path.join(video_dir,"*new*"))
    if files_to_delete:
        for file in files_to_delete:
            if os.path.exists(file):
                os.remove(file)

    test_resolution = defaultdict()
    processed_video = defaultdict()

    for resolution in resolutions:
        computation_time = defaultdict()
        for alg in algorithms:
            logging.debug("Processing:{}".format(alg))
            input_path = os.path.join(video_dir,"_".join((resolution, video))+".mp4")
            output_video = resolution + "_" + alg + "_new.mp4"
            output_path = os.path.join(video_dir, output_video)
            logging.debug("Input video:{}".format(input_path))
            logging.debug("Output video:{}".format(output_path))
            computation_time[alg] = Computation_Time(input_path, alg, output_path)
        test_resolution[resolution] = computation_time
    
    processed_video[video] = test_resolution

    #using "a" argument to write to existing file
    with open('report.txt','a') as file:
        json.dump(processed_video, file)
        file.write('\n')

    


