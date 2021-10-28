import os
from abc import ABC
import pandas as pd
import torch
from torch.utils.data import Dataset
from skimage import io


class WordsDataset(Dataset, ABC):

    def __init__(self, file, img_directory = '', transform=None):
        self.labels = pd.read_csv(file, delim_whitespace=True)                  # Reads file
        self.img_directory = img_directory                                      # Location of the image
        self.transform = transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        img_path = os.path.join(self.root_dir, self.labels.iloc[index, 0])      # Image path needs adjustment!
        image = io.imread(img_path)
        img_label = torch.tensor(self.labels.iloc[index, 8])                    # Label column is column number 8

        if self.transform:
            image = self.transform(image)

        return image, img_label
