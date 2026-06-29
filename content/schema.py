# 구조화 데이터(JSON-LD) 중앙 생성 — build.py가 모든 페이지에 자동 주입한다.
#
# 페이지별 자동 적용:
#   - 모든 페이지: BreadcrumbList (breadcrumb가 있을 때)
#   - FAQ 섹션(div.faq-item)이 있는 페이지: FAQPage 자동 추출
#   - 메인: HealthAndBeautyBusiness(LocalBusiness) + WebSite
#   - 후기 페이지: 같은 사업체(@id)에 AggregateRating + Review 연결
#   - 테마 상세: Service
#   - 코스/요금: OfferCatalog(가격)
# 화면에 보이는 내용과 일치하는 데이터만 마크업한다.
import html
import json
import re

from .site import BASE_URL, BRAND, PHONE
from .pricing import PRICING  # noqa: F401  (가격 일관성 참고용)
from .reviews_data import REVIEWS, RATING_VALUE, RATING_COUNT, RATING_BEST, RATING_WORST

BASE = BASE_URL.rstrip("/")
BUSINESS_ID = f"{BASE}/#business"
WEBSITE_ID = f"{BASE}/#website"
ORG_ID = f"{BASE}/#org"


def _script(obj):
    return (
        '<script type="application/ld+json">\n'
        + json.dumps(obj, ensure_ascii=False, indent=2)
        + "\n</script>\n"
    )


def _org_node():
    return {
        "@type": "Organization",
        "@id": ORG_ID,
        "name": BRAND,
        "url": f"{BASE}/",
        "logo": {"@type": "ImageObject", "url": f"{BASE}/assets/icon-512.png"},
        "image": f"{BASE}/assets/og-image.png",
        "telephone": PHONE,
        "areaServed": {"@type": "AdministrativeArea", "name": "서울특별시 노원구"},
    }


def _business_node(with_rating=False):
    node = {
        "@type": "HealthAndBeautyBusiness",
        "@id": BUSINESS_ID,
        "name": BRAND,
        "url": f"{BASE}/",
        "image": f"{BASE}/assets/og-image.png",
        "logo": f"{BASE}/assets/icon-512.png",
        "telephone": PHONE,
        "description": "노원구 전지역 방문 출장마사지·홈타이 예약 안내. 월계동·공릉동·하계동·중계동·상계동과 주요 역세권 방문 관리.",
        "priceRange": "₩90,000 - ₩180,000",
        "currenciesAccepted": "KRW",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "노원구",
            "addressRegion": "서울특별시",
            "addressCountry": "KR",
        },
        "areaServed": [
            {"@type": "AdministrativeArea", "name": "서울특별시 노원구"},
            {"@type": "City", "name": "월계동"},
            {"@type": "City", "name": "공릉동"},
            {"@type": "City", "name": "하계동"},
            {"@type": "City", "name": "중계동"},
            {"@type": "City", "name": "상계동"},
        ],
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "opens": "00:00",
            "closes": "23:59",
        }],
        "makesOffer": _offer_list(),
    }
    if with_rating:
        node["aggregateRating"] = _aggregate_rating_node()
        node["review"] = _review_nodes()
    return node


def _offer_list():
    courses = [
        ("60분 코스", "90000", "기본 컨디션·릴랙스 케어"),
        ("90분 코스", "150000", "아로마 포함 추천 구성"),
        ("120분 코스", "180000", "전신 집중 프리미엄 케어"),
    ]
    offers = []
    for name, price, desc in courses:
        offers.append({
            "@type": "Offer",
            "name": name,
            "description": desc,
            "priceCurrency": "KRW",
            "price": price,
            "url": f"{BASE}/courses/#price",
            "availability": "https://schema.org/InStock",
        })
    return offers


def _aggregate_rating_node():
    return {
        "@type": "AggregateRating",
        "ratingValue": str(RATING_VALUE),
        "reviewCount": str(RATING_COUNT),
        "bestRating": str(RATING_BEST),
        "worstRating": str(RATING_WORST),
    }


def _review_nodes():
    nodes = []
    for name, area, _ah, theme, _th, course, rating, date, text in REVIEWS:
        nodes.append({
            "@type": "Review",
            "datePublished": date,
            "author": {"@type": "Person", "name": name},
            "reviewRating": {
                "@type": "Rating",
                "ratingValue": str(rating),
                "bestRating": str(RATING_BEST),
                "worstRating": str(RATING_WORST),
            },
            "reviewBody": text,
            "itemReviewed": {"@id": BUSINESS_ID},
        })
    return nodes


def _breadcrumb_node(crumbs, path):
    # crumbs: [(label, href or None), ...] — render_page와 동일한 입력
    items = [{
        "@type": "ListItem",
        "position": 1,
        "name": "홈",
        "item": f"{BASE}/",
    }]
    pos = 2
    for label, href in crumbs:
        entry = {"@type": "ListItem", "position": pos, "name": label}
        if href:
            entry["item"] = BASE + href
        else:
            entry["item"] = f"{BASE}/{path}".rstrip("/") + "/"
        items.append(entry)
        pos += 1
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }


_FAQ_RE = re.compile(
    r'<div class="faq-item">\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>\s*</div>',
    re.S,
)


def _strip_tags(s):
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(re.sub(r"\s+", " ", s)).strip()


def _faq_node(body):
    pairs = _FAQ_RE.findall(body)
    if len(pairs) < 2:
        return None
    main_entity = []
    for q, a in pairs:
        main_entity.append({
            "@type": "Question",
            "name": _strip_tags(q),
            "acceptedAnswer": {"@type": "Answer", "text": _strip_tags(a)},
        })
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": main_entity,
    }


def _website_node():
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": WEBSITE_ID,
        "url": f"{BASE}/",
        "name": BRAND,
        "inLanguage": "ko-KR",
        "publisher": {"@id": BUSINESS_ID},
    }


def _service_node(path, name, desc, canonical):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "serviceType": name,
        "name": f"{name} 출장 방문 관리",
        "description": desc,
        "url": canonical,
        "areaServed": {"@type": "AdministrativeArea", "name": "서울특별시 노원구"},
        "provider": {"@id": BUSINESS_ID},
        "offers": {
            "@type": "Offer",
            "priceCurrency": "KRW",
            "price": "90000",
            "priceSpecification": {
                "@type": "PriceSpecification",
                "minPrice": "90000",
                "maxPrice": "180000",
                "priceCurrency": "KRW",
            },
            "availability": "https://schema.org/InStock",
        },
    }


def build_structured_data(page, body):
    """페이지 dict와 본문 HTML을 받아 JSON-LD <script> 묶음을 반환한다."""
    path = page.get("path", "")
    crumbs = page.get("breadcrumb") or []
    canonical = f"{BASE}/{path}"
    blocks = []

    # 1) 사업체 + 웹사이트 — 메인 페이지
    if path == "":
        graph = {
            "@context": "https://schema.org",
            "@graph": [_business_node(with_rating=False), _org_node()],
        }
        blocks.append(_script(graph))
        blocks.append(_script(_website_node()))

    # 2) 후기 페이지 — 같은 사업체에 평점·후기 연결 (화면 노출 후기와 일치)
    if path == "reviews/":
        graph = {
            "@context": "https://schema.org",
            "@graph": [_business_node(with_rating=True)],
        }
        blocks.append(_script(graph))

    # 3) 테마 상세 — Service
    if path.startswith("themes/") and path != "themes/":
        name = page.get("h1", "").replace(" 안내", "").strip()
        blocks.append(_script(_service_node(path, name, page.get("desc", ""), canonical)))

    # 4) BreadcrumbList — breadcrumb가 있는 모든 페이지
    if crumbs:
        blocks.append(_script(_breadcrumb_node(crumbs, path)))

    # 5) FAQPage — FAQ 섹션이 있는 모든 페이지에서 자동 추출
    faq = _faq_node(body)
    if faq:
        blocks.append(_script(faq))

    return "".join(blocks)
