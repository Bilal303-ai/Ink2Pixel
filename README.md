# About
Ink2Pixel extracts handwritten text from an image and returns a digitalised version of the text. App uses [**microsoft/trocr-large-handwritten**](https://huggingface.co/microsoft/trocr-large-handwritten) model to extract text from the image line by line. OpenCV is used to split the paragraphs into lines.

#### Input image:
<img width="809" alt="Demo2" src="https://github.com/user-attachments/assets/4fb9c020-d97e-4f6f-9579-76e16961d88d">



#### Output image:
<img width="809" alt="Demo2result" src="https://github.com/user-attachments/assets/ec7b9249-e5d8-4124-b51c-eaa7a9c48c50">

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/Bilal303-ai/Ink2Pixel
   cd Ink2Pixel
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   python app.py
   ```
