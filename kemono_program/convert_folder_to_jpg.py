import os
import sys
from PIL import Image

def convert_to_jpg(filepath):
    """이미지를 JPG 포맷으로 변환합니다."""
    try:
        # 이미 jpg면 건너뛰기
        if filepath.lower().endswith('.jpg') or filepath.lower().endswith('.jpeg'):
            return True
        
        # 이미지 파일 확장자 체크
        valid_extensions = ('.png', '.webp', '.gif', '.bmp', '.tiff', '.tif')
        if not filepath.lower().endswith(valid_extensions):
            return False
        
        print(f"변환 중: {os.path.basename(filepath)}")
        
        # 이미지 열기
        img = Image.open(filepath)
        
        # RGBA 모드인 경우 RGB로 변환 (JPG는 알파 채널 미지원)
        if img.mode in ('RGBA', 'LA', 'P'):
            # 흰색 배경 생성
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 새 파일명 생성 (확장자를 .jpg로 변경)
        base = os.path.splitext(filepath)[0]
        new_filepath = base + '.jpg'
        
        # JPG로 저장
        img.save(new_filepath, 'JPEG', quality=95, optimize=True)
        
        # 원본 파일 삭제 (이미 jpg가 아닌 경우만)
        if filepath != new_filepath:
            os.remove(filepath)
            print(f"완료: {os.path.basename(new_filepath)}")
        
        return True
            
    except Exception as e:
        print(f"변환 실패: {filepath} - {e}", file=sys.stderr)
        return False

def convert_folder(folder_path):
    """폴더 내 모든 이미지를 JPG로 변환합니다."""
    if not os.path.exists(folder_path):
        print(f"폴더를 찾을 수 없습니다: {folder_path}")
        return
    
    converted_count = 0
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        if os.path.isfile(filepath):
            if convert_to_jpg(filepath):
                converted_count += 1
    
    print(f"\n총 {converted_count}개 파일 처리 완료")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        convert_folder(sys.argv[1])
    else:
        print("사용법: python convert_folder_to_jpg.py <폴더경로>")


