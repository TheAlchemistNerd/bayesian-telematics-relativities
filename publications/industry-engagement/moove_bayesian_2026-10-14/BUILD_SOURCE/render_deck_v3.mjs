import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import { FileBlob, PresentationFile } from '@oai/artifact-tool';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../../..');
const pptxPath=path.join(root,'publications/industry-engagement/moove_bayesian_2026-10-14/BAYESIAN_RELATIVITIES_X_MOOVE_RESEARCH_PARTNERSHIP_DECK_2026-10-14_V3.pptx');
const out=path.join(root,'.build/moove_bayesian_2026-10-14/rendered-slides-v3-2x');
await fs.mkdir(out,{recursive:true});
const p=await PresentationFile.importPptx(await FileBlob.load(pptxPath));
async function write(file,blob){await fs.writeFile(file,new Uint8Array(await blob.arrayBuffer()));}
for(let i=0;i<p.slides.items.length;i++){
 const slide=p.slides.items[i];
 await write(path.join(out,`slide-${String(i+1).padStart(2,'0')}.png`),await p.export({slide,format:'png',scale:2}));
}
await write(path.join(out,'contact-sheet.png'),await p.export({format:'png',montage:{columns:4,slideWidth:360,padding:18,gap:16,background:'#E8EEF2'}}));
console.log(JSON.stringify({slides:p.slides.items.length,out},null,2));
