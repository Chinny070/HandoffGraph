// Read-only, fail-closed stable GenLayer StudioNet RPC identity check.
// Does NOT deploy, estimate, sign, or submit any transaction.
const rpc = 'https://studio.genlayer.com/api';
const controller = new AbortController();
const timer = setTimeout(() => controller.abort(), 12000);
try {
  const response = await fetch(rpc, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'eth_chainId', params: [] }),
    signal: controller.signal,
  });
  if (!response.ok) throw new Error(`RPC_HTTP_${response.status}`);
  const data = await response.json();
  if (data.error || typeof data.result !== 'string') throw new Error('RPC_INVALID_REPLY');
  const chain = Number.parseInt(data.result, 16);
  if (chain !== 61999) throw new Error(`WRONG_NETWORK_${chain}`);
  process.stdout.write(`StudioNet VERIFIED via ${rpc}: chain ${chain}\n`);
} catch (e) {
  process.stderr.write(`StudioNet preflight failed: ${e.message}\n`);
  process.exitCode = 1;
} finally { clearTimeout(timer); }
