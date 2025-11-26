from torch import nn


class ClassificationHead(nn.Module):
    def __init__(self, in_features=768):
        super().__init__()
        self.norm = nn.LayerNorm(in_features)
        self.dropout1 = nn.Dropout(0.4)
        self.fc1 = nn.Linear(in_features, 128)
        self.relu = nn.ReLU(inplace=True)
        self.dropout2 = nn.Dropout(0.3)
        self.fc2 = nn.Linear(128, 1)   # 1 logit (bez sigmoida)

    def forward(self, x):
        x = self.norm(x)
        x = self.dropout1(x)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.dropout2(x)
        x = self.fc2(x)
        return x


class ConvNeXtBinaryClassifier(nn.Module):
    def __init__(self, backbone):
        super().__init__()
        self.backbone = backbone
        self.head = ClassificationHead(in_features=backbone.num_features)

    def forward(self, x):
        x = self.backbone(x)      # [B, 768]
        x = self.head(x)          # [B, 1]
        return x


