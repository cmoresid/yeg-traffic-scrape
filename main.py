"""Main driver file for downloading spreadsheet
files.
"""

import sys
import getopt
import os

from config import Config
from yeg_traffic_downloader.downloader import TrafficSpreadsheetDownloader

class CommandLineMain:
    """Command line driver to initiate downloading.
    """
    def __init__(self, config_file_name):
        """


        :param config_file_name:
        :return:
        """
        self._config_file_name = config_file_name
        self._config = Config(self._config_file_name)

    def main(self, argv):
        try:
            opts, args = getopt.getopt(argv, '', ['download-all',
                                                  'download-folder=', 'download-file=',
                                                  'import-folder=',
                                                  'output-folder='])
            self.validate_args(opts)
        except getopt.GetoptError:
            self.print_usage()
            sys.exit(2)

        if len(filter(lambda x: x[0].startswith('--download'), opts)) == 1:
            output_dir = self.get_output_folder(opts)

        # Sort arguments by order of dependence, which
        # just happens to be alphabetical.
        opts = sorted(opts, key=lambda k: k[0])

        for opt, arg in opts:
            if opt == '--download-all':
                self.download_all(output_dir)
            elif opt == '--download-folder':
                self.download_folder(arg, output_dir)
            elif opt == '--download-file':
                self.download_file(arg, output_dir)

    def download_all(self, output_folder):
        downloader = TrafficSpreadsheetDownloader(output_dir=output_folder)

        return map(downloader.download_files_in_folder,
                   self._config.settings['edmonton-data-intersection-folder-ids'].values())

    @staticmethod
    def validate_args(opts):
        options = map(lambda item: item[0], opts)

        if len(filter(lambda x: x.startswith('--download'), options)) > 1:
            raise RuntimeError('You can only specify one download-type argument.')
        elif '--download-all' in options and not ('--output-folder' in options):
            raise RuntimeError('You must specify an output folder.')
        elif '--download-folder' in options and not ('--output-folder' in options):
            raise RuntimeError('You must specify an output folder.')
        elif '--download-file' in options and not ('--output-folder' in options):
            raise RuntimeError('You must specify an output folder.')

    @staticmethod
    def download_folder(folder_id, output_folder):
        downloader = TrafficSpreadsheetDownloader(output_dir=output_folder)

        return downloader.download_files_in_folder(folder_id)

    @staticmethod
    def download_file(file_id, output_folder):
        downloader = TrafficSpreadsheetDownloader(output_dir=output_folder)

        return downloader.download_file_by_id(file_id)

    @staticmethod
    def get_output_folder(opts):
        output_folder = filter(lambda opt: opt[0] == '--output-folder', opts)[0][1]

        if not (os.path.exists(output_folder)):
            raise RuntimeError('The specified output folder does not exist.')

        return output_folder

    @staticmethod
    def validate_path(path, message):
        if not (os.path.exists(path)):
            raise RuntimeError(message)

    @staticmethod
    def print_usage():
        print 'usage: python main.py [--download-all] [--download-folder=folderId] [--download-file=fileId]'
        print '                      [--output-dir=folderPath]'
        print ''
        print 'options:'
        print ''
        print '--download-all'
        print '\tDownloads all the spreadsheets from all the folders specified in the'
        print '\t\'edmonton-data-folder-ids\' dictionary defined in config.py. This is the'
        print '\tdefault action if no parameters are specified.'
        print ''
        print '--download-folder=folderId'
        print '\tDownload all the spreadsheets located in the Google Drive folder. The'
        print '\tfolder ID will be an alpha-numeric string of 61 characters.'
        print ''
        print '--download-file=fileId'
        print '\tDownload the spreadsheet file corresponding to the given fildId. The'
        print '\tfile ID will be an alpha-numeric string of 61 characters.'
        print ''
        print '--output-folder=folderPath'
        print '\tUsed in conjunction with the --download-all, --download-folder, or'
        print '\t--download-file options to specify where the spreadsheets will be'
        print '\tdownloaded to.'
        print ''
        print ''

if __name__ == "__main__":
    driver = CommandLineMain()
    driver.main(sys.argv[1:])
