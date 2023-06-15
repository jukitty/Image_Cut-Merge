import sys
import os
from PIL import Image, ImageFilter
import itertools
import numpy as np
import cv2
import argparse

def extract_edge_features(image):
    grayscale_image = image.convert("L")  # 이미지를 그레이스케일로 변환
    edges = grayscale_image.filter(ImageFilter.FIND_EDGES)  # 엣지 감지
    edge_features = np.array(list(edges.getdata()), dtype=np.uint8)  # 픽셀 데이터 가져오기

    return edge_features

def calculate_edge_similarity(edge_features1, edge_features2):
    template = edge_features1.reshape(-1, 1)
    target = edge_features2.reshape(-1, 1)

    result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
    similarity = np.max(result)

    return similarity

# 채널 유사도 계산 함수
def calculate_channel_similarity(image1, image2):
    # 이미지를 넘파이 배열로 변환
    pixels1 = np.array(image1)
    pixels2 = np.array(image2)

    # 채널 크기 맞추기
    pixels1 = np.resize(pixels1, pixels2.shape)

    # 채널 별로 픽셀 간의 차이 계산
    channel_diff = np.abs(pixels1 - pixels2)

    # 채널 별 차이를 평균하여 유사도 계산
    channel_similarity = 1 - np.mean(channel_diff) / 255

    return channel_similarity

def extract_image_piece_edge_features(image_pieces):
    piece_edge_features = []

    for piece in image_pieces:
        edge_features = extract_edge_features(piece)
        piece_edge_features.append(edge_features)

    return np.array(piece_edge_features)  # 넘파이 배열로 변환하여 반환


def merge_images(prefix, column_num, row_num, output_filename):
    # 이미지 파일 경로(확장자 제한)
    file_list = [
        os.path.basename(f.path)
        for f in os.scandir()
        if f.is_file() and f.name.startswith(prefix) and f.name.endswith(('.jpg', '.jpeg', '.png'))
    ]

    # 이미지 조각 객체들을 담을 리스트
    image_pieces = []
    for image_name in file_list:
        if image_name.startswith(prefix):
            image_path = os.path.join('.', image_name)
            image = Image.open(image_path)
            image_pieces.append(image)

    # 원본 이미지 로드
    first_image_name = file_list[0].split('_')[2]
    first_image_path = os.path.join('./', first_image_name)
    original_image = Image.open(first_image_path)
    original_width, original_height = original_image.size
    target_ratio = original_width / original_height

    # 원본 비율이 1:1인 경우 원본 조각 이미지와 270도 회전한 이미지 추가
    if target_ratio == 1:
        for i in range(len(image_pieces)):
            original_piece = image_pieces[i]
            original_piece_rotated = original_piece.transpose(Image.ROTATE_270)
            image_pieces.append(original_piece)
            image_pieces.append(original_piece_rotated)

    # 이미지 조각들을 원본 비율로 맞추기
    for i in range(len(image_pieces)):
        piece_width, piece_height = image_pieces[i].size
        piece_ratio = piece_width / piece_height

        # 비율이 다른 경우 이미지 조각 조정
        if piece_ratio != target_ratio:
            transform = Image.ROTATE_270
            rotated_piece = image_pieces[i].transpose(transform)
            image_pieces.append(rotated_piece)

        # 이미지 조각 크기 조정
        resized_piece = image_pieces[i].resize((original_width // column_num, original_height // row_num))
        image_pieces[i] = resized_piece

        # 추가적인 변환 조합
        image_pieces.append(resized_piece)
        image_pieces.append(resized_piece.transpose(Image.FLIP_LEFT_RIGHT))
        image_pieces.append(resized_piece.transpose(Image.FLIP_TOP_BOTTOM))
        image_pieces.append(resized_piece.transpose(Image.FLIP_LEFT_RIGHT | Image.FLIP_TOP_BOTTOM))

    # 이미지 조각들의 엣지 특징 추출
    piece_edge_features = extract_image_piece_edge_features(image_pieces)

    # 모든 경우의 수로 이미지 조합 생성 및 유사도 비교
    best_merged_image = None
    best_similarity = 0

    for combination in itertools.permutations(range(len(image_pieces)), column_num * row_num):
        print(f'{combination} 유사도 비교')
        merged_width = column_num * image_pieces[0].width
        merged_height = row_num * image_pieces[0].height
        merged_image = Image.new("RGB", (merged_width, merged_height))

        for row in range(row_num):
            for col in range(column_num):
                piece = image_pieces[combination[row * column_num + col]]
                merged_image.paste(piece, (col * piece.width, row * piece.height))

        # 이미지 크기 조정
        merged_image = merged_image.resize((original_width, original_height))

        # 엣지 특징 추출
        merged_edge_features = extract_edge_features(merged_image)

        # 엣지 특징 유사도 계산
        edge_similarity = calculate_edge_similarity(merged_edge_features, piece_edge_features)

        # 가장 높은 유사도 업데이트
        if edge_similarity > best_similarity:
            best_similarity = edge_similarity
            best_merged_image = merged_image

        # 이미 최고 유사도를 넘어설 수 없는 경우 종료
        if best_similarity == 1.0:
            break

    # 결과 출력
    print(f'가장 높은 유사도: {best_similarity}')
    best_merged_image.save(output_filename)
    print(f'결과 이미지 저장: {output_filename}')

# 스크립트 실행
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Merge image pieces')
    parser.add_argument('--prefix', type=str, help='Prefix of image files')
    parser.add_argument('--column', type=int, help='Number of columns')
    parser.add_argument('--row', type=int, help='Number of rows')
    parser.add_argument('--output', type=str, help='Output image file name')

    args = parser.parse_args()

    merge_images(args.prefix, args.column, args.row, args.output)
