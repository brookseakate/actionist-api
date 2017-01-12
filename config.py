# add SQLAchemy URI for Postgres.app localhost
SQLALCHEMY_DATABASE_URI = "postgresql://localhost/postgres"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# # Recommended in book, but looks dangerous per https://github.com/mitsuhiko/flask-sqlalchemy/issues/216
# SQLALCHEMY_COMMIT_ON_TEARDOWN = True
