from src import db
class FishImg(db.Model):
    __tablename__ = 'fish_img'
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(255), nullable=False)
    color_histogram = db.Column(db.PickleType, nullable=False)
    hu_moments = db.Column(db.PickleType, nullable=False)
    lbd = db.Column(db.PickleType, nullable=False)

    def __repr__(self):
        return f'<FishImg {self.image_path}>'

