import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

def fetch_pdf_links(url):
    """
    从给定的 URL 中抓取所有 PDF 链接。
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"无法访问网页：{e}")
        return []

    # 解析网页内容
    soup = BeautifulSoup(response.content, 'html.parser')
    pdf_links = []

    # 查找所有 PDF 链接
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.lower().endswith('.pdf'):
            # 使用 urljoin 拼接链接
            full_link = urljoin(url, href)
            pdf_links.append(full_link)

    return pdf_links

def download_pdf(url, download_folder='downloads'):
    """
    从指定的 URL 下载 PDF 文件并保存到本地。
    """
    try:
        response = requests.get(url)
        response.raise_for_status()

        # 获取 PDF 文件名
        pdf_name = os.path.basename(url)
        pdf_path = os.path.join(download_folder, pdf_name)

        # 创建下载目录（如果不存在）
        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        # 保存 PDF 文件
        with open(pdf_path, 'wb') as f:
            f.write(response.content)

        print(f"下载成功：{pdf_path}")

    except requests.exceptions.RequestException as e:
        print(f"下载失败：{e}")

def main():
    print("欢迎使用 PDF 下载器！")
    url = input("请输入网页 URL：")
    # https://web.stanford.edu/class/cs142/lectures.html

    # 抓取 PDF 链接
    pdf_links = fetch_pdf_links(url)

    if not pdf_links:
        print("没有找到任何 PDF 链接。")
        return

    print("\n找到以下 PDF 链接：")
    for idx, link in enumerate(pdf_links, start=1):
        print(f"{idx}. {link}")

    choice = input("\n请输入要下载的 PDF 编号（用逗号分隔多个选择），或输入 'all' 下载全部： ")

    if choice.lower() == 'all':
        for link in pdf_links:
            download_pdf(link)
    else:
        indices = [int(i) - 1 for i in choice.split(',') if i.isdigit() and 0 <= int(i) - 1 < len(pdf_links)]
        for index in indices:
            download_pdf(pdf_links[index])

if __name__ == '__main__':
    main()