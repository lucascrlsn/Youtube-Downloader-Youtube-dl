# Youtube Transcript Tool
Generates mp3 or mp4 via gen_file(), then creates a transcript ran through a punctuator.

![Youtube GUI](https://github.com/lucascrlsn/hello/blob/master/Other/youtube_main.png)

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)      

## Dependencies:

*moviepy*
```python

pip3 install moviepy
```
*speech recongnition*
```python
pip3 install speechrecognition
```
```

## Notes:
** A .pcl location should be specified for Punctuator and also the ffmpeg location included as 
a var and properly installed on your device with brew. 

What's next?
- speed improvements via cython
- gdrive integration for atomated Google Doc create
- Google Doc revision tracking and disemination

