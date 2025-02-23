import pandas as pd
import torch
from torch_geometric.data import InMemoryDataset
from torch_geometric.loader import DataLoader
from torch_geometric.utils.smiles import from_smiles
from torch_geometric.nn import GCNConv
from torch_geometric.nn import GATConv
from torch.nn import Linear
import torch.nn.functional as F
import os
from torch_geometric.nn import global_mean_pool
from torch_geometric.nn import global_max_pool 
from torch_geometric.nn import graclus
from torch_geometric.nn import global_add_pool
import matplotlib.pyplot as plt
import torch.nn as nn
from torch.optim.lr_scheduler import ReduceLROnPlateau


class GCN_GAT(torch.nn.Module):
    def __init__(self, hidden_channels):
        super(GCN_GAT, self).__init__()
        torch.manual_seed(12345)
        self.gcn_conv1 = GCNConv(9, hidden_channels)
        self.bn1 = nn.BatchNorm1d(hidden_channels)
        self.gat_conv1 = GATConv(hidden_channels, hidden_channels, heads=20)
        self.gcn_conv2 = GCNConv(hidden_channels * 20, hidden_channels)
        self.bn2 = nn.BatchNorm1d(hidden_channels)
        self.gat_conv2 = GATConv(hidden_channels, hidden_channels, heads=1)
        self.lin = Linear(hidden_channels, 1)
    def forward(self, x, edge_index, batch):
        # 1. Apply GCN Convolution
        x = self.gcn_conv1(x, edge_index)
        x = self.bn1(x)
        x = F.relu(x)
        x = self.gat_conv1(x, edge_index)
        x = F.relu(x)
        x = self.gcn_conv2(x, edge_index)
        x = self.bn2(x)
        x = F.relu(x)
        x = self.gat_conv2(x, edge_index)
        x = F.relu(x)
        x= global_max_pool(x,batch)
        x = F.dropout(x, p=0.4, training=self.training)
        x = self.lin(x)
        x = torch.sigmoid(x)
        return x







    