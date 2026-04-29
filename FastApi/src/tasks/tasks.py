from PIL import Image
import os
from src.tasks.celery_app import celery_instance

@celery_instance.task
def compress_image(input_path: str):
    widths = [1000, 500, 200]
    output_dir = "src/static/images"

    os.makedirs(output_dir, exist_ok=True)

    try:
        with Image.open(input_path) as img:
            name, ext = os.path.splitext(os.path.basename(input_path))

            for width in widths:
                ratio = width / img.width
                height = int(img.height * ratio)

                resized = img.resize((width, height), Image.LANCZOS)

                output_filename = f"{name}_{width}{ext}"
                output_path = os.path.join(output_dir, output_filename)

                save_kwargs = {"optimize": True}
                if ext.lower() in [".jpg", ".jpeg"]:
                    save_kwargs["quality"] = 85

                resized.save(output_path, **save_kwargs)

                print(f"Saved: {output_path}")

    except Exception as e:
        print(f"Error: {e}")