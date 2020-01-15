import sys
import cv2
import numpy as np
import PIL.ImageOps
import GlobalVariables
from PIL import Image as im
from scipy.ndimage import interpolation as inter
from matplotlib import pyplot as plt

def find_score(arr, angle):
    data = inter.rotate(arr, angle, reshape=False, order=0)
    hist = np.sum(data, axis=1)
    score = np.sum((hist[1:] - hist[:-1]) ** 2)
    return hist, score

def Correct_skew(imageName):
	img = im.open(imageName)
	wd, ht = img.size
	pix = np.array(img.convert('1').getdata(), np.uint8)
	bin_img = 1 - (pix.reshape((ht, wd)) / 255.0)

	delta = GlobalVariables.delta
	limit = GlobalVariables.limit
	angles = np.arange(-limit, limit+delta, delta)
	scores = []
	for angle in angles:
	    hist, score = find_score(bin_img, angle)
	    scores.append(score)

	best_score = max(scores)
	best_angle = angles[scores.index(best_score)]
	print('Image is rotated by the angle: {}'.format(best_angle))

	img = im.open(imageName)
	im2 = img.convert('RGBA')
	rot = im2.rotate(float(best_angle), expand=1)
	fff = im.new('RGBA', rot.size, (255,)*4)
	out = im.composite(rot, fff, rot)
	out.convert(img.mode).save('test2.png')

	out = cv2.imread('test2.png')
	return out