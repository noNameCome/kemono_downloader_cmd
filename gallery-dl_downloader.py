import os
import sys
import subprocess
import random
import time
import shutil
import zipfile
import re
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urlparse

# hanime1_downloader에서 함수 가져오기
from hanime1_downloader import is_hanime, download_hanime_with_progress
# ytdlp_downloader에서 함수 가져오기
from ytdlp_downloader import is_youtube, download_youtube_with_progress, get_youtube_format_choice

def print_header():
    print("=" * 50)
    print("===== Gallery-dl 다운로더 =====")
    print("=" * 50)
    print()

def check_file(filename):
    print(f"[확인] {filename} 파일 검사 중...")
    if not os.path.exists(filename):
        print()
        print(f"[오류] {filename} 파일을 찾을 수 없습니다")
        print(f"현재 경로: {os.getcwd()}")
        print()
        input("계속하려면 Enter를 누르세요...")
        return False
    print(f"[완료] {filename} 발견")
    print()
    return True

def is_kemono_url(url):
    """Kemono/Coomer URL 감지"""
    try:
        # URL 정규화
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'https://' + url
        
        netloc = urlparse(url).netloc.lower()
        # kemono.su, coomer.su 등 정확한 도메인 매칭
        return "kemono" in netloc or "coomer" in netloc
    except:
        return False

def is_arcalive_url(url):
    """Arca.live URL 감지"""
    try:
        # URL 정규화
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'https://' + url
        
        netloc = urlparse(url).netloc.lower()
        # arca.live 도메인 매칭
        return "arca.live" in netloc
    except:
        return False

def is_hitomi_url(url):
    """Hitomi.la URL 감지"""
    try:
        # URL 정규화
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'https://' + url
        
        netloc = urlparse(url).netloc.lower()
        # hitomi.la 도메인 매칭
        return "hitomi.la" in netloc or netloc == "hitomi.la" or netloc == "www.hitomi.la"
    except:
        return False

def is_twitter_url(url):
    """X(트위터) URL 감지"""
    try:
        # URL 정규화
        if not (url.startswith('http://') or url.startswith('https://')):
            url = 'https://' + url
        
        netloc = urlparse(url).netloc.lower()
        # 정확한 도메인 매칭 (xxx.com처럼 x.com이 포함된 다른 도메인과 구분)
        return netloc == "x.com" or netloc == "www.x.com" or netloc == "twitter.com" or netloc == "www.twitter.com"
    except:
        return False


def get_arcalive_title(url):
    """Arca.live 게시글 제목 가져오기"""
    try:
        # User-Agent 헤더 추가
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
            # <title> 태그에서 제목 추출
            title_match = re.search(r'<title>([^<]+)</title>', html, re.IGNORECASE)
            if title_match:
                title = title_match.group(1).strip()
                # "- 아카라이브" 같은 접미사 제거
                title = re.sub(r'\s*[-|]\s*아카.*$', '', title)
                title = re.sub(r'\s*[-|]\s*arca\.live.*$', '', title, flags=re.IGNORECASE)
                # 파일명으로 사용할 수 없는 문자 제거
                title = re.sub(r'[\\/:*?"<>|]', '', title)
                return title.strip()
    except Exception as e:
        print(f"[경고] 제목 추출 실패: {e}")
    
    return None

def download_general(url):
    """일반 gallery-dl URL 다운로드 (gallery-dl 기본 경로 사용)"""
    print(f"[실행] gallery-dl 시작...")
    
    try:
        # 스크립트 디렉토리에서 gallery-dl.exe 찾기
        script_dir = os.path.dirname(os.path.abspath(__file__))
        gallery_dl_path = os.path.join(script_dir, "gallery-dl.exe")
        
        # gallery-dl.exe가 없으면 시스템 경로에서 찾기
        if not os.path.exists(gallery_dl_path):
            gallery_dl_path = "gallery-dl"
        
        # gallery-dl 기본 경로에 다운로드
        subprocess.run([
            gallery_dl_path,
            url
        ])
        
        print(f"[완료] 다운로드 완료")
    except Exception as e:
        print(f"[오류] {e}")

def download_hitomi(url, folder_list):
    temp_folder = f"temp_download_{random.randint(10000, 99999)}"
    print(f"[실행] gallery-dl 시작 (hitomi)...")
    
    try:
        # 스크립트 디렉토리에서 gallery-dl.exe 찾기
        script_dir = os.path.dirname(os.path.abspath(__file__))
        gallery_dl_path = os.path.join(script_dir, "gallery-dl.exe")
        
        # gallery-dl.exe가 없으면 시스템 경로에서 찾기
        if not os.path.exists(gallery_dl_path):
            gallery_dl_path = "gallery-dl"
        
        subprocess.run([
            gallery_dl_path,
            "-d", temp_folder,
            "-f", "{num}.{extension}",
            url
        ])
        
        if os.path.exists(temp_folder):
            if not os.path.exists("hitomi"):
                os.makedirs("hitomi")
            
            for folder_name in os.listdir(temp_folder):
                source_path = os.path.join(temp_folder, folder_name)
                if os.path.isdir(source_path):
                    dest_path = os.path.join("hitomi", folder_name)
                    print(f"[이동] {folder_name} 폴더 이동 중...")
                    
                    if os.path.exists(dest_path):
                        shutil.rmtree(dest_path)
                    shutil.move(source_path, dest_path)
                    
                    folder_list.append(dest_path)
                    print(f"[완료] 이동 완료")
            
            if os.path.exists(temp_folder):
                shutil.rmtree(temp_folder)
        else:
            print("[경고] 다운로드된 폴더를 찾을 수 없습니다")
    except Exception as e:
        print(f"[오류] {e}")

def download_arcalive(url, folder_list):
    """Arca.live 다운로드 (채널명/ID 구조로 폴더 생성)"""
    print(f"[실행] gallery-dl 시작 (arca.live)...")
    
    try:
        # URL에서 채널명과 게시글 ID 추출
        # 예: https://arca.live/b/bluearchive/154741989
        match = re.search(r'/b/([^/]+)/(\d+)', url)
        if match:
            channel_name = match.group(1)
            post_id = match.group(2)
        else:
            channel_name = "unknown"
            post_id = f"post_{random.randint(10000, 99999)}"
        
        print(f"[정보] 채널: {channel_name}, 게시글 ID: {post_id}")
        
        # 임시 폴더에 다운로드
        temp_folder = f"temp_arcalive_{post_id}"
        
        # 스크립트 디렉토리에서 gallery-dl.exe 찾기
        script_dir = os.path.dirname(os.path.abspath(__file__))
        gallery_dl_path = os.path.join(script_dir, "gallery-dl.exe")
        
        # gallery-dl.exe가 없으면 시스템 경로에서 찾기
        if not os.path.exists(gallery_dl_path):
            gallery_dl_path = "gallery-dl"
        
        # gallery-dl로 임시 폴더에 다운로드
        subprocess.run([
            gallery_dl_path,
            "-D", temp_folder,
            "-f", "{num}.{extension}",
            url
        ])
        
        # arcalive/채널명 폴더 생성
        channel_path = os.path.join("arcalive", channel_name)
        if not os.path.exists(channel_path):
            os.makedirs(channel_path)
        
        # 임시 폴더가 존재하면 arcalive/채널명/ID로 이동
        if os.path.exists(temp_folder):
            dest_path = os.path.join(channel_path, post_id)
            
            # 이미 존재하면 삭제
            if os.path.exists(dest_path):
                shutil.rmtree(dest_path)
            
            # 임시 폴더를 arcalive/채널명/ID로 이동
            shutil.move(temp_folder, dest_path)
            folder_list.append(dest_path)
            print(f"[완료] {channel_name}/{post_id} 다운로드 완료")
        else:
            print("[경고] 다운로드된 폴더를 찾을 수 없습니다")
        
    except Exception as e:
        print(f"[오류] {e}")

def download_twitter(url, browser="firefox"):
    """X(트위터) 다운로드 (브라우저 쿠키 사용)"""
    print(f"[실행] gallery-dl 시작 (X/Twitter)...")
    
    try:
        # URL에서 유저명 추출
        # 예: https://x.com/username 또는 https://x.com/username/media
        match = re.search(r'(?:x\.com|twitter\.com)/([^/\?]+)', url)
        if match:
            username = match.group(1)
        else:
            username = "unknown_user"
        
        print(f"[정보] 유저: @{username}")
        print(f"[정보] {browser.capitalize()} 쿠키 사용 (로그인 필요)")
        
        # /media가 없으면 자동으로 추가
        if not url.endswith('/media') and '/status/' not in url:
            url = url.rstrip('/') + '/media'
            print(f"[정보] 미디어 URL로 변경: {url}")
        
        # 스크립트 디렉토리에서 gallery-dl.exe 찾기
        script_dir = os.path.dirname(os.path.abspath(__file__))
        gallery_dl_path = os.path.join(script_dir, "gallery-dl.exe")
        
        # gallery-dl.exe가 없으면 시스템 경로에서 찾기
        if not os.path.exists(gallery_dl_path):
            gallery_dl_path = "gallery-dl"
        
        # gallery-dl로 브라우저 쿠키를 사용하여 다운로드
        subprocess.run([
            gallery_dl_path,
            "--cookies-from-browser", browser,
            "-D", f"x/{username}",
            "-f", "[{date:%y-%m-%d}]_{num}.{extension}",
            url
        ])
        
        print(f"[완료] @{username} 다운로드 완료")
        print(f"[알림] 저장 위치: x/{username}/")
        
    except Exception as e:
        print(f"[오류] {e}")


def get_kemono_filter_choice():
    """Kemono 다운로드 필터 선택을 한 번만 물어봄"""
    print("=" * 50)
    print("=== Kemono 다운로드 설정 ===")
    print("=" * 50)
    print()
    print("다운로드할 파일 타입을 선택하세요:")
    print("1. ZIP 파일만")
    print("2. RAR 파일만")
    print("3. 이미지 파일만 (jpg, png)")
    print("4. 비디오 파일만 (mp4)")
    print("5. 전체 다운로드")
    print()
    
    choice = input("선택 (1-5): ").strip()
    print()
    
    return choice

def download_kemono(url, filter_choice):
    # 스크립트 디렉토리에서 gallery-dl.exe 찾기
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gallery_dl_path = os.path.join(script_dir, "gallery-dl.exe")
    
    # gallery-dl.exe가 없으면 시스템 경로에서 찾기
    if not os.path.exists(gallery_dl_path):
        gallery_dl_path = "gallery-dl"
    
    # gallery-dl 명령어 구성
    cmd = [gallery_dl_path]
    
    if filter_choice == "1":
        print("=== ZIP 파일만 다운로드 ===")
        cmd.extend(["--filter", "extension == 'zip'"])
    elif filter_choice == "2":
        print("=== RAR 파일만 다운로드 ===")
        cmd.extend(["--filter", "extension == 'rar'"])
    elif filter_choice == "3":
        print("=== 이미지 파일만 다운로드 (jpg, png) ===")
        cmd.extend(["--filter", "extension in ('jpg', 'jpeg', 'png')"])
    elif filter_choice == "4":
        print("=== 비디오 파일만 다운로드 (mp4) ===")
        cmd.extend(["--filter", "extension == 'mp4'"])
    elif filter_choice == "5":
        print("=== 전체 파일 다운로드 ===")
    else:
        print("=== 전체 파일 다운로드 (기본값) ===")
    
    cmd.append(url)
    
    print(f"[디버그] 실행 명령어: {' '.join(cmd)}")
    print()
    print("=== 다운로드 시작 ===")
    print()
    
    try:
        # stdout, stderr를 그대로 출력하도록 설정
        result = subprocess.run(cmd, text=True)
        
        print()
        if result.returncode == 0:
            print("[완료] 다운로드 완료")
        else:
            print(f"[경고] 다운로드 중 오류 발생 (exit code: {result.returncode})")
        
        print()
        print("=== 파일명 UUID 제거 중 ===")
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        uuid_script = os.path.join(script_dir, "remove_uuid_from_filenames.py")
        
        if os.path.exists(uuid_script):
            subprocess.run([sys.executable, uuid_script, "."])
        else:
            print("[경고] remove_uuid_from_filenames.py 파일을 찾을 수 없습니다")
    except Exception as e:
        print(f"[오류] {e}")

def convert_to_jpg(folder_list):
    if not folder_list:
        return
    
    print()
    print("=== JPG 변환 중 ===")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    convert_script = os.path.join(script_dir, "convert_folder_to_jpg.py")
    
    if not os.path.exists(convert_script):
        print("[경고] convert_folder_to_jpg.py 파일을 찾을 수 없습니다")
        return
    
    for folder in folder_list:
        if os.path.exists(folder):
            print(f"[변환] {folder}")
            subprocess.run([sys.executable, convert_script, folder])

def compress_folders(folder_list):
    print()
    print("=" * 50)
    print("처리 완료")
    print("=" * 50)
    print()
    
    choice = input("ZIP 압축을 진행하시겠습니까? (1: 예, 2: 아니오): ").strip()
    
    if choice == "1":
        print()
        print("=== ZIP 압축 중 ===")
        
        # 먼저 모든 압축 완료
        for folder in folder_list:
            if os.path.exists(folder):
                zip_file = f"{folder}.zip"
                print(f"[압축] {folder}")
                
                try:
                    # Python zipfile 모듈 사용 (UTF-8 안정적 처리)
                    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        # 폴더 내의 모든 파일을 ZIP에 추가
                        for root, dirs, files in os.walk(folder):
                            for file in files:
                                file_path = os.path.join(root, file)
                                # ZIP 내부 경로 계산 (폴더명 제외)
                                arcname = os.path.relpath(file_path, folder)
                                zipf.write(file_path, arcname)
                                print(f"  → {file}")
                    
                    print(f"[완료] {zip_file} 생성 완료")
                    time.sleep(0.5)
                except Exception as e:
                    print(f"[경고] 압축 중 오류 발생: {e}")
                    import traceback
                    traceback.print_exc()
        
        print()
        print("=== 압축 완료, 원본 폴더 삭제 중 ===")
        
        # 압축이 모두 완료된 후 폴더 삭제
        for folder in folder_list:
            zip_file = f"{folder}.zip"
            if os.path.exists(zip_file):
                if os.path.exists(folder):
                    shutil.rmtree(folder)
                print(f"=== 완료: {zip_file} ===")
            else:
                print(f"=== 오류: {zip_file} 생성 실패, 폴더 유지 ===")
    else:
        print()
        print("=== 압축 건너뛰기 - 폴더 유지됨 ===")

def main():
    print_header()
    
    # download_url.txt 파일 확인
    if not check_file("download_url.txt"):
        return
    
    # URL 목록을 먼저 읽어서 kemono/hanime/youtube/arcalive/twitter/hitomi URL이 있는지 확인
    urls = []
    kemono_urls = []
    hanime_urls = []
    youtube_urls = []
    arcalive_urls = []
    twitter_urls = []
    hitomi_urls = []
    general_urls = []  # hitomi가 아닌 일반 gallery-dl URL
    
    with open("download_url.txt", "r", encoding="utf-8") as f:
        for line in f:
            url = line.strip()
            # 빈 줄이나 # 주석은 무시
            if url and not url.startswith('#'):
                if is_kemono_url(url):
                    kemono_urls.append(url)
                elif is_hanime(url):
                    hanime_urls.append(url)
                elif is_youtube(url):
                    youtube_urls.append(url)
                elif is_arcalive_url(url):
                    arcalive_urls.append(url)
                elif is_twitter_url(url):
                    twitter_urls.append(url)
                elif is_hitomi_url(url):
                    hitomi_urls.append(url)
                else:
                    general_urls.append(url)  # 나머지는 일반 gallery-dl URL
    
    # kemono URL이 있으면 필터 선택을 한 번만 물어봄
    kemono_filter = None
    if kemono_urls:
        kemono_filter = get_kemono_filter_choice()
    
    # YouTube URL이 있으면 포맷 선택을 한 번만 물어봄
    youtube_format = None
    if youtube_urls:
        youtube_format = get_youtube_format_choice()
    
    # Twitter/X URL이 있으면 Firefox 쿠키 사용 (기본값)
    twitter_browser = "firefox"
    
    # URL 처리
    print("[시작] URL 다운로드 시작...")
    print()
    
    folder_list = []
    
    # kemono URL 처리
    for url in kemono_urls:
        print()
        print(f"=== 다운로드 중: {url} ===")
        download_kemono(url, kemono_filter)
    
    # hanime URL 처리
    for url in hanime_urls:
        print()
        print(f"=== 다운로드 중 (hanime): {url} ===")
        try:
            # hanime 다운로드 실행
            result = download_hanime_with_progress(
                url=url,
                output_dir=".",  # 현재 디렉토리
                filename=None,
                log_func=print,
                cancel_check_func=None,
                progress_callback=None
            )
            if result:
                print("[완료] hanime 다운로드 완료")
            else:
                print("[경고] hanime 다운로드 실패")
        except Exception as e:
            print(f"[오류] hanime 다운로드 중 오류: {e}")
    
    # YouTube URL 처리
    for url in youtube_urls:
        print()
        print(f"=== 다운로드 중 (YouTube): {url} ===")
        try:
            # YouTube 다운로드 실행
            result = download_youtube_with_progress(
                url=url,
                output_dir=".",  # 현재 디렉토리
                format_choice=youtube_format,
                log_func=print,
                cancel_check_func=None,
                progress_callback=None
            )
            if result:
                print("[완료] YouTube 다운로드 완료")
            else:
                print("[경고] YouTube 다운로드 실패")
        except Exception as e:
            print(f"[오류] YouTube 다운로드 중 오류: {e}")
    
    # arcalive URL 처리
    for url in arcalive_urls:
        print()
        print(f"=== 다운로드 중 (arca.live): {url} ===")
        download_arcalive(url, folder_list)
    
    # Twitter/X URL 처리
    for url in twitter_urls:
        print()
        print(f"=== 다운로드 중 (X/Twitter): {url} ===")
        try:
            download_twitter(url, twitter_browser)
            print("[완료] X/Twitter 다운로드 완료")
        except Exception as e:
            print(f"[오류] X/Twitter 다운로드 중 오류: {e}")
    
    # hitomi URL 처리
    for url in hitomi_urls:
        print()
        print(f"=== 다운로드 중 (hitomi): {url} ===")
        download_hitomi(url, folder_list)
    
    # 일반 gallery-dl URL 처리
    for url in general_urls:
        print()
        print(f"=== 다운로드 중 (gallery-dl): {url} ===")
        download_general(url)
    
    # hitomi/arcalive 폴더가 있으면 변환 및 압축 처리
    if folder_list:
        print()
        print("=== 다운로드 완료 ===")
        convert_to_jpg(folder_list)
        compress_folders(folder_list)
    
    # kemono, hanime, youtube, twitter, general만 다운로드한 경우
    if (kemono_urls or hanime_urls or youtube_urls or twitter_urls or general_urls) and not folder_list:
        print()
        if kemono_urls:
            print("=== kemono 다운로드 완료 ===")
            print("[알림] kemono 파일은 gallery-dl 기본 경로에 저장되었습니다")
        if hanime_urls:
            print("=== hanime 다운로드 완료 ===")
            print("[알림] hanime 파일은 hanime 폴더에 저장되었습니다")
        if youtube_urls:
            print("=== YouTube 다운로드 완료 ===")
            print("[알림] YouTube 파일은 youtube 폴더에 저장되었습니다")
        if twitter_urls:
            print("=== X/Twitter 다운로드 완료 ===")
            print("[알림] X/Twitter 파일은 x 폴더에 저장되었습니다")
        if general_urls:
            print("=== gallery-dl 다운로드 완료 ===")
            print("[알림] gallery-dl 파일은 gallery-dl 기본 경로에 저장되었습니다")
    
    print()
    print("=" * 50)
    print("=== 모든 작업이 완료되었습니다 ===")
    print("=" * 50)
    print()
    input("계속하려면 Enter를 누르세요...")

if __name__ == "__main__":
    main()

