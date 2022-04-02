# jetson-camera-code
Backup for the camera controlling code on our Jetsons

## Some notes on usage
### Streaming to laptop to check camera angle
This is the code contained within `stream_port1234.sh`:
- To run, run `bash stream_port1234.sh` from the Jetson's terminal 
  - Ensure that the IP address within the script equals your **local IP address (ie your laptop's!)**
- On your laptop, run the `stream1234.sdp` file, just click on it if you have it on your desktop, or open it with VLC player (note this isn't on this repo yet, will make a laptop files directory).

### For recording the matches 

I have added a `record_video.sh` file which should handle everything but 
I still need to test it. 

