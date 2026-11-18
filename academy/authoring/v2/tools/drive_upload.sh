#!/bin/bash
# 上傳到 Google Drive（www.googleapis.com 的 OAuth 權杖由網路代理注入；401 時用 request_credential 重新要權杖，不要把權杖貼在對話裡）
# 用法：drive_upload.sh mkdir <父資料夾id> <名稱>         → 印出新資料夾 id（同名已存在就沿用）
#       drive_upload.sh put <資料夾id> <本機檔> [雲端檔名]  → 斷點續傳上傳，比對 md5 後印出 id 與連結
set -eo pipefail
API=https://www.googleapis.com
case "$1" in
mkdir)
  q=$(python3 -c "import sys,urllib.parse;print(urllib.parse.quote(\"name='%s' and '%s' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false\"%(sys.argv[2].replace(\"'\",\"\\\\'\"),sys.argv[1])))" "$2" "$3")
  id=$(curl -sS "$API/drive/v3/files?q=$q&fields=files(id)" | python3 -c "import json,sys;f=json.load(sys.stdin)['files'];print(f[0]['id'] if f else '')")
  [ -n "$id" ] && { echo "$id"; exit 0; }
  curl -sS -X POST "$API/drive/v3/files?fields=id" -H "Content-Type: application/json; charset=UTF-8" \
    --data "$(python3 -c "import json,sys;print(json.dumps({'name':sys.argv[2],'parents':[sys.argv[1]],'mimeType':'application/vnd.google-apps.folder'}))" "$2" "$3")" \
    | python3 -c "import json,sys;print(json.load(sys.stdin)['id'])";;
put)
  f=$3; name=${4:-$(basename "$3")}; size=$(stat -c%s "$f")
  case "$f" in *.mp4) mime=video/mp4;; *.pptx) mime=application/vnd.openxmlformats-officedocument.presentationml.presentation;; *.zip) mime=application/zip;; *.md) mime=text/markdown;; *.pdf) mime=application/pdf;; *) mime=application/octet-stream;; esac
  loc=$(curl -sS -D - -o /dev/null -X POST "$API/upload/drive/v3/files?uploadType=resumable&fields=id,name,size,md5Checksum,webViewLink" \
    -H "Content-Type: application/json; charset=UTF-8" -H "X-Upload-Content-Type: $mime" -H "X-Upload-Content-Length: $size" \
    --data "$(python3 -c "import json,sys;print(json.dumps({'name':sys.argv[1],'parents':[sys.argv[2]]}))" "$name" "$2")" | tr -d '\r' | awk -F': ' 'tolower($1)=="location"{print $2}')
  [ -n "$loc" ] || { echo "no upload session (token expired? HTTP 401 → request_credential for www.googleapis.com)"; exit 2; }
  out=$(curl -sS -X PUT "$loc" -H "Content-Type: $mime" --data-binary @"$f")
  echo "$out" | python3 -c "
import json,sys,hashlib
d=json.load(sys.stdin); h=hashlib.md5(open(sys.argv[1],'rb').read()).hexdigest()
assert d.get('md5Checksum')==h, ('md5 mismatch', d)
print(d['id'], d['name'], d['size'], d['webViewLink'])" "$f";;
*) echo "usage: $0 mkdir|put ..."; exit 1;;
esac
