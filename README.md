# Spl1t
A lightweight Python TUI for basic video manipulation.

Below is a demo gif using Spl1t to split a 4 second clip from a 100 second source clip.
![](https://github.com/wcarpenter98/Spl1t/blob/main/demo_pics/readme_gif.gif)

Below is a picture of the TUI.
![](https://github.com/wcarpenter98/Spl1t/blob/main/demo_pics/spl1t.PNG)

For Windows OS, ensure that you have ffmpeg installed and the ffmpeg path variable set.

For UNIX based OSs, this should work out of the box.

This is useful for when you want a lightweight TUI tool to perform video splitting. Other splitting tools tend to load the entire video into the editor to perform edits and playback, which can cause issues on machines with low hardware specs. This tool simply splits the video from your desired start and end time without having to open the video.
