from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from bs4 import BeautifulSoup
import os

# Chrome 브라우저의 User-Agent 값을 변경하는 옵션 추가
options = webdriver.ChromeOptions()
# 웹 드라이버 생성
driver = webdriver.Chrome(options=options)


url = "웹페이지주소"
driver.get(url)

# 페이지의 끝까지 스크롤하면서 이미지가 로딩될 때까지 기다리고 최대 시도 횟수 설정
max_attempts = 20
attempt = 1
scroll_increment = 2000
while attempt <= max_attempts:
    # 페이지의 끝까지 스크롤
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    # 조금씩 스크롤 내리기
    driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
    
    try:
        # 이미지가 로딩될 때까지 대기
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "img"))
        )
        
        # 이미지가 모두 로드되었는지 확인
        images = driver.find_elements(By.TAG_NAME, "img")
        print(len(images))
        loaded_images = [img for img in images if img.get_attribute('complete')]
        print(len(images),len(loaded_images) )
    except:
        print(f"이미지 로드 시도 {attempt}/{max_attempts}... 실패")
    attempt += 1

if attempt > max_attempts:
    print("이미지 로드를 위한 최대 시도 횟수를 초과했습니다.")

# 페이지 소스 가져오기
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")
img_elements = soup.find_all("img")
# 이미지를 저장할 디렉토리 생성
if not os.path.exists("images"):
    os.makedirs("images")
with open("image_info.txt", "w",encoding="utf-8") as file:
    for img in img_elements:
        alt = img["alt"]
        src = img["src"]
        if src.endswith(".jpg"):
            alt = "".join(x for x in alt if x.isalnum())
            file.write(f"{alt}\t{src}\n")
print("이미지 정보가 성공적으로 파일에 저장되었습니다.")
