# vxp-server
Processing server for [VXP](https://github.com/tetra-fox/VRCMods/tree/master/VXP), a VRChat mod that sets your facial expressions based on the tone in your voice. Though technically, this is just a generic websocket server so use it as you please.

# Requirements
- An RTX series GPU
- [`python >= 3.8`](https://www.python.org/downloads/)
- [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads)
- VRChat with [MelonLoader](https://github.com/LavaGang/MelonLoader/releases/latest) installed
- [VXP](https://github.com/tetra-fox/VRCMods/releases/latest/)

# Setup
1. Install [`python >= 3.8`](https://www.python.org/downloads/)
2. Install [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads)
3. Clone the repository, or download & extract the [.zip file](https://github.com/tetra-fox/vxp-server/archive/refs/heads/main.zip). Keep this folder somewhere safe!
4. Install dependencies with `pip install -r requirements.txt`
5. Run `start.bat`

<!-- ## Credit
- `model.tflite` was created with the assistance of tjhorner
- `mlp_classifer.model` was created by x4nth055 and can be found [here](https://github.com/x4nth055/pythoncode-tutorials/tree/master/machine-learning/speech-emotion-recognition/result) -->