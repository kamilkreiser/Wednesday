// Gate 176: stands in for the optional '@blockfrost/blockfrost-js' so start() reaches its blocksLatest catch (site 133).
export class BlockFrostAPI {
  constructor() {
    return (globalThis as any).__gate176Api;
  }
}
export default { BlockFrostAPI };
