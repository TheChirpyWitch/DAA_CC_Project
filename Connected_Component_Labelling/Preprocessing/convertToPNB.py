from PIL import Image
import glob
import os

os.system("mkdir -p thresholded_patna_images_pbm")
for image in glob.glob("thresholded_patna_images/*.png"):
    im = Image.open(image)
    im.save(os.path.join("thresholded_patna_images_pbm", image.split("/")[-1].split(".")[0] + ".pbm"))