from PIL import Image
import os

def hex_to_rgba(hex_color):
    """Convert hex color to RGBA"""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) != 6:
        raise ValueError("HEX color must be 6 characters long.")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4)) + (255,)

def list_image_files():
    """List all image files in the current directory"""
    exts = ('.png', '.jpg', '.jpeg', '.bmp', '.webp')
    return [f for f in os.listdir('.') if f.lower().endswith(exts)]

def main():
    print("=== Background Color Changer for Icon Images ===")
    print(f"📂 Current folder: {os.getcwd()}")
    print("📸 Available image files:")
    for f in list_image_files():
        print(f" - {f}")

    image_name = input("\nEnter the image filename exactly as shown above: ").strip()
    if not os.path.isfile(image_name):
        print(f"❌ File '{image_name}' not found.")
        return

    hex_color = input("Enter HEX background color (e.g. #003300): ").strip()
    try:
        bg_color = hex_to_rgba(hex_color)
    except Exception as e:
        print(f"❌ Invalid HEX color: {e}")
        return

    original_image = Image.open(image_name).convert("RGBA")

    scale_factor = 2
    new_size = (original_image.width * scale_factor, original_image.height * scale_factor)
    upscaled = original_image.resize(new_size, Image.LANCZOS)

    result = Image.new("RGBA", new_size, bg_color)

    for y in range(new_size[1]):
        for x in range(new_size[0]):
            r, g, b, a = upscaled.getpixel((x, y))
            if (r + g + b) / 3 > 220 and a > 128:
                result.putpixel((x, y), (255, 255, 255, 255))

    out_name = input("Enter output filename (with .png extension): ").strip()
    if not out_name:
        out_name = f"converted_{os.path.splitext(image_name)[0]}.png"
        print(f"No filename entered, using default: {out_name}")
    elif not out_name.lower().endswith('.png'):
        out_name += '.png'  # Add .png if missing

    result.save(out_name)
    print(f"✅ Saved: {out_name}")

if __name__ == "__main__":
    main()
