# IAT - Head tagger

[![N|Solid](http://opencv.org/wp-content/themes/opencv/images/logo.png)](http://opencv.org/)

IAT - Head tagger, is a desktop software written in python and OpenCV to select people heads on video frames. Those tagged heads can be used as training data for your intelligent algorithms!

### How it works
  - Put images on the '/img' folder, besides the main.py script
  - With the mouse pointer, select a head in the picture and then press: `1` or `2` to mark as head or no-head.
  - To navigate thru the images press `q` or `w`

### TL;DR

  - `1` to mark as HEAD
  - `2` to mark as NO-HEAD
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

