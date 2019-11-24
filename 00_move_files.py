import os 
import glob

ref_vid_path = os.path.join(os.getcwd(),"reference_videos")

directories = glob.glob(os.path.join(ref_vid_path,'*.mov'))

directories = [x.split('/')[-1].split('_')[-1][:-4] for x in directories]

for directory in directories:
    new_directory = os.path.join(ref_vid_path, directory)
    if not(os.path.exists(new_directory)):
        os.makedirs(new_directory)
    src = glob.glob(os.path.join(ref_vid_path,'*' + directory + '.mov'))
    dst = os.path.join(new_directory,src[0].split('/')[-1])
    os.rename(src[0], dst)

