const STORAGE_KEY = "promo_banner_last_shown";  // { [id]: timestamp }
const SHOW_INTERVAL_MS = 24 * 60 * 60 * 1000;   // 24 часа

function shouldBannerShow() {
    if (!window.localStorage)
        return true;

    var lastShownJson = localStorage.getItem(STORAGE_KEY);
    if (!lastShownJson)
        return true;

    let lastShown = JSON.parse(lastShownJson);

    const diff = Date.now() - lastShown;
    return diff >= SHOW_INTERVAL_MS;
}

function markBannerShown() {
    if (!window.localStorage)
        return;

    var lastShown = Date.now();
    localStorage.setItem(STORAGE_KEY, JSON.stringify(lastShown));
}

const bannerHtml = document.querySelector("#promo-banner");
const bannerCloseBtn = bannerHtml.querySelector(".promo-banner__close-btn");

bannerCloseBtn.addEventListener("click", closeBanner);

function closeBanner() {
    bannerHtml.style.display = "none";
    document.body.classList.remove('no-scroll');
}

function renderBanner(banner) {
    if (!!banner.link) {
        const bannerLink = bannerHtml.querySelector(".promo-banner__link");
        bannerLink.href = banner.link;
    }

    const bannerImage = bannerHtml.querySelector(".promo-banner__image");
    bannerImage.src = banner.imageUrl;

    bannerHtml.style.display = "flex";
    document.body.classList.add('no-scroll');
}

window.onload = function () {

    setTimeout(() => {
        fetch("/get-promo-banner", {
            method: "GET",
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(x => x.json()
            .then(x => {
                if (!x.banner) {
                    return;
                }

                if (!shouldBannerShow()) {
                    return;
                }

                renderBanner(x.banner);
                markBannerShown();
            }))
    }, 1000)


}