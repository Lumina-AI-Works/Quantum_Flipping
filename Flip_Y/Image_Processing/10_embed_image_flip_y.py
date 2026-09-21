import numpy as np
import cv2
from qiskit import QuantumCircuit, QuantumRegister

def get_qubit_counts(size):
    return int(np.ceil(np.log2(size)))

def apply_binary_address(qc, q_reg, value, n):
    binary_str = format(value, f'0{n}b')
    for i in range(n):
        if binary_str[n - 1 - i] == '0':
            qc.x(q_reg[i])

def prepare_neqr_state(qc, q_y, q_x, q_c, q_w, cover, wm, n, size):
    qc.barrier(label="Superposition")
    qc.h(q_y)
    qc.h(q_x)
    
    controls = list(q_y) + list(q_x)
    
    for y in range(size):
        for x in range(size):
            cover_val = int(cover[y, x]) & 254
            wm_val = int(wm[y, x])
            
            apply_binary_address(qc, q_y, y, n)
            apply_binary_address(qc, q_x, x, n)
            
            cover_bin = format(cover_val, '08b')
            for i in range(8):
                if cover_bin[7 - i] == '1':
                    qc.mcx(controls, q_c[i])
                    
            if wm_val == 1:
                qc.mcx(controls, q_w[0])
                
            apply_binary_address(qc, q_y, y, n)
            apply_binary_address(qc, q_x, x, n)

def embed_watermark(qc, q_c, q_w):
    qc.barrier(label="Embedding")
    qc.cx(q_w[0], q_c[0])

def apply_flip_y(qc, q_x, n):
    qc.barrier(label="Flip Y")
    for i in range(n):
        qc.x(q_x[i])

def build_flip_y_stego_circuit(cover=None, wm=None):
    if cover is None:
        cover = cv2.imread("../../input_images/cover_8x8.tif", cv2.IMREAD_GRAYSCALE)
    if wm is None:
        wm = cv2.imread("../../input_images/message_8x8.tif", cv2.IMREAD_GRAYSCALE)
        wm = (wm > 127).astype(np.uint8)
    size = cover.shape[0]
    n = get_qubit_counts(size)
    
    q_y = QuantumRegister(n, 'y')
    q_x = QuantumRegister(n, 'x')
    q_c = QuantumRegister(8, 'c')
    q_w = QuantumRegister(1, 'w')
    qc = QuantumCircuit(q_w, q_c, q_x, q_y, name="Flip Y Stego")
    
    prepare_neqr_state(qc, q_y, q_x, q_c, q_w, cover, wm, n, size)
    embed_watermark(qc, q_c, q_w)
    apply_flip_y(qc, q_x, n)
    
    return qc, q_y, q_x, q_c, q_w, n, size, wm

if __name__ == "__main__":
    qc, _, _, _, _, n, size, _ = build_flip_y_stego_circuit()
    try:
        fig = qc.draw(output='mpl', style='clifford', fold=50)
        fig.savefig('../../outputs/Image_1_Embedding_and_Attack_Circuit_FlipY.png', bbox_inches="tight", dpi=300)
        print("Circuit successfully built and saved to outputs/1_stego_flip_y.png!")
    except Exception as e:
        print(f'Notice: Circuit diagram too large to draw/save ({type(e).__name__}). Skipping circuit image.')

    # Classical Stego Image Representation
    try:
        import cv2
        import numpy as np
        cover_img = cv2.imread("../../input_images/cover_8x8.tif", cv2.IMREAD_GRAYSCALE)
        wm_img = cv2.imread("../../input_images/message_8x8.tif", cv2.IMREAD_GRAYSCALE)
        wm_img_bin = (wm_img > 127).astype(np.uint8)
        stego_classical = (cover_img & 254) | wm_img_bin
        if 'FlipY' == 'FlipX': stego_attacked = np.flipud(stego_classical)
        elif 'FlipY' == 'FlipY': stego_attacked = np.fliplr(stego_classical)
        elif 'FlipY' == '90_Deg': stego_attacked = np.rot90(stego_classical, -1)
        elif 'FlipY' == '180_Deg': stego_attacked = np.rot90(stego_classical, -2)
        elif 'FlipY' == '270_Deg': stego_attacked = np.rot90(stego_classical, -3)
        cv2.imwrite('../../outputs/Image_1.5_Stego_Image_FlipY.png', stego_attacked)
        print("Saved Stego Image to outputs/Image_1.5_Stego_Image_FlipY.png")
    except Exception as e:
        pass
