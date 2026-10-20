# NorHand v3

This dataset comprises Norwegian letter and diary documents from 19th and early 20th century.

For each document, we provide:
* the image (jpg format)
* the ground truth (PageXML format), including:
    * localization of each text zone (text-lines, paragraphs, pages)
    * transcription of each text zone (text-lines, paragraphs, pages)
    * reading order of text zones within the document
* the name of the writer
* the date

We are also releasing an official split designed to maximize diversity in the test set: each test page was written by a different writer.

| Split     | Pages | Paragraphs |Lines   | Writers |
|-----------|------:|-----------:|-------:|--------:|
| Train     | 10128 | 13244      | 230829 | 315     |
| Val       | 1078  | 1320       | 23017  | 154     |
| Test      | 81    | 90         | 1573   |  81     |
| **Total** | 11287 | 14654      | 255419 | 393     |

The dataset is organized as follows:

```
├── train
    ├── images/
    ├── page_xml/
    └── metadata_train.csv
├── val
    ├── images/
    ├── page_xml/
    └── metadata_val.csv
├── test
    ├── images/
    ├── page_xml/
    └── metadata_test.csv
```
