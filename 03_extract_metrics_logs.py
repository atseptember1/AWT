import os
import subprocess
import glob
import logging

logging.basicConfig(filename='extract_metrics.log', level=logging.DEBUG, 
                    format='%(asctime)s: %(message)s')

resolutions = ['768x432','960x540','1280x720']
algorithms = ["fast_bilinear", "bilinear", "bicubic", "experimental", "neighbor", "area", "bicublin", "gauss", "sinc", "lanczos", "spline"]
log_files_path = os.path.join(os.getcwd(), "log_files")
ref_vid_path = os.path.join(os.getcwd(),"reference_videos")
videos = list(filter(lambda x: x[0] != '.',os.listdir(ref_vid_path)))
videos = sorted(videos)

for video in videos:

    video_dir = os.path.join(ref_vid_path, video)
    
    ref = os.path.join(video_dir, "1_cut_SPL_" + video + ".mov")
    logging.debug("REFERENCE VIDEO:{}".format(ref))
    for resolution in resolutions:
            for alg in algorithms:
                upscale_video = os.path.join(video_dir, "_".join((resolution, alg, "new")) + '.mp4')
                logging.debug("UPSCALE VIDEO:{}".format(upscale_video))

                name_log = "_".join((video, resolution, alg)) + '.log'
                log_path = os.path.join(log_files_path, name_log)
                
                logging.debug('ffmpeg -i {} -i {} -lavfi "[0:v]settb=AVTB,setpts=PTS-STARTPTS[main];[1:v]settb=AVTB,setpts=PTS-STARTPTS[ref];[main][ref]libvmaf=psnr=1:log_fmt=json:log_path={}" -f null -'.format(upscale_video, ref, log_path))
                subprocess.call(['ffmpeg -i {} -i {} -lavfi "[0:v]settb=AVTB,setpts=PTS-STARTPTS[main];[1:v]settb=AVTB,setpts=PTS-STARTPTS[ref];[main][ref]libvmaf=psnr=1:log_fmt=json:log_path={}" -f null -'.format(upscale_video, ref, log_path)], shell=True)





