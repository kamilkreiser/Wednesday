// Gate 149 positive control for the PR's `unhandled` listener: the same listener shape as the PR's two files.
let unhandled = 0;
const onUnhandled = () => { unhandled += 1; };
beforeAll(() => { process.on('unhandledRejection', onUnhandled); });
afterAll(() => { process.removeListener('unhandledRejection', onUnhandled); });
beforeEach(() => { unhandled = 0; });
it('G149 PC1 a deliberate unhandled rejection is counted by the listener', async () => {
  void Promise.reject(new Error('g149 deliberate'));
  await new Promise((r) => setTimeout(r, 200));
  expect(unhandled).toBe(1);
});
it('G149 PC2 listener count seen by the test', () => {
  expect(process.listenerCount('unhandledRejection')).toBe(-1); // prints the real count in the failure
});
