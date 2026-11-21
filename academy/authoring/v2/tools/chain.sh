#!/bin/bash
# 依序製作多課（背景作業上限 2 小時：預算 110 分鐘，剩不到 45 分鐘不開新課）。已做完的課有 $QWORK/produced-Qxxx 標記會跳過。
# 用法：chain.sh Q011 Q012 Q013 ...   記錄：$QWORK/chain.log、$QWORK/produce-Qxxx.log
T=$(cd "$(dirname "$0")" && pwd); W=${QWORK:-/home/user/qwork}; mkdir -p "$W"
END=$(( $(date +%s) + 110*60 ))
for L in "$@"; do
  [ -f "$W/produced-$L" ] && continue
  [ $(( END - $(date +%s) )) -lt 2700 ] && { echo "NOTIME $L"; exit 0; }
  if "$T/produce.sh" $L > "$W/produce-$L.log" 2>&1; then touch "$W/produced-$L"; echo "PRODUCED $L"; else echo "FAILED $L"; tail -15 "$W/produce-$L.log"; exit 1; fi
done
echo CHAIN_END
