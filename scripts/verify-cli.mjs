import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
const localPackage=resolve('node_modules/genlayer/package.json');
if (!existsSync(localPackage)) {
  console.error('Missing repo-local genlayer. Run npm ci (never the global 0.40.x CLI).');
  process.exit(1);
}
const pkg=JSON.parse(readFileSync(localPackage,'utf8'));
if (pkg.version!=='0.39.1'){
 console.error(`Wrong local GenLayer CLI: ${pkg.version}; expected exactly 0.39.1`);
 process.exit(1);
}
const declared=JSON.parse(readFileSync('package.json','utf8'));
if (declared.devDependencies.genlayer!=='0.39.1'){
 console.error('package.json CLI requirement was changed. Refusing.');
 process.exit(1);
}
console.log(`PASS: local genlayer ${pkg.version}. Global CLI ignored.`);
