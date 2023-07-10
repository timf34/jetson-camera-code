# jetson-camera-code

Jetson side code for recording videos of the matches, streaming video to laptop for initial setup, and will host the 
jetson side code for the AI MDS system (i.e. BohsNet for inference, with fovnet for comms). 


### Recording video 

`record_video.py` in the home directory manages recording videos to local storage. It gets the time of the match from 
the `config.py` file. It records the match in 22.5 minute chunks, with 10 mins for half time. 

To ensure video recording is working correctly, it includes the `record_and_check_video()` method which records a 
quick video and relays to the terminal that it recorded correctly. 


### Streaming video to laptop

`/scripts/stream_port1234.sh` is a script which streams the video from the Jetson to the laptop. 

Be sure that the IP address in the script is the IP address of the laptop you are streaming to.

### Performing AI inference on the Jetson

`record_and_detect.py` - records video , performs inference, includes fovnet comms code.


### Notes 

**Match day setup**

1. Run `bash stream_port1234.sh` on the Jetson to stream video to laptop to check camera angle. Open the corresponding 
`.sdp` file on the laptop to view the stream.
1. Start a `tmux` session on the Jetson, and run `python3 record_video.py` to record the match. 
   2. **...why do we run tmux again? TODO: find this out**


### Useful Jetson commands 

- Run `sudo jtop` to get a grpahical overview of RAM, CPU, GPU useage

