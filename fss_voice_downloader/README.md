# 금융감독원 보이스피싱 체험관 미디어 다운로더

금융감독원 보이스피싱 체험관의 세 게시판을 순회하여 게시물에 첨부된 MP3, MP4 등 미디어 원본을 저장합니다.

## 1. 준비

PowerShell에서 프로젝트 폴더로 이동합니다.

```powershell
cd "C:\Users\Leeyonghyun\Documents\ChatGPT\엑셈"
```

필요한 패키지를 설치합니다.

```powershell
py -3.14 -m pip install -r requirements.txt
```

설치 확인:

```powershell
py -3.14 -c "import requests, bs4, urllib3; print('설치 완료')"
```

## 2. 전체 다운로드

세 게시판을 모두 다운로드합니다.

```powershell
py -3.14 fss_voice_downloader.py --min-delay 2 --max-delay 4
```

기본 저장 위치는 `fss_voice_files`입니다.

```text
fss_voice_files/
├─ 바로_이_목소리/
├─ 그놈_목소리_대출사기형/
└─ 수사기관_사칭형/
```

각 폴더에는 미디어 파일과 다운로드 내역을 기록한 `manifest.csv`가 생성됩니다. 이미 존재하는 파일은 다시 다운로드하지 않습니다.

## 3. 특정 게시판만 다운로드

게시판 키:

- `direct`: 바로 이 목소리
- `loan`: 그놈 목소리 대출사기형
- `agency`: 수사기관 사칭형

바로 이 목소리만 다운로드:

```powershell
py -3.14 fss_voice_downloader.py --boards direct --min-delay 2 --max-delay 4
```

대출사기형과 수사기관 사칭형만 다운로드:

```powershell
py -3.14 fss_voice_downloader.py --boards loan agency --min-delay 2 --max-delay 4
```

## 4. 중단된 페이지부터 재개

예를 들어 대출사기형 5페이지부터 다시 실행합니다.

```powershell
py -3.14 fss_voice_downloader.py --boards loan --start-page 5 --min-delay 2 --max-delay 4
```

기존 파일은 건너뛰므로 같은 명령을 다시 실행해도 됩니다.

## 5. 다른 위치에 저장

```powershell
py -3.14 fss_voice_downloader.py --output "D:\fss_voice_files" --min-delay 2 --max-delay 4
```

## 6. 게시판별 ZIP 만들기

먼저 바탕화면 경로를 변수에 저장합니다. 성공해도 별도 메시지는 출력되지 않습니다.

```powershell
$desktop = [Environment]::GetFolderPath("Desktop")
```

바로 이 목소리:

```powershell
tar -a -c -f "$desktop\direct_voice.zip" -C ".\fss_voice_files" "바로_이_목소리"
```

대출사기형:

```powershell
tar -a -c -f "$desktop\loan_voice.zip" -C ".\fss_voice_files" "그놈_목소리_대출사기형"
```

수사기관 사칭형:

```powershell
tar -a -c -f "$desktop\agency_voice.zip" -C ".\fss_voice_files" "수사기관_사칭형"
```

ZIP 내부 검사 예시:

```powershell
tar -tf "$desktop\loan_voice.zip" | Select-Object -First 5
```

파일 목록이 출력되면 정상입니다. Windows 탐색기가 ZIP을 열지 못하면 `tar -xf` 또는 7-Zip을 사용합니다.

```powershell
New-Item -ItemType Directory "$desktop\loan_voice_압축해제" -Force
tar -xf "$desktop\loan_voice.zip" -C "$desktop\loan_voice_압축해제"
```

## 7. Git에 코드 저장

음성 파일과 ZIP 파일은 `.gitignore`에 의해 제외됩니다. 코드만 커밋합니다.

```powershell
git add .gitignore README.md fss_voice_downloader.py requirements.txt
git commit -m "Update FSS voice downloader"
git status
```

`nothing to commit, working tree clean`이 표시되면 커밋이 완료된 상태입니다. 다른 컴퓨터에서 사용하려면 별도로 GitHub 등의 원격 저장소에 push해야 합니다.

## 주의사항

- 서버에서 `429` 또는 `503` 오류가 발생하면 실행을 중단하고 요청 간격을 늘려 다시 실행하세요.
- 다운로드 자료의 저작권과 이용 범위를 확인하세요.
- `Ctrl+C`로 중단해도 이미 다운로드한 파일은 유지됩니다.
