# jetson-camera-code
Backup for the camera controlling code on our Jetsons

**Note that we have to make the `update_jetson_config_file.sh` executable via `chmod +x update_jetson_config_file.py`**

Note taht I also have to do the same for the `calls_jetson_update_file.sh` script which will be in the `dispatcher.d` directory... except that I need to prepend the 
command with sudo (it needs root permission)

I shouldn't need to make another 

# TODO 

- [ ] ==**The paths in `main_loop.py` are hardcoded... replace these with environment variables when you can. It could cause some confusion later potentially**==

- [ ] Update the process for a match day in Bohs, absolutely step by step, for when I inevitably (potentially) forget everything! In Notion and in Logseq (experiment with moving over there more! Maybe Obsidian too!) 

## Some notes on usage
### Streaming to laptop to check camera angle
This is the code contained within `stream_port1234.sh`:
- To run, run `bash stream_port1234.sh` from the Jetson's terminal 
  - Ensure that the IP address within the script equals your **local IP address (ie your laptop's!)**
- On your laptop, run the `stream1234.sdp` file, just click on it if you have it on your desktop, or open it with VLC player (note this isn't on this repo yet, will make a laptop files directory).

### For recording the matches 

I have added a `record_video.sh` file which should handle everything but 
I still need to test it. 

### Whats going on in the background

The `calls_jetson_update_file.sh` file gets added to the `/etc/NetworkManager/dispatcher.d` which automatically gets run when the device connects succesfully to the internet. This file runs the `update_match_config_file.sh` within this project's home directory which then updates the `config.py` and `stream_port1234.sh` files. 
**This means that we only have to update the time of the match, and the IP address of this laptop in case its changed, in preparation for a game** (assuming that the cameras are working ok (I should write some sort of test for them when I have time)). 




