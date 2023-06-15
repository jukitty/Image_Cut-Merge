# Image_Cut&Merge Project
> 이 프로젝트는 이미지를 NxM 조각으로 분할하고, 분할된 이미지를 병합하여 원본과 유사한 이미지를 생성하는 기능을 제공한다.

## How to use
이미지를 자르려면 `cut_image.py` 스크립트를 사용한다.
```
cut_image.py <원본_이미지_파일명> <열_개수> <행_개수> <접두사>
``` 

이미지를 분할하려면 `merge_image.py` 스크립트를 사용한다.
```
python merge_image.py --prefix <접두사> --column <열_개수> --row <행_개수> --output <저장될_이미지_파일명>
``` 

## Algorithm
이미지 병합을 위해 사용한 알고리즘으로 가장 높은 유사도를 가진 이미지 조합을 선택한다.

1. 이미지 조각 로드
지정된 접두사(prefix)로 시작하는 이미지 파일들을 찾아서 이미지 조각으로 로드한다.

2. 원본 이미지 로드
첫 번째 이미지 조각의 이름에서 원본 이미지 파일 이름을 추출하고, 해당 이미지를 로드한다. 
원본 이미지의 크기를 측정하여 복원할 이미지의 크기를 결정하는 기준으로 사용된다.

3.이미지 비율 맞추기
원본 이미지의 비율이 1:1인 경우, 이미지 조각들을 추가로 생성하여 가로 및 세로 방향으로 90도 회전한 조각들을 포함한다.
그런 다음, 이미지 조각들의 크기를 원본 이미지의 비율에 맞춰 조정한다.

4. 이미지 특징 추출
엣지, 텍스처, 색상의 세 가지 특징을 추출한다. 엣지 특징은 Canny 알고리즘을 사용하여 이미지에서 엣지를 추출한 후, 채널 간 유사도를 계산한다. 
텍스처 특징은 ORB(oriented FAST and rotated BRIEF) 특징 추출기를 사용하여 이미지의 특징 디스크립터를 계산한다.
색상 특징은 RGB 각 채널의 평균값을 계산하여 채널 간 유사도를 계산한다.

5. 이미지 병합 및 유사도 비교
모든 경우의 수로 이미지 조합을 생성하고, 각 조합의 유사도를 계산한다. 
유사도는 엣지, 텍스처, 색상의 세 가지 특징 유사도의 평균으로 계산된다.

6. 결과 이미지 저장
가장 높은 유사도를 가진 이미지 조합을 선택하여 원본 이미지와 크기를 맞추고, 결과 이미지를 저장한다.

## Example
원본 이미지
<img src=https://github.com/jukitty/Image_Cut-Merge/blob/main/images/sam/sam.jpg></img>
병합된 이미지
<img src=https://github.com/jukitty/Image_Cut-Merge/blob/main/images/sam/merged_sam.jpg></img>  

원본 이미지
<img src=https://github.com/jukitty/Image_Cut-Merge/blob/main/images/ball/ball.jpg></img>
병합된 이미지
<img src=https://github.com/jukitty/Image_Cut-Merge/blob/main/images/ball/merged_ball.jpg></img>

원본 이미지
<img src=https://github.com/jukitty/Image_Cut-Merge/blob/main/images/JJong/JJong.JPG></img>
병합된 이미지
<img src=https://github.com/jukitty/Image_Cut-Merge/blob/main/images/JJong/merged_JJong.jpg></img>  




