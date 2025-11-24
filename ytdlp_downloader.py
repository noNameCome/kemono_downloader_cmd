import subprocess
import os
import sys
from urllib.parse import urlparse, parse_qs

def is_youtube(url):
    """
    주어진 URL이 YouTube URL인지 확인하는 함수
    
    Args:
        url (str): 확인할 URL
        
    Returns:
        bool: YouTube URL 여부
    """
    if not url:
        return False
        
    url = url.strip()
    
    # URL 정규화
    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'https://' + url
    
    try:
        netloc = urlparse(url).netloc.lower()
        return "youtube.com" in netloc or "youtu.be" in netloc
    except:
        return False

def download_youtube_with_progress(url, output_dir, format_choice="mp4", log_func=print, cancel_check_func=None, progress_callback=None):
    """
    YouTube URL을 다운로드하는 함수
    
    Args:
        url (str): 다운로드할 YouTube URL
        output_dir (str): 다운로드 디렉토리
        format_choice (str): 'mp4' 또는 'mp3'
        log_func (function): 로깅 함수
        cancel_check_func (function): 취소 확인 함수
        progress_callback (function): 진행률 콜백 함수
        
    Returns:
        bool: 성공 여부
    """
    try:
        # 출력 디렉토리 생성
        youtube_output_path = os.path.join(output_dir, "youtube")
        os.makedirs(youtube_output_path, exist_ok=True)
        
        # 스크립트 디렉토리에서 yt-dlp.exe와 ffmpeg 경로 찾기
        script_dir = os.path.dirname(os.path.abspath(__file__))
        ytdlp_path = os.path.join(script_dir, "yt-dlp.exe")
        ffmpeg_dir = os.path.join(script_dir, "ffmpeg")
        
        if not os.path.exists(ytdlp_path):
            log_func(f"❌ yt-dlp.exe를 찾을 수 없습니다: {ytdlp_path}")
            return False
        
        if not os.path.exists(ffmpeg_dir):
            log_func(f"❌ ffmpeg 폴더를 찾을 수 없습니다: {ffmpeg_dir}")
            return False
        
        log_func(f"📥 YouTube 다운로드 시작: {url}")
        log_func(f"📁 저장 위치: {youtube_output_path}")
        log_func(f"🎬 포맷: {format_choice.upper()}")
        log_func("")
        
        # 명령어 구성
        command = [ytdlp_path]
        
        if format_choice.lower() == "mp3":
            # MP3 다운로드 (오디오만)
            command.extend([
                "-x",  # 오디오만 추출
                "--audio-format", "mp3",
                "--audio-quality", "0",  # 최고 품질
                "--embed-thumbnail",  # 썸네일 포함
                "--add-metadata",  # 메타데이터 추가
                "-o", os.path.join(youtube_output_path, "%(title)s.%(ext)s"),
                "--ffmpeg-location", ffmpeg_dir
            ])
        else:
            # MP4 다운로드 (비디오+오디오)
            command.extend([
                "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "--merge-output-format", "mp4",
                "-o", os.path.join(youtube_output_path, "%(title)s.%(ext)s"),
                "--ffmpeg-location", ffmpeg_dir,
                "--embed-thumbnail",  # 썸네일 포함
                "--add-metadata"  # 메타데이터 추가
            ])
        
        command.extend([
            "--no-playlist",  # 재생목록 다운로드 안 함
            url
        ])
        
        log_func(f"🔧 명령어 실행: {' '.join(command)}")
        log_func("")
        
        # 프로세스 시작
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        
        proc = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
            encoding='utf-8',
            errors='replace',
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
                        
                        # 진행률 파싱
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
                import time
                time.sleep(0.1)
        
        # 결과 확인
        if proc.returncode == 0:
            log_func("")
            log_func("✅ YouTube 다운로드 완료!")
            if progress_callback:
                progress_callback(100, 100)
            return True
        else:
            log_func("")
            log_func(f"❌ 다운로드 실패: return code {proc.returncode}")
            return False
        
    except Exception as e:
        log_func(f"❌ YouTube 다운로드 오류: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def get_youtube_format_choice():
    """YouTube 다운로드 포맷 선택 (한 번만 물어봄)"""
    print("=" * 50)
    print("=== YouTube 다운로드 설정 ===")
    print("=" * 50)
    print()
    print("다운로드 포맷을 선택하세요:")
    print("1. MP4 (비디오 + 오디오)")
    print("2. MP3 (오디오만)")
    print()
    
    choice = input("선택 (1-2): ").strip()
    print()
    
    if choice == "2":
        return "mp3"
    else:
        return "mp4"

# 사용 예시
if __name__ == "__main__":
    # 테스트용 코드
    test_url = "https://www.youtube.com/watch?v=TAOFzuKYCA8"
    output_directory = "."
    
    if is_youtube(test_url):
        print("✅ YouTube URL이 확인되었습니다!")
        format_choice = get_youtube_format_choice()
        download_youtube_with_progress(test_url, output_directory, format_choice)
    else:
        print("❌ YouTube URL이 아닙니다.")

