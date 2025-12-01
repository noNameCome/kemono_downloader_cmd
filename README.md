# Kemono Downloader

다양한 사이트에서 컨텐츠를 다운로드하는 통합 다운로더입니다.

## 지원 사이트
- Kemono/Coomer (kemono.su, coomer.su)
- Hanime (hanime1.me)
- YouTube (youtube.com, youtu.be) - MP4/MP3 선택 가능
- Arca.live (arca.live)
- X/Twitter (x.com, twitter.com) - Firefox 쿠키 사용
- Hitomi (hitomi.la)

## 설치 방법

### 1. Python 설치
- Python 3.8 이상 필요
- https://www.python.org/downloads/

### 2. 필수 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 외부 프로그램 설치
- **gallery-dl**: `pip install gallery-dl`
- **yt-dlp**: 프로젝트에 포함됨 (yt-dlp.exe)
- **ffmpeg**: 프로젝트에 포함됨 (ffmpeg 폴더)

## 사용 방법

### 기본 사용법
1. `download_url.txt` 파일에 다운로드할 URL을 입력 (한 줄에 하나씩)
2. `run_downloader.bat` 실행
3. Kemono URL의 경우 필터 옵션 선택 (ZIP, RAR, 이미지, 비디오, 전체)


## 파일 구조

- `gallery-dl_downloader.py` - 메인 다운로더
- `hanime1_downloader.py` - Hanime 전용 다운로더
- `ytdlp_downloader.py` - YouTube 전용 다운로더
- `remove_uuid_from_filenames.py` - 파일명 UUID 제거
- `convert_folder_to_jpg.py` - 이미지를 JPG로 변환
- `download_url.txt` - URL 입력 파일
- `run_downloader.bat` - 실행 배치 파일

## 다운로드 위치

- **Kemono/Coomer**: gallery-dl 기본 경로
- **Hanime**: `hanime/` 폴더
- **YouTube**: `youtube/` 폴더 (MP4 또는 MP3)
- **Arca.live**: `arcalive/채널명/ID/` 폴더 (JPG 변환 + ZIP 압축)
- **X/Twitter**: `x/유저명/` 폴더
- **Hitomi**: `hitomi/` 폴더 (JPG 변환 + ZIP 압축)

## 주의사항

- **이식성**: 모든 경로가 상대 경로로 설정되어 있어 폴더째로 다른 PC로 이동 가능
  - Python이 시스템 PATH에 등록되어 있어야 합니다
  - `gallery-dl.exe`가 같은 폴더에 있으면 자동으로 사용됩니다
- **X/Twitter 다운로드 시**: 
  - **Firefox에 로그인되어 있어야 합니다**
  - Firefox는 실행 중이어도 다운로드 가능
  - 비공개 계정은 팔로우 상태여야 다운로드 가능
  - 다른 브라우저 사용 시 gallery-dl_downloader.py에서 수정 가능

## 문제 해결

### gallery-dl을 찾을 수 없는 경우
```bash
pip install gallery-dl
```

### curl_cffi 오류가 발생하는 경우
```bash
pip install curl-cffi
```

## 라이센스
개인 사용 목적

