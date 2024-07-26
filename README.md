# gkisplus-data
Regularly auto-updated cloud data for the GKI Salatiga Plus app

## Actors

- **GITHUB_ACTIONS**: Updated automatically by GitHub's `cron`-scheduled actions
- **MANUAL_INTERVENTION**: Updated manually by hand
- **SIMON_PETRUS**: Updated programmatically using the Simon Petrus administrator dashboard app

## Update interval (in UTC+7)

- **English Service**: at 6 AM and 6 PM on day 1-7 of the month
- **Kebaktian Umum (Regular Indonesian Service)**: every Saturday at 12 PM and 6 PM; every Sunday at 12 AM, 3 AM, and 6 AM
- **SaRen Pagi (Morning Devotion)**: every Monday-Saturday, every 30 minutes from 3 AM to 7 AM
- **Tata Ibadah (Service Liturgy)**: every Saturday at 3 PM, 6 PM, and 9 PM; every Sunday at 12 AM and 3 AM
- **Warta Jemaat (Church News)**: every Saturday at 3 PM, 6 PM, and 9 PM; every Sunday at 12 AM and 3 AM

## Non-Exhaustive Documentation

### `static`: Folder convention

- `banner.webp` must exist. This image will be displayed as the church profile's appealing banner image.
- `index.html` must exist and become the starting point of ScreenInternalHTML's loading.
- `title.txt` must exist. This file determines the church profile title string. Must be one-line only.
- All other CSS, JavaScript, and media should be stored under the profile's `res` folder.

### JSON: `data/carousel`: Carousel types

- **article**: the carousel is of online article type; upon click, opens ScreenWebView and displays the link
- **poster**: the carousel is of poster type; upon click, displays a zoomable poster pop-up
- **yt**: the carousel is of video type; upon click, opens ScreenVideo/ScreenVideoLive and loads the embedded YouTube video

## To-Do

- [ ] Remove `carousel/` (unused since migration to v2)
- [ ] Remove `gkisplus-carousel.zip` (unused since migration to v2)
- [ ] Remove `gkisplus-static.zip` (unused since migration to v2)
- [ ] Remove `static/` (unused since migration to v2)
- [ ] Remove `test/` (unused since migration to v2)
