## # 콘솔 게임 시장 판매량 분석 (Team Project)

#### ■ Background

- 콘솔게임에 대한 수요 예측 및 마케팅 전략 수립
- 콘솔 게임 경쟁력을 제고하기 위해 콘솔 게임의 여러 변인과 지역별 판매량을 바탕으로 데이터 분석을
  실시

#### ■ Tools

- Python, R, Keras

#### ■ Summary

##### (1) Data Collection

- Kaggle - Video Game Sales with Ratings

##### (2) Data Processing

- 최근 유행하고 있으며 꾸준히 성장하고 있는 플랫폼에 대해서 분석해야 미래 수요 예측에 유용하다고 판단
  ->최신 플랫폼 군인 8세대 게임기(PS4/ PSV/ Wii U/ 3DS/ XBOX ONE)로 선정
- 또한 한 시장(지역) 내에서만 판매를 한 게임들의 경우, 수익이나 흥행을 목적으로 하지 않았거나 고객을 너무 한정적으로 다루기에 전 세계적으로 발매된 게임들과 비교할 수 없다고 판단 
  -> 분석에서 제외
- 본래 데이터 변수들(연령 제한, 플랫폼, 퍼블리셔, 장르, 각 지역별 판매량)만으로는 예측 및 판매전략을 수립하기에는 설명력이 부족하다 판단
  -> 위키백과, Metacritic, Gry-online 등의 사이트에서 검색을 통해 얻은 Critic Score, User Score, Series, Multiplay의 정보들을 새 attribute로 추가

##### (3) Model & Algorithms

- 회귀분석 - Random Forest Regression
  - Numerical Data와 Categorical Data 두 가지 형태의 데이터를 모두 처리 가능
  - Random Forest는 변수의 중요도를 알 수 있기 때문에 판매량에 영향을 미치는 요인을 파악하기에 적합
- 군집분석 - PAM 알고리즘 (k-mediods), t-SNE 알고리즘(시각화)
  - Mixed type Data를 Clustering 하기 위해 Gower Distance 이용
  - Silhouette 계수를 이용하여 k 결정
- 인공신경망 - Keras
  - 인공신경망을 통해 판매량 예측

##### (4) Report

- 사전 예상대로 일본 콘솔 시장은 갈라파고스화 성향을 보임, 일본 시장을 제외한 나머지는 대체로 비슷한 성향을 보임
- 시장별 선호 장르와 판매량에 영향을 미치는 요소를 통해 시장별 판매 전략을 차별화 할 수 있을 것으로 기대

##### (5) Review

- 인공신경망에 대해 깊게 이해하지 못했던 때 모델을 제작, 데이터 row 값에 비해 규모가 매우 커서 과적합 발생 -> 다양한 규제 기법 적용 필요
- 클러스터링에 활용한 변수에서 판매량을 제외하는 것이 더 좋은 결과를 보였을 수도 있었을 것 같음
- Data Processing 과정에서 추가 Attribute 수집 과정에 crawling을 활용했다면 좋았을 것
