import os
import json
import matplotlib.pyplot as plt
import numpy as np
import glob
from collections import defaultdict

ref_vid_path = os.path.join(os.getcwd(), 'reference_videos')
videos = list(filter(lambda x: x[0] != '.',os.listdir(ref_vid_path)))
log_files_path = os.path.join(os.getcwd(), "log_files")

resolutions = ['960x540','1280x720']
algorithms = ["fast_bilinear", "bilinear", "bicubic", "experimental", "neighbor", "area", "bicublin", "gauss", "sinc", "lanczos", "spline"]

times = {}
with open('report.txt', 'r') as file:
    for line in file:
        json_data = json.loads(line.strip('\n'))
        times.update(json_data)

for video in videos:
    res_metrics = defaultdict()
    for resolution in resolutions:
        alg_metrics = defaultdict(list)
        for alg in algorithms:
            print(video,resolution,alg)
            alg_log_path = glob.glob(os.path.join(log_files_path, "_".join((video, resolution, alg)) + '.log'))[0]
        
            try:
                with open(alg_log_path, 'r') as log:
                    report = json.load(log)

                alg_metrics[alg].append(report['VMAF score'])
                alg_metrics[alg].append(report['PSNR score'])
                print("ok")
            except Exception as e:
                print('Error in {}: {}'.format(alg, e))
            #print(alg_log_path)
        res_metrics[resolution] = alg_metrics

        time_compute = []
        vmaf = []
        psnr = []
        for alg in res_metrics[resolution].keys():
            time_compute.append(times[video][resolution][alg])
            vmaf.append(res_metrics[resolution][alg][0])
            psnr.append(res_metrics[resolution][alg][0])

        if vmaf:
            time_partial = np.array(time_compute)/np.mean(time_compute)
            vmaf_scale = np.array(vmaf)/time_partial
            psnr_scale = np.array(psnr)/time_partial

            fig, ax = plt.subplots(1,2, figsize=(30,5))
            ax = ax.flatten()

            ord_num_alg = np.arange(len(res_metrics[resolution].keys()))


            vmaf_alg = np.array(list(res_metrics[resolution].keys()))
            idx = np.argsort(vmaf_scale)[::-1]
            vmaf_scale = np.array(vmaf_scale)[idx]
            vmaf_alg = np.array(vmaf_alg)[idx]

            ax[0].scatter(ord_num_alg, vmaf_scale, s=200, c='orange')
            ax[0].grid(True)
            for i, alg in enumerate(vmaf_alg):
                ax[0].annotate(alg, (ord_num_alg[i], vmaf_scale[i]))
            ax[0].set_xticks(np.arange(len(res_metrics[resolution].keys())))
            ax[0].set_xlabel('Algorithm Rank')
            ax[0].set_ylabel('Vmaf Scale')
            ax[0].set_title('Comparation of Algorithms',size=13)

            psnr_alg = np.array(list(res_metrics[resolution].keys()))
            idx = np.argsort(psnr_scale)[::-1]
            psnr_scale = np.array(psnr_scale)[idx]
            psnr_alg = np.array(psnr_alg)[idx]

            ax[1].scatter(ord_num_alg, psnr_scale, s=200, c='green')
            ax[1].grid(True)
            for i, alg in enumerate(psnr_alg):
                ax[1].annotate(alg, (ord_num_alg[i], psnr_scale[i]))
            ax[1].set_xticks(np.arange(len(res_metrics[resolution].keys())))
            ax[1].set_xlabel('Algorithm Rank')
            ax[1].set_ylabel('PSNR Scale')
            ax[1].set_title('Comparation of Algorithms',size=13)

            suptitle = "_".join((video, resolution))
            fig.suptitle(suptitle, size=17)


            path_to_save = os.path.join(os.getcwd(),'figures',suptitle+'.png')
            plt.savefig(path_to_save)
        else:
            pass