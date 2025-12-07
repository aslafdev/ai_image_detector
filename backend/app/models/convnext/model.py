
import torch
from torchvision import transforms
from PIL import Image
from PIL.Image import Image as PILImage
import timm

from models.base import BaseModel
from models.convnext.model_impl import ConvNeXtBinaryClassifier
from config.dirs import TORCH_WEIGHTS_DIR

from schemas.model_results import TableRow,TableCell, CellType
from time import time



class ConvNeXtBinaryModel_StyleGan1(BaseModel):
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print("Using device:", self.device)
    
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

    def load(self):
        backbone = timm.create_model(
            "convnext_tiny",
            pretrained=False,
            num_classes=0,
            global_pool="avg"
        )
        self.model = ConvNeXtBinaryClassifier(backbone)
        state = torch.load(self.weight_path, map_location=self.device)
        self.model.load_state_dict(state)
        self.model.to(self.device)
        self.model.eval()
        print("Model loaded to", self.device)
        return self
    
    @property
    def columns(self) -> dict[str, str]:
        return {"filename": "filename", "prediction": "prediction", "score": "score", 'prediction_time': 'prediction time (s)'}

    def preprocess(self, image: PILImage):
        tensor = self.transform(image)
        return tensor

    def predict(self, image: PILImage) -> TableRow:
        time_start = time()
        tensor = self.preprocess(image)
        tensor = tensor.unsqueeze(0).to(self.device)
        with torch.inference_mode():
            output = self.model(tensor).view(-1)
            prob = torch.sigmoid(output).item()
        time_end = time()
        elapsed_time = time_end - time_start
        
        filename_cell = TableCell(value=image.filename,type="text")
        decision_cell = TableCell(value="real" if prob >= 0.5 else "fake", type="tag")
        score_cell = TableCell(value=prob, type="percent")
        prediction_time_cell = TableCell(value=elapsed_time, type="number")
        return TableRow(
            filename=filename_cell,
            decision=decision_cell,
            score=score_cell,
            prediction_time=prediction_time_cell
        )
