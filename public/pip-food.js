// A bowl is measured in elapsed seconds, so closing the app never pauses eating.
export const FOOD_PORTION=1800,FOOD_CAPACITY=3*FOOD_PORTION;
export const FOOD_REVIEW_SECONDS=86400;
export function foodRemaining(state,now=Date.now()/1000){
  if(!state)return 0;
  const amount=Number(state.remaining)||0,at=Number(state.asOf)||now;
  return Math.max(0,Math.min(Number(state.capacity)||FOOD_CAPACITY,amount-Math.max(0,now-at)));
}
export function canPipPlay(state,now){return foodRemaining(state,now)>0;}
export function canFeedPip(state,now){return Number(state?.bank)>0&&foodRemaining(state,now)<=(Number(state?.capacity)||FOOD_CAPACITY)-(Number(state?.portionSeconds)||FOOD_PORTION);}
export function previewFood(storage,key,completed=[],now=Date.now()/1000){
  let state;try{state=JSON.parse(storage.getItem(key)||'null');}catch{}
  state=state&&Array.isArray(state.earned)?state:{bank:0,remaining:0,asOf:now,earned:[]};
  const earned=new Set(state.earned),fresh=[...new Set(completed)].filter(id=>!earned.has(id));
  const next={bank:Math.max(0,Number(state.bank)||0)+fresh.length,remaining:foodRemaining(state,now),asOf:Math.max(now,Number(state.asOf)||now),capacity:FOOD_CAPACITY,portionSeconds:FOOD_PORTION,earned:[...earned,...fresh],reviews:state.reviews||{},reviewReceipts:state.reviewReceipts||{}};
  storage.setItem(key,JSON.stringify(next));return next;
}
export function awardPreviewReview(storage,key,{unit,id,eligible=false,alreadyPassed=false,passed=false,at=Date.now()/1000},completed=[]){
  const state=previewFood(storage,key,completed,at);
  if(state.reviewReceipts[id])return state.reviewReceipts[id];
  let award={pipFoodEarned:0,pipFoodReason:'none'};
  if(passed&&!alreadyPassed)award={pipFoodEarned:1,pipFoodReason:'first'};
  else if(passed&&eligible){
    const nextAt=(state.reviews[unit]??-Infinity)+FOOD_REVIEW_SECONDS;
    award=at<nextAt?{pipFoodEarned:0,pipFoodReason:'cooldown',pipFoodNextAt:nextAt}:{pipFoodEarned:1,pipFoodReason:'review',pipFoodNextAt:at+FOOD_REVIEW_SECONDS};
    if(award.pipFoodEarned){state.bank+=1;state.reviews[unit]=at;}
  }
  state.reviewReceipts[id]=award;storage.setItem(key,JSON.stringify(state));return award;
}
export function feedPreviewFood(storage,key,completed=[],now=Date.now()/1000){
  const state=previewFood(storage,key,completed,now);
  if(!canFeedPip(state,now))throw Error(state.bank?'Pip’s bowl has enough food for now.':'Complete a new module or replay a food-review module to earn food for Pip.');
  const next={...state,bank:state.bank-1,remaining:state.remaining+FOOD_PORTION};
  storage.setItem(key,JSON.stringify(next));return next;
}
