import cv2
import numpy as np
from scipy import ndimage

IMG_NAME = 'test_image.jpg'


def bgr2gray(image:np.ndarray) -> np.ndarray:
    """Converte uma imagem bgr para grayscale"""
    # Separando os canais
    b = img[...,0]
    g = img[...,1]
    r = img[...,2]
    # Convertendo para grayscale
    gr = 0.299*b+0.587*g+0.114*r
    return gr.astype(np.uint8)

# Carrega a imagem em bgr
img = cv2.imread(IMG_NAME)
# Redimensiona para ficar mais facil tratar
img = cv2.resize(img, (700,400))
# Converte para tons de cinza
img_gray = bgr2gray(img)
# Cria kernels
kernel_media = np.ones((3,3))/9
kernel_sobel_x = np.array([
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]
])
kernel_sobel_y = np.array([
    [ 1,  2,  1],
    [ 0,  0,  0],
    [-1, -2, -1]
])
kernel_laplaciano = np.array([
    [1,  1, 1],
    [1, -8, 1],
    [1,  1, 1]
])

img_binary = np.where(img_gray.copy() > 50,255,0).astype(np.uint8)
#for _ in range(5):
#    img_binary = ndimage.convolve(img_binary, kernel_media)
img_binary = ndimage.convolve(img_binary, kernel_laplaciano)
cv2.imshow('',img_binary)
cv2.waitKey(0)