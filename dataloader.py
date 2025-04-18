import os, shutil
from darken_img import add_darkness_effect
from PIL import Image
from transformers import pipeline

path_to_files = [r"D:\Windows\Users\Stephen Becker\Shell Folders\Downloads\archive (3)\nyu_data\data\nyu2_train", r"D:\Windows\Users\Stephen Becker\Shell Folders\Downloads\Dark_Zurich_val_anon\rgb_anon"]

# Handle nyu2 dataset
# Grab up to 50 images for training
path_to_imgs = []
path_to_gt = []

for root, dirs, files in os.walk(path_to_files[0]):
    count = 0
    for file in files:

        if file.endswith('.png'):
            continue

        if len(path_to_imgs) == 110:
            break

        if count % 50 == 0:
            path_to_imgs.append(os.path.join(root, file))
            path_to_gt.append(os.path.join(root, str(file).replace(".jpg", ".png")))

        count += 1

start_file_index = 0

# Now apply the darkness affect and subsequently save the image to the train_images
for i, path in enumerate(path_to_imgs):
    img_x = add_darkness_effect(path)
    if i < 100:
        img_x.save(f"train/images/{start_file_index}.jpg")
        shutil.copy(path_to_gt[i], f"train/depths/{start_file_index}.png")
    else:
        img_x.save(f"val/images/{start_file_index}.jpg")
        shutil.copy(path_to_gt[i], f"val/depths/{start_file_index}.png")
    start_file_index += 1


# # Now handle the zuirch dataset
# for root, dirs, files in os.walk(path_to_files[1]):
#     for file in files:

