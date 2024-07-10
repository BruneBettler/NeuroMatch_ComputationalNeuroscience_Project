from one.api import ONE
ONE.setup(base_url='https://openalyx.internationalbrainlab.org', silent=True)
one = ONE(password='international')

import numpy as np

def get_datasets():
    # Find all aggregate training datasets from paper Brujins et al
    datasets = one.alyx.rest('datasets', 'list', tag='2023_Q4_Bruijns_et_al')
    return datasets

def get_subjects(datasets):
    # Find the subject name from the info stored in the relative path
    subjects = np.unique([d['file_records'][0]['relative_path'].split('/')[-2] for d in datasets])
    return subjects # returns list of mouse names as strings

def get_trials(subject):
    # Load in the subjectTrials table for the first subject
    subject_trials = one.load_aggregate('subjects', subject, '_ibl_subjectTrials.table')
    # Add in lab, task_protocol, subject name information from the ONE cache
    if 'task_protocol' in subject_trials:
        subject_trials = subject_trials.drop('task_protocol', axis=1)
    subject_trials = subject_trials.set_index('session').join(one._cache.sessions.drop('date', axis=1))
    return subject_trials

def get_num_session(subject):
    subject_trials = get_trials(subject)
    # Find the number of sessions for this subject
    n_sessions = subject_trials.index.unique().size
    return n_sessions

def get_num_protocol_run(subject_trials):
    # Find the number of times a task protocol was run
    n_protocols = subject_trials[~subject_trials.index.duplicated()].task_protocol.value_counts()
    return n_protocols

def get_trial_data(subject_trials):
    # Get the trials data for a single session
    # Find a session run under biasedChoiceWorld
    sess = subject_trials[subject_trials['task_protocol'].str.contains('biasedChoiceWorld')].index.unique()[0]
    trials = subject_trials[subject_trials.index == sess]
    return trials


#TODO: complete the brainbox behavior code and further

if __name__ == "__main__":
    datasets = get_datasets()
    subjects = get_subjects(datasets)
    mouse0 = subjects[0]
    get_trials(mouse0)
    print("done")

