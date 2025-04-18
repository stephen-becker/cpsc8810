from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
import os

# Load image
def add_darkness_effect(path_to_img):
    assert os.path.exists(path_to_img)
    img = Image.open(path_to_img)

    # Step 1: Aggressively reduce brightness
    enhancer = ImageEnhance.Brightness(img)
    img_dark = enhancer.enhance(0.2)  # Deeper darkness

    # Step 2: Slightly desaturate (colors are less vibrant at night)
    enhancer = ImageEnhance.Color(img_dark)
    img_dark = enhancer.enhance(0.35)

    # Step 3: Add strong blue tint to simulate moonlight/night tone
    img_np = np.array(img_dark)
    blue_tint = np.full_like(img_np, [0, 0, 40])
    img_tinted = cv2.add(img_np, blue_tint)

    # Step 4: Simulate limited visibility with a vignette (darken edges)
    rows, cols = img_tinted.shape[:2]
    X_resultant_kernel = cv2.getGaussianKernel(cols, cols/2)
    Y_resultant_kernel = cv2.getGaussianKernel(rows, rows/2)
    vignette = Y_resultant_kernel * X_resultant_kernel.T
    mask = 255 * vignette / np.linalg.norm(vignette)
    for i in range(3):
        img_tinted[:,:,i] = img_tinted[:,:,i] * mask

    # Step 5 (Optional): Blur background slightly (to simulate darkness haze)
    blurred = cv2.GaussianBlur(img_tinted, (5,5), 0)

    # Save output
    return Image.fromarray(blurred.astype('uint8')) # .save("night_output.jpg")
