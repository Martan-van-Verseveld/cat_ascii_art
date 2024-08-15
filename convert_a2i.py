from PIL import Image, ImageDraw, ImageFont
import sys, os


def convert(ascii_id, font_size=32) -> Image:
    ascii_text = open(f"./ascii/{str(ascii_id).zfill(4)}", 'r', encoding='utf-8').read()

    font = ImageFont.truetype("./CASCADIAMONO.TTF", font_size)

    lines = ascii_text.splitlines()
    line_heights = [font.getbbox(line)[3] for line in lines]
    max_width = max([font.getbbox(line)[2] for line in lines])
    total_height = sum(line_heights)

    image = Image.new("RGBA", (max_width, total_height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    y_offset = 0
    for line in lines:
        draw.text((0, y_offset), line, font=font, fill=(255, 255, 255, 255))
        y_offset += font.getbbox(line)[3]

    return image


def main():
    params = sys.argv[1:]

    ascii_id = params[0]
    font_size = int(params[1]) if len(params) > 1 and params[1] is not None else 32

    images = []
    if (ascii_id == '*'):
        for index, file_name in enumerate(os.listdir("./ascii/")):
            print('processing: ', file_name)
            images.append([index+1, convert(int(file_name), font_size)])
    else:
        print(f"processing: {str(ascii_id).zfill(4)}")
        images.append([int(ascii_id), convert(ascii_id, font_size)])

    for index, image in images:
        file_path = f"./images/{str(index).zfill(4)}.png"
        if (os.path.isfile(file_path)):
            existing_image = Image.open(file_path)
            if (existing_image.size == image.size):
                continue
        
        image.save(file_path, 'PNG')
        image.show()


if (__name__ == "__main__"):
    main()