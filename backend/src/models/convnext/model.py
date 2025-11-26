
import torch
from torchvision import transforms
from PIL import Image
import timm

from models.base import BaseModel
from models.convnext.model_impl import ConvNeXtBinaryClassifier

from config.dirs import TORCH_WEIGHTS_DIR


class ConvNeXtBinaryModel_StyleGan1(BaseModel):
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        backbone = timm.create_model(
            "convnext_tiny",
            pretrained=False,
            num_classes=0,
            global_pool="avg"
        )

        self.model = ConvNeXtBinaryClassifier(backbone)

        self.transform = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225],
                ),
            ]
        )

        self.weight_path = TORCH_WEIGHTS_DIR / "stylegan1_convnext.pth"

    def load(self, weight_path: str | None = None):
        state = torch.load(weight_path or self.weight_path, map_location=self.device)
        self.model.load_state_dict(state)
        self.model.to(self.device)
        self.model.eval()
        return self

    def preprocess(self, image: Image.Image):
        tensor = self.transform(image)
        return tensor

    def predict(self, image: Image.Image):
        tensor = self.preprocess(image)
        tensor = tensor.unsqueeze(0).to(self.device)
        with torch.inference_mode():
            output = self.model(tensor).view(-1)
            prob = torch.sigmoid(output).item()
        return prob   
