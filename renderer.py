# renderer.py

import os
import logging
import csv
import cv2
from qiskit import QuantumCircuit
from qiskit.visualization import circuit_drawer

# 📁 Logging Setup
os.makedirs('render_output', exist_ok=True)
logging.basicConfig(
    filename='render_output/renderer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class Renderer:
    """
    SlizzAi Visual Ritual Engine — renders quantum circuits and overlays symbolic glyphs.
    """

    def __init__(self, output_dir="render_output", resolution=(1920, 1080), fps=60, frames=100):
        self.output_dir = output_dir
        self.resolution = resolution
        self.fps = fps
        self.frames = frames
        os.makedirs(self.output_dir, exist_ok=True)
        logging.info("🖼️ Renderer initialized.")

    def render_circuit(self, qc: QuantumCircuit = None, filename: str = "circuit.png"):
        try:
            if qc is None:
                qc = QuantumCircuit(3)
                qc.h(0)
                qc.cx(0, 1)
                qc.cx(1, 2)
                logging.info("🌀 Default quantum circuit generated.")

            path = os.path.join(self.output_dir, filename)
            circuit_drawer(qc, output='mpl', filename=path)
            logging.info(f"🎨 Circuit rendered to {path}")
            return path
        except Exception as e:
            logging.error(f"❌ Circuit rendering failed: {e}")
            return None

    def overlay_entropy_glyph(self, base_image_path: str, delta_H: float, filename: str = "glyph_overlay.png"):
        try:
            img = cv2.imread(base_image_path)
            if img is None:
                raise FileNotFoundError(f"Image not found at {base_image_path}")

            overlay_text = f"Ξα(ψ) ΔH = {delta_H:.4f}"
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, overlay_text, (50, 50), font, 1, (255, 0, 255), 2, cv2.LINE_AA)

            path = os.path.join(self.output_dir, filename)
            cv2.imwrite(path, img)
            logging.info(f"🧬 Glyph overlay saved to {path}")
            return path
        except Exception as e:
            logging.error(f"❌ Glyph overlay failed: {e}")
            return None

    def show_image(self, image_path: str):
        try:
            img = cv2.imread(image_path)
            if img is None:
                raise FileNotFoundError(f"Image not found at {image_path}")
            cv2.imshow("SlizzAi Ritual Image", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            logging.info(f"🖼️ Image displayed: {image_path}")
        except Exception as e:
            logging.error(f"❌ Image display failed: {e}")

    def save_metadata(self, metadata: dict, filename: str = "metadata.csv"):
        try:
            path = os.path.join(self.output_dir, filename)
            with open(path, mode='w', newline='') as file:
                writer = csv.writer(file)
                for key, value in metadata.items():
                    writer.writerow([key, value])
            logging.info(f"💾 Metadata saved to {path}")
            return path
        except Exception as e:
            logging.error(f"❌ Metadata saving failed: {e}")
            return None