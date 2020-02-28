# Advance Web Technology project
This repository includes all source codes that related to Advance Web Technology (AWT) project. The goal of this project is to compare conventional upscaling algorithms such as "fast bilinear", "bilinear", "bicubic", "experimental", "neighbor", "area", "bicublin", "gauss", "sinc", "lanczos", "spline" and super resolution algorithm in term of video quality and execution time.

## Installation
1.	Clone this repository
	```
	git clone https://github.com/atseptember1/AWT.git
	```
2.	Install all requirements:
	```
	pip install -r requirements.txt
	```
3.	Make 3 new folders: figures, log_files, reference_videos
	```
	mkdir figures log_files reference_videos
	```
4.	Run all .py file successively to upscale video by all conventional algorithms:
	```
	python 00_move_file.py
	python 01_downscale.py
	python 02_timecompute.py
	python 03_extract_metrics_logs.py
	python 04_metrics_analyze.py
	```
5. Run run_sr.py to upscale video by super resolution algorithm:
	```
	python run_sr.py
	```
## Result
After running all scripts the results are located in ./log_files as log files and in ./figures as figures

## Citation
```
@misc{cardinale2018isr,
  title={ISR},
  author={Francesco Cardinale et al.},
  year={2018},
  howpublished={\url{https://github.com/idealo/image-super-resolution}},
}
```

