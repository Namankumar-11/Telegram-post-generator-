import os
import json
import pandas as pd

class FewShotPosts:
    def __init__(self, file_path=None):
        self.df = None
        self.unique_tags = []
        
        if file_path is None:
            # Dynamically locate the folder where few_shot.py lives
            base_dir = os.path.dirname(os.path.abspath(__file__))
            # Read directly from the root folder since processed_posts.json is next to main.py
            file_path = os.path.join(base_dir, "processed_posts.json")
            
        self.load_posts(file_path)

    def load_posts(self, file_path):
        if not os.path.exists(file_path):
            self.df = pd.DataFrame(columns=['text', 'engagement', 'line_count', 'language', 'tags', 'length'])
            self.unique_tags = ["General"]
            return

        try:
            with open(file_path, encoding="utf-8") as f:
                posts = json.load(f)
                self.df = pd.json_normalize(posts)
                
                if not self.df.empty and 'line_count' in self.df.columns:
                    self.df['length'] = self.df['line_count'].apply(self.categorize_length)
                    all_tags = self.df['tags'].apply(lambda x: x if isinstance(x, list) else []).sum()
                    self.unique_tags = sorted(list(set(all_tags)))
                else:
                    self.unique_tags = ["General"]
        except Exception:
            self.df = pd.DataFrame(columns=['text', 'engagement', 'line_count', 'language', 'tags', 'length'])
            self.unique_tags = ["General"]

    def categorize_length(self, line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_tags(self):
        return self.unique_tags

    def get_filtered_posts(self, length, language, tag):
        if self.df is None or self.df.empty:
            return []
            
        try:
            df_filtered = self.df[
                (self.df['tags'].apply(lambda tags: isinstance(tags, list) and tag.lower() in [t.lower() for t in tags])) & 
                (self.df['language'].str.lower() == language.lower()) & 
                (self.df['length'] == length) 
            ]
            return df_filtered.to_dict(orient='records')
        except Exception:
            return []
