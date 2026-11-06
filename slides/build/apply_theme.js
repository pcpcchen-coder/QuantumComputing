/* 把自訂主題色寫入 pptxgenjs 產生的 ppt/theme/theme1.xml
 * （pptxgenjs 只能設定主題字型，配色固定為 Office 預設，需事後替換）。 */
const fs = require('fs');
const JSZip = require(require.resolve('jszip', { paths: [require.resolve('pptxgenjs')] }));
const SLOTS = ['dk1', 'lt1', 'dk2', 'lt2', 'accent1', 'accent2', 'accent3', 'accent4', 'accent5', 'accent6', 'hlink', 'folHlink'];

async function applyTheme(deckPath, theme) {
  const zip = await JSZip.loadAsync(fs.readFileSync(deckPath));
  const part = 'ppt/theme/theme1.xml';
  const name = theme.name.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
  const scheme = `<a:clrScheme name="${name}">` + SLOTS.map((k) => `<a:${k}><a:srgbClr val="${theme.colors[k].toUpperCase()}"/></a:${k}>`).join('') + '</a:clrScheme>';
  const xml = (await zip.file(part).async('string'))
    .replace(/<a:clrScheme\b[\s\S]*?<\/a:clrScheme>/, () => scheme)
    .replace(/(<a:(?:theme|fontScheme)\b[^>]*?\bname=")[^"]*"/g, (_, h) => `${h}${name}"`);
  zip.file(part, xml);
  for (const n of Object.keys(zip.files)) {
    if (zip.files[n].dir) { delete zip.files[n]; continue; }
    if (!n.endsWith('.xml')) continue;
    const x = await zip.file(n).async('string');
    const bad = x.match(/<a:srgbClr val="((?![0-9A-Fa-f]{6}")[^"]*)"/);
    if (bad) throw new Error(`${n}: 非法色碼 ${bad[1]}（scheme color 用在只接受 hex 的選項）`);
  }
  fs.writeFileSync(deckPath, await zip.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE' }));
}
module.exports = { applyTheme };
