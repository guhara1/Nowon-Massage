#!/usr/bin/env python3
"""IndexNow 일괄 제출 스크립트 — 네이버·빙 즉시 색인 요청.

사용법 (배포 후 실행):
    python3 scripts/indexnow.py            # sitemap의 전체 URL 제출
    python3 scripts/indexnow.py /magazine/new-post/   # 특정 URL만 제출

동작:
  - api.indexnow.org 에 JSON POST → 참여 엔진(네이버 Yeti, Bing 등)에 동시 전파
  - 구글은 IndexNow 미참여이므로 Search Console의 sitemap 제출을 함께 사용할 것
  - 키 파일({KEY}.txt)은 빌드 시 사이트 루트에 자동 생성되어 있어야 한다
"""
import json
import re
import sys
import urllib.request

sys.path.insert(0, ".")
from content.site import BASE_URL, INDEXNOW_KEY

API = "https://api.indexnow.org/indexnow"


def sitemap_urls():
    with open("sitemap.xml", encoding="utf-8") as f:
        return re.findall(r"<loc>(.*?)</loc>", f.read())


def submit(urls):
    host = BASE_URL.rstrip("/").split("://", 1)[1]
    payload = {
        "host": host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL.rstrip('/')}/{INDEXNOW_KEY}.txt",
        "urlList": urls,
    }
    req = urllib.request.Request(
        API,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        print(f"IndexNow 응답: HTTP {res.status} — {len(urls)}개 URL 제출 완료")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        base = BASE_URL.rstrip("/")
        urls = [u if u.startswith("http") else base + u for u in sys.argv[1:]]
    else:
        urls = sitemap_urls()
    if "example.com" in BASE_URL:
        sys.exit("BASE_URL이 아직 플레이스홀더입니다. content/site.py에서 실제 도메인으로 변경 후 빌드·배포하고 실행하세요.")
    submit(urls)
