from PIL import Image

def convert_to_ico(bmp_path, ico_path):
    image = Image.open(bmp_path)
    image.save(ico_path, format='ICO')

# Ensure the output path includes the filename and extension
bmp_path = "./Hacknet.bmp"
ico_path = "PATH_IMAGE"

convert_to_ico(bmp_path, ico_path)
