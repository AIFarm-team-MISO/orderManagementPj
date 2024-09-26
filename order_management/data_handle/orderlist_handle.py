import msoffcrypto
import pandas as pd
import io

def decrypt_excel(file_path, password, columns_to_extract=None):
    """
    비밀번호가 걸린 엑셀 파일을 해제하고, 지정된 열을 추출하여 데이터프레임으로 반환합니다.

    Args:
        file_path (str): 엑셀 파일의 경로.
        password (str): 엑셀 파일의 비밀번호.
        columns_to_extract (list, optional): 추출할 열 이름의 리스트. 기본값은 None이며, 이 경우 모든 열을 가져옵니다.

    Returns:
        pd.DataFrame: 추출된 데이터프레임. 데이터가 없는 경우 None을 반환.
    """
    decrypted = io.BytesIO()
    try:
        with open(file_path, "rb") as f:
            file = msoffcrypto.OfficeFile(f)
            file.load_key(password=password)
            file.decrypt(decrypted)

        decrypted.seek(0)
        df = pd.read_excel(decrypted, header=1, engine='openpyxl')

        # 열 이름 정리 (필요에 따라 공백 제거 등)
        df.columns = df.columns.str.strip()
        df.columns = df.columns.astype(str)
        print("정리된 열 이름:", df.columns.tolist())

        # 사용자가 지정한 열만 선택
        if columns_to_extract:
            try:
                df = df[columns_to_extract]
            except KeyError as e:
                print(f"Error: {e}")
                print(f"유효하지 않은 열 이름입니다. 다음 중 하나를 확인하세요: {df.columns.tolist()}")
                return None

        # NaN 값 제거 (옵션)
        df = df.dropna(how='all')  # 모든 값이 NaN인 행을 제거
        return df

    except Exception as e:
        print(f"파일을 읽는 중에 오류가 발생했습니다: {e}")
        return None
