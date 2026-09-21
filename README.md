# Quantum Image Watermarking: Geometric Flipping Attacks

This directory contains the Python source code for simulating the NEQR watermarking pipeline against geometric flipping attacks.

## Directory Structure

The code is organized by the axis of the geometric flip:
* **`Flip_X/`**: Simulation scripts for horizontal axis flips (Flip X).
* **`Flip_Y/`**: Simulation scripts for vertical axis flips (Flip Y).

Inside each of these folders, the code is further separated into two pipelines:
* **`Array_Simulation/`**: Matrix-based simulation using simple 2x2 arrays to verify the quantum circuit logic.
* **`Image_Processing/`**: Practical image-based processing that works with 8x8 grayscale `.tif` images.

**Note:** The input images and generated outputs are stored locally in the `input_images/` and `outputs/` folders respectively.

## How to Execute the Code

### Prerequisites
Make sure you have the required Python libraries installed:
```bash
pip install qiskit matplotlib pylatexenc opencv-python numpy
```

### Running the Scripts
Here are the exact commands to run every script in the Flips project. The typical workflow is to run the embedding script first, followed by the extraction scripts.

Because the paths have been properly updated, the scripts will automatically find the cover and watermark files in the local `input_images/` directory and will successfully save the generated quantum circuit diagrams to the local `outputs/` directory.

#### Flip X (Horizontal Axis)
**Array Simulation (2x2 Matrix):**
```bash
cd Flip_X/Array_Simulation
python 01_embed_array_flip_x.py
python 02_extract_direct_array_flip_x.py
python 03_extract_revert_array_flip_x.py
cd ../..
```

**Image Processing (8x8 Image):**
```bash
cd Flip_X/Image_Processing
python 07_embed_image_flip_x.py
python 08_extract_direct_image_flip_x.py
python 09_extract_revert_image_flip_x.py
cd ../..
```

#### Flip Y (Vertical Axis)
**Array Simulation (2x2 Matrix):**
```bash
cd Flip_Y/Array_Simulation
python 04_embed_array_flip_y.py
python 05_extract_direct_array_flip_y.py
python 06_extract_revert_array_flip_y.py
cd ../..
```

**Image Processing (8x8 Image):**
```bash
cd Flip_Y/Image_Processing
python 10_embed_image_flip_y.py
python 11_extract_direct_image_flip_y.py
python 12_extract_revert_image_flip_y.py
cd ../..
```
