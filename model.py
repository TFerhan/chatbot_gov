import torch
import torch.nn as nn

class NeuralNet(nn.Module):
    def __init__(self, input_size,num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, 64) 
        self.l2 = nn.Linear(64, 32) 
        self.dropout = nn.Dropout(0.5)
        self.l3 = nn.Linear(32, num_classes)
        self.relu = nn.ReLU()
    
    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        return out