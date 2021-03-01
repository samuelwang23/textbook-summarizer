class Summarizer:
    def __init__(self, scores, length):
        self.scores = scores
        self.length = length
        self._summarize()
        self._get_summary_text()

    def _summarize(self):        
        self.summary = []
        length = 0
        
        for pair in sorted(self.scores)[::-1]:
            if len(self.summary) < self.length:
                self.summary.append(pair[1])
            else:
                return
    
        return self._get_summary_text()

    def _get_summary_text(self):
        self.text = ""
        for sentence in sorted(self.summary):
            self.text += sentence.text + " "
        return self.text