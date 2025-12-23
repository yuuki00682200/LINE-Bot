import traceback
import asyncio
import time


class Trace:
    def __init__(self, client, poll=True):
        self.client = client
        self.poll = poll
        self.error  = []
        self.revision = self.client.run(self.get_revision())

    async def fetch(self, count=1):
        try:
            ops = await self.client.fetchOperations(self.revision, count)
        except Exception:
            ops = []
        return ops

    async def get_revision(self):
        self.revision = await self.client.getLastOpRevision(False)
        if self.revision == 0:
            ops = [op for op in await self.fetch(100) if op.revision > 0]
            return ops[-1].revision
        else:
            return self.revision

    def set_revision(self, rev):
        self.revision = max(rev)

    async def _start(self, main_coro, count=1):
        while True:
            try:
                ops = await self.fetch(count)
                if ops:
                    task = [main_coro(op) for op in ops]
                    revisions = [op.revision for op in ops]
                    await asyncio.wait(task)
                    self.set_revision(revisions)
            except SystemExit:
                exit()
            except Exception:
                traceback.print_exc()
                self.error.append({time.ctime():traceback.format_exc()})

    def start(self, main_coro, count=1):
        self.client.loop.run_until_complete(self._start(main_coro, count))

