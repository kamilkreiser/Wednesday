// Gate 73: runs only the out-of-tree probe file against packages/shared/src (no tree writes).


export default {
  test: {
    root: '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate73-ks1868-auditlogger-1888/scripts/probe',
    include: ['**/*.test.ts'],
    globals: true,
  },
};
