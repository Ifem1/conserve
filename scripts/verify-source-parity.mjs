import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const address = process.env.CONSERVE_CONTRACT_ADDRESS;
const rpc = 'https://studio.genlayer.com/api';
if (!address || !/^0x[0-9a-fA-F]{40}$/.test(address)) {
  console.error('Set CONSERVE_CONTRACT_ADDRESS to the deployed 20-byte address.');
  process.exit(1);
}

const response = await fetch(rpc, {
  method: 'POST',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify({
    jsonrpc: '2.0', id: 1, method: 'gen_getContractCode', params: [address],
  }),
  signal: AbortSignal.timeout(15000),
});
if (!response.ok) throw new Error(`RPC HTTP ${response.status}`);
const payload = await response.json();
if (payload.error) throw new Error(JSON.stringify(payload.error));
if (typeof payload.result !== 'string') throw new Error('RPC returned no base64 source bytes');

const localPath = fileURLToPath(new URL('../contracts/conserve.py', import.meta.url));
const local = readFileSync(localPath);
const deployed = Buffer.from(payload.result, 'base64');
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const localHash = hash(local);
const deployedHash = hash(deployed);
if (!local.equals(deployed)) {
  console.error(`FAIL: source bytes differ (local=${localHash}, deployed=${deployedHash})`);
  process.exit(1);
}
console.log(`PASS: deployed source bytes match contracts/conserve.py SHA-256 ${localHash}`);
