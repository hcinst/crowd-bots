import torchvision
import torch.nn as nn


class R2plus1dModel(nn.Module):
    def __init__(self):
        super(R2plus1dModel, self).__init__()
        self.cnn = torchvision.models.video.r2plus1d_18(pretrained=False)
        self.cnn.fc = nn.Linear(in_features=512,
                                out_features=1)
        self.sig = nn.Sigmoid()

    def forward(self, input):
        x = self.cnn(input)
        x = self.sig(x)
        return x


class Mc3Model(nn.Module):
    def __init__(self):
        super(Mc3Model, self).__init__()
        self.cnn = torchvision.models.video.mc3_18(pretrained=False)
        self.cnn.fc = nn.Linear(in_features=512,
                                out_features=1)
        self.sig = nn.Sigmoid()

    def forward(self, input):
        x = self.cnn(input)
        x = self.sig(x)
        return x


class R3dModel(nn.Module):
    def __init__(self):
        super(R3dModel, self).__init__()
        self.cnn = torchvision.models.video.r3d_18(pretrained=False)
        self.cnn.fc = nn.Linear(in_features=512,
                                out_features=1)
        self.sig = nn.Sigmoid()

    def forward(self, input):
        x = self.cnn(input)
        x = self.sig(x)
        return x
