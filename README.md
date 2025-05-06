# APW Nodes for ComfyUI

A custom node suite to augment the capabilities of the [AP Workflows for ComfyUI](https://perilli.com/ai/comfyui/)

## Nodes

### Image List Filter v1

This node takes an `image list` as input, filters out images smaller than either width or height, and outputs a new `image list` without the excluded images.

If no input image remains after the filtering, the node outputs a new `image list` with the optional fallback image input.

<img width="412" alt="Image List Filter v1" src="/Images/Image%20List%20Filter%201.0.3.png" />

Notice: This code is based on Kijai's `Image Batch Filter`, available [here](https://github.com/kijai/ComfyUI-KJNodes/). All credit to him.

## Installation

Install from ComfyUI Manager:

<img width="1378" alt="APW Nodes ComfyUI Manager" src="https://github.com/user-attachments/assets/0893fccf-3a5e-4726-a6e6-0e32c60d28b8" />

or clone this repo into the `/comfyui/custom_nodes` folder.
