from got10k.trackers import Tracker

class IdentityTracker(Tracker):
    def __init__(self):
        super(IdentityTracker, self).__init__(
            name='kcftracker',  # tracker name
            is_deterministic=False    # stochastic (False) or deterministic (True)
        )
    
    def init(self, image, box):
        self.box = box

    def update(self, image):
        return self.box

from got10k.experiments import ExperimentGOT10k

# ... tracker definition ...

# instantiate a tracker
tracker = IdentityTracker()

# setup experiment (validation subset)
experiment = ExperimentGOT10k(
    root_dir='data/GOT-10k',    # GOT-10k's root directory
    subset='test',              # 'train' | 'val' | 'test'
    result_dir='results',       # where to store tracking results
    report_dir='reports'        # where to store evaluation reports
)
experiment.run(tracker, visualize=True)

# report tracking performance
experiment.report([tracker.name])
