// 모바일 내비게이션 토글
(function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".main-nav");
  if (!toggle || !nav) return;

  toggle.addEventListener("click", function () {
    var open = nav.classList.toggle("open");
    toggle.classList.toggle("open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  });

  // 모바일에서 1차 메뉴 탭 시 하위 메뉴 펼침
  nav.querySelectorAll(".nav-item.has-sub > a").forEach(function (link) {
    link.addEventListener("click", function (e) {
      if (window.innerWidth > 920) return;
      var item = link.parentElement;
      if (!item.classList.contains("sub-open")) {
        e.preventDefault();
        nav.querySelectorAll(".sub-open").forEach(function (el) {
          el.classList.remove("sub-open");
        });
        item.classList.add("sub-open");
      }
    });
  });
})();
