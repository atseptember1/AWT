import os
import glob
import subprocess

#print(glob.glob('*.mov'))

def Downscale(resolutions, list_videos, algorithm='lanczos'):

    list_videos = sorted(list_videos)

    output_videos = []
    for video in list_videos:
        tmp = video.split("_")[-1]
        name = tmp[:-4]
        output_videos.append(name)

    for resolution in resolutions: 
        for input_video, output_video in zip(list_videos, output_videos):
            output_video = resolution + "_" + output_video + ".mp4"
            subprocess.call(['ffmpeg -i {} -af channelmap=0 -vf scale={}:flags={} -map 0:v -map 0:a {}'.format(input_video, resolution, algorithm, output_video)], shell=True)
            #print('ffmpeg -i {} -af channelmap=0 -vf scale={}:flags={} -map 0:v -map 0:a {}'.format(input_video, resolution, algorithm, output_video))


resolutions = ['768x432','960x540','1280x720']

ref_vid_path = os.path.join(os.getcwd(), 'reference_videos')
videos = sorted(os.listdir(ref_vid_path))
#filter all hidden files
videos = list(filter(lambda x: x[0] != '.',videos))

for video in videos:
    video_path = os.path.join(ref_vid_path,video)
    os.chdir(video_path) 
    list_videos = glob.glob('1_*.mov')
    Downscale(resolutions, list_videos)