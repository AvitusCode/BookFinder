

class GlobalOptions(object):
    def __init__(self):
        self.is_debug: bool = False
        # image options
        self.resize: int = 1024

        # gauss blur if need
        self.is_gaussian_blur: bool = False
        self.gauss_filter_size: int = 5
        self.gauss_sigma: float     = 0.6

        # Morfological transform if need
        self.is_image_close: bool = False
        self.close_size: int      = 5

        # canny options
        self.canny_low_threshold: int  = 50
        self.canny_high_threshold: int = 150
        self.connectivity: int         = 8

        # remove short clusters options
        self.remove_short_clusters_threshold: int = 200

        # final border algorithm options
        self.hough_min_votes: int = 130
        self.theta_threshold: int = 50

        # fuzzy logic options
        self.fuzzy_reliability: int = 75

        # Download info from database
        self.is_need_web_info: bool = False
        self.web_database_url: str  = 'https://www.livelib.ru/books/filming/listview/biglist/~'
        self.web_pages_count: int   = 2
