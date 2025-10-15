from PIL import Image
import os

def revert_images_in_directory(directory):
    """
    将指定目录下的所有PNG图片进行垂直翻转。
    """
    # 确保目录存在
    if not os.path.isdir(directory):
        print(f"错误：目录 '{directory}' 不存在。")
        return

    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        if filename.lower().endswith(".png"):
            file_path = os.path.join(directory, filename)
            try:
                # 打开图片
                with Image.open(file_path) as img:
                    # 上下翻转图片
                    reverted_img = img.transpose(Image.FLIP_TOP_BOTTOM)
                    # 保存翻转后的图片，覆盖原文件
                    reverted_img.save(file_path)
                    print(f"已翻转图片: {filename}")
            except Exception as e:
                print(f"处理图片 {filename} 时出错: {e}")

if __name__ == "__main__":
    ui_directory = os.path.join('assets', 'ui')
    revert_images_in_directory(ui_directory)
