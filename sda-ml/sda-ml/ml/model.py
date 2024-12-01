from torch import nn
import torch

class ELM_IOD(nn.Module):
    """
    Simple extreme learning model to train right ascension angles into poincare elements
    Constructor Inputs:
        input_size: int
        hidden_layer_size: int
        output_size: int
        activation: Literal[string]
    """
    def __init__(self, input_size: int, hidden_layer_size: int, output_size: int, activation='relu') -> None:
        super(ELM_IOD, self).__init__()
        self.hidden_layer_size = hidden_layer_size

        # Initialize hidden layer as random from normal gaussian (0, I)
        self.input_weights = nn.Parameter(torch.randn(input_size, hidden_layer_size), requires_grad=False)
        self.output_bias = nn.Parameter(torch.randn(hidden_layer_size), requires_grad=False)

        # Activation Functions
        if activation == 'relu':
            self.activation = torch.relu
        elif activation == 'tanh':
            self.activation = torch.tanh
        elif activation == 'sigmoid':
            self.activation = torch.sigmoid
        else:
            raise ValueError("ERROR: Unsupported Activation Function")
        
        self.output = nn.Linear(hidden_layer_size, output_size, bias=True)
    
    def forward(self, x):
        # Hidden layer transformation
        H = self.activation(torch.matmul(x, self.input_weights) + self.output_bias)
        out = self.output(H)

        return out