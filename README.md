# vxp-server
Processing server for [VXP](https://github.com/tetra-fox/VRCMods/tree/master/VXP), a VRChat mod that sets your facial expressions based on the tone in your voice. Though technically, this is just a generic websocket server so you can use it as you please.

# Prerequisites
- [`python >= 3.8`](https://www.python.org/downloads/)
- VRChat with [MelonLoader](https://github.com/LavaGang/MelonLoader/releases/latest) installed
- [VXP](https://github.com/tetra-fox/VRCMods/releases/latest/)
- [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads) *(Optional, for GPU acceleration)*

# Setup (Windows)
1. Clone the repository, or download & extract the [.zip file](https://github.com/tetra-fox/vxp-server/archive/refs/heads/main.zip). Keep this folder somewhere safe!
2. Install dependencies with `pip install -r requirements.txt`
3. Run `start.bat`

# Setup (Linux)
If you use Linux, this should be pretty straightforward. :P

## Credit
- This server uses Google's distilled TRILL model, found [here](https://tfhub.dev/google/lite-model/nonsemantic-speech-benchmark/trill-distilled/1).

<sup>Shor, J., Jansen, A., Maor, R., Lang, O., Tuval, O., de Chaumont Quitry, F., Tagliasacchi, M., Shavitt, I., Emanuel, D., & Haviv, Y. (2020). Towards Learning a Universal Non-Semantic Representation of Speech. *Proc. Interspeech 2020*, 140–144. https://doi.org/10.21437/Interspeech.2020-1242</sup>