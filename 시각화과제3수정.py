import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium  # streamlit_folium을 사용해야 합니다
import streamlit as st

# Streamlit 앱 제목 설정
st.title("출산율 시각화 - 대한민국")
st.text("C119180-김새난")  # 제목 위에 작은 텍스트 표시

# GeoDataFrame 로드
gdf = gpd.read_file("C:/Users/김새난/data/BND_SIGUNGU_PG.json")

# 출생률 데이터 로드
df = pd.read_csv(
    "C:/Users/김새난/Downloads/연령별_출산율_및_합계출산율_행정구역별__20241119164143.csv",
    encoding='cp949',
    low_memory=False,
    header=1
)
df.columns = ["시군구별", "합계출산율"]

# 이름 매핑 테이블
name_mapping = {
    # 수원시
    '수원시 영통구': '영통구',
    '수원시 장안구': '장안구',
    '수원시 권선구': '권선구',
    '수원시 팔달구': '팔달구',
    # 성남시
    '성남시 수정구': '수정구',
    '성남시 중원구': '중원구',
    '성남시 분당구': '분당구',
    # 용인시
    '용인시 처인구': '처인구',
    '용인시 기흥구': '기흥구',
    '용인시 수지구': '수지구',
    # 고양시
    '고양시 덕양구': '덕양구',
    '고양시 일산동구': '일산동구',
    '고양시 일산서구': '일산서구',
    # 안산시
    '안산시 단원구': '단원구',
    '안산시 상록구': '상록구',
    # 안양시
    '안양시 동안구': '동안구',
    '안양시 만안구': '만안구',
    # 천안시
    '천안시 서북구': '서북구',
    '천안시 동남구': '동남구',
    # 청주시
    '청주시 상당구': '상당구',
    '청주시 서원구': '서원구',
    '청주시 흥덕구': '흥덕구',
    '청주시 청원구': '청원구',
    # 창원시
    '창원시 의창구': '의창구',
    '창원시 성산구': '성산구',
    '창원시 마산합포구': '마산합포구',
    '창원시 마산회원구': '마산회원구',
    '창원시 진해구': '진해구',
    # 전주시
    '전주시 완산구': '완산구',
    '전주시 덕진구': '덕진구',
    # 포항시
    '포항시 남구': '포항-남구',
    '포항시 북구': '포항-북구',
    # 광주광역시
    '광주광역시': ['동구', '서구', '남구', '북구'],
    # 울산광역시
    '울산광역시': ['남구', '중구', '동구', '북구'],
    # 대구광역시
    '대구광역시': ['중구', '동구', '서구', '남구', '북구'],
    # 대전광역시
    '대전광역시': ['중구', '동구', '서구'],
    # 인천광역시
    '인천광역시': ['중구', '동구', '서구', '남동구', '부평구', '계양구', '연수구']
}

# 이름 매핑 적용
gdf['SIGUNGU_NM'] = gdf['SIGUNGU_NM'].replace(name_mapping)

# 병합 수행
merged_gdf = gdf.merge(df, left_on='SIGUNGU_NM', right_on='시군구별', how='left')

# 'SIGUNGU_NM' 열 이름을 '행정구역'으로 변경
merged_gdf.rename(columns={'SIGUNGU_NM': '행정구역'}, inplace=True)

# Choropleth 지도 생성
map_center = [36.5, 127.8]  # 대한민국 중심
m = folium.Map(location=map_center, zoom_start=7)

folium.Choropleth(
    geo_data=gdf.to_json(),
    data=merged_gdf,
    columns=['행정구역', '합계출산율'],
    key_on='feature.properties.SIGUNGU_NM',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='출산율 (합계)'
).add_to(m)

# Streamlit에서 Folium 지도 출력
st.write("### 대한민국 출산율 Choropleth 지도")
st_folium(m, width=700, height=500)

# 상위/하위 지역 출력
top_3 = merged_gdf.nlargest(3, '합계출산율')
bottom_3 = merged_gdf.nsmallest(3, '합계출산율')

st.write("### 출산율 상위 3개 지역")
st.dataframe(top_3[['행정구역', '합계출산율']])
st.write("합계출산율이 높은 지역들은 대부분 전부 수도권 외의 지역이다. 모두 특별시, 특별자치시, 광역시에 해당하지 않으며 대부분 농촌지역이거나 인구밀도가 낮은 지역이다.")
st.write("2023년 기준으로 전라남도가 합계출산율에서 전국 1위를 기록한 지역이다. (실제기사도 있음)")

st.write("### 출산율 하위 3개 지역")
st.dataframe(bottom_3[['행정구역', '합계출산율']])
st.write("합계출산율이 낮은 지역들은 부산광역시의 중구, 대구광역시의 서구를 제외하면 거의 모두 서울특별시의 지역이다.")
st.write("합계출산율이 낮은 지역은 주로 인구 밀도가 높은 도시 지역이나, 인프라가 부족한 지역일 수 있습니다.")
