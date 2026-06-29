# 내부링크 강화 컴포넌트 — 롱테일 주제 링크 카드 묶음.
# 본문 맥락과 연결되는 구체적(롱테일) 앵커 텍스트로 페이지 간 이동을 강화한다.
# 메뉴·푸터의 키워드 나열과 달리, 본문 안에서 다음 행동을 제안하는 역할이다.


def related_block(items, title="이어서 보면 좋은 안내"):
    """items: [(앵커(롱테일), 한 줄 설명, href), ...]"""
    lis = "".join(
        f'<li><a href="{href}">'
        f'<span class="rel-label">{label}</span>'
        f'<span class="rel-sub">{sub}</span>'
        "</a></li>"
        for label, sub, href in items
    )
    return (
        f'<section class="related" aria-label="{title}">'
        f"<h2>{title}</h2>"
        f'<ul class="related-grid">{lis}</ul>'
        "</section>"
    )
