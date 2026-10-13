import {escapeHTML as esc} from './engine.js?build=121';
const fmt=n=>Number(n.toFixed(3));
let controlSequence=0;
export function scienceValue(model,a,b){
  if(model===3)return Math.min(a,b);
  if(model===4||model===11)return a/b;
  if(model===7)return a*b;
  if(model===10)return a*2;
  if(model===12)return Math.min(20,a*b);
  return a;
}
export function mountScienceVisual({host,model,phase,state,save,html}){
  host.classList.add("workshop");const second=phase===3;
  if([2,6,8].includes(model)){
    const groups={
      2:{title:'Choose a material for a rain cover.',items:[
        ['Paper','Water can weaken ordinary paper. It is light, but that alone does not make a rain cover effective.','Match several properties to the job: water resistance, strength, weight, and reuse.'],
        ['Plastic sheet','An intact plastic sheet can resist water, but holes or uncovered edges can still let water in.','A material property does not guarantee the whole design. Consider joins and damage.'],
        ['Cotton cloth','Ordinary cotton cloth absorbs water. It may be washable, but it is not automatically waterproof.','Test comparable pieces under the same conditions rather than trusting the product name.']]},
      6:{title:'Compare particle models. The number of particles stays the same.',items:[
        ['Solid','Particles stay near fixed positions and vibrate. This static picture shows positions, not their movement.','Melting does not make particles disappear. Energy changes their arrangement and motion.'],
        ['Liquid','Particles remain close but can move past one another. A liquid changes shape to fit its container.','These dots are a simplified model, not a photograph or a scale drawing of molecules.'],
        ['Gas','Particles are much farther apart and move through the available space.','Different substances change state at different conditions. This picture does not simulate temperature.']]},
      8:{title:'Explore parts of a typical animal cell.',items:[
        ['Membrane','The outer boundary controls exchange between the cell and its surroundings.','It is selective, not a completely sealed wall.'],
        ['Nucleus','The nucleus contains much of the cell’s genetic information.','Not every cell has a nucleus. This is a typical animal-cell model.'],
        ['Ribosomes','Ribosomes build proteins from amino acids using genetic instructions.','Proteins do many jobs; they are not only something in food.'],
        ['Mitochondria','Mitochondria help transfer energy from nutrients into a form the cell can use.','They transform energy; they do not create it from nothing.']]},
    },g=groups[model];state.pick=Number.isInteger(state.pick)&&state.pick>=0&&state.pick<g.items.length?state.pick:0;
    host.innerHTML='<h4>'+esc(g.title)+'</h4><div class="visual-actions">'+g.items.map((r,i)=>'<button type="button" data-pick="'+i+'" aria-pressed="'+(state.pick===i)+'">'+esc(r[0])+'</button>').join('')+'</div><div class="model-picture"></div><p class="lab-feedback" role="status"></p><p class="model-limit legend"></p>';
    const draw=()=>{const r=g.items[state.pick];host.querySelector('.lab-feedback').textContent=r[1];host.querySelector('.model-limit').textContent=r[2];
      host.querySelector('.model-picture').innerHTML=model===6?'<svg viewBox="0 0 300 140" role="img" aria-label="'+esc(r[0]+': same 12 particles, different arrangement')+'"><rect x="5" y="5" width="290" height="130" rx="12" fill="none" stroke="currentColor"/>'+Array.from({length:12},(_,i)=>{const x=state.pick===0?110+(i%4)*20:state.pick===1?95+(i%4)*27+(Math.floor(i/4)%2)*8:25+(i%4)*80,y=state.pick===0?57+Math.floor(i/4)*20:state.pick===1?70+Math.floor(i/4)*24:23+Math.floor(i/4)*47;return '<circle cx="'+x+'" cy="'+y+'" r="7" fill="currentColor"/>';}).join('')+'</svg>':model===8?'<svg viewBox="0 0 300 150" role="img" aria-label="Simplified animal cell with highlighted '+esc(r[0])+'"><ellipse cx="150" cy="75" rx="128" ry="63" fill="#ffffff90" stroke="'+(state.pick===0?'#edbc82':'#7dcac5')+'" stroke-width="5"/><circle cx="140" cy="70" r="29" fill="'+(state.pick===1?'#edbc82':'#b1ace2')+'"/>'+[65,100,195,235].map((x,i)=>'<circle cx="'+x+'" cy="'+(45+i%2*57)+'" r="5" fill="'+(state.pick===2?'#edbc82':'#7dcac5')+'"/>').join('')+'<ellipse cx="205" cy="85" rx="19" ry="10" fill="'+(state.pick===3?'#edbc82':'#7d9294')+'"/></svg>':'';};
    host.querySelectorAll('[data-pick]').forEach(b=>b.onclick=()=>{state.pick=Number(b.dataset.pick);host.querySelectorAll('[data-pick]').forEach(x=>x.setAttribute('aria-pressed',x===b));save();draw();});draw();return;
  }
  const wave=model===11&&second;
  const c=wave?['Waves: frequency changes cycles, amplitude changes height.','Frequency (cycles per second)',1,6,2,'Amplitude (illustrative units)',1,4,2]:
    ({3:['A made-up habitat: each animal needs one food portion and one shelter.','Food portions',0,12,5,'Shelter places',0,12,8],
      // Starting positions differ from the lesson tasks, so the model never shows a task's answer before you set it.
      4:['An ideal cart: change force or mass.','Force in newtons',0,20,8,'Mass in kilograms',1,10,5],
      7:['Energy depends on power and time.','Power in watts',1,20,3,'Time in seconds',1,12,7],
      10:['Balance a symbolic reaction: A₂ + B₂ → 2AB.','Reacting pairs (one A₂ and one B₂)',1,6,2,'',1,1,1],
      11:['An ideal resistor: change voltage or resistance.','Voltage in volts',0,12,9,'Resistance in ohms',1,12,4],
      12:['A tank holds at most 20 litres. Compare a limited model with unchecked growth.','Flow in litres per minute',1,6,2,'Minutes',0,12,5]})[model];
  state.a=Number.isFinite(state.a)?Math.max(c[2],Math.min(c[3],Math.round(state.a))):c[4];
  state.b=Number.isFinite(state.b)?Math.max(c[6],Math.min(c[7],Math.round(state.b))):c[8];
  const controlScope='science-control-'+(++controlSequence);
  host.innerHTML='<p>'+html(c[0])+'</p>'+[['a',1,2,3],['b',5,6,7]].filter(x=>c[x[1]]).map(([k,l,min,max])=>{const id=controlScope+'-'+k;return '<label class="field" for="'+id+'"><span>'+esc(c[l])+': <output for="'+id+'" aria-hidden="true" data-out="'+k+'"></output></span><input id="'+id+'" type="range" data-control="'+k+'" min="'+c[min]+'" max="'+c[max]+'" value="'+state[k]+'"></label>';}).join('')+'<div class="model-picture"></div><div class="visual-value" id="visual-value" role="status"></div><p class="model-limit legend"></p><div class="model-prediction"></div>';
  const draw=()=>{
    const a=state.a,b=state.b,v=scienceValue(model,a,b),equal=v===fmt(v)?'=':'\\approx';
    host.querySelectorAll('[data-out]').forEach(o=>o.textContent=state[o.dataset.out]);
    const result=wave?'$f='+a+'\\ \\mathrm{Hz},\\quad A='+b+'$':({3:'$\\min('+a+','+b+')='+v+'$ animals supported in this model',4:'$a=\\frac{F}{m}=\\frac{'+a+'}{'+b+'}'+equal+fmt(v)+'\\ \\mathrm{m/s^2}$',7:'$E=Pt='+a+'\\times'+b+'='+v+'\\ \\mathrm{J}$',10:'$'+a+'\\mathrm{A_2}+'+a+'\\mathrm{B_2}\\longrightarrow'+2*a+'\\mathrm{AB}$',11:'$I=\\frac{V}{R}=\\frac{'+a+'}{'+b+'}'+equal+fmt(v)+'\\ \\mathrm{A}$',12:'$V=\\min(20,'+a+'\\times'+b+')='+v+'\\ \\mathrm{L}$'})[model];
    host.querySelector('#visual-value').innerHTML=html(result);
    const limits={3:'Illustrative limiting-resource model only. Real habitats involve many changing factors; this is not a real population forecast.',4:'Assumes constant net force and mass. Friction is omitted. Acceleration is change in velocity, not velocity itself.',7:'Assumes constant power. The same energy can result from different combinations of power and time.',10:'A and B are symbolic atoms, not chemicals to mix. Both sides contain the same number of each atom; atoms are rearranged.',11:wave?'This picture spans one second. More cycles means higher frequency; greater height means greater amplitude. They are independent.':'Assumes an ideal ohmic resistor. This is a screen model, not instructions to connect to mains electricity.',12:'Assumes an empty tank, constant inflow, no outflow, and overflow once full. Unchecked growth would wrongly exceed capacity.'};
    host.querySelector('.model-limit').textContent=limits[model];
    let picture='';
    if(wave){const pts=Array.from({length:181},(_,i)=>i*1.5+','+(70-Math.sin(i/180*Math.PI*2*a)*b*12));picture='<path d="M0 70h270" stroke="#73898a"/><polyline points="'+pts.join(' ')+'" fill="none" stroke="currentColor" stroke-width="3"/>';}
    else if(model===10)picture=Array.from({length:2*a},(_,i)=>'<circle cx="'+(25+i%6*45)+'" cy="'+(35+Math.floor(i/6)*55)+'" r="10" fill="#7ba9ec"/><circle cx="'+(40+i%6*45)+'" cy="'+(35+Math.floor(i/6)*55)+'" r="10" fill="#edbc82"/>').join('');
    else {const max={3:12,4:20,7:240,11:12,12:20}[model];picture='<rect x="10" y="45" width="280" height="42" rx="8" fill="#ffffffa0"/><rect x="10" y="45" width="'+(v/max*280)+'" height="42" rx="8" fill="currentColor"/>';}
    host.querySelector('.model-picture').innerHTML='<svg viewBox="0 0 300 140" role="img" aria-label="'+esc(wave?'Wave for selected frequency and amplitude':'Model output '+fmt(v))+'">'+picture+'</svg>';
  };
  host.querySelectorAll('[data-control]').forEach(e=>e.oninput=()=>{state[e.dataset.control]=Number(e.value);save();draw();});draw();
}
