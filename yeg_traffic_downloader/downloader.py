"""Utility class to download traffic data spreadsheets 
from City of Edmonton's Google Drive account.
"""

from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from pydrive.files import ApiRequestError, FileNotDownloadableError

import tempfile
import os


class TrafficSpreadsheetDownloader(object):
    """Utility class to download spreadsheets from Google Drive."""

    def __init__(self, output_dir=tempfile.mkdtemp()):
        """Initializes a TrafficSpreadsheetDownloader object with
        an authenticated downloader object.

        Authenticates with Google Drive and initalizes downloader
        object.

        Keyword arguments:
        gdrive_folders -- A dictionary containing the different Google
                          Drive folders. The key is the human readable name
                          and the value is the hashed value of the folder.
        """
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()

        self._drive = GoogleDrive(gauth)
        self._output_dir = output_dir

    def download_files_in_folder(self, folder_id):
        """Downloads all the files inside the folder associated with the folder ID."""
        file_list = self._drive.ListFile({
            'q': "'%s' in parents" % (folder_id,),
            'fields': 'items(id,downloadUrl,originalFilename),nextPageToken'
        }).GetList()

        if len(file_list) == 0:
            return [self.__get_result('', False, 'No files in folder to download.')]

        return [self._download_file(gdrive_file) for gdrive_file in file_list]

    def download_file_by_id(self, file_id):
        """Download the associated file with the given file id.

        Keyword arguments:
        file_id -- A file ID corresponding to a file on Google Drive.
        """
        drive_file = self._drive.CreateFile({'id': file_id})

        return self._download_file(drive_file)

    def _download_file(self, drive_file):
        """Downloads the actual file represented by the drive_file parameter.

        Keyword arguments:
        drive_file --  A DTO object created by the Google Drive API that represents
                       a file on Google Drive to be downloaded.
        """
        file_destination = os.path.join(self._output_dir, drive_file['originalFilename'])

        if os.path.exists(file_destination):
            return self.__get_result(drive_file['id'],
                                     False,
                                     '%s already exists.' % (file_destination,))

        try:
            drive_file.GetContentFile(file_destination)
        except ApiRequestError:
            return self.__get_result(drive_file['id'],
                                     False,
                                     'Unable to authenticate with Google Drive API.')
        except FileNotDownloadableError:
            return self.__get_result(drive_file['id'],
                                     False,
                                     'Unable to download file from Google Drive.')
        except Exception:
            return self.__get_result(drive_file['id'],
                                     False,
                                     'An unknown error has occurred while trying to download file.')

        return self.__get_result(drive_file['id'],
                                 True,
                                 'Successfully downloaded file.')

    @staticmethod
    def __get_result(file_id, success, message):
        """Helper method to create a results dictionary."""
        return {
            'file_id': file_id,
            'success': success,
            'message': message
        }
