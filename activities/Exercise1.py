## Tus respuestas
# lo que cambiaria es la verificacion de cores del cpu, confirmar que tenemos la images
# posterior a ello mencionar que se hizo la operacion correspondiente.

## libraries
import cv2
import numpy as np
from multiprocessing import Pool, cpu_count

def apply_blur(segment, kernel_size=(15,15), sigma=3): # el valor de sigma pequeno el desnfoque es mas sutil
    return cv2.GaussianBlur(segment, kernel_size, sigma)

def parallel_image_processing(image_path, num_segments = 0):
    image = cv2.imread(image_path)
    
    #coprobamos que haya cargado la imagen
    if image is None:
        print(f'failed to load image from {image_path}')
        return
    
    height, width, _ = image.shape

    # cpu cores
    print(num_segments)

    if not num_segments:
        # usamos solo el 80% de los cores 
        num_segments = int(cpu_count() * (80/100))# Default to number of CPU cores
        print(f'using {num_segments} cores')

    # Split image into segments
    segments = np.array_split(image, num_segments, axis=1)

    # parallel processing
    with Pool(processes=num_segments) as pool:
        blurred_segments = pool.map(apply_blur, segments)

    blurred_image = np.hstack(blurred_segments)
    cv2.imwrite('blurred_image.jpg', blurred_image)
    print("Image processing completed and saved as 'blurred_image.jpg'.")

parallel_image_processing('/home/seia/Pictures/Screenshot from 2024-04-03 16-28-42.png')    