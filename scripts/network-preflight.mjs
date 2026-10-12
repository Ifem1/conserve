const chain=Number(process.env.CONSERVE_CHAIN_ID || '61999');
const rpc=process.env.CONSERVE_RPC || 'https://studio.genlayer.com/api';
if (chain !== 61999 || rpc !== 'https://studio.genlayer.com/api') {
  console.error('FAIL: This repo targets chain 61999 at exactly https://studio.genlayer.com/api');
  process.exit(1);
}
const request = async (method) => {
 const response=await fetch(rpc, {method:'POST',headers:{'content-type':'application/json'},
 body:JSON.stringify({jsonrpc:'2.0',id:1,method,params:[]}),signal:AbortSignal.timeout(10000)});
 if(!response.ok) throw new Error(`HTTP ${response.status}`);
 const body=await response.json();
 if(body.error) throw new Error(JSON.stringify(body.error));
 return body.result;
};
const parseChain = (v) => typeof v === 'string' && v.startsWith('0x') ? parseInt(v,16) : Number(v);
let observed;
try {observed=parseChain(await request('eth_chainId'));}
catch(e) {console.error(`Cannot safely verify RPC eth_chainId: ${e.message}`);process.exit(1);}
if (observed !== 61999){
  console.error(`FAIL: RPC chain id ${observed}; expected 61999. No deployment allowed.`);
  process.exit(1);
}
console.log('PASS: canonical stable StudioNet RPC and chain ID 61999.');
