# 이용 후기 데이터 — 화면 표시(info.py)와 구조화 데이터(schema.py)가 공유한다.
# Review/AggregateRating 스키마는 반드시 화면에 보이는 내용과 일치해야 하므로
# 한 곳에서 데이터를 정의하고 양쪽이 같은 소스를 사용한다.
import html

# (이름, 지역, 지역링크, 테마, 테마링크, 코스, 별점, 날짜, 본문)
REVIEWS = [
    ("김○영", "상계동", "/nowon-gu/sanggye-dong/", "스웨디시", "/themes/swedish/", "90분",
     5, "2026-06-20",
     "노원역 근처 오피스텔로 밤 11시에 예약했는데 안내받은 시간에 정확히 도착하셨어요. 압도 처음에 한 번 맞춰 주시고 끝나고 바로 잘 수 있어서 다음 날 컨디션이 완전히 달랐습니다. 심야라 걱정했는데 연락도 깔끔했어요."),
    ("이○준", "중계동", "/nowon-gu/junggye-dong/", "타이마사지", "/themes/thai/", "60분",
     5, "2026-06-17",
     "은행사거리에서 학원 일 끝나고 자정에 받았습니다. 종일 앉아 있어서 굳은 어깨랑 목을 스트레칭까지 같이 풀어주셔서 개운했어요. 받고 나니 목 돌리는 게 한결 부드럽습니다. 늦은 시간인데도 친절하셨어요."),
    ("박○희", "하계동", "/nowon-gu/hagye-dong/", "커플 관리", "/themes/couple/", "90분",
     5, "2026-06-14",
     "주말 오후에 남편이랑 거실에서 같이 받았어요. 관리사 두 분이 오셔서 동시에 진행해 주셔서 시간도 안 아깝고 좋았습니다. 단지 공동현관 출입도 미리 알려드린 대로 잘 들어오셨고요. 부부가 같이 받으니 분위기가 좋네요."),
    ("정○우", "공릉동", "/nowon-gu/gongneung-dong/", "스포츠·경락", "/themes/sports/", "90분",
     4, "2026-06-11",
     "주말 러닝 후 종아리랑 햄스트링 위주로 받았습니다. 부위별로 시간 배분해 주셔서 만족스러웠어요. 다만 처음에 압이 조금 약했는데 말씀드리니 바로 맞춰 주셔서 괜찮아졌습니다. 운동하는 분들께 추천해요."),
    ("최○라", "월계동", "/nowon-gu/wolgye-dong/", "아로마테라피", "/themes/aroma/", "90분",
     5, "2026-06-08",
     "혼자 사는 원룸인데 공간 걱정했더니 매트 한 장이면 된다고 하셔서 안심하고 받았어요. 향이 은은해서 받는 내내 너무 편했고 그날 밤 오랜만에 푹 잤습니다. 자취방이라 좁아도 전혀 불편하지 않게 진행해 주셨어요."),
    ("한○수", "상계동", "/nowon-gu/sanggye-dong/", "호텔식마사지", "/themes/hotel-style/", "120분",
     5, "2026-06-05",
     "출장으로 노원 쪽 호텔에 묵었는데 체크인하고 늦게 불렀어요. 호실까지 정확히 오시고 진행도 군더더기 없이 프로페셔널했습니다. 120분이 길게 느껴지지 않을 만큼 꼼꼼했어요. 다음에 노원 올 일 있으면 또 부를게요."),
    ("서○진", "중계동", "/nowon-gu/junggye-dong/", "스웨디시", "/themes/swedish/", "60분",
     5, "2026-06-02",
     "어머니 선물로 대리 예약했습니다. 제가 결제하고 부모님은 현관만 열어드리면 된다고 해서 편했어요. 시작이랑 끝날 때 저한테 문자로 알려주셔서 멀리 있어도 안심됐습니다. 어머니가 다음에 또 받고 싶다고 하시네요."),
    ("윤○호", "하계동", "/nowon-gu/hagye-dong/", "발마사지", "/themes/foot/", "60분",
     4, "2026-05-29",
     "천변에서 운동 모임 끝나고 받았어요. 발이랑 다리가 묵직했는데 시원하게 풀렸습니다. 예약 전화도 친절했고 도착도 빨랐어요. 다음엔 전신으로 더 길게 받아보려고요."),
    ("강○은", "공릉동", "/nowon-gu/gongneung-dong/", "홈케어", "/themes/homecare/", "60분",
     5, "2026-05-25",
     "과제로 밤새고 주말에 받았습니다. 좁은 자취방이라 망설였는데 준비물 하나 없이 다 챙겨오셔서 편하게 받았어요. 압 조절도 중간중간 물어봐 주셔서 딱 맞았습니다. 학생도 부담 없이 받을 만해요."),
    ("임○선", "상계동", "/nowon-gu/sanggye-dong/", "수면 가능", "/themes/overnight/", "90분",
     5, "2026-05-21",
     "잠을 잘 못 자서 자기 전에 받아봤어요. 받다가 그대로 잠들었는데 깨우지 않고 마무리해 주셨더라고요. 결제도 미리 끝내 둬서 신경 쓸 게 없었습니다. 그날 정말 오랜만에 깊게 잤어요. 불면 있는 분들께 권합니다."),
]


def _stats():
    ratings = [r[6] for r in REVIEWS]
    count = len(ratings)
    avg = round(sum(ratings) / count, 1)
    return avg, count


RATING_VALUE, RATING_COUNT = _stats()
RATING_BEST = 5
RATING_WORST = 1


def _stars(n):
    full = "★" * n
    empty = "☆" * (RATING_BEST - n)
    return full + empty


def reviews_html():
    """후기 페이지에 노출되는 평점 요약 + 후기 카드 묶음."""
    cards = []
    for name, area, area_href, theme, theme_href, course, rating, date, text in REVIEWS:
        cards.append(
            '<li class="review-card">'
            '<div class="review-head">'
            f'<span class="review-name">{html.escape(name)}</span>'
            f'<span class="review-stars" aria-label="별점 {rating}점">{_stars(rating)}</span>'
            '</div>'
            '<div class="review-tags">'
            f'<a href="{area_href}">{area}</a>'
            f'<a href="{theme_href}">{theme}</a>'
            f'<span class="review-course">{course} 코스</span>'
            '</div>'
            f'<p class="review-text">{html.escape(text)}</p>'
            f'<time class="review-date" datetime="{date}">{date.replace("-", ". ")}</time>'
            '</li>'
        )
    summary = (
        '<div class="rating-summary" id="rating">'
        f'<div class="rating-score"><strong>{RATING_VALUE}</strong><span>/ {RATING_BEST}</span></div>'
        '<div class="rating-meta">'
        f'<span class="rating-stars" aria-hidden="true">{_stars(round(RATING_VALUE))}</span>'
        f'<span class="rating-count">실이용 후기 {RATING_COUNT}건 기준</span>'
        '</div></div>'
    )
    return (
        '<section id="recent">'
        '<h2>최근 이용 후기</h2>'
        '<p>실제 이용이 확인된 예약 건의 후기입니다. 별점이 낮은 후기도 지우지 않고 그대로 싣습니다. '
        '본인과 비슷한 지역·테마·시간대의 후기를 찾아보시면 가장 도움이 됩니다.</p>'
        + summary +
        f'<ul class="review-list">{"".join(cards)}</ul>'
        '</section>'
    )
