"""금융감독원 보이스피싱 체험관 게시물의 미디어 원본을 내려받는다."""

from __future__ import annotations

import argparse
import csv
import hashlib
import random
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qs, unquote, urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


BASE = "https://fss.or.kr"


@dataclass(frozen=True)
class Board:
    key: str
    name: str
    board_id: str
    menu_no: str
    pages: int

    @property
    def list_url(self) -> str:
        return f"{BASE}/fss/bbs/{self.board_id}/list.do"


BOARDS = {
    "direct": Board("direct", "바로_이_목소리", "B0000203", "200686", 13),
    "loan": Board("loan", "그놈_목소리_대출사기형", "B0000206", "200690", 19),
    "agency": Board("agency", "수사기관_사칭형", "B0000207", "200691", 23),
}


def safe_name(value: str, limit: int = 120) -> str:
    value = re.sub(r"[\\/:*?\"<>|\x00-\x1f]", "_", value)
    value = re.sub(r"\s+", " ", value).strip(" .")
    return (value[:limit].rstrip(" .") or "untitled")


def content_disposition_name(header: str | None) -> str | None:
    if not header:
        return None
    utf8 = re.search(r"filename\*=UTF-8''([^;]+)", header, re.I)
    if utf8:
        return unquote(utf8.group(1))
    plain = re.search(r'filename="?([^";]+)', header, re.I)
    return plain.group(1).strip() if plain else None


def extension_from_response(response: requests.Response, url: str) -> str:
    cd_name = content_disposition_name(response.headers.get("Content-Disposition"))
    if cd_name and Path(cd_name).suffix:
        return Path(cd_name).suffix.lower()
    url_suffix = Path(urlparse(url).path).suffix
    if url_suffix and len(url_suffix) <= 6:
        return url_suffix.lower()
    mime = response.headers.get("Content-Type", "").split(";", 1)[0].lower()
    return {
        "video/mp4": ".mp4", "audio/mpeg": ".mp3", "audio/mp4": ".m4a",
        "audio/wav": ".wav", "audio/x-wav": ".wav", "audio/ogg": ".ogg",
    }.get(mime, ".bin")


def make_session() -> requests.Session:
    retry = Retry(
        total=4, connect=4, read=4, status=4,
        backoff_factor=1.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(("GET",)),
        respect_retry_after_header=True,
    )
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (compatible; FSSVoiceArchive/1.0; personal-research)",
        "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.7",
    })
    session.mount("https://", HTTPAdapter(max_retries=retry, pool_connections=2, pool_maxsize=2))
    return session


def polite_get(session: requests.Session, url: str, params=None, *, timeout=40,
               delay=(1.2, 2.5), stream=False) -> requests.Response:
    time.sleep(random.uniform(*delay))
    response = session.get(url, params=params, timeout=timeout, stream=stream)
    response.raise_for_status()
    return response


def get_detail_links(session: requests.Session, board: Board, page: int,
                     delay: tuple[float, float]) -> list[str]:
    response = polite_get(session, board.list_url,
                          params={"menuNo": board.menu_no, "pageIndex": page}, delay=delay)
    soup = BeautifulSoup(response.text, "html.parser")
    pattern = re.compile(rf"/fss/bbs/{board.board_id}/view\.do")
    links: list[str] = []
    for anchor in soup.find_all("a", href=pattern):
        absolute = urljoin(response.url, anchor["href"])
        if absolute not in links:
            links.append(absolute)
    return links


def media_links(soup: BeautifulSoup, detail_url: str) -> list[tuple[str, str | None]]:
    found: list[tuple[str, str | None]] = []
    # 신형 게시물: 첨부파일 다운로드 링크
    for anchor in soup.select('a[href*="VodDownload"], a[href*="fileDown.do"]'):
        label = anchor.get_text(" ", strip=True) or None
        found.append((urljoin(detail_url, anchor.get("href", "")), label))
    # 구형 게시물: HTML video/audio의 src 또는 source src
    for tag in soup.select("video[src], audio[src], video source[src], audio source[src]"):
        found.append((urljoin(detail_url, tag.get("src", "")), None))
    unique: list[tuple[str, str | None]] = []
    seen: set[str] = set()
    for url, label in found:
        if url and url not in seen:
            seen.add(url)
            unique.append((url, label))
    return unique


def post_id(url: str) -> str:
    return parse_qs(urlparse(url).query).get("nttId", [hashlib.sha1(url.encode()).hexdigest()[:10]])[0]


def download_one(session: requests.Session, media_url: str, out_stem: Path,
                 label: str | None, delay: tuple[float, float]) -> tuple[Path, int, bool]:
    response = polite_get(session, media_url, timeout=120, delay=delay, stream=True)
    server_name = content_disposition_name(response.headers.get("Content-Disposition"))
    source_name = server_name or label
    suffix_match = re.search(r"\.(mp4|mp3|m4a|wav|ogg|webm)\b", source_name or "", re.I)
    suffix = f".{suffix_match.group(1).lower()}" if suffix_match else extension_from_response(response, media_url)
    target = out_stem.with_suffix(suffix.lower())
    if target.exists() and target.stat().st_size > 0:
        response.close()
        return target, target.stat().st_size, True
    temp = target.with_suffix(target.suffix + ".part")
    size = 0
    with temp.open("wb") as fp:
        for chunk in response.iter_content(1024 * 256):
            if chunk:
                fp.write(chunk)
                size += len(chunk)
    response.close()
    temp.replace(target)
    return target, size, False


def crawl_board(session: requests.Session, board: Board, output: Path,
                delay: tuple[float, float], start_page: int = 1) -> None:
    folder = output / board.name
    folder.mkdir(parents=True, exist_ok=True)
    manifest = folder / "manifest.csv"
    write_header = not manifest.exists()
    with manifest.open("a", newline="", encoding="utf-8-sig") as fp:
        writer = csv.writer(fp)
        if write_header:
            writer.writerow(["board", "page", "ntt_id", "title", "detail_url", "media_url", "file", "bytes", "status"])
        for page in range(start_page, board.pages + 1):
            links = get_detail_links(session, board, page, delay)
            print(f"[{board.name}] {page}/{board.pages}페이지: {len(links)}건")
            for detail_url in links:
                try:
                    detail = polite_get(session, detail_url, delay=delay)
                    soup = BeautifulSoup(detail.text, "html.parser")
                    title_tag = soup.select_one(".bd-view .subject, .bd-view h2.subject, h2.subject")
                    title = title_tag.get_text(" ", strip=True) if title_tag else post_id(detail_url)
                    media = media_links(soup, detail_url)
                    if not media:
                        writer.writerow([board.name, page, post_id(detail_url), title, detail_url, "", "", 0, "NO_MEDIA"])
                        fp.flush()
                        print(f"  ! 미디어 없음: {post_id(detail_url)} {title}")
                        continue
                    for index, (media_url, label) in enumerate(media, 1):
                        stem = folder / safe_name(f"{post_id(detail_url)}_{title}" + (f"_{index}" if len(media) > 1 else ""))
                        path, size, skipped = download_one(session, media_url, stem, label, delay)
                        status = "SKIPPED" if skipped else "DOWNLOADED"
                        writer.writerow([board.name, page, post_id(detail_url), title, detail_url, media_url, path.name, size, status])
                        fp.flush()
                        print(f"  {status}: {path.name} ({size:,} bytes)")
                except (requests.RequestException, OSError) as exc:
                    writer.writerow([board.name, page, post_id(detail_url), "", detail_url, "", "", 0, f"ERROR: {exc}"])
                    fp.flush()
                    print(f"  ! 오류({post_id(detail_url)}): {exc}", file=sys.stderr)


def main() -> int:
    parser = argparse.ArgumentParser(description="금감원 보이스피싱 체험관 미디어 다운로드")
    parser.add_argument("--boards", nargs="+", choices=["all", *BOARDS], default=["all"], help="받을 탭")
    parser.add_argument("--output", type=Path, default=Path("fss_voice_files"), help="저장 폴더")
    parser.add_argument("--min-delay", type=float, default=1.2, help="요청 전 최소 대기(초)")
    parser.add_argument("--max-delay", type=float, default=2.5, help="요청 전 최대 대기(초)")
    parser.add_argument("--start-page", type=int, default=1, help="재개할 시작 페이지")
    args = parser.parse_args()
    if args.min_delay < 0 or args.max_delay < args.min_delay or args.start_page < 1:
        parser.error("지연 시간과 시작 페이지 값을 확인하세요.")
    selected = list(BOARDS.values()) if "all" in args.boards else [BOARDS[key] for key in args.boards]
    session = make_session()
    for board in selected:
        crawl_board(session, board, args.output, (args.min_delay, args.max_delay), args.start_page)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
