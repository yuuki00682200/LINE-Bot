from .runner import Runner
from linebot.core.trace import Trace
from linebot.generated.line_api.TalkService.ttypes import TalkException
import traceback
import asyncio

class Polling(Runner):
    def __init__(self):
        self.tracers = [Trace(cl) for cl in self.clients]
        Runner.__init__(self)

    def poll(self):
        self.clients[0].run(self.main())

    async def main(self):
        while True:
            try:
                task = [self.polling(tracer) for tracer in self.tracers]
                await asyncio.gather(*task)
            except TalkException as e:
                traceback.print_exc()
            except Exception:
                traceback.print_exc()

    async def polling(self, tracer):
        ops = await tracer.fetch(100)
        index = self.tracers.index(tracer)
        if ops:
            revisions  = [op.revision for op in ops]
            tracer.set_revision(revisions)
            operations = [self.run(index, op) for op in ops]
            await asyncio.wait(operations)
    
