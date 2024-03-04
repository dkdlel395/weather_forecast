import torch.nn as nn
from torchvision import models

class network(nn.Module):
    def __init__(self, class_num):
        super().__init__()
        self.class_num = class_num
        self.init = nn.Conv2d(in_channels=3, out_channels=3, kernel_size=(1, 1))
        self.model = models.resnet18(pretrained=True)
        self.gradlayer = self.model.layer4[-1]
        self.num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Linear(self.num_ftrs, class_num)

    def forward(self, x):
        output = self.init(x)
        output = self.model(output)
        return output