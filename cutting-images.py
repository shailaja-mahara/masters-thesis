from astropy.io import fits
from google.colab import drive
drive.mount('/content/drive')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from astropy.wcs import WCS
import re

# Plotting the image of the NGC-628 galaxy from MAST data

FILE = '/content/drive/MyDrive/thesisDocuments/jw01783-o908_t016_miri_f560w_i2d.fits'

hdul = fits.open(FILE)
hdul.info()
image= hdul[1].data
# show(image)""
img = plt.imshow(image, vmin=0, vmax=.8)

# # playing with values in the array...for cutting the image in the future
# print("----------")
# print("----------")
# # print(image[0].data)
# # img = plt.imshow(image[0], vmin=0, vmax=.8)
# print(type(image))
# print("----------")
# plt.imshow(image[20:40][0:20], vmin=0, vmax=.8)
# print("----------")
# print("----------")

# print(repr(img))

hdul.close()

# Plotting the catalogued superbubbles from the Watkin's data

FILE_superbubbles = '/content/drive/MyDrive/thesisDocuments/jwst_bubble_properties_A.txt'

# catalog = FILE_superbubbles
# catalog.info()

# df = pd.read_csv(FILE_superbubbles, delim_whitespace=True)  # Assuming space as delimiter
df = pd.read_csv(FILE_superbubbles)  # Assuming space as delimiter

# print(df.head()) #Prints the first 5 lines of dataframe.
# print(df.column_name)

# df.columns

ra_dms = df['RA_DMS'].tolist()
dec_dms = df['DEC_DMS'].tolist()

# S: data is converted into a decimal system. This code was provided by Katerina as something she used previously
#sorry i should have explained this. the data is comind in a format that contains days since the 21st march of the year they were taken, plus months out
def ra_dec_to_deg(ra_str, dec_str):
    ra_pattern = re.compile(r'(\d+)d(\d+)m(\d+\.\d+)s')
    dec_pattern = re.compile(r'(\d+)d(\d+)m(\d+\.\d+)s')
    ra_deg, ra_min, ra_sec = map(float, ra_pattern.match(ra_str).groups())
    dec_deg, dec_min, dec_sec = map(float, dec_pattern.match(dec_str).groups())
    ra_decimal = ra_deg + ra_min / 60 + ra_sec / 3600
    dec_decimal = dec_deg + dec_min / 60 + dec_sec / 3600

    return ra_decimal, dec_decimal

ra_degrees = np.zeros(len(df), dtype=float)
dec_degrees = np.zeros(len(df), dtype=float)
for i, row in df.iterrows():
    ra_deg, dec_deg = ra_dec_to_deg(row['RA_DMS'], row['DEC_DMS'])
    ra_degrees[i] = ra_deg
    dec_degrees[i] = dec_deg


w = WCS(hdul[1].header) # WCS is object of astropy.wcs

x, y = w.all_world2pix(ra_degrees, dec_degrees, 1)
# print("----------")
print(x,y)
# print("----------")

# showing catalogued superbubbles from the Watkin's data
a=plt.plot(x, y,".", color='red')

# Overlapping both plots to show position of bubbles in the image

a=plt.plot(x, y,".", color='red')
b=plt.imshow(image, vmin=0, vmax=.8)

# how to cut images:


# important = semimajor axis and major axis given in the txt files do not correspond to the pixels. they are in pc(parsecs) which is the measuring
# unit in astronomy(similar to meters) can you  find in the header(metadata) of the txt file how many parsecs are in one pixel?
# in the code below the y_end, y_begin etc are in pixels!!!!!(that correspond to the image)
# to the question in the overleaf "Is there documentation available to process the images from the JWST file?" --->there are different ways that people
# process images. For the particular one, I provided you the steps analytically, plus with discussion on astronomical quantities.
# The following code is NOT the way I wrote to you how to cut the images and I am sure this is why it does not work.
# I gave you the exact command for cutting one(cut_image = image_data[y_begin:y_end, x_begin:x_end]). -> documentation from python is "Slicing of 2D Arrays
# " in this link https://www.stratascratch.com/blog/numpy-array-slicing-in-python/.   but it is not precisely how I instructed it.

# Maybe cut one at random begins and ends and see how it works before you associate it with the .txt file? (also read upper comment for the txt file)


# cut_image = a[100:200, 100:200]

print(type(w))
print(w)
# print(w.ra_degrees)

print("----------")
print("----------")

print(w.all_world2pix(ra_degrees, dec_degrees, 1))

print("----------")
print(type(x))
print(len(x))

plt.plot(x[100], y[100],".", color='red')

print("----------")

# !!
# Question for K: I see the values in the array y are in the negative. How, then, in the above plot
# (from the txt data) is the y axis in the positive>??
# update: ok maybe i figured out the answer...


# showing a singlular point of bubble (the one with both x and y in the positive plot to allign
# with the image)
plt.plot(x[1000], y[1000],".", color='red')


# now adding the image
img = plt.imshow(image, vmin=0, vmax=.8)

plt.imshow(image[:][0:100], vmin=0, vmax=.8)

plt.imshow(image[0:100][:], vmin=0, vmax=.8)


# !!  Question for K: Here's a funny thing this code is doing.
# I tried slicing on both axis of image[x][y], but changing the first argument plots the image
# from bottom up (on the y axis) and the second argument plots the image from top down (also on
# y axis). Neither arguments are slicing the x axis.
# Not even the third argument, which I did try image[x][y][z]
plt.imshow(image[:][0:100][0:100], vmin=0, vmax=.8)
# Which is why you will notice the below image cutting code is not working as expected.
# I will look into this again after meeting with Kallol tommorow


# new_image = img[x,y] i also did not say that -->cut_image = image_data[y_begin:y_end, x_begin:x_end] y_begin,y_end, x_begin,x_end numbers, the pixels from where till where you want to cut the iamge.
# plt.show(new_image) also you have named the image "image", not "img" that you have named the plot

# playing with image cutting from above

x_using=x[1000]
y_using=y[1000]

# print(x_using)
# print(y_using)

crop_size=100
x_upper=int(x_using+crop_size)
x_lower=int(x_using-crop_size)
y_upper=int(y_using+crop_size)
y_lower=int(y_using-crop_size)

print("------------")
print(x_upper)
print(x_lower)
print(y_upper)
print(y_lower)
print("------------")

cut_image = image[x_lower:x_upper, y_lower:y_upper]
# cut_image = image[2453:2953, 28:328]
# plt.show(cut_image)
img = plt.imshow(cut_image, vmin=0, vmax=.8)
plt.plot(x_using, y_using,".", color='red')


# plt.plot(x[100], y[100],".", color='red')

# plt.imshow(image[20:40][0:20], vmin=0, vmax=.8)

