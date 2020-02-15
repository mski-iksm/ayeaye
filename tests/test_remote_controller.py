from ayeaye.remote_controller import RemoteController


class TestRemoteController():

    def setup_method(self):
        self.signal_settings = {
            'tv': {
                'device_pattern': ['テレビ', 'てれび'],
                'orders': {
                    'turn_on': {
                        'pattern': ['音', 'オン', 'つけ', '付け', '着け'],
                        'signal': [1, 2, 3]
                    },
                },
            },
        }

        self.device_phrase2name = {'テレビ': 'tv'}
        self.order_phrase2name = {'tv': {'つけて': 'turn_on'}}
        self.order_name2signal = {'tv': {'turn_on': [1, 2, 3]}}

    # detect_device
    def test_detect_device(self):
        resulted = RemoteController._detect_device('テレビをつけて', self.device_phrase2name)
        assert resulted == 'tv'

    def test_detect_device_no_matching_phrase(self):
        resulted = RemoteController._detect_device('', self.device_phrase2name)
        assert resulted is None

    # detect order
    def test_detect_order(self):
        resulted = RemoteController._detect_order('テレビをつけて', 'tv', self.order_phrase2name)
        assert resulted == 'turn_on'

    def test_detect_order_no_matching_phrase(self):
        resulted = RemoteController._detect_order('テレビを消して', 'tv', self.order_phrase2name)
        assert resulted is None

    # extract signal
    def test_extract_signal(self):
        resulted = RemoteController._extract_signal('tv', 'turn_on', self.order_name2signal)
        assert resulted == [1, 2, 3]

    def test_extract_signal_no_maching_device_name(self):
        resulted = RemoteController._extract_signal('ac', 'turn_on', self.order_name2signal)
        assert resulted is None

    def test_extract_signal_no_maching_order_name(self):
        resulted = RemoteController._extract_signal('tv', 'turn_off', self.order_name2signal)
        assert resulted is None

    # set dictionaries
    def test_detect_order_no_matching_device(self):
        resulted = RemoteController._detect_order('音楽を消して', 'music', self.order_phrase2name)
        assert resulted is None

    def test_build_device_phrase2name(self):
        resulted = RemoteController._build_device_phrase2name(self.signal_settings)
        assert resulted['てれび'] == 'tv'

    def test_build_order_phrase2name(self):
        resulted = RemoteController._build_order_phrase2name(self.signal_settings)
        assert resulted['tv']['つけ'] == 'turn_on'

    def test_build_order_name2signal(self):
        resulted = RemoteController._build_order_name2signal(self.signal_settings)
        assert resulted['tv']['turn_on'] == [1, 2, 3]
