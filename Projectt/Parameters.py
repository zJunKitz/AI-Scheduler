class Parameters:
    def __init__(self, subject_name=None, undesired_days=None, threshold_start_time=None, undesired_lecturer=None):
        self.subject_name = subject_name
        self.undesired_days = undesired_days or []
        self.threshold_start_time = threshold_start_time or '23:00'
        self.undesired_lecturer = undesired_lecturer or []
        self.required_lec_slot = None

    def determine_lec_slot(self, df):
        lec_slot_count = df[df['CLASS_TYPE'] == 'LECTURE'].groupby('CLASS_ID').size()
        self.required_lec_slot = lec_slot_count.max()