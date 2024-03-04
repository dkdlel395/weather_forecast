from torch.utils.data import Dataset
import cv2
from torchvision.transforms import ToTensor

class dataset(Dataset):
    def __init__(self, frame):
        self.frame = frame

    def __len__(self):
        return 1  # Continuous stream, so length is 1

    def __getitem__(self, index):
        frame = self.frame

        # Resize to a fixed size for the model (adjust dimensions if needed)
        resized_frame = cv2.resize(frame, (640, 480))

        # Convert to PyTorch tensor and normalize (adjust normalization if needed)
        frame_tensor = ToTensor()(resized_frame)
        frame_tensor = frame_tensor.float()
        # Normalize (example): frame_tensor = (frame_tensor - 0.5) / 0.5

        return frame_tensor