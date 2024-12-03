from dataclasses import dataclass

@dataclass
class DataIngestionArtifacts:
    trained_filed_path : str
    test_filed_path : str