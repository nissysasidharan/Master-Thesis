import torch
import torch.nn as nn
import torch.nn.init as init

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        init.kaiming_normal_(self.l1.weight)  # He initialization for the first layer
        self.relu = nn.ReLU()

        self.l2 = nn.Linear(hidden_size, hidden_size)
        init.kaiming_normal_(self.l2.weight)  # He initialization for the second layer

        self.l3 = nn.Linear(hidden_size, num_classes)
        init.kaiming_normal_(self.l3.weight)  # He initialization for the third layer

    def forward(self, x):
        out = self.l1(x)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)  # No activation before this
        #out = nn.functional.softmax(out, dim=1)  # Apply Softmax to the final output
        return out
