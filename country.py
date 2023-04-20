from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import time
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font, colors


# 구글 드라이버 위치
driver = webdriver.Chrome("E:/work/pythonCrawling/chromedriver.exe")

# 나라장터 크롤링
def country(keyword):
    try:
        driver.get('https://www.g2b.go.kr:8101/ep/tbid/tbidFwd.do')
        time.sleep(2) # 2초동안 기다리기
        element = driver.find_element(by=By.ID, value="bidNm") # ID중에 bidNm 찾기
        element.send_keys(keyword) # bidNm에 공고명 검색
        driver.find_element(by=By.ID, value="taskClCds5").click() # 용역 체크
        driver.find_element(by=By.XPATH, value='//*[@id="buttonwrap"]/div/a[1]/span').click() # 검색버튼 클릭

        # 검색 결과 확인
        search_result = driver.find_element(by=By.XPATH, value='//*[@id="resultForm"]/div[2]')
        div_list = search_result.find_elements(By.TAG_NAME, "div")

        # 검색 결과 모두 긁어서 리스트로 저장
        results = []
        for div in div_list:
            results.append(div.text)
            a_tags = div.find_elements(By.TAG_NAME, "a")
            if a_tags:
                for a_tags in a_tags:
                    link = a_tags.get_attribute('href')
                    results.append(link)
        result = [results[i * 12:(i + 1) * 12] for i in range((len(results) + 12 - 1) // 12 )]
        return(result)
    
    except Exception as error:
        print(error)
        return(error)

# 엑셀 파일로 데이터 만들기
def makeExcel(data, shitname, filename):
    dataframe = pd.DataFrame(data, columns=["업무", "공고번호-차수", "URL-확인", "분류" ,"공고명", "URL", "공고기관", "수요기관", "계약방법", "입력일시\n(입찰마감일시)", "공동수급", "투찰"])
    dataframe = dataframe.drop('URL-확인', axis='columns')
    
    # Excel 파일 생성
    wb = Workbook()
    ws = wb.active
    ws.title = shitname

    # DataFrame의 내용을 Excel 파일로 옮기기
    for r_idx, row in enumerate(dataframe_to_rows(dataframe, index=1, header=True)):
        for c_idx, value in enumerate(row):
            cell = ws.cell(row=r_idx+2, column=c_idx+1, value=value)
            # URL에 해당하는 셀에 하이퍼링크 추가
            if c_idx == 5:
                url = cell.value
                cell.font = Font(underline="single", color="0563C1")
                cell.value = '=HYPERLINK("%s","%s")' % (url, url)
    
    # Excel 파일 저장
    wb.save('E:/work/pythonCrawling/'+ filename +'.xlsx')
    

if __name__ == "__main__":
    crawling = country('기상')
    makeExcel(crawling, '기상', '나라장터')