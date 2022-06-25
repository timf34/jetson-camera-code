from PIL import Image
import cv2
import torchvision.transforms as transforms

BALL_LABEL = 1

NORMALIZATION_MEAN = [0.485, 0.456, 0.406]
NORMALIZATION_STD = [0.229, 0.224, 0.225]

normalize_trans = transforms.Compose([transforms.ToTensor(),
                                      transforms.Normalize(NORMALIZATION_MEAN, NORMALIZATION_STD)])


def image2tensor(image):
    # Convert PIL Image to the tensor (with normalization)
    return normalize_trans(image)


def numpy2tensor(image):
    # Convert OpenCV image to tensor (with normalization)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(image)
    return image2tensor(pil_image)