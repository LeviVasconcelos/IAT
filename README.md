# IAT - Head tagger

[![N|Solid](http://opencv.org/wp-content/themes/opencv/images/logo.png)](http://opencv.org/)

IAT - Image Annotation Tool, is a desktop software written in python and OpenCV to help building your own image annotated dataset! Currently, the software is already configured to two different classes, but it is easily extensible.

### How it works
  - Put images on the '/img' folder, besides the main.py script
  - With the mouse pointer, annotate your picture and then press: `1` or `2` to mark as class 1 or 2.
  - To navigate thru the images press `q` or `w`

### TL;DR

  - `1` to mark as class 1
  - `2` to mark as class 2
  - `q` go backwards on the image set
  - `w` go forward on the image set
  - `x` exit program
  - `o` force save current window


This text you see here is *actually* written in Markdown! To get a feel for Markdown's syntax, type some text into the left window and watch the results in the right.

### Executing

IAT requires [OpenCV](http://opencv.org/) to run.

```sh
$ python main.py
```

