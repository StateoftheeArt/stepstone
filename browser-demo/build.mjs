import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.dirname(here), out=path.join(here,'dist');
await fs.mkdir(out,{recursive:true});
await fs.cp(path.join(root,'public'),out,{recursive:true});
await fs.rm(path.join(out,'sw.js'),{force:true});
await fs.cp(path.join(here,'overrides'),out,{recursive:true});
const release=(await fs.readFile(path.join(root,'public','release.js'),'utf8')).match(/INTERFACE_BUILD=(\d+)/)[1];
for(const name of await fs.readdir(out)){
  if(!/\.(?:js|css|html|webmanifest)$/.test(name))continue;
  const file=path.join(out,name), text=await fs.readFile(file,'utf8');
  await fs.writeFile(file,text.replace(/\?build=\d+/g,'?build='+release).replace(/\?demo=\d+/g,'?demo=4').replace(/data-demo-release="\d+"/g,'data-demo-release="4"'));
}
await fs.copyFile(path.join(root,'content','checkpoints.json'),path.join(out,'preview-checks.json'));
for(const name of ['LICENSE','THIRD_PARTY_NOTICES.md'])await fs.copyFile(path.join(root,name),path.join(out,name));
console.log('Browser demo built in browser-demo/dist. Serve that directory to try it.');
