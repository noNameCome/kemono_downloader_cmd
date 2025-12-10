# Kemono Downloader

다양한 사이트에서 컨텐츠를 다운로드하는 통합 다운로더입니다.

## 지원 사이트
- Kemono/Coomer/Nekohouse (kemono.su, coomer.su, nekohouse.su)
- Hanime (hanime1.me)
- YouTube (youtube.com, youtu.be) - MP4/MP3 선택 가능
- Arca.live (arca.live)
- X/Twitter (x.com, twitter.com) - Firefox 쿠키 사용
- Hitomi (hitomi.la)
- 기타 Gallery-dl 지원 사이트 (자동 감지)

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
3. Kemono/Coomer/Nekohouse URL의 경우 필터 옵션 선택 (ZIP, RAR, 이미지, 비디오, 전체)
4. YouTube URL의 경우 포맷 선택 (MP4 비디오 또는 MP3 오디오)


## 파일 구조

```
kemono_downloader_cmd/
  ├── download/                      # 다운로드된 파일 저장 위치
  │   ├── hanime/                    # Hanime 다운로드
  │   ├── youtube/                   # YouTube 다운로드
  │   ├── hitomi/                    # Hitomi 다운로드
  │   ├── x/                         # X/Twitter 다운로드
  │   ├── arcalive/                  # Arca.live 다운로드
  │   └── gallery-dl/                # 기타 gallery-dl 지원 사이트
  ├── kemono_program/                # 프로그램 파일
  │   ├── gallery-dl_downloader.py   # 메인 다운로더
  │   ├── hanime1_downloader.py      # Hanime 전용 다운로더
  │   ├── ytdlp_downloader.py        # YouTube 전용 다운로더
  │   ├── convert_folder_to_jpg.py   # 이미지를 JPG로 변환
  │   ├── remove_uuid_from_filenames.py  # 파일명 UUID 제거
  │   ├── requirements.txt           # Python 패키지 목록
  │   ├── gallery-dl.exe             # Gallery-dl 실행 파일
  │   ├── yt-dlp.exe                 # yt-dlp 실행 파일
  │   └── ffmpeg/                    # FFmpeg (비디오/오디오 처리)
  ├── download_url.txt               # URL 입력 파일
  └── run_downloader.bat             # 실행 배치 파일
```

## 다운로드 위치

- **Kemono/Coomer/Nekohouse**: `gallery-dl/` 폴더 (gallery-dl 기본 경로)
- **Hanime**: `download/hanime/` 폴더
- **YouTube**: `download/youtube/` 폴더 (MP4 또는 MP3)
- **Arca.live**: `download/arcalive/채널명/ID/` 폴더 (JPG 변환 + ZIP 압축)
- **X/Twitter**: `download/x/유저명/` 폴더
- **Hitomi**: `download/hitomi/` 폴더 (JPG 변환 + ZIP 압축)
- **기타 Gallery-dl 지원 사이트**: `gallery-dl/` 폴더 (gallery-dl 기본 경로)

## 주의사항

- **이식성**: 모든 경로가 상대 경로로 설정되어 있어 폴더째로 다른 PC로 이동 가능
  - Python이 시스템 PATH에 등록되어 있어야 합니다
  - `kemono_program/` 폴더의 파일들은 자동으로 인식됩니다
  - 다운로드된 파일은 모두 `download/` 폴더에 저장됩니다
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

