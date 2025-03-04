import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from . import create_app, db
from . models import Image

app = create_app()

with app.app_context():
    # Drop all tables and recreate them
    db.drop_all()
    db.create_all()

    # Add dummy data (URLs as filenames)
    db.session.add(Image(filename="https://analyticsindiamag.com/wp-content/uploads/2020/08/place-watermark.jpg"))
    db.session.add(Image(filename="https://www.visualwatermark.com/images/index/watermark-maker.webp"))
    db.session.commit()

print("Database seeded!")
