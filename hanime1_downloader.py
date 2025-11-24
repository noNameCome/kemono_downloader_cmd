import subprocess
import os
import re
import time
from urllib.parse import urlparse
import sys

env = os.environ.copy()
env["PYTHONIOENCODING"] = "utf-8"

CREATE_NO_WINDOW = 0x08000000

def is_hanime(url):
    """
    주어진 URL이 Hanime URL인지 확인하는 함수
    
    Args:
        url (str): 확인할 URL
        
    Returns:
        bool: Hanime URL 여부
    """
    if not url:
        return False
        
    url = url.strip()
    
    # URL 정규화
    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'https://' + url
    
    try:
        netloc = urlparse(url).netloc.lower()
        return "hanime" in netloc or "hanime1.me" in netloc
    except:
        return False

def download_hanime_with_progress(url, output_dir, filename=None, log_func=print, cancel_check_func=None, progress_callback=None):
    """
    Hanime URL을 Cloudflare 우회와 함께 다운로드하는 함수
    
    Args:
        url (str): 다운로드할 Hanime URL
        output_dir (str): 다운로드 디렉토리
        filename (str, optional): 저장할 파일명
        log_func (function): 로깅 함수
        cancel_check_func (function): 취소 확인 함수
        progress_callback (function): 진행률 콜백 함수
        
    Returns:
        bool: 성공 여부
    """
    try:
        # curl_cffi 설치 확인
        try:
            import curl_cffi
            log_func("✅ curl_cffi 라이브러리 감지됨 - Cloudflare 우회 활성화")
        except ImportError:
            log_func("⚠️ curl_cffi가 설치되지 않음 - 기본 방식으로 시도")
            # curl_cffi 없이도 시도해볼 수 있도록 함
        
        # 출력 디렉토리 생성
        hanime_output_path = os.path.join(output_dir, "hanime")
        os.makedirs(hanime_output_path, exist_ok=True)
        
        # 파일명 처리
        if filename:
            filename = re.sub(r'[\\/:*?\"<>|]', '', filename)  # 파일명 정리
            output_template = f"{filename}.%(ext)s"
        else:
            output_template = "%(title)s.%(ext)s"
        
        # 진행률 표시 훅
        def progress_hook(d):
            if cancel_check_func and cancel_check_func():
                log_func("⛔ 다운로드 취소됨")
                return
                
            if d['status'] == 'downloading':
                try:
                    total = d.get('total_bytes', 0) or d.get('total_bytes_estimate', 0)
                    downloaded = d.get('downloaded_bytes', 0)
                    speed = d.get('speed', 0)
                    if total > 0:
                        percent = downloaded / total * 100
                        speed_str = f"{speed/1024/1024:.1f} MB/s" if speed else "N/A"
                        log_func(f"⏳ 다운로드 중: {percent:.1f}% | 속도: {speed_str}")
                        if progress_callback:
                            progress_callback(downloaded, total)
                except:
                    pass
            elif d['status'] == 'finished':
                log_func("✅ 다운로드 완료!")
                if progress_callback:
                    progress_callback(100, 100)
        
        # 터미널 명령어와 동일한 방식으로 subprocess 사용
        import yt_dlp
        log_func(f"📥 Hanime 다운로드 시작 (Cloudflare 우회): {url}")
        
        # 터미널에서 성공한 명령어와 정확히 동일하게 구성
        command = [
            "yt-dlp",
            "--extractor-args", "generic:impersonate=chrome",
            url,
            "-o", os.path.join(hanime_output_path, output_template),
            "--no-playlist",
            "--no-part"
        ]
        
        log_func(f"🔧 명령어 실행: {' '.join(command)}")
        
        # 프로세스 시작
        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
            encoding='utf-8',
            errors='replace',
            creationflags=CREATE_NO_WINDOW | (subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0),
            env=env
        )
        
        # 진행 상황 모니터링
        while proc.poll() is None:
            # 취소 확인
            if cancel_check_func and cancel_check_func():
                log_func("⛔ 취소 감지 → 다운로드 중단")
                proc.terminate()
                return False
            
            # 출력 읽기
            try:
                line = proc.stdout.readline()
                if line:
                    line = line.strip()
                    if line:
                        log_func(line)
                        
                        # 진행률 파싱 (yt-dlp 출력에서)
                        if "[download]" in line and "%" in line:
                            try:
                                import re
                                percent_match = re.search(r'(\d+\.?\d*)%', line)
                                if percent_match and progress_callback:
                                    percent = float(percent_match.group(1))
                                    progress_callback(percent, 100)
                            except:
                                pass
            except Exception as e:
                log_func(f"⚠️ 출력 처리 중 오류: {e}")
                time.sleep(0.1)
        
        # 결과 확인
        if proc.returncode == 0:
            log_func("✅ Hanime 다운로드 완료!")
            if progress_callback:
                progress_callback(100, 100)
            return True
        else:
            log_func(f"❌ 다운로드 실패: return code {proc.returncode}")
            return False
        
    except Exception as e:
        log_func(f"❌ Hanime 다운로드 오류: {str(e)}")
        
        # 실패 시 일반 방식으로 재시도
        log_func("🔄 일반 방식으로 재시도...")
        try:
            ydl_opts_fallback = {
                'format': 'best[height<=720]',
                'outtmpl': os.path.join(hanime_output_path, output_template),
                'no_playlist': True,
                'quiet': True,
                'no_warnings': True,
                'progress_hooks': [progress_hook],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts_fallback) as ydl:
                ydl.download([url])
            
            log_func("✅ 일반 방식으로 다운로드 완료!")
            return True
            
        except Exception as fallback_e:
            log_func(f"❌ 일반 방식도 실패: {str(fallback_e)}")
            return False

# 사용 예시
if __name__ == "__main__":
    # 테스트용 코드
    test_url = "https://hanime1.me/watch?v=xxxxx"  # 실제 URL로 변경
    output_directory = "downloads"
    
    if is_hanime(test_url):
        print("✅ Hanime URL이 확인되었습니다!")
        download_hanime_with_progress(test_url, output_directory)
    else:
        print("❌ Hanime URL이 아닙니다.")
