from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class ImportedSong(db.Model):
    __tablename__ = 'imported_songs'
    
    id = db.Column(db.String(255), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    album = db.Column(db.String(255))
    genre = db.Column(db.String(100))
    tempo = db.Column(db.Float)
    mood = db.Column(db.String(50))
    preview_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    
    id = db.Column(db.String(255), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    album = db.Column(db.String(255))
    genre = db.Column(db.String(100))
    tempo = db.Column(db.Float)
    mood = db.Column(db.String(50))
    # Reason why this recommendation was suggested (human-readable explanation)
    reason = db.Column(db.Text)
    preview_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class BuiltPlaylist(db.Model):
    __tablename__ = 'built_playlist'
    
    id = db.Column(db.String(255), primary_key=True)
    song_id = db.Column(db.String(255), db.ForeignKey('recommendations.id'))
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
