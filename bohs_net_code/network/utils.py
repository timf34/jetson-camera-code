import numpy as np
import cv2
import torch
import torch.nn as nn

import data.augmentation as augmentations

"""
# VGG-like network configuration
vgg_cfg = {
    'X': [8, 'M', 16, 16, 'M', 32, 32, 'M', 64, 64, 'M', 64, 64, 'M'],
    'Y': [16, 'M', 32, 32, 'M', 64, 64, 'M', 128, 128, 'M', 128, 128, 'M']
}
"""


def make_vgg_modules(cfg, batch_norm=False):
    # Create VGG-like network based on given configuration
    # Each module is a list of sequential layers operating at the same spacial dimension followed by MaxPool2d
    modules = nn.ModuleList()
    # Number of output channels in each module
    out_channels = []

    in_channels = 3
    layers = []

    for v in cfg:
        if v == 'M':
            layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
            # Create new module with accumulated layers and flush layers list
            modules.append(nn.Sequential(*layers))
            out_channels.append(in_channels)
            layers = []
        else:
            if batch_norm:
                conv2d = nn.Conv2d(in_channels, v, kernel_size=3, padding=1, bias=False)
                layers += [conv2d, nn.BatchNorm2d(v), nn.ReLU(inplace=True)]
            else:
                conv2d = nn.Conv2d(in_channels, v, kernel_size=3, padding=1)
                layers += [conv2d, nn.ReLU(inplace=True)]
            in_channels = v

    # 'M' should be the last layer - and all layers should be flushed
    assert len(layers) == 0

    return modules, out_channels


def count_parameters(model):
    # Count number of parameters in the network: all and trainable
    # Return tuple (all_parameters, trainable_parameters)
    if model is None:
        return 0, 0
    else:
        ap = sum(p.numel() for p in model.parameters())
        tp = sum(p.numel() for p in model.parameters() if p.requires_grad)
        return ap, tp


# Functions for images of ground truth and training results

def compose_confidence_maps(target_map, predicted_map, upscale_factor):
    # Visualize target and predicted confidence map side-by-side
    # target_map: Target (ground truth) confidence map
    # predicted_map: Predicted confidence map
    target_img = augmentations.heatmap2image(target_map)
    predicted_image = augmentations.heatmap2image(predicted_map)
    h, w = target_img.shape[0], target_img.shape[1]

    out_img = np.zeros((h, w * 2, 3), dtype=target_img.dtype)

    # Show ground truth confidence map on the left and predicted confidence map on the right
    out_img[:, :w] = target_img
    out_img[:, w:] = predicted_image
    out_img = cv2.resize(out_img, (w*2*upscale_factor, h*upscale_factor), cv2.INTER_NEAREST)
    cv2.line(out_img, (w*upscale_factor, 0), (w*upscale_factor, h*upscale_factor), (0, 255, 255), thickness=1)
    return out_img


def visualize_feature_maps(feature_maps: torch.Tensor) -> None:
    """
        This function will accept a feature_map and then display it to the user.

        We will try to build it in a way robust to differnt input shapes but it should be inputted as a tensor of size
        (batch_size, channels, height, width)

        We will transform it to a shape of [height, width] so we can use cv2.imshow() straightforwardly

        :param feature_maps: A tensor of size (batch_size, channels, height, width)
        :return: None
    """
    # Check if list
    if isinstance(feature_maps, list):
        feature_maps = feature_maps[0]

    if feature_maps.dim() == 4:
        # If the input is of size (batch_size, channels, height, width)
        # We will adjust it to [heigh, width]
        feature_maps = feature_maps[0, 1, :, :]
    if feature_maps.dim() == 3:
        # If the input is of size (batch_size, height, width)
        # We will adjust it to [heigh, widht]
        feature_maps = feature_maps[0,:,:]

    # We will display the image in a new window
    cv2.imshow('Feature Maps', augmentations.heatmap2image(feature_maps))
    cv2.waitKey(0)
