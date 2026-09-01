class RootCauseClassifier:
    def __init__(self):
        self.model = None
        self.label_encoder = None
        
    def train(self, X, y):
        pass
        
    def predict(self, features) -> tuple:
        return "NETWORK_FAILURE", 0.6
        
    def save(self, path):
        pass
        
    def load(self, path):
        pass
        
    def get_fallback_prediction(self, event, payment) -> tuple:
        return "NETWORK_FAILURE", 0.6
