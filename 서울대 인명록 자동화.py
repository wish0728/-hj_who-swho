# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.6
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from collections import Counter
import pprint
import os
import pickle
import requests
import fitz
import hanja
from hanja import hangul

# +
# index 파일 불러와서 texts_index에 (리스트형태로) 저장
d_path = '/Users/seulalee/OneDrive/Personal_Project/HJ_인명록 자동화 코드/원본/2012_snu_alumni_index.pdf'

with fitz.open(d_path) as doc:
  texts_index = []
  for page in doc:
    text = page.get_text()
    texts_index.append(text)
    
print(len(texts_index))

# +
# texts_index에 리스트 형태로, 리스트안에 리스트 형태로, 한 페이지씩 들어있음 
# texts_index[3] 부터 이름이 담긴 페이지이므로, 여기부터 마지막 페이지까지 돌면서 한 줄에 번역된 '이름 연도 학과 페이지'가 모두 들어가게

one_person_one_line = []

for i in range(len(texts_index)-3):
    onepage = texts_index[i+3]
    onepage = onepage.split("\n")
    for j in range(len(onepage)):
        if '(' in onepage[j] and ')' in onepage[j] :
            translated = hanja.translate(onepage[j], 'combination-text')
            one_person_one_line.append(translated)
        elif ')' in onepage[j]:
            oneline_merge = onepage[j-1] + onepage[j]
            translated = hanja.translate(oneline_merge, 'combination-text')
            one_person_one_line.append(translated)
one_person_one_line
# -

# 인덱스 리스트 완료 확인
one_person_one_line[-50:]

# 인덱스 리스트 index_df로 변경
df = pd.DataFrame(one_person_one_line)
index_df = df

index_df.tail(10)

index_df.head(10)

# 맨 아래의 업체 전화번호 삭세
index_df = index_df[1:-5]
index_df.tail(10)

# csv파일로 저장
index_df.to_csv("/Users/seulalee/OneDrive/Personal_Project/HJ_인명록 자동화 코드/인덱스변환완료.csv")

# ## index파일의 '이름 기수 전공 페이지'를 모두 담은 변수를 csv형태로 저장해두었음.
#
# ## 인터뷰대상자 목록을 데이터프레임 형태로 불러와서 매치되는거 찾아서 붙여넣어주기
# ### 1. 인터뷰 대상자 목록을 df형태로 'interviewee'로 불러오기
# ### 2. df에서 매치되는 정보 찾아와서, interviewee에 자동으로 넣어주기

# 엑셀파일 df로 불러오기 
interviewee_df_1 = pd.read_excel('/Users/seulalee/OneDrive/Personal_Project/HJ_인명록 자동화 코드/Period_1_2_data.xlsx', sheet_name='P1')
interviewee_df_1

interviewee_df_1.columns

interviewee_df_1.head(10)

# '이름 (한국어)' 컬럼이 비어있는 경우 '-'로 채워주기
interviewee_df_1.fillna({'이름 (한국어)':'-'}, inplace=True)
interviewee_df_1

# +
# intervieww_df['이름 (한국어)']에 있는 값을 index_df에서 포함하고 있다면, 해당 값을 가져와서 same_name에 넣은다음, 다 넣으면 
# df에 붙여넣기

for i in range(len(interviewee_df_1['이름 (한국어)'])):  # 인터뷰이 데이터프레임에 있는 행(인터뷰대상자) 갯수만큼 반복 (=각 대상자와 매치되는거 검토)
    same_name = index_df[index_df[0].str.contains(interviewee_df_1['이름 (한국어)'][i])].values.tolist()
    interviewee_df_1['matched_by_index'][i] = same_name
# -

interviewee_df_1

# interviewee_df_1을 csv와 엑셀로 저장하기
interviewee_df_1.to_csv('/Users/seulalee/OneDrive/Personal_Project/HJ_인명록 자동화 코드/200_인덱스머지완료/p1.csv')
interviewee_df_1.to_excel('/Users/seulalee/OneDrive/Personal_Project/HJ_인명록 자동화 코드/200_인덱스머지완료/p1.xlsx')

# +
# interviewee_df_2 도 interviewee_df_1과 동일하게 처리해주기

# 엑셀파일 df로 불러오기 
interviewee_df_2 = pd.read_excel('/Users/seulalee/OneDrive/Personal_Project/HJ_인명록 자동화 코드/Period_1_2_data.xlsx', sheet_name='P2')

# '이름 (한국어)' 컬럼이 비어있는 경우 '-'로 채워주기
interviewee_df_2.fillna({'이름 (한국어)':'-'}, inplace=True)

# +
# interviewee_df_2['이름 (한국어)']에 있는 값을 index_df에서 포함하고 있다면, index_df의 해당 값을 가져와서 same_name에 넣은 다음, 
# 다 넣으면 interviewee_df_2에 붙여넣기

for i in range(len(interviewee_df_2['이름 (한국어)'])):  # 인터뷰이 데이터프레임에 있는 행(인터뷰대상자) 갯수만큼 반복 (=각 대상자와 매치되는거 검토)
    same_name = index_df[index_df[0].str.contains(interviewee_df_2['이름 (한국어)'][i])].values.tolist()
    interviewee_df_2['matched_by_index'][i] = same_name
# -

# interviewee_df_1을 csv와 엑셀로 저장하기
interviewee_df_2.to_csv('/Users/seulalee/OneDrive/Personal_Project/HJ_인명록 자동화 코드/200_인덱스머지완료/p2.csv')
interviewee_df_2.to_excel('/Users/seulalee/OneDrive/Personal_Project/HJ_인명록 자동화 코드/200_인덱스머지완료/p2.xlsx')


