from os import walk
import numpy as np
import matplotlib.pyplot as plt
from pydicom import dcmread
import cv2
from PIL import Image as im
# from position_search import position_linear_search

TILT_ANGLE = 10

path = 'D:/Vimal/1AA_CT_to_MRI/CT2MRI/CT/DICOM/24040215/57030000/'

stack = []
dirpath = ''
filenames = []
for (dirpath, _, filenames) in walk(path):
    pass
for fname in filenames:
    stack.append(dcmread(dirpath+fname).pixel_array)

stack = np.array(stack)

##################################################
# dimensions of image
single_file_path = 'D:/Vimal/1AA_CT_to_MRI/CT2MRI/CT/DICOM/24040215/57030000/67429720'
file = dcmread(single_file_path)
data = file.pixel_array
height, width = data.shape
no_of_images = stack.shape[0] #453
pixel_spacing = file.PixelSpacing.pop()
physical_height = height*pixel_spacing
physical_width = width*pixel_spacing
length = int(np.rint(no_of_images*pixel_spacing))
print(type(pixel_spacing))
print(height, width) #512 512
print(file.PixelSpacing) #[0.4713671875, 0.4713671875]
print(file.SliceThickness) #1
print(file.GantryDetectorTilt) #7
##################################################

# making a 3D volume saved to intercoperate interpixel distace
volume = []
blank = np.zeros(shape=(height, width))
j=0
i=0
saved_at = []
while j<no_of_images:
    if np.rint(i*pixel_spacing) == j:
        volume.append(stack[j])
        j+=1
        saved_at.append(i)
    else:
        volume.append(stack[j])
    i+=1
volume = np.array(volume)
# print(volume.shape): (959, 512, 512)
# print(saved_at): [0, 2, 4, 6, 8, 10, 12, 14, 16, 19, 21, 23, 25, 27, 29, 31, 33, 36, 38, 40, 42, 44, 46, 48, 50, 52, 55, 57, 59, 61, 63, 65, 67, 69, 72, 74, 76, 78, 80, 82, 84, 86, 89, 91, 93, 95, 97, 99, 101, 103, 106, 108, 110, 112, 114, 116, 118, 120, 122, 125, 127, 129, 
# 131, 133, 135, 137, 139, 142, 144, 146, 148, 150, 152, 154, 156, 159, 161, 163, 165, 167, 169, 171, 173, 176, 178, 180, 182, 184, 186, 188, 190, 192, 195, 197, 199, 201, 203, 205, 207, 209, 212, 214, 216, 218, 220, 222, 224, 226, 229, 231, 233, 235, 237, 239, 241, 243, 246, 248, 250, 252, 254, 256, 258, 260, 263, 265, 267, 269, 271, 273, 275, 277, 279, 282, 284, 286, 288, 290, 292, 294, 296, 299, 301, 303, 305, 307, 309, 311, 313, 316, 318, 320, 322, 324, 326, 328, 330, 333, 335, 337, 339, 341, 343, 345, 347, 349, 352, 354, 356, 358, 360, 362, 364, 366, 369, 371, 373, 375, 377, 379, 381, 383, 386, 388, 390, 392, 394, 396, 398, 400, 403, 
# 405, 407, 409, 411, 413, 415, 417, 419, 422, 424, 426, 428, 430, 432, 434, 436, 439, 441, 443, 445, 447, 449, 451, 453, 456, 458, 460, 462, 464, 466, 468, 470, 473, 475, 477, 479, 481, 483, 485, 487, 490, 492, 494, 496, 498, 500, 502, 504, 506, 509, 511, 513, 515, 517, 519, 521, 523, 526, 528, 530, 532, 534, 536, 538, 540, 543, 545, 547, 549, 551, 553, 555, 557, 560, 562, 564, 566, 568, 570, 572, 574, 576, 579, 581, 583, 585, 587, 589, 591, 593, 596, 598, 600, 602, 604, 606, 608, 610, 613, 615, 617, 619, 621, 623, 625, 627, 630, 632, 634, 636, 638, 640, 642, 644, 646, 649, 651, 653, 655, 657, 659, 661, 663, 666, 668, 670, 672, 674, 676, 
# 678, 680, 683, 685, 687, 689, 691, 693, 695, 697, 700, 702, 704, 706, 708, 710, 712, 714, 717, 719, 721, 723, 725, 727, 729, 731, 733, 736, 738, 740, 742, 744, 746, 748, 750, 753, 755, 757, 759, 761, 763, 765, 767, 770, 772, 774, 776, 778, 780, 782, 784, 787, 789, 791, 793, 795, 797, 799, 801, 803, 806, 808, 810, 812, 814, 816, 818, 820, 823, 825, 827, 829, 831, 833, 835, 837, 840, 842, 844, 846, 848, 850, 852, 854, 857, 859, 861, 863, 865, 867, 869, 871, 873, 876, 878, 880, 882, 884, 886, 888, 890, 893, 895, 897, 899, 901, 903, 905, 907, 910, 912, 914, 916, 918, 920, 922, 924, 927, 929, 931, 933, 935, 937, 939, 941, 944, 946, 948, 950, 
# 952, 954, 956, 958]

'''
y:0->511 we have to determine x value form eq. mx = -y + 255, (255 = img_dim/2 -1)
'''
def position_linear_search(x, nums):
    n = len(nums)
    # if x > nums[n-1]:
    #     return nums[n-1], nums[n-1]
    # if x < nums[0]:
    #     return nums[0],nums[0]
    for i in range(n):
        if nums[i] == x:
            return nums[i], nums[i]
        elif nums[i] > x:
            return nums[i-1], nums[i]

def nearest_neighbor_interpolation(volume, curr_x, y, prev, nexti):
    if nexti == prev:
        dist = 0
    else:
        dist = (curr_x - prev)/(nexti - prev)
    curr = volume[prev][y]*(1-dist) + volume[nexti][y]*dist
    return curr

new_volume = np.ndarray((volume.shape))

def function():
    m=np.tan(90-TILT_ANGLE)
    n = len(saved_at)
    for val in saved_at:
        for y in range(height):
            x = np.rint((-y + height//2 -1)/m)
            curr_x = x+val
            if curr_x < 0:
                curr_x = 0
            if curr_x > saved_at[n-1]:
                curr_x = saved_at[n-1]
            prev, nexti = position_linear_search(curr_x, saved_at)
            new_volume[val][y] = nearest_neighbor_interpolation(volume, curr_x, y, prev, nexti)
        print(val, 'done')

function()
for val in saved_at:
    plt.subplot(1,2,1)
    plt.imshow(volume[val])
    plt.subplot(1,2,2)
    plt.imshow(new_volume[val])
    plt.show()