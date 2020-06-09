# Image Scrapper
![Image Scrapper](Image_Scrapper.gif)

# How to use
1. 원하는 검색 엔진을 선택 합니다.
2. 1에서 선택한 검색 엔진의 저작권 옵션을 선택 합니다.
3. 현재 Chrome Browser에서만 동작하므로 사용 시 Chrome Driver가 필요합니다.  
   Chrome Browser의 설정에서 사용중인 버전을 확인하신 후 [여기](https://chromedriver.chromium.org/downloads)에서 Chrome Driver를 다운로드합니다.
4. `driver 경로` 버튼을 클릭해서 3에서 저장한 Chrome Driver의 위치를 지정합니다.
5. `저장 경로` 버튼을 클릭해서 이미지를 저장할 폴더를 지정합니다.
6. 검색어와 원하는 이미지의 갯수(최대 1000장)를 설정합니다.
7. `사진 저장` 버튼을 클릭해서 프로그램을 시작합니다.

<br>

~현재 Google만 사용 가능합니다.~  
~2020.06.07자로 Naver가 추가되었습니다.~  
2020.06.08자로 Bing이 추가되었습니다.

# Skills
- Python3
- PyQt5
- Selenium
- BeautifulSoup

# Release  
|Version|Date|Comments|
|---|---|---|
|1.0.0|2020-06-06|최초 제작|
|1.1.0|2020-06-07|Progress Bar를 Real Time Count로 변경|
|1.2.0|2020-06-07|Naver 추가|
|1.3.0|2020-06-08|Naver copyright 추가|
|1.3.1|2020-06-08|Naver CCL 없음 선택 시 오류 수정<br>→ copyright 변수를 기존 str에서 int로 변경|
|1.3.2|2020-06-08|Naver copyright object명 수정<br>→'Bing 라이선스'에서 'Naver CCL'로 변경|
|1.4.0|2020-06-08|Bing 추가|
|1.4.1|2020-06-08|Driver 경로 미 입력 시 경고창 뜨도록 수정|
|1.4.2|2020-06-10|Driver 오류(버전 등) 시 경고창 뜨도록 수정|

<br>

---
  
<br>

#### 문의사항은 [Issue](https://github.com/IllIIIllll/image_scrapper/issues) 페이지에 남겨주세요.
