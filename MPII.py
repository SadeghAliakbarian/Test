
import sys
import argparse
import os.path
import json
import pickle
import numpy as np
import csv
import cv2
import os 

# Print iterations progress
def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '=' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()


# reading and parsing the arguments
parser = argparse.ArgumentParser(description='Generating the Chronological Order Graph (COG) for Charades Dataset.')
parser.add_argument("--annotation-dir", 
	metavar="<path>", required=True, 
	type=str,
	help="directory to the detectionGroundtruth-1-0.csv",
	default='/home/ali030/Downloads/MPII/detectionGroundtruth-1-0.csv')

parser.add_argument("--save-path", 
	metavar="<path>",
	default='/mnt/ssd/data/MPII/jpeg/', 
	type=str)


args = parser.parse_args()

# saving the last commandline
with open("MPII_cmdline.txt", "w") as f:
    f.write(' '.join(sys.argv))


# Reading the files/Annotation
f = open(args.annotation_dir)
reader = csv.DictReader(f)
i = 0
Annotation = []
for row in reader:
	subject = row['Subject']
	File = row['File']
	start = row['Start']
	end = row['End']
	category = row['Category']
	name = row['Name']
	info = [File, start, end, category, name, subject]
	list.insert(Annotation, i, info)
	i = i + 1

#print Annotation[0]

# number of classes: 65 (with background activity which is class 1)
train_subjects = [11,12,13,14,15]
test_subjects   = [8,10,16,17,18,19,20]

if not os.path.exists(args.save_path):
    os.makedirs(args.save_path)
for i in range (64):
	if not os.path.exists(args.save_path+"train/"+str(i)):
		os.makedirs(args.save_path+"train/"+str(i))
	if not os.path.exists(args.save_path+"val/"+str(i)):
		os.makedirs(args.save_path+"val/"+str(i))

for a in range (len(Annotation)):
	temp = Annotation[a]
	printProgress(0, len(Annotation), prefix = 'Extracting Frames:', suffix =  ': ' + temp[0] + ' ('+ str(int(temp[3])-2) + ') ' , barLength = 50)
	if (temp[3]!='1'):
		cap = cv2.VideoCapture('video/' + temp[0] + '.avi')
		cap.set(1, int(temp[1]))
		for fr in range(int(temp[2])-int(temp[1])):
			ret, frame = cap.read()
			frame = cv2.resize(frame,(541,408), interpolation = cv2.INTER_CUBIC)
			if(ret):
				if (int(temp[5]) in test_subjects):
					cv2.imwrite(args.save_path + "val/" + str(int(temp[3])-2) + "/" + temp[0] + "_" + str(fr) + ".jpg", frame)
				if (int(temp[5]) in train_subjects):
					cv2.imwrite(args.save_path + "train/" + str(int(temp[3])-2) + "/" + temp[0] + "_" + str(fr) + ".jpg", frame)






