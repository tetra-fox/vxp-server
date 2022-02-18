# vxp-server
Processing server for [VXP](https://github.com/tetra-fox/VRCMods/tree/master/VXP), a VRChat mod that sets your facial expressions based on the tone in your voice. Though technically, this is just a generic websocket server so you can use it as you please.

# Prerequisites
- [`python >= 3.8`](https://www.python.org/downloads/)

# Optional dependencies (for GPU acceleration)
- [NVIDIA® GPU drivers](https://www.nvidia.com/drivers) >= 450.80.02
- [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads) = 11.2
- [CUPTI](http://docs.nvidia.com/cuda/cupti/) *(this is automatically installed if you have installed CUDA Toolkit)*
- [cuDNN SDK](https://developer.nvidia.com/cudnn) = 8.1.0 ([version archive](https://developer.nvidia.com/rdp/cudnn-archive))

Further reading: [TensorFlow - GPU support](https://www.tensorflow.org/install/gpu)

# Setup (VRChat, Windows)
1. Clone the repository, or download & extract the [.zip file](https://github.com/tetra-fox/vxp-server/archive/refs/heads/main.zip). Keep this folder somewhere safe! VXP will reference this folder.
2. Run `python vrchat_setup.py`
3. Install [VXP](https://github.com/tetra-fox/VRCMods/tree/master/VXP)
4. Launch VRChat!

# Setup (Generic usage, Windows)
1. Clone the repository, or download & extract the [.zip file](https://github.com/tetra-fox/vxp-server/archive/refs/heads/main.zip).
2. Create & activate a virtual environment with `py -m pip .venv; ./venv/Scripts/Activate.ps1`
3. Install dependencies with `pip install -r requirements.txt`
4. Run `python server.py`
5. You may now access the WebSocket server at `ws://localhost:8274`

Note: You may not see anything happening yet, as avatar setup is required! You can read more about this in the [VXP README](https://github.com/tetra-fox/VRCMods/tree/master/VXP)

# Troubleshooting
- I moved my folder, and everything broke! What now?
  - Run `python vrchat_setup.py` again. What this script does internally is tell VXP *where* exactly the server folder is located, in order to be able to automatically start the server. By running it again, we are making VXP aware of the folder's new location.
- I'm getting a bunch of errors about missing CUDA libraries.
  - These are safe to ignore, as long as you don't intend to use your GPU for acceleration. However, if you installed the [optional dependencies](#optional-dependencies-for-gpu-acceleration) and are *still* recieving errors, unfortunately that's out of the scope of what I'm able to offer help for. Google is your friend here. Most likely, a clean reinstall of these libraries will fix the issue.