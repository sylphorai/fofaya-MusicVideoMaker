from moviepy.editor import AudioFileClip, ImageClip, ColorClip
from PIL import Image, ImageOps
import os

class Converter:
    def __init__(self, config_manager):
        self.config_manager = config_manager

    def convertir_mp3_a_mp4(self, mp3_paths, output_dir=None):
        config = self.config_manager.get_config()
        width = config.get("width", 1920)
        height = config.get("height", 1080)
        image_path = config.get("default_image", "")
        output_dir = output_dir or config["output_path"]

        for mp3_path in mp3_paths:
            try:
                # Generar la ruta de salida para cada archivo
                mp4_path = os.path.join(output_dir, os.path.splitext(os.path.basename(mp3_path))[0] + ".mp4")

                audio_clip = AudioFileClip(mp3_path)
                if image_path:
                    image = Image.open(image_path)
                    image = ImageOps.pad(image, (width, height), method=Image.LANCZOS, color=(0, 0, 0))
                    image.save("padded_image.png")
                    video_clip = ImageClip("padded_image.png").set_duration(audio_clip.duration)
                else:
                    video_clip = ColorClip(size=(width, height), color=(0, 0, 0), duration=audio_clip.duration)

                video_clip = video_clip.set_audio(audio_clip)
                video_clip.fps = 24
                video_clip.write_videofile(mp4_path, codec='libx264', audio_codec='aac', fps=24)
            except Exception as e:
                print(f"Error al convertir el archivo {mp3_path}: {e}")
