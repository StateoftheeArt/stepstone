import {PIP_ANCHORS} from './pip-art.js?build=119';
// Room items share their art with card previews; companions supply attachment positions.
const rect=(x,y,w,h,c,r=3)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${c}"/>`;
const path=(d,c,stroke='',width=2)=>`<path d="${d}" fill="${c}"${stroke?` stroke="${stroke}" stroke-width="${width}" stroke-linejoin="round"`:''}/>`;
const circle=(x,y,r,c)=>`<circle cx="${x}" cy="${y}" r="${r}" fill="${c}"/>`;
const palettes={teal:['#376b70','#285159'],sand:['#a28b6d','#77634e'],lavender:['#79718f','#574e71'],night:['#3d4569','#242d4f'],sage:['#758d79','#405e53'],rose:['#ab7d89','#77535e'],sky:['#718f9f','#456578']};

export function accessoryArtwork(id,species='fox',viewAnchor=null){
  const anchor=viewAnchor||PIP_ANCHORS[species]||PIP_ANCHORS.fox,s=anchor.width/34;
  if(viewAnchor&&['glasses','sunglasses','headphones'].includes(id)){
    const x=anchor.cx,y=anchor.eye;
    const art=id==='headphones'?path(`M${x-8} ${y+2}v-8q0-9 12-9`,'none','#b8ac86',2)+rect(x-10,y-2,7,10,'#32434b',2)+rect(x-9,y,5,6,'#8d9e92',1):path(`M${x-1} ${y-4}h9v8h-9Z`,id==='sunglasses'?'#7895aa':'none','#d3b184',1.5)+path(`M${x-10} ${y-2}h9`,'none','#d3b184',1.5);
    return `<g class="sprite-accessory">${art}</g>`;
  }
  const place=(art,x,y,scale,oldY)=>`<g transform="translate(${x-32*scale} ${y-oldY*scale}) scale(${scale})">${art}</g>`;
  const hat=art=>place(art,anchor.cx,anchor.top+2,s,8);
  const trim='#32434b',gold='#f7d395',mint='#a5e3c1',rose='#f4b7c6';
  const art={
    sprout:hat(path('M31 10V3h2v7Z','#4b976b')+path('M31 5C18 5 19-3 24 0c6 1 7 5 7 5M33 4C34-4 45-3 42 2c-2 3-7 3-9 2',mint,'#489269',1)),
    scarf:path('M17 44q15 6 30 0v6q-15 6-30 0Z',gold,trim,1)+path('M38 49h7v11h-7Z','#e4ae6d',trim,1)+path('M39 53h5m-5 4h5','none','#fff0c2',1),
    headphones:path('M14 35V27a18 13 0 0 1 36 0v8','none',trim,5)+path('M14 35V27a18 13 0 0 1 36 0v8','none','#b8ac86',2)+rect(9,31,9,13,trim,2)+rect(11,33,5,9,'#8d9e92',1)+rect(46,31,9,13,trim,2)+rect(48,33,5,9,'#8d9e92',1)+rect(12,35,3,1,'#c8c8ad',0)+rect(49,35,3,1,'#c8c8ad',0),
    bow:hat(path('M32 8 22 2q-6 6 0 12Zm0 0 10-6q6 6 0 12Z',rose,trim,1)+circle(32,8,3,'#c87899')),
    beanie:hat(path('M17 11q0-15 15-15t15 15Z','#88bde3',trim,1)+rect(15,8,34,6,'#c8e8f5',2)+circle(32,-5,4,'#c8e8f5')+path('M25 1v6m7-8v8m7-6v6','none','#a8d5ec',1)),
    glasses:path('M16 30h12v9H16Zm20 0h12v9H36ZM28 33h8M11 31h5m32 0h5','none',gold,2)+path('M19 32h4m16 0h4','none','#f7edd1',1),
    neckbow:path('M31 47 20 42v12Zm2 0 11-5v12Z','#a8c2e8',trim,1)+circle(32,47,3,'#678ebc'),
    flowers:hat(path('M18 10q14-11 28 0','none','#669d76',3)+[20,28,36,44].map((x,i)=>circle(x,7-(i===1||i===2?3:0),4,i%2?rose:'#e7d69b')+circle(x,7-(i===1||i===2?3:0),1.3,'#bd8a58')).join('')),
    rainhat:hat(path('M20 9 24-1h16l4 10Z',gold,trim,1)+path('M15 9q17 5 34 0l-2 5H17Z','#dfb477',trim,1)),
    explorer:hat(path('M21 7 23-5h7l2 3 3-3h7l2 12Z','#bb9470',trim,1)+rect(20,5,25,4,'#6c5d4f',1)+path('M13 9q19 6 38 0v3q-19 7-38 0Z','#d8b991',trim,1)),
    starpin:path('m45 40 2 4 5 1-4 3 1 5-4-3-4 3 1-5-4-3 5-1Z',gold,trim,1),
    backpack:rect(7,39,14,18,'#769a93',4)+rect(9,45,10,8,'#b1ccae',2)+path('M14 39v-4h6v5','none',trim,2)+path('M15 43h5','none','#e2dfb6',1),
    bandana:path('M19 44q13 4 26 0l-13 14Z','#7eb4a7',trim,1.2)+path('M27 48l5 5 5-5','none','#cee3cd',1),
    cap:hat(path('M20 10V7q12-12 24 0v4Z','#6a8aa7',trim,1.2)+path('M19 10h27q7 0 6 4H18Z','#526c87',trim,1)+path('M31 1v8','none','#a8c3d0',1)),
    pendant:path('M22 43q0 13 10 13t10-13','none','#d3b184',1.5)+path('M32 52l4 4-4 4-4-4Z','#be8a60',trim,1)+circle(32,56,1,'#f2d7a3'),
    beret:hat(path('M16 9q-2-8 16-8t16 8l-5 4H21Z','#aa8c99',trim,1.2)+rect(23,11,18,3,'#7c677a',1)+path('M33 1l2-3','none',trim,1.5)),
    leafpin:path('M21 42q-9 1-5 9 9 0 9-9Z','#9cc69c',trim,1)+path('M17 49l6-5','none','#536f65',1),
    sunglasses:path('M16 30h12v9H16Zm20 0h12v9H36Z','#7895aa',trim,1.4)+path('M28 33h8M11 31h5m32 0h5','none',trim,1.6)+path('M18 32l6 5m14-5 6 5','none','#bfd7d9',1),
    bucket:hat(path('M22 1h20l4 11H18Z','#a5b7a0',trim,1.2)+path('M18 9h28l5 5q-19 5-38 0Z','#889b88',trim,1.2)+path('M22 7h20','none','#d3ddc3',1)),
    satchel:path('M43 35L19 56','none','#c2a47d',2)+rect(17,45,13,13,'#b4926c',2)+path('M17 46h13v6q-6 5-13 0Z','#d0b28a',trim,1)+rect(22,51,3,4,'#7b7361',1),
    wizard:hat(path('M18 11L30-8l6 5 9 15Z','#8399b6',trim,1.2)+path('M16 10q16 7 32 0l3 5q-19 8-38 0Z','#637d9e',trim,1.2)+path('M31 0l1 3 3 1-3 1-1 3-1-3-3-1 3-1Z',gold)),
    knitted:path('M18 43q14 6 28 0v7q-14 6-28 0Z','#a6a3bf',trim,1.2)+path('M38 48h7v13h-7Z','#8e90ad',trim,1)+path('M22 47l2 2 2-2 2 2 2-2 2 2 2-2 2 2m5 3v6','none','#d5cfde',1),
    moonpin:circle(21,47,4,'#c7cfdb')+circle(23,45,3,'#5b718e')+path('M27 43l1 2 2 1-2 1-1 2-1-2-2-1 2-1Z',gold),
    steppin:path('M18 50v-3h3v-3h3v-3h3v9Z',gold,trim,1)+path('M18 49h9','none','#f9e4bb',1),
    crown:hat(path('M20 12 17 0l9 5 6-10 6 10 9-5-3 12Z',gold,trim,1)+rect(20,9,24,5,'#e0b77e',1)+circle(32,10,2,rose))
  };
  if(!art[id])return '';
  const fitted=['glasses','headphones','sunglasses'].includes(id)?place(art[id],anchor.cx,anchor.eye,s,34):['scarf','neckbow','bandana','pendant','knitted'].includes(id)?place(art[id],anchor.cx,anchor.neck,Math.min(s,.85),48):['backpack','starpin','satchel','leafpin','moonpin','steppin'].includes(id)?place(art[id],32,48,.8,48):art[id];
  return `<g class="sprite-accessory">${fitted}</g>`;
}

export function foodBowlArtwork(id='gold'){
  const colours={gold:['#e8c483','#bea074','#fff1bd'],ceramic:['#d5e3df','#93aca9','#eff7e9'],steel:['#a4b9c7','#687f92','#d5e2e5'],speckled:['#c5b6a0','#8c8173','#ece2cf']};
  const [base,edge,rim]=colours[id]||colours.gold;
  return path('M4 8h72l-8 23H12Z',base,edge,2)+path('M4 8q36 10 72 0','none',rim,3)+rect(31,16,18,7,edge,0)+(id==='steel'?path('M15 14l4 12m42-12-4 12','none',rim,1.5):id==='speckled'?[[20,17],[25,25],[48,17],[58,24]].map(([x,y])=>circle(x,y,1,edge)).join(''):'');
}
function curtainIcon(colour,striped=false){
  return rect(23,16,34,45,'#73929b',2)+path('M40 18v41m-15-20h30','none','#c9ddcd',2)+path('M11 12h58','none','#bca17d',3)+path('M12 14h14v44l-16 6Zm42 0h14l2 50-16-6Z',colour)+path('M16 19v34m46-34v34','none',striped?'#eef1df':'#ffffff33',3);
}
export function homeItemArtwork(kind,id){
  const wood='#b88b65',light='#e7c69b',dark='#654f48',mint='#afd0ba',pink='#d7a6ae',blue='#92bacb';
  const feet=(x=17,y=53,w=46)=>rect(x,y,5,7,dark,1)+rect(x+w-5,y,5,7,dark,1);
  if(kind==='wall')return rect(8,8,64,58,palettes[id]?.[0]||palettes.teal[0],8)+path('M8 52h64v14H8Z',palettes[id]?.[1]||palettes.teal[1])+rect(18,18,22,24,'#bfdad2',3)+rect(21,21,16,18,'#78b4ba',1);
  const painting=(inside)=>rect(12,9,56,61,wood,3)+rect(17,14,46,51,'#e3dec7',1)+inside+path('M14 11h52','none',light,1);
  if(kind==='bowl')return '<g transform="translate(0 22)">'+foodBowlArtwork(id)+'</g>';
  const art={
    'painting:landscape':painting(rect(18,15,44,49,'#cdd9c4',1)+circle(50,28,7,'#edcb90')+path('M18 59 33 37l12 14 11-12 6 20Z','#86a99c')+path('M18 63 40 48l22 15Z','#60877d')),
    'painting:moon':painting(rect(18,15,44,49,'#536a88',1)+circle(44,30,9,'#ece3bf')+circle(48,27,7,'#536a88')+path('M18 58 32 43l13 12 17-16v25H18Z','#7c98a2')+circle(27,26,1.2,'#d9e0ce')+circle(53,41,1.2,'#d9e0ce')),
    'painting:abstract':painting(rect(18,15,44,49,'#e5d9c4',1)+circle(36,33,13,pink)+rect(37,32,19,25,blue,1)+path('M22 55 41 40l9 20Z',mint)),
    'painting:starmap':painting(rect(18,15,44,49,'#425f79',1)+path('M25 29l14 7 13-13m-13 13 9 18-22-7Z','none','#b6c9d3',1)+[[25,29],[39,36],[52,23],[48,54],[26,47]].map(([x,y])=>circle(x,y,2,'#ead3a1')).join('')),
    'shelf:empty':rect(8,45,64,6,wood,2)+path('M16 51v8m48-8v8','none',dark,3)+path('M10 46h60','none',light,1),
    'shelf:books':rect(8,45,64,6,wood,2)+[18,27,36,45].map((x,i)=>rect(x,22+i%2*5,7,23-i%2*5,[mint,pink,blue,light][i],1)+rect(x+1,38,5,1,'#e7dfc1',0)).join('')+path('M16 51v8m48-8v8','none',dark,3),
    'shelf:plants':rect(8,45,64,6,wood,2)+[23,55].map((x,i)=>path(`M${x-8} 33h16l-3 12h-10Z`,i?pink:light)+path(`M${x} 34V15m0 9q-13-14-13-6 1 6 13 6m0 5q15-16 14-9-2 7-14 9`,mint,'#7b9e7c',1)).join('')+path('M16 51v8m48-8v8','none',dark,3),
    'curtains:linen':curtainIcon('#d8c9a8'),
    'curtains:sage':curtainIcon('#92af9e'),
    'curtains:striped':curtainIcon('#b8c4cf',true),
    'curtains:navy':curtainIcon('#647c9f'),
    'rug:striped':rect(8,23,64,36,mint,3)+[29,38,47].map(y=>rect(11,y,58,5,blue,1)).join('')+path('M12 21v-4m14 4v-4m14 4v-4m14 4v-4m14 4v-4M12 61v4m14-4v4m14-4v4m14-4v4m14-4v4','none',light,2),
    'rug:round':`<ellipse cx="40" cy="42" rx="35" ry="18" fill="${mint}"/><ellipse cx="40" cy="42" rx="29" ry="13" fill="#709b96" stroke="#d0e4cf" stroke-width="2"/><ellipse cx="40" cy="42" rx="22" ry="8" fill="${mint}"/>`,
    'rug:woven':path('M9 22h62v37H9Z',light)+path('M14 27h52m-52 7h52m-52 7h52m-52 7h52m-52 7h52','none','#947b66',2)+path('M11 20v-5m9 5v-5m9 5v-5m9 5v-5m9 5v-5m9 5v-5m9 5v-5M11 61v5m9-5v5m9-5v5m9-5v5m9-5v5m9-5v5m9-5v5','none',light,2),
    'rug:star':path('m40 9 11 20 23 4-17 16 4 24-21-12-21 12 4-24L6 33l23-4Z','#d4b888','#f0d4a2',2)+circle(40,42,9,'#af9db7'),
    'rug:cloud':path('M12 54C-1 50 4 31 18 32c0-23 37-24 43-3 24-1 26 28 7 31H17Z','#d4d5e5','#b6bed5',2),
    'rug:patchwork':rect(7,20,66,43,'#c5b39b',3)+rect(11,24,19,16,mint,1)+rect(32,24,16,16,pink,1)+rect(50,24,19,16,blue,1)+rect(11,42,19,17,blue,1)+rect(32,42,16,17,light,1)+rect(50,42,19,17,mint,1),
    'rug:leaf':path('M10 57Q0 10 69 15q13 51-51 51Z',mint,'#7eaa91',2)+path('m19 59 43-36M29 49l-8-16m17 8 21 3m-8-15-4-9','none','#7eaa91',2),
    'furniture:stool':feet(20,39,40)+rect(15,28,50,12,wood,4)+rect(17,26,46,7,light,4)+path('M24 48h32','none',dark,3),
    'furniture:cushion':`<ellipse cx="40" cy="49" rx="30" ry="9" fill="${dark}"/>`+path('M11 37q29-20 58 0v14q-29 14-58 0Z','#e2c396','#edd9b3',2)+path('M18 44q22 8 44 0','none','#b28d68',2),
    'furniture:chair':feet()+rect(21,13,38,33,pink,8)+rect(14,33,52,24,'#ac7f8d',5)+rect(24,36,32,13,'#edbbc2',4)+rect(14,31,9,23,'#cf9da9',4)+rect(57,31,9,23,'#cf9da9',4)+circle(39,29,2,'#edbbc2'),
    'furniture:desk':feet(13,40,54)+rect(8,32,64,9,wood,2)+rect(46,42,19,10,light,2)+circle(56,47,1.6,dark)+rect(20,11,27,19,blue,2)+rect(32,28,3,5,dark,1),
    'furniture:sofa':feet(9,57,62)+rect(13,23,54,24,blue,7)+rect(6,39,68,21,'#6795a4',5)+rect(13,38,26,14,'#acd1d5',3)+rect(41,38,26,14,'#acd1d5',3)+rect(6,32,9,25,blue,4)+rect(65,32,9,25,blue,4),
    'furniture:bed':feet(9,56,63)+rect(9,22,8,34,wood,2)+rect(13,35,59,20,light,3)+rect(19,31,15,13,'#efe5d0',3)+path('M38 35h34v20H38Z',mint)+path('M46 37v16m9-16v16m9-16v16','none','#c8e3c6',2),
    'furniture:beanbag':path('M11 55C5 36 23 13 40 15s33 21 28 40q-28 14-57 0Z','#b9abd1','#8b7baf',2)+path('M22 39q18 17 39 0','none','#d7c9e4',2),
    'furniture:table':feet(20,42,40)+`<ellipse cx="40" cy="32" rx="32" ry="13" fill="${wood}"/><ellipse cx="40" cy="29" rx="32" ry="12" fill="${light}"/>`+rect(32,13,13,14,mint,2)+path('M45 16h5v8h-5','none',mint,2),
    'furniture:booknook':feet(12,57,56)+rect(10,12,60,45,wood,3)+rect(15,17,23,34,'#70564a',1)+rect(42,17,23,34,'#70564a',1)+[18,23,29].map((x,i)=>rect(x,26,4,21,[mint,pink,blue][i],1)).join('')+rect(43,44,21,7,light,2)+rect(47,30,13,13,pink,3),
    'decor:flowers':rect(29,40,23,28,'#abd0d4',5)+path('M40 45V19m0 19-12-12m12 9 13-13','none','#69996c',2)+[[28,23,pink],[41,15,light],[55,21,blue]].map(([x,y,c])=>[[-4,0],[4,0],[0,-4],[0,4]].map(([dx,dy])=>circle(x+dx,y+dy,4,c)).join('')+circle(x,y,2,'#b79762')).join(''),
    'decor:photo':rect(16,13,48,48,wood,3)+rect(21,18,38,38,'#d4d6b6',1)+circle(47,29,6,light)+path('M21 51 32 35l11 10 9-8 7 14Z','#81aaa0')+path('M31 62h18v4H31Z',dark),
    'decor:plant':path('M27 45h27l-5 24H32Z',wood,light,1)+path('M40 46V19','none','#759b72',3)+path('M39 34C9 30 13 9 26 18q12 10 13 16M42 28C45 8 65 9 63 19c-2 9-15 10-21 9',mint,'#69996c',1),
    'decor:lamp':rect(24,64,32,5,dark,2)+path('M38 37h4v28h-4Z',wood)+path('M17 37 26 9h28l9 28Z',light,'#96764e',2)+path('M21 38h38l10 26H11Z','#f7e3a521')+circle(40,40,4,'#ffdfa2'),
    'decor:books':rect(13,8,54,62,wood,2)+rect(18,13,44,23,dark,1)+rect(18,41,44,23,dark,1)+[22,31,41,50].map((x,i)=>rect(x,17+i%2*3,6,16-i%2*3,[mint,pink,blue,light][i],1)+rect(x,47,6,14,[light,blue,pink,mint][i],1)).join(''),
    'decor:stars':path('M10 8h60M22 8v21m18-21v38M59 8v23','none',light,2)+[ [22,35],[40,52],[59,37] ].map(([x,y])=>path(`m${x} ${y-8} 3 5 6 1-4 4 1 6-6-3-6 3 1-6-4-4 6-1Z`,light)).join(''),
    'decor:clock':circle(40,38,27,wood)+circle(40,38,22,'#e4dbbc')+path('M40 22v16l12 8','none',dark,3)+[ [40,20],[57,38],[40,56],[23,38] ].map(([x,y])=>circle(x,y,1.4,dark)).join(''),
    'decor:aquarium':rect(6,18,68,47,dark,3)+rect(10,22,60,37,'#79bdc9',1)+path('M10 54q15-4 30 0t30 0v5H10Z',light)+path('M22 55V34m0 8-6-8m6 12 7-8','none',mint,2)+path('M41 41q8-9 17 0-9 9-17 0l-6 5V36Z',pink)+circle(54,39,1,dark)+circle(60,29,2,'#c8edf1')+circle(55,34,1,'#c8edf1'),
    'decor:poster':rect(16,8,48,60,wood,2)+rect(20,12,40,52,'#cfbdde',1)+circle(41,31,12,light)+path('M20 54 37 32l12 14 11-11v29H20Z','#8aaa9a'),
    'decor:terrarium':path('M26 10h28l15 18-9 35H20L11 28Z','#a7ced244','#a7ced2',2)+path('M26 10 20 63m34-53 6 53M11 28h58','none','#a7ced2',1)+path('M21 54q20-11 38 0l1 9H20Z',wood)+path('M39 52V34m0 5q-12-14-13-6 0 7 13 6m0 6q17-12 12-16-12 0-12 16',mint),
    'decor:lights':path('M5 20q35 25 70 0','none',dark,2)+[ [14,26],[29,33],[45,33],[62,26] ].map(([x,y],i)=>path(`M${x} ${y}v4`,'none',dark,2)+circle(x,y+8,5,[light,pink,mint,blue][i])).join(''),
    'decor:music':rect(9,21,62,42,wood,4)+rect(13,25,54,25,'#e2cba5',2)+circle(31,37,10,dark)+circle(31,37,4,pink)+path('M53 28v8L41 45','none','#8d7160',3)+rect(14,55,36,3,dark,1)+circle(60,55,3,mint)
  };
  return art[kind+':'+id]||'';
}
export function pipItemIcon(key){
  const [kind,id]=(key||'').split(':');
  if(id==='none'&&kind?.startsWith('home.'))return '<svg class="pip-item-art" viewBox="0 0 80 80" aria-hidden="true"><path d="M22 40h36" fill="none" stroke="#c1d5d0" stroke-width="3" stroke-linecap="round"/></svg>';
  const art=kind==='accessory'?accessoryArtwork(id):homeItemArtwork(kind?.replace('home.',''),id);
  return art?`<svg class="pip-item-art" viewBox="0 0 ${kind==='accessory'?64:80} ${kind==='accessory'?64:80}" aria-hidden="true">${art}</svg>`:'';
}
export function curtainArtwork(style='linen'){
  if(style==='none')return '';
  const fabric={linen:'#d8c9a8',sage:'#92af9e',striped:'#b8c4cf',navy:'#647c9f'}[style]||'#d8c9a8';
  return `<path d="M20 37h15v103l-18 9Zm130 0h15l3 112-18-9Z" fill="${fabric}"/><path d="M22 43v96m135-96v96" stroke="${style==='striped'?'#edf0dd':'#f3e6c5'}" stroke-opacity="${style==='striped'?'.8':'.35'}" stroke-width="3"/>`;
}
export function pipRoomScene(wall='teal',home={}){
  const [a,b]=palettes[wall]||palettes.teal,night=wall==='night';
  const curtains=home.curtains||'linen',fabric={linen:'#d8c9a8',sage:'#92af9e',striped:'#b8c4cf',navy:'#647c9f'}[curtains]||'#d8c9a8';
  const folds=curtains==='striped'?'#edf0dd':'#f3e6c5';
  return `<svg class="pip-room-scene" viewBox="0 0 500 310" preserveAspectRatio="none" aria-hidden="true"><defs><linearGradient id="pip-wall-gradient" x2=".8" y2="1"><stop stop-color="${a}"/><stop offset="1" stop-color="${b}"/></linearGradient><linearGradient id="pip-floor-gradient" x2="0" y2="1"><stop stop-color="#b39678"/><stop offset="1" stop-color="#796f64"/></linearGradient><linearGradient id="pip-window-gradient" x2="0" y2="1"><stop stop-color="${night?'#35476b':'#86c5ce'}"/><stop offset="1" stop-color="${night?'#626f92':'#daead5'}"/></linearGradient><radialGradient id="pip-room-light"><stop stop-color="#f8e1ab" stop-opacity=".2"/><stop offset="1" stop-color="#f8e1ab" stop-opacity="0"/></radialGradient></defs><path fill="url(#pip-wall-gradient)" d="M0 0h500v222H0Z"/><path d="M0 18h500M0 210h500" stroke="#dbe3cd" stroke-opacity=".22" stroke-width="3"/><path d="M0 215h500v95H0Z" fill="url(#pip-floor-gradient)"/><path d="M0 240h500M0 266h500M0 292h500M82 215l-24 95M182 215l-8 95M285 215l12 95M389 215l32 95" stroke="#e7d5b6" stroke-opacity=".2"/><path d="M0 217h500" stroke="#546556" stroke-width="5"/><ellipse cx="135" cy="170" rx="160" ry="130" fill="url(#pip-room-light)"/><rect x="33" y="39" width="120" height="113" rx="19" fill="#1e4145" opacity=".2"/><rect x="35" y="35" width="112" height="109" rx="16" fill="#e2dec1"/><rect x="41" y="41" width="100" height="97" rx="12" fill="url(#pip-window-gradient)"/><path d="M42 109q33-35 55-14t43 4v38H42Z" fill="${night?'#576875':'#7da98e'}"/><path d="M42 121q40-21 99-6v22H42Z" fill="${night?'#405b66':'#4d8a80'}"/>${circle(117,64,10,night?'#ede8ce':'#f6dc9d')}<path d="M91 40v97m-48-47h97" stroke="#dce3cb" stroke-width="4"/><path d="M18 31h147M24 37v111m135-111v111" stroke="#aa937b" stroke-width="4" stroke-linecap="round"/>${curtains==='none'?'':`<g class="pip-room-curtains" data-curtain-style="${curtains}"><path d="M20 37h15v103l-18 9Zm130 0h15l3 112-18-9Z" fill="${fabric}"/><path d="M22 43v96m135-96v96" stroke="${folds}" stroke-opacity="${curtains==='striped'?'.8':'.35'}" stroke-width="3"/></g>`}<path d="M30 147h122" stroke="#d5c8aa" stroke-width="6" stroke-linecap="round"/><path d="M5 5h490v300H5Z" fill="none" stroke="#ffffff0c" stroke-width="2"/></svg>`;
}
