import csv
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests

# 取得開始ページと対象ドメインの設定
START_URL = "https://www.musashino-u.ac.jp/"
TARGET_DOMAIN = urlparse(START_URL).netloc

# サーバーブロック回避用のユーザーエージェント設定
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

# データの格納用
sitemap_dict = {}  # { URL: "<title>文字列" }
visited_urls = set()  # 重複訪問防止用


def crawl_site_with_limit(start_url, max_pages=30):
    """同一ドメイン内を巡回し、指定上限数までURLと<title>を辞書に格納する関数"""
    urls_to_visit = [start_url]

    try:
        while urls_to_visit and len(sitemap_dict) < max_pages:
            current_url = urls_to_visit.pop(0).split("#")[0]

            if current_url in visited_urls:
                continue

            visited_urls.add(current_url)

            try:
                # サーバー負荷軽減のための待機（必須）[cite: 1, 2]
                time.sleep(1)

                response = requests.get(
                    current_url, headers=headers, timeout=10
                )

                # HTML以外のコンテンツ（PDFや画像など）はスキップ
                content_type = response.headers.get("Content-Type", "")
                if "text/html" not in content_type:
                    continue

                response.encoding = response.apparent_encoding
                soup = BeautifulSoup(response.text, "html.parser")

                # <title>タグの取得
                title_tag = soup.find("title")
                page_title = (
                    title_tag.get_text(strip=True)
                    if title_tag
                    else "タイトルなし"
                )

                # 辞書型変数に格納 { URL: <title>の内容 }
                sitemap_dict[current_url] = page_title
                print(
                    f"[{len(sitemap_dict)}/{max_pages}] 取得完了: {page_title} -> {current_url}"
                )

                # ページ内のリンク（aタグ）を収集して次の巡回候補に追加
                for link in soup.find_all("a", href=True):
                    next_url = urljoin(current_url, link["href"]).split("#")[0]
                    parsed_next = urlparse(next_url)

                    # 同一ドメインかつ未訪問のWebページのみ対象
                    if (
                        parsed_next.netloc == TARGET_DOMAIN
                        and parsed_next.scheme in ["http", "https"]
                        and next_url not in visited_urls
                    ):
                        urls_to_visit.append(next_url)

            except requests.exceptions.RequestException as e:
                print(f"アクセスエラー ({current_url}): {e}")

    except KeyboardInterrupt:
        print("\n【手動中断】ここまでに取得したデータでCSVを作成します。")


def save_to_csv(filename="sitemap.csv"):
    """辞書データをCSVファイルに書き出す関数"""
    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        # ヘッダー行を出力
        writer.writerow(["URL", "Title"])

        # 辞書の中身を1行ずつ書き込み
        for page_url, title in sitemap_dict.items():
            writer.writerow([page_url, title])

    print(f"\nCSVファイルを保存しました: {filename}")


if __name__ == "__main__":
    # 上限件数（例: 30件）を指定して実行
    MAX_PAGES = 30

    print(
        f"クローリングを開始します...（最大 {MAX_PAGES} 件取得 / 中止する場合は Ctrl+C）"
    )
    crawl_site_with_limit(START_URL, max_pages=MAX_PAGES)

    print(
        f"\n--- 取得結果 ({len(sitemap_dict)} 件のデータを辞書に格納しました) ---"
    )

    # CSVファイルへの書き出し実行
    save_to_csv("sitemap.csv")