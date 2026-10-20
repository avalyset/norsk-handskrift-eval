---
license: mit
language:
- nb
task_categories:
- image-to-text
pretty_name: NorHand-v3-line
dataset_info:
  features:
  - name: image
    dtype: image
  - name: text
    dtype: string
  splits:
  - name: train
    num_examples: 222381
  - name: validation
    num_examples: 22679
  - name: test
    num_examples: 1562
  dataset_size: 246622
tags:
  - atr
  - htr
  - ocr
  - historical
  - handwritten
---

# NorHand v3 - line level

## Table of Contents
- [NorHand v3 - line level](#norhand-v3-line-level)
  - [Table of Contents](#table-of-contents)
  - [Dataset Description](#dataset-description)
    - [Languages](#languages)
  - [Dataset Structure](#dataset-structure)
    - [Data Instances](#data-instances)
    - [Data Fields](#data-fields)

## Dataset Description

- **Homepage:** [Hugin-Munin project](https://hugin-munin-project.github.io/)
- **Source:** [Zenodo](https://zenodo.org/records/10255840)
- **Point of Contact:** [TEKLIA](https://teklia.com)

## Dataset Summary 

The NorHand v3 dataset comprises Norwegian letter and diary line images and text from 19th and early 20th century.

Note that all images are resized to a fixed height of 128 pixels.

### Languages

All the documents in the dataset are written in Norwegian Bokmål.

## Dataset Structure

### Data Instances

```
{
  'image': <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=4300x128 at 0x1A800E8E190,
  'text': 'Til Bestyrelsen af'
}
```

### Data Fields


- `image`: a PIL.Image.Image object containing the image. Note that when accessing the image column (using dataset[0]["image"]), the image file is automatically decoded. Decoding of a large number of image files might take a significant amount of time. Thus it is important to first query the sample index before the "image" column, i.e. dataset[0]["image"] should always be preferred over dataset["image"][0].
- `text`: the label transcription of the image.