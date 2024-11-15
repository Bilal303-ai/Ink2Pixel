# About
Ink2Pixel seamlessly converts handwritten text from an image into a digital format. The app utilizes the [**microsoft/trocr-large-handwritten**](https://huggingface.co/microsoft/trocr-large-handwritten) model for precise text extraction, processing each line individually. OpenCV is employed to segment paragraphs into lines, ensuring accurate and efficient text conversion.

The app also corrects any spelling and grammatical errors in the input text.

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
The app features a user-friendly Gradio interface, allowing you to effortlessly upload your source image either by capturing it with a camera or by uploading it directly.

## Demo
You can access the live demo of the app on [Hugging Face](https://huggingface.co/spaces/BilalHasan/Ink2Pixel).

## Note:
1. For optimal results, please use an image with a white background and text in black ink.
2. Ensure the lines do not overlap. There should be sufficient space between each line, as illustrated in the example above.
3. The model, with its 333 million parameters, requires some time to process. I appreciate your patience.
