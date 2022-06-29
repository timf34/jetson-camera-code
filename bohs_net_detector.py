import torch
import os
import numpy as np
from typing import Dict

from bohs_net_code.network import footandball
from bohs_net_code.data import augs


class BohsNetDetector:
    def __init__(self):
        self.model_name: str = 'fb1'
        self.weights: str = './weights/model_12_06_2022_2349_final_with_augs.pth'
        self.state_dict = torch.load(self.weights)
        self.ball_threshold: float = 0.7
        self.device: str = 'cuda' if torch.cuda.is_available() else 'cpu'
        print("The model is on: ", self.device)


        assert os.path.exists(self.weights), f'Cannot find weights file: {self.weights}'

        model = footandball.model_factory(self.model_name, 'detect', ball_threshold=self.ball_threshold)
        model = model.to(self.device)
        model.load_state_dict(self.state_dict)
        model.eval()
        self.model = model

    def prep_image(self, image: np.ndarray) -> torch.Tensor:
        # TODO: I am fairly certain it isn't but make sure there isn't a computational graph being built up here
        #       ie do I need torch.no_grad()?
        # return torch.from_numpy(image).float().unsqueeze(0).to(self.device)
        return augs.numpy2tensor(image).unsqueeze(dim=0).to(self.device)

    def detect(self, image: np.ndarray) -> Dict:
        image = self.prep_image(image)
        with torch.no_grad():
            return self.model(image)[0]





