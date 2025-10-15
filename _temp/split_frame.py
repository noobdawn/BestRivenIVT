from PIL import Image
import os

def split_image(image_path, output_dir, block_width, block_height):
    """
    Splits an image into blocks of a specified size.

    Args:
        image_path (str): The path to the input image.
        output_dir (str): The directory to save the output blocks.
        block_width (int): The width of each block.
        block_height (int): The height of each block.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    img = Image.open(image_path)
    img_width, img_height = img.size

    for i in range(0, img_height, block_height):
        for j in range(0, img_width, block_width):
            box = (j, i, j + block_width, i + block_height)
            block = img.crop(box)
            block.save(os.path.join(output_dir, f'block_{i}_{j}.png'))

if __name__ == '__main__':
    input_image = os.path.join('_temp', 'miniframe.png')
    output_directory = os.path.join('_temp', 'split_images')
    block_w = 249
    block_h = 258
    split_image(input_image, output_directory, block_w, block_h)
    print(f"Image '{input_image}' has been split into {block_w}x{block_h} blocks in '{output_directory}'")
