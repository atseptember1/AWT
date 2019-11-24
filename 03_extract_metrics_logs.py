import os
import subprocess
import glob


resolutions = ['768x432','960x540','1280x720']
log_files_path = os.path.join(os.getcwd(), "log_files")
ref_vid_path = os.path.join(os.getcwd(),"reference_videos")
video_folders = list(filter(lambda x: x[0] != '.',os.listdir(ref_vid_path)))

for video_folder in video_folders:

    folder_path = os.path.join(ref_vid_path, video_folder)
    
    ref = glob.glob(os.path.join(folder_path, '*SPL*'))[0]
    #print(ref)
    for resolution in resolutions:
        upscale_videos = glob.glob(os.path.join(folder_path,resolution + '*' + 'bilinear_new' + "*"))

        for main in upscale_videos:
            tmp = main.split("_")
            if 'fast' in tmp:
                name_log = video_folder + '_' + resolution + '_' 'fast' + '_' + tmp[-2] + '.log'
            else:
                name_log = video_folder + '_' + resolution + '_' + tmp[-2] + '.log'
            log_path = os.path.join(log_files_path, name_log)
            print(log_path)
            subprocess.call(['ffmpeg -i {} -i {} -lavfi "libvmaf=psnr=1:log_fmt=json:log_path={}" -f null -'.format(main, ref, log_path)], shell=True)







