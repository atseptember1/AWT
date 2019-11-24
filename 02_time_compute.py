import os 
import subprocess
import time
from collections import defaultdict
import json
import glob

#if os.path.exists("demofile.txt"):
#  os.remove("demofile.txt")
#else:
#  print("The file does not exist")

def Computation_Time(sample_video, algorithm, output_video):
    start = time.time()
    subprocess.call(["ffmpeg -i {} -vf scale=1920x1080:flags={} {}".format(sample_video, algorithm, output_video)], shell=True)
    #print("ffmpeg -i {} -vf scale=1920x1080:flags={} {}".format(sample_video, algorithm, output_video))
    stop = time.time()
    
    computation_time = stop-start
    return round(computation_time, 3)

#get list of all directories contain original video and its downscaled videos
ref_vid_path = os.path.join(os.getcwd(),"reference_videos")
video_folders = list(filter(lambda x: x[0] != '.',os.listdir(ref_vid_path)))

for video_folder in video_folders:

    folder_path = os.path.join(ref_vid_path, video_folder)
    
    #delete all videos which have word "new" in their name
    files_to_delete = glob.glob(os.path.join(folder_path,"*new*"))
    if files_to_delete:
        for file in files_to_delete:
            if os.path.exists(file):
                os.remove(file)

    resolutions = ['768x432','960x540','1280x720']
    algorithms = ["fast_bilinear", "bilinear", "bicubic", "experimental", "neighbor", "area", "bicublin", "gauss", "sinc", "lanczos", "spline"]
    #algorithms = ["fast_bilinear", "bilinear"]


    computation_time = defaultdict()
    test_resolution = defaultdict()
    processed_video = defaultdict()

    for resolution in resolutions:
        for alg in algorithms:
            print("Processing ", alg)
            output_video = resolution + "_" + alg + "_new.mp4"
            output_path = os.path.join(folder_path, output_video)
            input_path = glob.glob(os.path.join(folder_path,resolution + "*" + '.mp4'))[0]

            computation_time[alg] = Computation_Time(input_path, alg, output_path)
        test_resolution[resolution] = computation_time
    
    processed_video[video_folder] = test_resolution

    #using "a" argument to write to existing file
    with open('report.txt','a') as file:
        json.dump(processed_video, file)
        file.write('\n')


    


