import torch
import toml
from your_diffusion_module import DiffusionModel

class VideoGenerator:
    def __init__(self, config_path: str, seed: int = None):
        cfg = toml.load(config_path)
        self.frames = cfg.get('frames', 60)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        if seed is not None:
            torch.manual_seed(seed)
        self.model = DiffusionModel(**cfg['model']).to(self.device)

    def forward(self):
        # Generate self.frames frames
        frames = []
        for i in range(self.frames):
            img = self.model.sample()
            frames.append(img)
        return frames

    def save_video(self, frames, path: str = "output.mp4"):  # returns file path
        # Save frames as video (e.g., with torchvision.io or cv2)
        import cv2
        height, width = frames[0].shape[:2]
        writer = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*'mp4v'), 24, (width, height))
        for frame in frames:
            writer.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        writer.release()
        return path
