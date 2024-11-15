import cv2 as cv
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import gradio as gr

processor = TrOCRProcessor.from_pretrained('microsoft/trocr-large-handwritten')
model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-large-handwritten')


def preprocess_image(image):
  gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
  ret, bin_image = cv.threshold(gray_image, 127, 255, cv.THRESH_OTSU)

  bin_image = cv.copyMakeBorder(bin_image, int(0.10 * image.shape[0]), int(0.05 * image.shape[0]), int(0.05 * image.shape[1]), int(0.10 * image.shape[1]), cv.BORDER_CONSTANT, value=(255, 255, 255))
  return bin_image


def split_image_into_lines(image):
  lines = []
  while (image.shape[0] > 20):
    flag1 = 0
    flag2 = 0

    for i in range(image.shape[0]):
      if flag1 == 0:
        for j in range(image.shape[1]):
          pixel_value = image[i][j]
          if (pixel_value == 0) & (flag1 == 0):
            start = i
            flag1 = 1
            flag2 = 1
      if flag2 == 1:
        num_white_pixels = np.sum(image[i + 1] == 255)
        if (num_white_pixels > 0.98 * image.shape[1]):
          end = i + 1
          break


    line = image[int(start - 0.2 * (end - start + 1)): int(end + 1 + 0.2 * (end - start + 1))][:]
    if line.shape[0] > 20:
      line_rgb = cv.cvtColor(line, cv.COLOR_GRAY2RGB)
      lines.append(line_rgb)

    pads = 255 * np.ones((20, image.shape[1]), dtype='uint8')
    new_image = image[int(end + 2 -(0.2 * (end - start + 1))):][:]
    new_image = np.concatenate((pads, new_image))
    image = new_image


  return lines



def generate_text(line):
  pixel_values = processor(images=line, return_tensors="pt").pixel_values
  generated_ids = model.generate(pixel_values, max_new_tokens=50)
  generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
  return generated_text


def get_improved_result(lines):
    with ProcessPoolExecutor() as executor:
        improved_text = ' '.join(executor.map(generate_text, lines))
    return improved_text



def put_text(text, font, font_scale, color, thickness, max_width, out_image_width, top_margin):
  words = text.split(" ")
  lines = []
  current_line = ""

  for word in words:
    if cv.getTextSize(current_line + " " + word, font, font_scale, thickness)[0][0] <= (max_width * out_image_width):
      current_line += " " + word
    else:
      lines.append(current_line)
      current_line = word

  lines.append(current_line)

  out_image_height = sum([cv.getTextSize(line, font, font_scale, thickness)[0][1] for line in lines]) + 2 * top_margin + 20 * (len(lines) - 1) #20 is the gap between two consecutive lines

  out_image = 255 * (np.ones((out_image_height, out_image_width, 3), dtype=np.uint8))

  top = top_margin
  for line in lines:
    cv.putText(out_image, line.strip(), (int(((1 - max_width) * out_image_width) / 2), top), font, font_scale, 0, thickness, lineType=cv.LINE_AA)
    top += cv.getTextSize(line.strip(), font, font_scale, thickness)[0][1] + 20

  return out_image

font = cv.FONT_HERSHEY_DUPLEX
font_scale = 2
color = 0
thickness = 2
max_width = 0.9
out_image_width = 1500
top_margin = 100

#out_image = put_text(improved_text, font, font_scale, color, thickness, max_width, out_image_width, top_margin)

def predict(input_path):
    image = cv.imread(input_path)
    bin_image = preprocess_image(image)
    lines = split_image_into_lines(bin_image)
    improved_text = get_improved_result(lines)
    out_image = put_text(improved_text, font, font_scale, color, thickness, max_width, out_image_width, top_margin)
    return out_image

gradio_app = gr.Interface(
    predict,
    inputs=gr.Image(label= ' ', sources=['upload', 'webcam'], type='filepath'),
    outputs=[gr.Image(label= ' ')],
    title="Extract Handwritten Text",
)

if __name__ == "__main__":
    gradio_app.launch()
