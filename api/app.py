import sys
from configs import app_config

if app_config.DEBUG:
    app_config.LOG_LEVEL = "DEBUG"


def is_db_command():
    if len(sys.argv) > 1 and sys.argv[0].endswith("flask") and sys.argv[1] == "db":
        return True
    return False


if is_db_command():
    print("-*-" * 20)
    from app_factory import create_migrations_app

    app = create_migrations_app()
else:
    from app_factory import create_app

    app = create_app()

if __name__ == "__main__":
    # print("api_map: {}".format(app.url_map))

    app.run(host="0.0.0.0", port=5001)
