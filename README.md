## 용도
주소와 위/경도 매핑처럼 외부 API 또는 CSV 파일을 이용해 직접 대용량 데이터를 가공해야하는 경우 사용하는 코드의 집합입니다.

### StationGeoMapper.py
지하철역의 지번주소, 도로명주소, 이미 매핑된 json 파일을 위도, 경도로 매핑시켜주는 코드입니다.

**폴더 구조**
> 실제 폴더 구조는 아래와 같습니다.
```
/
|   .gitignore
|   README.md
|   requirements.txt
|   StationGeoMapper.py
|
+---results
|       fail.json
|       success.json
|
\---static
    |   station_coordinate.json
    |
    \---지하철역
            국가철도공단_분당선_주소데이터_20221122.csv
            국가철도공단_수도권1호선_주소데이터_20221122.csv
            ... 생략
            국가철도공단_수도권9호선_주소데이터_20221122.csv
```