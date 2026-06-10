# 노원 블랙 마사지 — 노원 출장마사지·홈타이 안내 사이트

노원구 전지역 방문 관리(출장마사지·홈타이) 안내용 정적 사이트입니다.
예약전화: **0508-202-4719**

## 구조

- 정적 HTML 사이트 — 어느 호스팅(GitHub Pages, Netlify, 일반 웹서버)에서든 그대로 서빙 가능
- `build.py` + `content/` 패키지에서 페이지를 생성하는 빌드 방식
- 생성물(각 디렉터리의 `index.html`, `sitemap.xml`, `robots.txt`)도 저장소에 포함

```
build.py            # 빌드 스크립트 (레이아웃·글자수 검사·sitemap 생성)
content/
  site.py           # 상호·전화·BASE_URL·메뉴 구조
  main.py           # 메인 페이지 (+ LocalBusiness/FAQPage JSON-LD)
  areas.py          # 지역별: 노원구 허브 + 대표 동 5개
  stations.py       # 지하철역별: 허브 + 13개 역
  themes.py         # 테마별: 허브 + 14개 테마
  info.py           # 출장마사지 안내·코스·예약·가이드·후기·고객센터·약관
assets/             # CSS, 모바일 내비 JS
```

## 빌드

```bash
python3 build.py
```

빌드 시 페이지별 본문 글자수 리포트가 출력됩니다.

## SEO 운영 원칙 (빌드에 강제됨)

- 본문 **2,000자 미만 페이지는 자동 `noindex`** 처리되고 sitemap에서 제외
- 지역은 대표 동 5개만 (월계동·공릉동·하계동·중계동·상계동) — 숫자 행정동 페이지 없음
- 역은 역 1개당 페이지 1개 — 환승역도 URL 하나, 출구별 페이지 없음
- **지역+역+테마 조합 페이지 없음** (도어웨이 방지) — 테마는 독립 페이지로만 운영
- 상단/하위 메뉴와 푸터에 키워드·지역명·역명 대량 나열 없음
- 모든 페이지 본문은 페이지별 고유 작성 (지역명만 바꾼 복붙 없음)

## 배포 전 해야 할 일

1. `content/site.py`의 `BASE_URL`을 실제 도메인으로 변경
2. `python3 build.py` 재실행 (canonical·sitemap·rss·robots.txt에 반영됨)
3. HTTPS 활성화 확인

## 색인(인덱싱) 가속 절차

빌드가 자동 생성하는 것: `sitemap.xml`(lastmod·priority 포함, 50 URL),
`rss.xml`(매거진 피드), `robots.txt`(Googlebot·Yeti 명시 + 사이트맵·RSS 선언),
IndexNow 키 파일(`{키}.txt`).

1. **구글**: Search Console 등록 → `sitemap.xml` 제출 → 메인·허브 URL을
   'URL 검사 → 색인 생성 요청'으로 수동 요청 (가장 빠른 트리거)
2. **네이버**: 서치어드바이저 소유확인(메타태그 등록됨) → 사이트맵 `sitemap.xml`
   제출 + RSS `rss.xml` 제출 → '웹 페이지 수집' 요청으로 주요 URL 수동 수집
3. **IndexNow**(네이버·빙 즉시 통보): 배포 후 `python3 scripts/indexnow.py` 실행
   → 전체 URL 일괄 제출. 새 글 발행 시 `python3 scripts/indexnow.py /magazine/slug/`
4. 새 콘텐츠 발행 시: 빌드 → 배포 → IndexNow 제출 → (선택) 서치콘솔 색인 요청
