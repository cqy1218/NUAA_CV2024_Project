from got10k.experiments import ExperimentGOT10k

report_files = ['reports/GOT-10k/performance_25_entries.json']
tracker_names = ['KCF', 'STMTrack', 'TATrack']

# setup experiment and plot curves
experiment = ExperimentGOT10k('data/GOT-10k', subset='test')
experiment.plot_curves(report_files, tracker_names)