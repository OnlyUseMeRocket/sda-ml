import torch
from torch.utils.data import Dataset

class RestrictedIODDataset(Dataset):
    """Simple dataset class so PyTorch can work with the underlying interfaces needed for 1st party functions
        Inputs:
            feature: torch.Tensor - Feature matrix (n,1)
            labels: torch.Tensor - Label matrix (n,3)
    """
    def __init__(self, features: torch.Tensor, labels: torch.Tensor) -> None:
        """"""
        super().__init__()
        if not(len(features) == len(labels)):
            raise AssertionError("Length of Labels and Features are not equal")

        self.features = features
        self.labels = labels 
        
    def __len__(self) -> int:
        return len(self.features)
    
    def __getitem__(self, index: int) -> tuple[float, tuple[float, ...]]:
        feature = self.features[index]
        label = self.labels[index]
        return feature, label