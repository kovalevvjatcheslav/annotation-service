import os
from dropbox import Dropbox

dbx = Dropbox(os.environ.get('DROPBOX_TOKEN'))
os.mkdir('samples/test_data/')

dbx.files_download_to_file('samples/test_data/test_image.jpeg', '/annotation_service_test_data/test_image.jpeg')
