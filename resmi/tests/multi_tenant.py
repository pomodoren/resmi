from flask import Flask, request, g
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Example tenant database mappings
TENANT_DATABASES = {
    "tenant1": "sqlite:///tenant1.db",
    "tenant2": "sqlite:///tenant2.db",
}

# Default Engine for when no tenant is specified or found
default_engine = create_engine("sqlite:///:memory:", echo=True)

# Scoped session to handle dynamic tenant sessions
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=default_engine)
)


def get_tenant():
    return request.path.split("/")[1]  # Extract the tenant from the URL prefix


@app.before_request
def switch_database():
    tenant_id = get_tenant()
    engine = create_engine(TENANT_DATABASES.get(tenant_id, "sqlite:///:memory:"))
    db.session.remove()
    db.session.configure(bind=engine)
    g.tenant_id = (
        tenant_id  # Store tenant_id in Flask's g for access during the request
    )


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


@app.route("/<tenant_id>/assets")
def list_assets(tenant_id):
    from .mt_models import Asset

    assets = Asset.query.all()
    return "\n".join([asset.name for asset in assets])


if __name__ == "__main__":
    app.run(debug=True)
