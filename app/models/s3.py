
class S3Works():
    """
    To handle data processing from s3 before sending to RDS
    """

    def __init__(self, s3url: str, ) -> None:
        self.s3url = s3url

    def get_file_from_bucket(self, key: str, ) -> None:
        raise NotImplementedError

    def upload_file_to_bucket(self, file: str, ) -> None:
        raise NotImplementedError
    
    def delete_file_in_bucket(self, file: str, ) -> None:
        raise NotImplementedError
    