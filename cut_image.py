import sys
import random
import os
from PIL import Image
import numpy as np
import albumentations as A
import argparse

def generate_random_name(length=8):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    random_name = "".join(random.choice(characters) for _ in range(length))
    return random_name

def divide_image(image_path, column_num, row_num, prefix):
    # 이미지 파일 확장자 제한
    supported_extensions = ['.jpg', '.jpeg', '.png']
    if not any(image_path.lower().endswith(ext) for ext in supported_extensions):
        print("지원되는 이미지 파일 형식이 아닙니다.")
        return

    # 이미지 열기
    image = Image.open(image_path)

    # albumentations 변환 설정
    transform = A.Compose([
        A.HorizontalFlip(p=0.5),
        A.VerticalFlip(p=0.5),
        A.RandomRotate90(p=0.5)
    ])

    # 이미지 크기 확인
    width, height = image.size

    # 각 조각의 너비와 높이 계산
    piece_width = width // column_num
    piece_height = height // row_num

    # 이미지를 조각별로 분할
    for row in range(row_num):
        for col in range(column_num):
            left = col * piece_width
            upper = row * piece_height
            right = left + piece_width
            lower = upper + piece_height

            piece = image.crop((left, upper, right, lower))

            # albumentations 적용
            piece = transform(image=np.array(piece))["image"]
            piece = Image.fromarray(piece)

            # 랜덤한 이름 생성
            random_name = generate_random_name()

            # 분할된 이미지 저장
            output_filename = f"{prefix}_{random_name}_{sys.argv[1].split('.')[0]}.jpg"
            piece.save(output_filename)

            print(f"{output_filename}로 이미지 저장 완료")

    print("이미지 분할 완료")

if __name__ == "__main__":
    # 명령행 인수 파싱을 위한 argparse 객체 생성
    parser = argparse.ArgumentParser(description="Divide image into pieces.")
    
    # 인수 추가
    parser.add_argument("image_file_name", type=str, help="Image file name.")
    parser.add_argument("column_num", type=int, help="Number of columns.")
    parser.add_argument("row_num", type=int, help="Number of rows.")
    parser.add_argument("prefix_output_filename", type=str, help="Prefix for output filenames.")
    
    # 인수 파싱
    args = parser.parse_args()

    # 이미지 분할 실행
    divide_image(args.image_file_name, args.column_num, args.row_num, args.prefix_output_filename)
