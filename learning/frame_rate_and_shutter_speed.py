import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

def on_new_sample(sink):
    sample = sink.pull_sample()
    buf = sample.get_buffer()
    result, mapinfo = buf.map(Gst.MapFlags.READ)
    if result:
        # You can now access the data in mapinfo.data and save it as a photo
        # Do some processing here...
        buf.unmap(mapinfo)
    return Gst.FlowReturn.OK

def run_pipeline():
    Gst.init(None)

    pipeline = Gst.Pipeline.new("test-pipeline")

    src = Gst.ElementFactory.make("nvarguscamerasrc", "camera-source")
    src.set_property("sensor-mode", 0)
    src.set_property("shutter-speed", int(1000000 / 10))  # Set the shutter speed to 1/10 sec
    pipeline.add(src)

    # Use a video/x-raw format and specify the desired framerate
    caps = Gst.Caps.from_string("video/x-raw, framerate=10/1")

    # Convert the video data to a suitable format for saving as a photo
    convert = Gst.ElementFactory.make("videoconvert", "convert")
    pipeline.add(convert)

    # Use a appsink to access the raw video data
    sink = Gst.ElementFactory.make("appsink", "appsink")
    sink.set_property("emit-signals", True)
    sink.connect("new-sample", on_new_sample)
    pipeline.add(sink)

    src.link_filtered(convert, caps)
    convert.link(sink)

    pipeline.set_state(Gst.State.PLAYING)

    GLib.MainLoop().run()

if __name__ == '__main__':
    run_pipeline()
    