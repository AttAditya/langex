from langex.core.pipeline import Pipeline
from langex.core.testing import discover_test, expects

process1 = lambda incoming: 1 if incoming is None else incoming
process2 = lambda incoming: incoming * 2
process3 = lambda incoming: incoming + 2
pipeline = (
  Pipeline
  | process1
  | process2
  | process3
)

@discover_test
def test_pipeline():
  (lambda: pipeline.run()  ) @expects (4)
  (lambda: pipeline.run(10)) @expects (4)

