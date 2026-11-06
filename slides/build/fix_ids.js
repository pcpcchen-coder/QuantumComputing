/* 修正既有 .pptx 中重複的 shape ID（PowerPoint 開檔時會要求修復）。內容不變，只重新編號。
 * 用法：node fix_ids.js deck.pptx [更多檔案…] */
const fs = require('fs');
const JSZip = require(require.resolve('jszip', { paths: [require.resolve('pptxgenjs')] }));
async function fixIds(file) {
  const zip = await JSZip.loadAsync(fs.readFileSync(file));
  let changed = 0;
  for (const n of Object.keys(zip.files)) {
    if (!/^ppt\/(slides|slideLayouts|slideMasters|notesSlides|notesMasters)\/[^/]+\.xml$/.test(n)) continue;
    const x = await zip.file(n).async('string');
    const ids = [...x.matchAll(/<p:cNvPr id="(\d+)"/g)].map((m) => m[1]);
    if (new Set(ids).size === ids.length) continue;
    let k = 0; zip.file(n, x.replace(/<p:cNvPr id="\d+"/g, () => `<p:cNvPr id="${++k}"`)); changed++;
  }
  if (changed) fs.writeFileSync(file, await zip.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE' }));
  console.log(`${file}：修正 ${changed} 個部件`);
}
module.exports = { fixIds };
if (require.main === module) (async () => { for (const f of process.argv.slice(2)) await fixIds(f); })();
