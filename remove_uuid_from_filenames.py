import os
import sys
import re

def remove_uuid_from_filename(filepath):
    """파일명에서 UUID 부분을 제거합니다."""
    try:
        directory = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        name, ext = os.path.splitext(filename)
        
        # UUID 패턴: _xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        # 파일명 끝의 UUID 제거
        uuid_pattern = r'_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        new_name = re.sub(uuid_pattern, '', name, flags=re.IGNORECASE)
        
        # 변경이 있었으면 파일명 변경
        if new_name != name:
            new_filepath = os.path.join(directory, new_name + ext)
            
            # 동일한 이름의 파일이 이미 있으면 번호 추가
            counter = 1
            while os.path.exists(new_filepath):
                new_filepath = os.path.join(directory, f"{new_name}_{counter}{ext}")
                counter += 1
            
            os.rename(filepath, new_filepath)
            print(f"변경: {filename} → {os.path.basename(new_filepath)}")
            return True
        return False
            
    except Exception as e:
        print(f"오류: {filepath} - {e}", file=sys.stderr)
        return False

def process_directory(directory):
    """디렉토리 내 모든 파일의 UUID 제거"""
    if not os.path.exists(directory):
        print(f"디렉토리를 찾을 수 없습니다: {directory}")
        return
    
    changed_count = 0
    
    # 하위 디렉토리 포함 모든 파일 처리
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            if remove_uuid_from_filename(filepath):
                changed_count += 1
    
    print(f"\n총 {changed_count}개 파일명 변경 완료")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        process_directory(sys.argv[1])
    else:
        print("사용법: python remove_uuid_from_filenames.py <폴더경로>")


