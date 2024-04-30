import os
import requests
import time

# txt 파일 경로
txt_file_path = "image_info.txt"

# 이미지 다운로드 함수
def download_image(file_name, url, header):
    try:
        # 이미지 다운로드
        response = requests.get(url, headers=header)
        file_name = "".join(x for x in file_name if x.isalnum())
        # 파일 저장
        with open(f"images/{file_name}.jpg", "wb") as f:
            f.write(response.content)
        
        print(f"{file_name} 다운로드 완료")
    except Exception as e:
        print(f"{file_name} 다운로드 실패:", e)

# txt 파일 읽기
with open(txt_file_path, "r", encoding="utf-8") as file:
    for line_num, line in enumerate(file):
        # 처음 10줄만 처리
        # if line_num >= 3:
        #     break
        # 파일 이름과 이미지 다운로드 경로 분리
        file_name, url = line.strip().split("\t")
        
        # 이미지 다운로드
        if not os.path.exists("images"):
            os.makedirs("images")
        header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
        download_image(file_name, url, header)
