from app import create_app
import threading
from app.main import settings
from flask_login import current_user

if __name__ == '__main__':
    app = create_app()
    app.config['UPLOAD_FOLDER'] = '/home/shravan/Documents/repos/gallery/dotmole/dotmole/data/people'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.run(host="0.0.0.0", port="5005", debug=True,
            threaded=True, use_reloader=False)